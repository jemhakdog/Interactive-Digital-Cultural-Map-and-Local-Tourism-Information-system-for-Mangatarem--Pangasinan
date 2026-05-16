import os
import sys
# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db
from models import VisitorLog, Attraction, Establishment, User
from datetime import datetime

app = create_app()

with app.app_context():
    print("\n" + "="*40)
    print("[START] VISITOR LOG DATABASE TEST")
    print("="*40 + "\n")

    # 1. Get a test user (Admin)
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        print("[ERROR] Admin user not found. Please run seed first.")
        sys.exit(1)

    # 2. Get a test Attraction or Establishment
    target = Attraction.query.first() or Establishment.query.first()
    if not target:
        print("[ERROR] No attractions or establishments found in the database.")
        print("Please ensure you have seeded the database or added items.")
        sys.exit(1)

    target_type = 'attraction' if isinstance(target, Attraction) else 'establishment'
    print(f"[INFO] Target Found: '{target.name}' ({target_type})")
    print(f"[INFO] Testing Steward: {admin.username} (ID: {admin.id})")

    # 3. Create a test VisitorLog entry
    new_log = VisitorLog(
        target_type=target_type,
        target_id=target.id,
        visitor_count=12,
        logged_by=admin.id,
        notes="Manual verification test"
    )

    print("\n[PROCESS] Saving test log entry...")
    try:
        db.session.add(new_log)
        db.session.commit()
        print(f"[SUCCESS] Database Save")
        
        # 4. Retrieve it back to verify persistence
        saved_log = VisitorLog.query.order_by(VisitorLog.id.desc()).first()
        print(f"\n--- LOG DETAILS ---")
        print(f"ID: {saved_log.id}")
        print(f"Visitors: {saved_log.visitor_count}")
        print(f"Date: {saved_log.visit_date}")
        print(f"Notes: {saved_log.notes}")
        print(f"Steward Backlink: {saved_log.steward.username}")
        print(f"-------------------")
        
        print("\n[COMPLETE] Database synchronization is working!")
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Database Error: {e}")

    print("\n" + "="*40)
    print("[FINISH] TEST COMPLETED")
    print("="*40 + "\n")
