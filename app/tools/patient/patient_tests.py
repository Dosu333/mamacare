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


def get_patient_tests(patient_id: str, created_at: str = None):
    try:
        url = f"{BASE_URL}/patients/{patient_id}/tests"
        if created_at:
            url += f"?created_at__date={created_at}"
        response = requests.get(
            url=url,
            headers=HEADERS
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


schema_get_patient_tests = types.FunctionDeclaration(
    name="get_patient_tests",
    description="Retrieve medical tests for a patient",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "patient_id": types.Schema(
                type=types.Type.STRING,
                description="Unique ID of the patient"
            ),
            "created_at": types.Schema(
                type=types.Type.STRING,
                description="Filter by date in YYYY-MM-DD format (optional)"
            ),
        },
        required=["patient_id"]
    )
)
