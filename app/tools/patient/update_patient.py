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


def update_patient_record(patient_id: str, update_data: dict):
    try:
        response = requests.patch(
            url=f"{BASE_URL}/patients/{patient_id}",
            headers=HEADERS,
            json=update_data
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


schema_update_patient = types.FunctionDeclaration(
    name="update_patient_record",
    description="Update a patient's information",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "patient_id": types.Schema(
                type=types.Type.STRING,
                description="Unique ID of the patient"
            ),
            "update_data": types.Schema(
                type=types.Type.OBJECT,
                description="Fields to update in the patient record",
            ),
        },
        required=["patient_id", "update_data"]
    )
)
