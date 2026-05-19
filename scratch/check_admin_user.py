import os
import sys
from werkzeug.security import check_password_hash

print("Script started.")

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from modules.auth.models import User
from extensions import db

app = create_app()

with app.app_context():
    print("=== Checking Admin User ===")
    admin_user = User.query.filter_by(username="admin").first()

    if admin_user:
        print(f"Admin User Found:")
        print(f"  Username: {admin_user.username}")
        print(f"  Email: {admin_user.email}")
        print(f"  Role: {admin_user.role}")
        print(f"  Is Approved: {admin_user.is_approved}")

        # Check password
        test_password = "admin123"
        if admin_user.check_password(test_password):
            print(f"  Password '{test_password}' is CORRECT.")
        else:
            print(f"  Password '{test_password}' is INCORRECT.")
            print(f"  Stored hash: {admin_user.password}")
    else:
        print("Admin user 'admin' not found in the database.")

    print("=== Check Complete ===")