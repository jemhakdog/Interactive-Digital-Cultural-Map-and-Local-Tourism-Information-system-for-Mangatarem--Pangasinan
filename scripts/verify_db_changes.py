import os
from app import app, db
from sqlalchemy import inspect

def verify_schema():
    print("🚀 Starting verification...")
    with app.app_context():
        # Ensure directory exists for sqlite
        instance_path = os.path.join(os.getcwd(), 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
            
        print("Initializing database...")
        db.create_all()
        print("✅ Database initialized (create_all finished).")
        
        inspector = inspect(db.engine)
        tables_to_check = {
            'attraction': ['status', 'reviewed_by', 'reviewed_at'],
            'event': ['status', 'reviewed_by', 'reviewed_at'],
            'gallery_item': ['status', 'reviewed_by', 'reviewed_at'],
            'review': ['status', 'reviewed_by', 'reviewed_at']
        }
        
        all_passed = True
        for table, expected_columns in tables_to_check.items():
            actual_columns = [c['name'] for c in inspector.get_columns(table)]
            print(f"\nChecking table '{table}':")
            print(f"  Actual: {actual_columns}")
            
            missing = [col for col in expected_columns if col not in actual_columns]
            if missing:
                print(f"  ❌ MISSING: {missing}")
                all_passed = False
            else:
                print("  ✅ All expected columns present.")
        
        if all_passed:
            print("\n🌟 VERIFICATION SUCCESSFUL: All tables updated correctly.")
        else:
            print("\n❌ VERIFICATION FAILED: Some columns are missing.")

if __name__ == "__main__":
    verify_schema()
