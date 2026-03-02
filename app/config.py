import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/hackerz"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production")

    API_USERNAME = os.getenv("API_USERNAME", "admin")
    API_PASSWORD = os.getenv("API_PASSWORD", "admin123")
