import os
import sys
import psycopg2
from dotenv import load_dotenv

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def debug_schema():
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port", "5432")
    dbname = os.getenv("dbname")
    
    conn_str = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        print("--- TABLES IN PUBLIC SCHEMA ---")
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        tables = cur.fetchall()
        for t in tables:
            print(f"Table: {t[0]}")
            
        print("\n--- COLUMNS FOR 'attraction' / 'ATTRACTION' ---")
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name IN ('attraction', 'ATTRACTION') AND table_schema = 'public'")
        cols = cur.fetchall()
        for c in cols:
            print(f"Column: {c[0]}")
            
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug_schema()
