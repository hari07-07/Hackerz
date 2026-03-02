from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# -------------------------
# In-memory data storage
# -------------------------
patients = []
doctors = []

# -------------------------
# Helper Functions
# -------------------------


def get_patient_summary():
    emergency = sum(1 for p in patients if p["category"] == "emergency")
    outpatient = sum(1 for p in patients if p["category"] == "outpatient")
    inpatient = sum(1 for p in patients if p["category"] == "inpatient")

    return {
        "emergency": emergency,
        "outpatient": outpatient,
        "inpatient": inpatient,
    }


def get_doctor_summary():
    available = sum(1 for d in doctors if d["status"] == "available")
    on_call = sum(1 for d in doctors if d["status"] == "on_call")
    on_leave = sum(1 for d in doctors if d["status"] == "on_leave")

    return {
        "available": available,
        "on_call": on_call,
        "on_leave": on_leave,
    }


def check_emergency_alert():
    summary = get_patient_summary()
    doctor_summary = get_doctor_summary()

    if summary["emergency"] > 15 and doctor_summary["available"] < 2:
        return True
    return False


def get_doctors_to_call():
    """Return doctors who are on call or on leave for emergency"""
    return [d["name"] for d in doctors if d["status"] in ["on_call", "on_leave"]]


# -------------------------
# Routes
# -------------------------


@app.route("/")
def home():
    return jsonify({"message": "Hospital Emergency Management API Running"})


# Add Patient
@app.route("/patients", methods=["POST"])
def add_patient():
    data = request.json

    if not data.get("id") or not data.get("category"):
        return jsonify({"error": "id and category required"}), 400

    if data["category"] not in ["emergency", "outpatient", "inpatient"]:
        return jsonify({"error": "Invalid category"}), 400

    patient = {
        "id": data["id"],
        "category": data["category"],
        "time_admitted": datetime.now().isoformat(),
    }

    patients.append(patient)

    return jsonify({"message": "Patient added successfully", "patient": patient})


# Get Patient Summary
@app.route("/patients-summary", methods=["GET"])
def patients_summary():
    summary = get_patient_summary()
    doctor_summary = get_doctor_summary()
    alert = check_emergency_alert()

    response = {"patients": summary, "doctors": doctor_summary, "alert": alert}

    if alert:
        response["doctors_to_call"] = get_doctors_to_call()

    return jsonify(response)


# Add Doctor
@app.route("/doctors", methods=["POST"])
def add_doctor():
    data = request.json

    if not data.get("id") or not data.get("name") or not data.get("status"):
        return jsonify({"error": "id, name and status required"}), 400

    if data["status"] not in ["available", "on_call", "on_leave"]:
        return jsonify({"error": "Invalid status"}), 400

    doctor = {
        "id": data["id"],
        "name": data["name"],
        "department": data.get("department", "General"),
        "status": data["status"],
    }

    doctors.append(doctor)

    return jsonify({"message": "Doctor added successfully", "doctor": doctor})


# Get All Doctors
@app.route("/doctors", methods=["GET"])
def list_doctors():
    return jsonify({"doctors": doctors})


# Update Doctor Status
@app.route("/doctors/<int:doctor_id>", methods=["PUT"])
def update_doctor(doctor_id):
    data = request.json

    for doctor in doctors:
        if doctor["id"] == doctor_id:
            doctor["status"] = data.get("status", doctor["status"])
            return jsonify({"message": "Doctor updated", "doctor": doctor})

    return jsonify({"error": "Doctor not found"}), 404


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
