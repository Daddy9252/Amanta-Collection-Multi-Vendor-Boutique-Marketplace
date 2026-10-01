"""
Run this once to create the database tables:
    python create_db.py

Optionally creates a demo admin account (edit the values below first).
"""
from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created (amanta.db).")

    # Create a default admin account if one doesn't already exist
    if not User.query.filter_by(email='admin@amanta.test').first():
        admin = User(
            name='Amanta Admin',
            email='admin@amanta.test',
            password_hash=generate_password_hash('AdminPass123'),
            role='admin',
            status='active'
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin created -> email: admin@amanta.test | password: AdminPass123")
    else:
        print("Admin account already exists, skipped.")
