from google.genai import types
from extensions import db
from models import Doctor, User


def get_doctors(specialty: str = None, facility: str = None):
    """
    Get all doctors or filter by specialty / facility
    """

    query = db.session.query(
            Doctor,
            User
            ).join(
                User,
                Doctor.user_id == User.id
            )

    if specialty:
        query = query.filter(Doctor.specialty.ilike(f"%{specialty}%"))

    if facility:
        query = query.filter(Doctor.facility.ilike(f"%{facility}%"))

    results = query.all()

    doctors = []

    for doctor, user in results:
        doctors.append({
            "doctor_id": doctor.id,
            "full_name": user.full_name,
            "email": user.email,
            "specialty": doctor.specialty,
            "facility": doctor.facility,
            "phone": doctor.phone,
        })

    return {
        "count": len(doctors),
        "doctors": doctors
    }


schema_get_doctors = types.FunctionDeclaration(
    name="get_doctors",
    description="Get all doctors or search by specialty or facility",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "specialty": types.Schema(
                type=types.Type.STRING,
                description="Filter doctors by area of specialization"
            ),
            "facility": types.Schema(
                type=types.Type.STRING,
                description="Filter doctors by hospital or clinic name"
            )
        },
        required=[]
    )
)
