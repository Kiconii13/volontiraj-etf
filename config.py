import os

class Config:
    if os.environ.get("FLASK_ENV") == "deployment":
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
        SECRET_KEY = os.environ.get("SECRET_KEY")
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"
        SECRET_KEY = "8PvUV36JVw59"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
