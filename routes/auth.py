from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_anonymous:
        return render_template("index.html")
    else:
        return redirect(url_for("main.main"))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Collect info from the form
        username = request.form['username']
        password = request.form['password']

        # Check if it's in the db / login
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            user.authenticated = True
            login_user(user)
            return redirect(url_for("main.main"))
        # If False show index
        else:
            flash('Nepostojeća kombinacija korisničkog imena i lozinke!', 'Greška')
    return render_template("index.html")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_anonymous:
        if request.method == "POST":
            user = User()
            if User.query.filter_by(username=request.form.get('username')).first():
                flash("Korisnik sa datim korisničkim imenom već postoji!")
                return redirect(url_for("auth.register"))
            if User.query.filter_by(email=request.form.get('email')).first():
                flash("Korisnik sa datim emailom već postoji!")
                return redirect(url_for("auth.register"))
            user.username = request.form['username']
            user.set_password(request.form['password'])
            user.name = request.form['name']
            user.email = request.form['email']
            user.phone = request.form['phone']
            user.telegram = request.form['telegram']
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("main.main"))
        else:
            return render_template("register.html")
    return redirect(url_for("main.main"))


@auth_bp.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.commit()

    logout_user()

    return redirect(url_for('auth.index'))
