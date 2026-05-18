import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Set VERCEL=1 to prevent app.py from running db.create_all() or seeding
os.environ['VERCEL'] = '1'
os.environ['DB_PROVIDER'] = 'supabase'

from app import create_app
from extensions import db

def check_schema():
    print("Initializing Flask App context...")
    app = create_app('production')
    
    with app.app_context():
        supabase_uri = app.config['SQLALCHEMY_DATABASE_URI']
        display_uri = supabase_uri.split('@')[1] if '@' in supabase_uri else supabase_uri
        print(f"Connecting to Supabase at: {display_uri}")
        
        try:
            live_engine = create_engine(supabase_uri)
            live_inspector = inspect(live_engine)
            
            # Get live tables and map them to lowercase
            live_tables = live_inspector.get_table_names()
            live_tables_lower = {t.lower(): t for t in live_tables}
            
            # Get local models
            local_metadata = db.metadata
            local_tables = local_metadata.tables
            
            mismatches = []
            
            print(f"\nComparing {len(local_tables)} local models with Supabase (Case-Insensitive)...")
            
            print("\n--- TABLE CHECK ---")
            for table_name, local_table in sorted(local_tables.items()):
                table_name_lower = table_name.lower()
                
                if table_name_lower not in live_tables_lower:
                    print(f"[MISSING TABLE] '{table_name}' is missing in Supabase")
                    mismatches.append(('missing_table', table_name))
                else:
                    actual_table_name = live_tables_lower[table_name_lower]
                    if actual_table_name != table_name:
                        print(f"[CASE MISMATCH] Model says '{table_name}', Supabase has '{actual_table_name}'")
                    
                    # Check columns
                    live_columns = live_inspector.get_columns(actual_table_name)
                    live_col_names_lower = {c['name'].lower(): c['name'] for c in live_columns}
                    
                    table_ok = True
                    for col_name, local_col in local_table.columns.items():
                        col_name_lower = col_name.lower()
                        if col_name_lower not in live_col_names_lower:
                            print(f"[MISSING COLUMN] '{actual_table_name}.{col_name}' is missing in Supabase")
                            mismatches.append(('missing_column', f"{actual_table_name}.{col_name}"))
                            table_ok = False
                    
                    if table_ok:
                        print(f"[MATCH] '{table_name}' (as '{actual_table_name}')")

            # Extra tables check
            local_tables_lower = {t.lower() for t in local_tables.keys()}
            extra_tables = [t for t in live_tables if t.lower() not in local_tables_lower and not t.startswith('alembic')]
            if extra_tables:
                print("\n--- EXTRA TABLES IN SUPABASE ---")
                for t in sorted(extra_tables):
                    print(f"[EXTRA] {t}")

            print("\n" + "="*40)
            if not mismatches:
                print("SUCCESS: Functional schema match found!")
            else:
                print(f"FAILURE: Found {len(mismatches)} functional mismatches.")
            print("="*40)
            
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    check_schema()
