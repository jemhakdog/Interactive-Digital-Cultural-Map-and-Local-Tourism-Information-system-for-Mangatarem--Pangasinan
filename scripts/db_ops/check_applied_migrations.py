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
        result = conn.execute(text("SELECT migration_name FROM _migrations ORDER BY id"))
        applied = [row[0] for row in result]
        print(f"Applied migrations: {applied}")

except Exception as e:
    print(f"ERROR: {e}")
