import psycopg2
import os
from dotenv import load_dotenv
from utils.db_manager import get_database_uri

load_dotenv()
os.environ['DB_PROVIDER'] = 'supabase'

def check_case():
    uri = get_database_uri().replace('+psycopg2', '')
    conn = psycopg2.connect(uri)
    cursor = conn.cursor()
    
    # Check "USER" table casing in information_schema
    cursor.execute("""
        SELECT table_name, column_name 
        FROM information_schema.columns 
        WHERE table_name ILIKE 'user'
    """)
    rows = cursor.fetchall()
    print("Found columns for 'user':")
    for r in rows:
        print(f"Table: '{r[0]}', Column: '{r[1]}'")
        
    conn.close()

if __name__ == "__main__":
    check_case()
