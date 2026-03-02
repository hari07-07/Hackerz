from flask import Flask, jsonify

from app.config import Config
from app.extensions import db, jwt
from app.routes.alerts import alerts_bp
from app.routes.auth import auth_bp
from app.routes.doctors import doctors_bp
from app.routes.patients import patients_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(alerts_bp)

    @app.get("/")
    def health():
        return jsonify({"message": "Hospital Emergency Management API Running"}), 200

    with app.app_context():
        db.create_all()

    return app
