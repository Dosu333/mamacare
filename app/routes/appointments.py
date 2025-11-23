from flask import Blueprint, request
from extensions import db
from models import Appointment

bp = Blueprint("appointments", __name__)


@bp.route("/create", methods=["POST"])
def create_appointment():
    d = request.json
    appt = Appointment(
        patient_id=d["patient_id"],
        doctor_id=d.get("doctor_id"),
        date=d["date"],
        reason=d.get("reason")
    )
    db.session.add(appt)
    db.session.commit()
    return {"id": appt.id}, 201


@bp.route("/patient/<int:pid>", methods=["GET"])
def patient_appointments(pid):
    appts = Appointment.query.filter_by(patient_id=pid).all()
    return {
            "appointments": [{
                    "id": a.id,
                    "date": a.date.isoformat(),
                    "status": a.status,
                    "reason": a.reason
                } for a in appts]
            }
