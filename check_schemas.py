import psycopg2
import os
from dotenv import load_dotenv
from utils.db_manager import get_database_uri

load_dotenv()
os.environ['DB_PROVIDER'] = 'supabase'

def check_schemas():
    uri = get_database_uri().replace('+psycopg2', '')
    conn = psycopg2.connect(uri)
    cursor = conn.cursor()
    
    # Check all schemas for 'USER' table
    cursor.execute("""
        SELECT table_schema, table_name, column_name 
        FROM information_schema.columns 
        WHERE table_name ILIKE 'user' AND column_name ILIKE 'password_hash'
    """)
    rows = cursor.fetchall()
    print("Found 'password_hash' in these tables:")
    for r in rows:
        print(f"Schema: {r[0]}, Table: {r[1]}, Column: {r[2]}")
        
    conn.close()

if __name__ == "__main__":
    check_schemas()
