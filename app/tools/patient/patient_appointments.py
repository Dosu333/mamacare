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


def get_patient_appointments(patient_id: str):
    try:
        response = requests.get(
            url=f"{BASE_URL}/patients/{patient_id}/appointments",
            headers=HEADERS
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


schema_get_patient_appointments = types.FunctionDeclaration(
    name="get_patient_appointments",
    description="Get all appointments for a specific patient",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "patient_id": types.Schema(
                type=types.Type.STRING,
                description="Unique ID of the patient"
            ),
        },
        required=["patient_id"]
    )
)
