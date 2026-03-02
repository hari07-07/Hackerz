from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if (
        username != current_app.config["API_USERNAME"]
        or password != current_app.config["API_PASSWORD"]
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=username)
    return jsonify({"access_token": token}), 200
