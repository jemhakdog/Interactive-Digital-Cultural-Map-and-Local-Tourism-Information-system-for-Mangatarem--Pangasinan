import sqlite3
import os

def migrate():
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(base_dir, 'instance', 'mangatarem.db')
    
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if the column already exists
        cursor.execute("PRAGMA table_info(ATTRACTION)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'osm_alternatives' in columns:
            print("Column 'osm_alternatives' already exists in ATTRACTION table. Skipping.")
        else:
            print("Adding column 'osm_alternatives' to ATTRACTION table...")
            cursor.execute("ALTER TABLE ATTRACTION ADD COLUMN osm_alternatives TEXT")
            conn.commit()
            print("Column 'osm_alternatives' successfully added!")
            
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
