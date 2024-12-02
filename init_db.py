from werkzeug.security import generate_password_hash
from backend.models import db, Users  # Ensure your models are correctly imported
from app import app  # Ensure the app instance is correctly imported

# Bind the app context to the database
with app.app_context():
    # Create tables only if they don't already exist
    db.create_all()

    # Check if the admin user already exists
    if not Users.query.filter_by(username="admin").first():
        admin_user = Users(
            username="admin",
            passhash=generate_password_hash("admin123", method='pbkdf2:sha256'),
            role=0
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

    print("DATABASE AND ADMIN CHECK COMPLETE.")
