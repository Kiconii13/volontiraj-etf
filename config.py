import os

class Config:
    if os.environ.get("FLASK_ENV") == "deployment":
        db_url = os.environ.get("DATABASE_URL")
        if db_url and db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://")
        SQLALCHEMY_DATABASE_URI = db_url or "sqlite:///fallback.db"
        SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"
        SECRET_KEY = "vUV3s@N3VeRY5JhQTi"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
