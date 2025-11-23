from flask import Blueprint
from models import Appointment, ChatMessage, Observation
from extensions import db

bp = Blueprint("doctors", __name__)


@bp.route("/dashboard/<int:doctor_id>", methods=["GET"])
def dashboard(doctor_id):
    # a simple view: recent alerts (observations with concerning types),
    # recent chats, upcoming appointments
    recent_chats = ChatMessage.query.order_by(
                    ChatMessage.created_at.desc()).limit(20).all()
    recent_obs = Observation.query.order_by(
                    Observation.recorded_at.desc()).limit(20).all()
    upcoming = Appointment.query.filter(
                Appointment.date >= db.func.now()
                ).order_by(Appointment.date).limit(20).all()
    return {
        "recent_chats": [
            {
                "pid": c.patient_id,
                "msg": c.message,
                "at": c.created_at.isoformat()} for c in recent_chats],
        "recent_observations": [
            {
                "pid": o.patient_id,
                "type": o.type,
                "val": o.value
            } for o in recent_obs],
        "upcoming": [
            {
                "id": a.id,
                "patient_id": a.patient_id,
                "date": a.date.isoformat()
            } for a in upcoming]
    }
