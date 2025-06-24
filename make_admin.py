from app import create_app, db
from models import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(username="Kiconii13").first()

    if not user:
        print("Korisnik sa usernameom 'Kiconii13' ne postoji.")
    else:
        user.role = "admin"
        db.session.commit()
        print(f"Korisniku '{user.username}' uspešno dodeljena rola 'admin'.")
