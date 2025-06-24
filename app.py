from models import db, User
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from routes import register_blueprints

from config import Config
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicijalizuj db sa app
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth.index'))  # login view

    # Register Blueprints
    register_blueprints(app)

    return app



if __name__ == "__main__":
    app=create_app()
    app.run(debug=True)
