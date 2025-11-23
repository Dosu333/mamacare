from datetime import datetime
from google.genai import types
from models import Observation
from extensions import db


def log_symptom(patient_id: int, symptom: str, unit: str = None):
    """
    Logs a symptom or health observation for the patient.
    """
    observation = Observation(
        patient_id=patient_id,
        type="symptom",
        value=symptom,
        unit=unit,
        recorded_at=datetime.utcnow(),
        source="system"
    )
    db.session.add(observation)
    db.session.commit()
    return {"status": "success", "observation_id": observation.id}


schema_log_symptom = types.FunctionDeclaration(
    name="log_symptom",
    description="Log a symptom or health observation for a patient.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "patient_id": types.Schema(
                type=types.Type.STRING,
                description="Unique ID of the patient"
            ),
            "symptom": types.Schema(
                type=types.Type.STRING,
                description="Symptom or observation to record"
            ),
            "unit": types.Schema(
                type=types.Type.STRING,
                description="Optional unit for the symptom (e.g., 'Celsius', 'bpm')"
            ),
        },
        required=["patient_id", "symptom"]
    )
)
