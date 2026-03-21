import psycopg2
import os
from dotenv import load_dotenv
from utils.db_manager import get_database_uri

load_dotenv()
os.environ['DB_PROVIDER'] = 'supabase'

def check_exact_names():
    uri = get_database_uri().replace('+psycopg2', '')
    conn = psycopg2.connect(uri)
    cursor = conn.cursor()
    
    # Get all tables in public schema
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    rows = cursor.fetchall()
    print("Tables in 'public' schema:")
    for r in rows:
        print(f"'{r[0]}'")
        
    conn.close()

if __name__ == "__main__":
    check_exact_names()
