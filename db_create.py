# create_db.py

from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Kreiranje baze
    db.create_all()
    print("Baza podataka je uspešno kreirana.")

    # Unos podataka za admina
    print("\nUnos podataka za novog admin korisnika:")

    username = input("Korisničko ime: ").strip()
    name = input("Ime i prezime: ").strip()
    email = input("Email: ").strip()
    phone = input("Telefon: ").strip()
    telegram = input("Telegram (opciono): ").strip()
    password = input("Lozinka: ").strip()

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"Korisnik sa korisničkim imenom '{username}' već postoji.")
    else:
        admin = User(
            username=username,
            password_hash=generate_password_hash(password),
            name=name,
            phone=phone,
            email=email,
            telegram=telegram if telegram else None,
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Admin korisnik '{username}' je uspešno dodat.")
