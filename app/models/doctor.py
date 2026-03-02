from app.extensions import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "status": self.status,
        }
