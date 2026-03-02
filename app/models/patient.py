from app.extensions import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), nullable=False)
    admission_time = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "admission_time": self.admission_time.isoformat(),
        }
