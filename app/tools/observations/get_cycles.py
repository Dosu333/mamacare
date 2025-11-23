from models import Cycle
from google.genai import types


def get_patient_cycles(patient_id: int):
    cycles = (
        Cycle.query
        .filter_by(patient_id=patient_id)
        .order_by(Cycle.start_date.desc())
        .all()
    )

    return {"data": [
        {
            "id": c.id,
            "start_date": c.start_date.isoformat(),
            "end_date": c.end_date.isoformat() if c.end_date else None,
            "notes": c.notes,
            "created_at": c.created_at.isoformat(),
        }
        for c in cycles
    ]}


schema_get_patient_cycles = types.FunctionDeclaration(
    name="get_patient_cycles",
    description="Get all menstrual cycle records for a patient",
    parameters=types.Schema(
        type="object",
        properties={
            "patient_id": types.Schema(type="integer")
        },
        required=["patient_id"]
    )
)
