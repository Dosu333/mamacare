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


def get_patient_record(patient_id: str):
    try:
        response = requests.get(
            url=f"{BASE_URL}/patients/{patient_id}",
            headers=HEADERS
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def get_all_patients():
    try:
        response = requests.get(
            url=f"{BASE_URL}/patients",
            headers=HEADERS
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


schema_get_patient_record = types.FunctionDeclaration(
    name="get_patient_record",
    description="Retrieve the full record of a patient",
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

schema_get_all_patients = types.FunctionDeclaration(
    name="get_all_patients",
    description="Retrieve a list of patients.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
        required=[]
    )
)
