import os
import sys
# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import VisitorLog, Attraction

app = create_app()

with app.app_context():
    print("--- Verifying VisitorLog ---")
    try:
        # Check if VisitorLog table exists by attempting a query
        count = VisitorLog.query.count()
        print(f"VisitorLog table check: SUCCESS (Found {count} records)")
    except Exception as e:
        print(f"VisitorLog table check: FAILED - {e}")

    print("\n--- Verifying Attraction Stewardship ---")
    try:
        # Get first attraction and check if user relationship exists
        attraction = Attraction.query.first()
        if attraction:
            print(f"Attraction '{attraction.name}' found.")
            print(f"Steward ID (user_id): {attraction.user_id}")
            if attraction.user:
                print(f"Steward User Name: {attraction.user.username}")
            else:
                print("No steward linked yet, but relationship check: SUCCESS")
        else:
            print("No attractions found in DB to verify.")
    except Exception as e:
        print(f"Attraction stewardship check: FAILED - {e}")

    print("\n--- Verification Complete ---")
