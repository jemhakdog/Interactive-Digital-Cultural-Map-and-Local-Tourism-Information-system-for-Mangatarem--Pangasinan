import sqlite3
import os

def migrate():
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(base_dir, 'instance', 'mangatarem.db')
    
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if parent_id column already exists
        cursor.execute("PRAGMA table_info(ESTABLISHMENT_REVIEW)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'parent_id' in columns:
            print("Column 'parent_id' already exists in ESTABLISHMENT_REVIEW. Skipping.")
        else:
            print("Adding column 'parent_id' to ESTABLISHMENT_REVIEW...")
            cursor.execute("ALTER TABLE ESTABLISHMENT_REVIEW ADD COLUMN parent_id INTEGER REFERENCES ESTABLISHMENT_REVIEW(id) ON DELETE CASCADE")
            conn.commit()
            print("Column 'parent_id' successfully added!")
            
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
