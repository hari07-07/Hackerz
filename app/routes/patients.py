from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Doctor, Patient
from app.services.alert_service import check_and_create_alert


patients_bp = Blueprint("patients", __name__)
VALID_CATEGORIES = {"emergency", "outpatient", "inpatient"}


@patients_bp.post("/patients")
@jwt_required()
def create_patient():
    data = request.get_json(silent=True) or {}

    if not all(key in data for key in ["id", "category"]):
        return jsonify({"error": "id and category are required"}), 400

    if data["category"] not in VALID_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    if Patient.query.get(data["id"]):
        return jsonify({"error": "Patient with this id already exists"}), 409

    admission_time = datetime.utcnow()
    patient = Patient(
        id=data["id"],
        category=data["category"],
        admission_time=admission_time,
    )
    db.session.add(patient)
    db.session.commit()

    check_and_create_alert()

    return jsonify(patient.to_dict()), 201


@patients_bp.get("/patients-summary")
@jwt_required()
def patient_summary():
    summary = {
        "emergency": Patient.query.filter_by(category="emergency").count(),
        "outpatient": Patient.query.filter_by(category="outpatient").count(),
        "inpatient": Patient.query.filter_by(category="inpatient").count(),
    }
    doctor_summary = {
        "available": Doctor.query.filter_by(status="available").count(),
        "on_call": Doctor.query.filter_by(status="on_call").count(),
        "on_leave": Doctor.query.filter_by(status="on_leave").count(),
    }

    return jsonify({"patients": summary, "doctors": doctor_summary}), 200
