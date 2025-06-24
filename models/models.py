from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from . import db

from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telegram = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(16), default='user')

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    number_required = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref='projects')
    ongoing = db.Column(db.Boolean, default=True)
    approved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Project {self.name}>"

class Volunteers(db.Model):
    __tablename__ = 'volunteers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='volunteers')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project', backref='volunteers')