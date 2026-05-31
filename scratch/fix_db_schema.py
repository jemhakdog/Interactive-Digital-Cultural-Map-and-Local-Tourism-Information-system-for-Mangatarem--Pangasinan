"""
Database repair script to physically alter tables in SQLite and add missing consolidated columns.
"""

import sys
import os
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

def fix_schema():
    app = create_app()
    with app.app_context():
        # Get path to local SQLite database from Flask config
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if not db_uri.startswith('sqlite:///'):
            print("Database is not local SQLite. Bypassing manual migration.")
            return

        db_path = db_uri.replace('sqlite:///', '')
        # Handle relative/absolute paths correctly
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(os.path.join(app.root_path, db_path))
            
        print(f"Connecting to database: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Helper function to alter table safely
        def add_column_if_missing(table, column, type_def):
            try:
                # Check if column already exists
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]
                if column not in columns:
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type_def}")
                    print(f"Added column {column} ({type_def}) to table {table}")
                else:
                    print(f"Column {column} already exists in table {table}")
            except Exception as e:
                print(f"Error checking/adding {column} to {table}: {e}")

        # 1. Alter USER table
        add_column_if_missing("USER", "reset_token", "VARCHAR(128)")
        add_column_if_missing("USER", "reset_token_expires_at", "DATETIME")
        add_column_if_missing("USER", "reset_token_used", "BOOLEAN DEFAULT 0")

        # 2. Alter REVIEW table
        add_column_if_missing("REVIEW", "photo_urls", "JSON")

        # 3. Alter NEWSLETTER_SUBSCRIBER table
        add_column_if_missing("NEWSLETTER_SUBSCRIBER", "user_id", "INTEGER")

        # 4. Alter NEWSLETTER_HISTORY table
        add_column_if_missing("NEWSLETTER_HISTORY", "sender_id", "INTEGER")

        conn.commit()
        conn.close()
        print("Manual schema adjustments completed successfully!")

if __name__ == "__main__":
    fix_schema()
