from datetime import datetime
from google.genai import types
from models import Observation, Cycle
from extensions import db


def log_cycle_end(patient_id: int, end_date: str):
    try:
        parsed_date = datetime.fromisoformat(end_date).date()
    except Exception:
        raise ValueError("Date must be in ISO format (YYYY-MM-DD)")

    # Get latest cycle for patient
    cycle = Cycle.query.filter_by(
            patient_id=patient_id).order_by(Cycle.start_date.desc()).first()
    if not cycle:
        return {"error": "No cycle found for patient"}

    cycle.end_date = parsed_date

    # Add observation
    observation = Observation(
        patient_id=patient_id,
        type="menstrual_cycle_end",
        value="Cycle ended",
        recorded_at=datetime.utcnow(),
        source="system"
    )
    db.session.add(observation)
    db.session.commit()

    return {
                "status": "success",
                "cycle_id": cycle.id,
                "observation_id": observation.id
            }


schema_log_cycle_end = types.FunctionDeclaration(
    name="log_cycle_end",
    description="Log the end of the latest menstrual cycle for a patient.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "patient_id": types.Schema(
                type=types.Type.STRING,
                description="Unique ID of the patient"
            ),
            "end_date": types.Schema(
                type=types.Type.STRING,
                description="Cycle end date in YYYY-MM-DD format"
            ),
        },
        required=["patient_id", "end_date"]
    )
)
