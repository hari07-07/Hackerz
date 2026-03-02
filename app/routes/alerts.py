from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.models import Alert


alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.get("/alerts")
@jwt_required()
def list_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).all()
    return jsonify([alert.to_dict() for alert in alerts]), 200
