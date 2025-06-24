import os

class Config:
    if os.environ.get("FLASK_ENV") == "deployment":
        SQLALCHEMY_DATABASE_URI = os.environ.get("NEW_DATABASE_URL")
        SECRET_KEY = os.environ.get("SECRET_KEY")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"
        SECRET_KEY = "vUV3s@N3VeRY5JhQTi"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
