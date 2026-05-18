import os
import psycopg2
import traceback
from pathlib import Path
from dotenv import load_dotenv
from utils.db_manager import get_database_uri

load_dotenv()

# Force provider to supabase/postgres for testing
os.environ['DB_PROVIDER'] = 'supabase'

def run_debug():
    uri = get_database_uri()
    # psycopg2.connect doesn't like +psycopg2 and some other params
    if '+psycopg2' in uri:
        uri = uri.replace('+psycopg2', '')
    
    print("Connecting to host...") 
    try:
        conn = psycopg2.connect(uri)
    except Exception as e:
        print(f"Connection failed: {e}")
        return
        
    cursor = conn.cursor()
    
    migrations_dir = Path('migrations')
    # Try 001
    f1 = migrations_dir / '001_initial_schema_postgresql.sql'
    print(f"Running {f1.name}...")
    with open(f1, 'r', encoding='utf-8') as f:
        sql = f.read()
        try:
            # Split by semicolon for Postgres
            statements = [s.strip() for s in sql.split(';') if s.strip()]
            for s in statements:
                if not s.startswith('--'):
                    cursor.execute(s)
            conn.commit()
            print("✓ 001 Success")
            print("OK 001 Success")
        except Exception as e:
            conn.rollback()
            print(f"FAIL 001 Failed: {e}")
            traceback.print_exc()
            # Continue to 002? Maybe 001 failed because tables exist but 002 handles them.
            
    # Try 002
    f2 = migrations_dir / '002_sync_production_schema_postgresql.sql'
    print(f"Running {f2.name}...")
    with open(f2, 'r', encoding='utf-8') as f:
        sql = f.read()
        try:
            # 002 has complex DO blocks, need to be careful with splitting
            # But DO blocks end with END $$;
            # Let's try executing the whole thing or split by $$;?
            # Actually, standard psycopg2 execute works for multiple statements if they are valid SQL
            cursor.execute(sql)
            conn.commit()
            print("OK 002 Success")
        except Exception as e:
            conn.rollback()
            print(f"FAIL 002 Failed: {e}")
            traceback.print_exc()

    conn.close()

if __name__ == "__main__":
    run_debug()
