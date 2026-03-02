from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import Doctor
from app.services.alert_service import check_and_create_alert


doctors_bp = Blueprint("doctors", __name__)
VALID_STATUSES = {"available", "on_call", "on_leave"}


@doctors_bp.post("/doctors")
@jwt_required()
def create_doctor():
    data = request.get_json(silent=True) or {}

    if not all(key in data for key in ["id", "name", "department", "status"]):
        return jsonify({"error": "id, name, department, and status are required"}), 400

    if data["status"] not in VALID_STATUSES:
        return jsonify({"error": "Invalid status"}), 400

    if Doctor.query.get(data["id"]):
        return jsonify({"error": "Doctor with this id already exists"}), 409

    doctor = Doctor(
        id=data["id"],
        name=data["name"],
        department=data["department"],
        status=data["status"],
    )
    db.session.add(doctor)
    db.session.commit()
    check_and_create_alert()

    return jsonify(doctor.to_dict()), 201


@doctors_bp.get("/doctors")
@jwt_required()
def list_doctors():
    doctors = Doctor.query.order_by(Doctor.id.asc()).all()
    return jsonify([doctor.to_dict() for doctor in doctors]), 200


@doctors_bp.put("/doctors/<int:doctor_id>")
@jwt_required()
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = request.get_json(silent=True) or {}

    if "name" in data:
        doctor.name = data["name"]
    if "department" in data:
        doctor.department = data["department"]
    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return jsonify({"error": "Invalid status"}), 400
        doctor.status = data["status"]

    db.session.commit()
    check_and_create_alert()
    return jsonify(doctor.to_dict()), 200
