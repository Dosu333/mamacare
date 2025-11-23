from flask import Blueprint, request
from extensions import db
from models import Patient
from sqlalchemy.exc import IntegrityError


bp = Blueprint("patients", __name__)


@bp.route("/create", methods=["POST"])
def create_patient():
    data = request.json
    p = Patient(full_name=data.get("full_name"),
                phone=data["phone"],
                email=data.get("email"))
    db.session.add(p)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"msg": "patient exists"}, 400
    return {"id": p.id}, 201


@bp.route("/by-phone/<phone>", methods=["GET"])
def get_patient_by_phone(phone):
    p = Patient.query.filter_by(phone=phone).first()
    if not p:
        return {"msg": "not found"}, 404
    return {
        "id": p.id,
        "full_name": p.full_name,
        "phone": p.phone,
        "email": p.email
    }
