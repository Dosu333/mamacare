from flask import Blueprint, request
from extensions import db
from models import ChatMessage

bp = Blueprint("chat", __name__)


@bp.route("/log", methods=["POST"])
def log_message():
    d = request.json
    cm = ChatMessage(
        patient_id=d.get("patient_id"),
        sender=d["sender"],
        message=d["message"]
    )
    db.session.add(cm)
    db.session.commit()
    return {"id": cm.id}
