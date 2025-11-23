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


def create_patient(
    email: str,
    first_name: str,
    last_name: str,
    phone: str,
    gender: str,
    age: int,
    dob: str,
    allergies: list = [],
    address: str = "",
):
    try:
        data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'gender': gender,
            'age': age,
            'date_of_birth': dob,
            'allergies': allergies,
            'address': address
        }
        response = requests.post(
            url=f"{BASE_URL}/patients/create",
            headers=HEADERS,
            json=data
        )
        return response.json()
    except Exception as e:
        print(str(e))
        return {"error": str(e)}


schema_create_patient = types.FunctionDeclaration(
    name="create_patient",
    description="Create a new patient record in the system",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "email": types.Schema(
                type=types.Type.STRING,
                description="Patient's email address"
            ),
            "first_name": types.Schema(
                type=types.Type.STRING,
                description="Patient's first name"
            ),
            "last_name": types.Schema(
                type=types.Type.STRING,
                description="Patient's last name"
            ),
            "phone": types.Schema(
                type=types.Type.STRING,
                description="Patient's phone number"
            ),
            "gender": types.Schema(
                type=types.Type.STRING,
                description="Patient's gender"
            ),
            "age": types.Schema(
                type=types.Type.INTEGER,
                description="Patient's age"
            ),
            "dob": types.Schema(
                type=types.Type.STRING,
                description="Patient's date of birth in YYYY-MM-DD format"
            ),
            "allergies": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="List of known allergies",
            ),
            "address": types.Schema(
                type=types.Type.STRING,
                description="Patient's residential address"
            ),
        },
        required=["email", "first_name", "last_name", "phone",
                  "gender", "age", "dob"]
    )
)


# if __name__ == "__main__":
#     p = create_patient(**{'age': 27, 'phone': '08143041214', 'last_name': 'Dolapo', 'email': 'ogooluwaniadewale@gmail.com', 'dob': '1998-06-04', 'first_name': 'Blessing', 'gender': 'Female'})
#     print(p)
