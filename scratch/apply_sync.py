import os
import sys
import psycopg2
from dotenv import load_dotenv
from urllib.parse import quote_plus, urlparse

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def apply_sync():
    # Use components from .env for robustness
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port", "5432")
    dbname = os.getenv("dbname")
    
    # Supabase usually uses port 5432 for direct and 6543 for pooler. 
    # For DDL (Data Definition Language) like CREATE/ALTER, direct connection (5432) is often preferred.
    
    conn_str = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    
    print(f"Connecting to Supabase (DDL Sync) at: {host}")
    
    try:
        conn = psycopg2.connect(conn_str)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Read the SQL script
        script_path = os.path.join(os.path.dirname(__file__), 'sync_schema.sql')
        with open(script_path, 'r') as f:
            sql_script = f.read()
        
        print("Executing sync script...")
        cur.execute(sql_script)
        
        print("SUCCESS: Supabase schema updated successfully!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"ERROR: Failed to apply sync: {e}")
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    apply_sync()
