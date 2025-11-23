from flask import Blueprint, request
from extensions import db
from models import Drug, DrugInteraction

bp = Blueprint("drugs", __name__)


@bp.route("/seed", methods=["POST"])
def seed():
    d1 = Drug(name="Paracetamol", pregnancy_safe=True)
    d2 = Drug(name="Ibuprofen", pregnancy_safe=False)
    db.session.add_all([d1, d2])
    db.session.commit()
    return {"msg": "seeded"}


@bp.route("/check-interaction", methods=["GET"])
def check_interaction():
    a = request.args.get("a")
    b = request.args.get("b")
    da = Drug.query.filter_by(name=a).first()
    db = Drug.query.filter_by(name=b).first()

    if not da or not db:
        return {"msg": "drug not found"}, 404

    inter = DrugInteraction.query.filter(
        (
            (DrugInteraction.drug_a_id == da.id) &
            (DrugInteraction.drug_b_id == db.id)) |
        (
            (DrugInteraction.drug_a_id == db.id) &
            (DrugInteraction.drug_b_id == da.id))
    ).first()
    if inter:
        return {"interaction": inter.note, "severity": inter.severity}
    return {"interaction": None}
