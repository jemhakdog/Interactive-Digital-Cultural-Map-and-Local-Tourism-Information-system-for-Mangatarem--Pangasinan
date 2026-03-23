import os
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
from utils.db_manager import get_database_uri

load_dotenv()

# Force provider to supabase/postgres for testing
os.environ['DB_PROVIDER'] = 'supabase'

try:
    uri = get_database_uri()
    print(f"Connecting to host...") 
    engine = create_engine(uri)
    with engine.connect() as conn:
        for table in ['USER', 'ATTRACTION', 'EVENT', 'BARANGAY_INFO', 'HERITAGE_PROFILE']:
            result = conn.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table.lower()}'"))
            cols = [row[0] for row in result]
            if not cols:
                 result = conn.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"))
                 cols = [row[0] for row in result]
            print(f"TABLE {table}: {cols}")

except Exception as e:
    print(f"ERROR: {e}")
