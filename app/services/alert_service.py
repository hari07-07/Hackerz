from app.extensions import db
from app.models import Alert, Doctor, Patient


ALERT_EMERGENCY_THRESHOLD = 15
ALERT_AVAILABLE_DOCTORS_THRESHOLD = 2


def compute_counts():
    emergency_count = Patient.query.filter_by(category="emergency").count()
    available_doctors = Doctor.query.filter_by(status="available").count()
    return emergency_count, available_doctors


def check_and_create_alert():
    emergency_count, available_doctors = compute_counts()
    if (
        emergency_count > ALERT_EMERGENCY_THRESHOLD
        and available_doctors < ALERT_AVAILABLE_DOCTORS_THRESHOLD
    ):
        alert = Alert(
            emergency_count=emergency_count,
            available_doctors=available_doctors,
        )
        db.session.add(alert)
        db.session.commit()
        return alert
    return None
