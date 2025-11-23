from datetime import datetime
from google.genai import types
from models import Observation, Cycle
from extensions import db


def log_cycle_start(patient_id: int, start_date: str, notes: str = None):
    """
    Logs a menstrual cycle start.
    """
    try:
        parsed_date = datetime.fromisoformat(start_date).date()
    except Exception:
        raise ValueError("Date must be in ISO format (YYYY-MM-DD)")

    # Create cycle record
    cycle = Cycle(patient_id=patient_id, start_date=parsed_date, notes=notes)
    db.session.add(cycle)

    # Create FHIR-compatible observation
    observation = Observation(
        patient_id=patient_id,
        type="menstrual_cycle_start",
        value="Cycle started",
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


schema_log_cycle_start = types.FunctionDeclaration(
    name="log_cycle_start",
    description="Log the start of a menstrual cycle for a patient, optionally with notes.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "patient_id": types.Schema(
                type=types.Type.STRING,
                description="Unique ID of the patient"
            ),
            "start_date": types.Schema(
                type=types.Type.STRING,
                description="Cycle start date in YYYY-MM-DD format"
            ),
            "notes": types.Schema(
                type=types.Type.STRING,
                description="Optional notes for the cycle"
            ),
        },
        required=["patient_id", "start_date"]
    )
)
