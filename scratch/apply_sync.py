import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def apply_sync():
    # Use components from .env
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port", "5432")
    dbname = os.getenv("dbname")
    
    if not all([user, password, host, dbname]):
        print("ERROR: Missing database credentials in .env")
        return

    # Construct SQLAlchemy URI
    encoded_password = quote_plus(password)
    db_url = f"postgresql://{user}:{encoded_password}@{host}:{port}/{dbname}"
    
    print(f"Connecting to Supabase (SQLAlchemy Sync) at: {host}")
    
    try:
        engine = create_engine(db_url)
        
        # Read the SQL script
        script_path = os.path.join(os.path.dirname(__file__), 'sync_schema.sql')
        with open(script_path, 'r') as f:
            sql_script = f.read()
        
        print("Executing sync script...")
        with engine.connect() as conn:
            # SQLAlchemy 2.0 requires text() and commit() if not in transaction
            # Using raw execution for multiple statements
            from sqlalchemy import text
            
            # Split script into individual statements to handle DO blocks and CREATE TABLE
            # However, for simplicity and since it's a migration, we can wrap in a transaction
            with conn.begin():
                conn.execute(text(sql_script))
        
        print("SUCCESS: Supabase schema updated successfully!")
        
    except Exception as e:
        print(f"ERROR: Failed to apply sync: {e}")

if __name__ == "__main__":
    apply_sync()
