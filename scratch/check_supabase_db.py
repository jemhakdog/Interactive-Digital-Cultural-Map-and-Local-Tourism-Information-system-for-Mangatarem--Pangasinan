import os
import sys
import psycopg2
from dotenv import load_dotenv

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def check_supabase():
    load_dotenv()
    
    user = os.getenv("user", "").strip()
    password = os.getenv("password", "").strip()
    host = os.getenv("host", "").strip()
    port = os.getenv("port", "5432").strip()
    dbname = os.getenv("dbname", "").strip()
    
    if not all([user, host, dbname]):
        print("Supabase credentials missing in .env!")
        return
        
    print(f"Connecting to Supabase host: {host}...")
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=dbname
        )
        cursor = conn.cursor()
        
        # Query to list all tables in the public schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\nFound {len(tables)} tables in Supabase database:")
        for t in tables:
            print(f"  - {t}")
            
        conn.close()
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")

if __name__ == "__main__":
    check_supabase()
