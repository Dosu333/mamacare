from flask import Blueprint, request
from extensions import db
from models import Observation

bp = Blueprint("observations", __name__)


@bp.route("/log", methods=["POST"])
def log_observation():
    d = request.json
    obs = Observation(
        patient_id=d["patient_id"],
        type=d["type"],
        value=d["value"],
        unit=d.get("unit")
    )
    db.session.add(obs)
    db.session.commit()
    return {"id": obs.id}, 201


@bp.route("/patient/<int:pid>", methods=["GET"])
def list_patient_obs(pid):
    obs = Observation.query.filter_by(patient_id=pid).order_by(
                Observation.recorded_at.desc()).limit(50).all()
    return {
        "observations":
            [{
                "type": o.type,
                "value": o.value,
                "at": o.recorded_at.isoformat()
            } for o in obs]
        }
