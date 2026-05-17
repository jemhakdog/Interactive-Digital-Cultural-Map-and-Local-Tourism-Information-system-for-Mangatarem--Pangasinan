import os
import sys
sys.path.append(os.getcwd())

from app import create_app
from models import User

app = create_app()
with app.app_context():
    print("=== USERS IN SYSTEM ===")
    for u in User.query.all():
        print(f"Username: {u.username} | Role: {u.role} | Approved: {u.is_approved}")
