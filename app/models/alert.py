from datetime import datetime

from app.extensions import db


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    emergency_count = db.Column(db.Integer, nullable=False)
    available_doctors = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "emergency_count": self.emergency_count,
            "available_doctors": self.available_doctors,
            "created_at": self.created_at.isoformat(),
        }
