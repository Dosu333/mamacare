import requests
from google.genai import types
from dotenv import load_dotenv
import os


load_dotenv()


API_TOKEN = os.getenv("DORRA_API_TOKEN")
BASE_URL = "https://hackathon-api.aheadafrica.org/v1"
HEADERS = {
        "Authorization": f"Token {API_TOKEN}"
    }


def create_appointments_and_encounters_via_ai(prompt: str, patient_id: int):
    try:
        data = {
            "prompt": prompt,
            "patient": patient_id
        }
        response = requests.post(
            url=f"{BASE_URL}/ai/emr",
            json=data,
            headers=HEADERS
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


schema_create_appointments_and_encounters_via_ai = types.FunctionDeclaration(
    name="create_appointments_and_encounters_via_ai",
    description="""
    Use AI to automatically create patient appointments and encounters
    based on a natural language prompt.
    This is used when a patient describes symptoms, complaints, or
    medical situations that should result in an encounter or appointment.
    """,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "prompt": types.Schema(
                type=types.Type.STRING,
                description="Natural language description of the patient's issue or medical request"
            ),
            "patient_id": types.Schema(
                type=types.Type.INTEGER,
                description="The unique ID of the patient"
            ),
        },
        required=["prompt", "patient_id"]
    )
)
