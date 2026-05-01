import sqlite3
import os

db_path = 'instance/mangatarem.db'

if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def add_column_if_missing(table, column, type):
    try:
        # Check if column exists
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [info[1] for info in cursor.fetchall()]
        
        if column not in columns:
            print(f"Adding column '{column}' to table '{table}'...")
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type} DEFAULT 0")
            print("Done.")
        else:
            print(f"Column '{column}' already exists in table '{table}'.")
    except Exception as e:
        print(f"Error adding column to {table}: {e}")

# Add is_featured to ATTRACTION
add_column_if_missing('ATTRACTION', 'is_featured', 'BOOLEAN')

# Add is_featured to ESTABLISHMENT
add_column_if_missing('ESTABLISHMENT', 'is_featured', 'BOOLEAN')

conn.commit()
conn.close()
print("Schema update complete.")
