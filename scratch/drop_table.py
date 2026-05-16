import os
import sys
# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    print("Dropping VISITOR_LOG table to allow Alembic to detect it as a new change...")
    try:
        db.session.execute(db.text("DROP TABLE IF EXISTS VISITOR_LOG"))
        db.session.commit()
        print("Success.")
    except Exception as e:
        print(f"Error: {e}")
