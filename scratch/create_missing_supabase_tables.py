import os
import sys

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from extensions import db
import models

def create_tables():
    app = create_app()
    print("Running db.create_all() on Supabase to generate missing tables...")
    with app.app_context():
        try:
            db.create_all()
            print("Successfully created all missing tables!")
        except Exception as e:
            print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
