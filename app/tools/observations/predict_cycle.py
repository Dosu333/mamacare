from datetime import timedelta
from models import Cycle
from statistics import mean
from google.genai import types


def predict_next_cycle_start(patient_id: int):
    cycles = (
        Cycle.query
        .filter_by(patient_id=patient_id)
        .filter(Cycle.end_date.isnot(None))
        .order_by(Cycle.start_date.asc())
        .all()
    )

    if len(cycles) < 2:
        return {
            "error": "Not enough data to make prediction",
            "required_cycles": 2,
            "available_cycles": len(cycles)
        }

    cycle_lengths = []

    # Calculate differences between cycle starts
    for i in range(1, len(cycles)):
        prev = cycles[i - 1]
        current = cycles[i]
        diff = (current.start_date - prev.start_date).days
        cycle_lengths.append(diff)

    avg_length = round(mean(cycle_lengths))

    last_cycle = cycles[-1]
    last_start = last_cycle.start_date

    # Range +/- 2 days
    earliest = last_start + timedelta(days=avg_length - 2)
    latest = last_start + timedelta(days=avg_length + 2)

    # Confidence estimation
    variation = max(cycle_lengths) - min(cycle_lengths)
    confidence = (
        "High" if variation <= 3
        else "Medium" if variation <= 6
        else "Low"
    )

    return {
        "last_cycle_start": last_start.isoformat(),
        "average_cycle_length": avg_length,
        "earliest_next_start": earliest.isoformat(),
        "latest_next_start": latest.isoformat(),
        "confidence": confidence
    }


schema_predict_next_cycle = types.FunctionDeclaration(
    name="predict_next_cycle_start",
    description="Predict the next menstrual cycle start date range based on patient cycle history",
    parameters=types.Schema(
        type="object",
        properties={
            "patient_id": types.Schema(type="integer"),
        },
        required=["patient_id"],
    ),
)
