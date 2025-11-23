from datetime import datetime
from google.genai import types
from models import Observation
from extensions import db


def record_pregnancy(patient_id: int, status: str, notes: str = None):
    """
    Record pregnancy status for a patient (e.g., "Pregnant", "Not Pregnant").
    """
    observation = Observation(
        patient_id=patient_id,
        type="pregnancy_status",
        value=status,
        recorded_at=datetime.utcnow(),
        source="system"
    )
    db.session.add(observation)

    if notes:
        cycle_note = Observation(
            patient_id=patient_id,
            type="note",
            value=notes,
            recorded_at=datetime.utcnow(),
            source="system"
        )
        db.session.add(cycle_note)

    db.session.commit()
    return {"status": "success", "observation_id": observation.id}


def get_pregnancy_status(patient_id: int):
    """
    Retrieve the latest pregnancy status for a patient.
    """
    observation = Observation.query.filter_by(
        patient_id=patient_id,
        type="pregnancy_status"
    ).order_by(Observation.recorded_at.desc()).first()

    if not observation:
        return {"status": "not found"}

    return {
        "status": "success",
        "pregnancy_status": observation.value,
        "recorded_at": observation.recorded_at.isoformat()
    }


schema_record_pregnancy = types.FunctionDeclaration(
    name="record_pregnancy",
    description="Record pregnancy status for a patient, optionally with notes.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "patient_id": types.Schema(
                type=types.Type.STRING,
                description="Unique ID of the patient"
            ),
            "status": types.Schema(
                type=types.Type.STRING,
                description="Pregnancy status (e.g., 'Pregnant', 'Not Pregnant')"
            ),
            "notes": types.Schema(
                type=types.Type.STRING,
                description="Optional notes related to the pregnancy"
            ),
        },
        required=["patient_id", "status"]
    )
)

schema_pregnancy_status = types.FunctionDeclaration(
    name="get_pregnancy_status",
    description="Retrieve the latest pregnancy status for a patient.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "patient_id": types.Schema(
                type=types.Type.STRING,
                description="Unique ID of the patient"
            ),
        },
        required=["patient_id", ]
    )
)
