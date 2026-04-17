import os
import sys

# Ensure the project directory is in the path
sys.path.append(os.getcwd())

from app import create_app
from extensions import db
from models import * # Import all models to ensure they are registered

def reset_database():
    print("Initializing Application Context...")
    app = create_app()
    with app.app_context():
        print("Dropping all tables...")
        # Note: SQLite might fail to drop iff locked, but we'll try
        try:
            db.drop_all()
            print("Successfully dropped all tables.")
        except Exception as e:
            print(f"Error dropping tables: {e}")
            print("Attempting to delete files manually if locked...")
            return False

        print("Creating all tables from new schema...")
        db.create_all()
        print("Database schema successfully recreated!")
    return True

if __name__ == "__main__":
    success = reset_database()
    if not success:
        sys.exit(1)
