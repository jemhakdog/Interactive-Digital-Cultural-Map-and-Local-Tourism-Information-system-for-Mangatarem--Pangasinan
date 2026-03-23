import os
import psycopg2
import traceback
from pathlib import Path
from dotenv import load_dotenv
from utils.db_manager import get_database_uri

load_dotenv()
os.environ['DB_PROVIDER'] = 'supabase'

def run_final_sync():
    uri = get_database_uri().replace('+psycopg2', '')
    print("Connecting to Supabase...")
    try:
        conn = psycopg2.connect(uri)
        cursor = conn.cursor()
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    migrations_dir = Path('migrations')
    
    # 1. Execute 002 (Sync/Renames with robust guards) - RUN FIRST
    f2 = migrations_dir / '002_sync_production_schema_postgresql.sql'
    print(f"Applying {f2.name} (Renames FIRST)...")
    with open(f2, 'r', encoding='utf-8') as f:
        sql002 = f.read()
        print(f"SQL 002 snippet: {sql002[:200]}...")
        try:
            cursor.execute(sql002)
            conn.commit()
            print("OK: 002 Sync/Renames Schema applied.")
        except Exception as e:
            conn.rollback()
            print(f"WARN: 002 might have had issues, but continuing: {e}")
            cursor = conn.cursor()

    # 2. Execute 001 (Initial Tables with IF NOT EXISTS) - RUN SECOND
    f1 = migrations_dir / '001_initial_schema_postgresql.sql'
    print(f"Applying {f1.name} (Creations SECOND)...")
    with open(f1, 'r', encoding='utf-8') as f:
        sql001 = f.read()
        print(f"SQL 001 snippet: {sql001[:200]}...")
        try:
            # Postgres can handle multi-statement strings if they don't have block-specific syntax issues
            cursor.execute(sql001)
            conn.commit()
            print("SUCCESS: 001 Initial Schema applied/verified.")
        except Exception as e:
            conn.rollback()
            print("ERROR: 001 Schema sync failed.")
            traceback.print_exc()

    conn.close()

if __name__ == "__main__":
    run_final_sync()
