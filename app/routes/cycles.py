from flask import Blueprint, request
from extensions import db
from models import Cycle, Patient
from datetime import datetime

bp = Blueprint("cycles", __name__)


@bp.route("/start", methods=["POST"])
def start_cycle():
    data = request.json
    patient_id = data["patient_id"]
    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    cycle = Cycle(patient_id=patient_id, start_date=start_date)
    db.session.add(cycle)
    db.session.commit()
    # update patient.last_cycle_start
    p = Patient.query.get(patient_id)
    p.last_cycle_start = start_date
    db.session.commit()
    return {"msg": "ok", "cycle_id": cycle.id}
