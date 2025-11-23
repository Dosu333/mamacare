from flask import Blueprint, request
from extensions import db
from models import User, Doctor
from flask_jwt_extended import create_access_token


bp = Blueprint("auth", __name__)


@bp.route("/register_doctor", methods=["POST"])
def register_doctor():
    data = request.json
    email = data["email"]
    pw = data["password"]
    if User.query.filter_by(email=email).first():
        return {"msg": "User exists"}, 400
    user = User(email=email, role="doctor", full_name=data.get("full_name"))
    user.set_password(pw)
    db.session.add(user)
    db.session.commit()
    doc = Doctor(
        user_id=user.id, specialty=data.get("specialty"),
        phone=data.get("phone"))
    db.session.add(doc)
    db.session.commit()
    return {"msg": "doctor created", "doctor_id": doc.id}, 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return {"msg": "invalid credentials"}, 401
    access = create_access_token(
        identity={"user_id": user.id, "role": user.role}
    )
    return {"access_token": access}
