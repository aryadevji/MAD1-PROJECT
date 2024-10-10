from werkzeug.security import generate_password_hash
from backend.models import *
from app import *
db.drop_all()
db.create_all()

admin_user = Users(username="admin",passhash=generate_password_hash("admin123", method='pbkdf2:sha256'),role=0)

db.session.add(admin_user)
db.session.commit()

print("DATABASE AND ADMIN CREATED......")