import os
import sys

def reset_local_db():
    db_file = 'mangatarem.db'
    
    if os.path.exists(db_file):
        print(f"Found {db_file}. Attempting to delete...")
        try:
            # Try to close potential connections by just deleting
            os.remove(db_file)
            print(f"SUCCESS: {db_file} has been deleted.")
            print("\nNext Steps:")
            print("1. Stop your running Flask application (app.py).")
            print("2. Restart it using 'python app.py' or 'uv run app.py'.")
            print("3. The system will automatically recreate the database and seed it with the NEW specialized owners.")
        except PermissionError:
            print(f"ERROR: Could not delete {db_file}. It is likely being used by your running Flask app.")
            print("Please STOP the Flask application and run this script again.")
        except Exception as e:
            print(f"ERROR: An unexpected error occurred: {e}")
    else:
        print(f"{db_file} does not exist. It's already 'synced' or missing.")
        print("Run app.py to create and seed a new one.")

if __name__ == "__main__":
    reset_local_db()
