import os
import sys

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sqlite3
from app import create_app
from extensions import db
import sqlalchemy as sa
from sqlalchemy import inspect

def verify_database():
    app = create_app()
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    print(f"Database URI: {db_uri}")
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # 1. Get all table names in the database
        db_tables = inspector.get_table_names()
        print(f"\nFound {len(db_tables)} tables in the database:")
        for t in sorted(db_tables):
            print(f"  - {t}")
            
        # 2. List of merged detail tables that were dropped
        merged_tables = [
            'BUILT_HERITAGE_DETAIL',
            'MOVABLE_HERITAGE_DETAIL',
            'NATURAL_HERITAGE_DETAIL',
            'INTANGIBLE_HERITAGE_DETAIL',
            'PERSONALITY_DETAIL',
            'INSTITUTION_DETAIL',
            'LGU_PROGRAM_DETAIL'
        ]
        
        print("\n--- Merged Tables Verification ---")
        print("Checking if old heritage detail tables were successfully dropped/merged:")
        
        dropped_successfully = True
        for mt in merged_tables:
            if mt in db_tables:
                print(f"  [FAIL] Old table '{mt}' STILL EXISTS in the database!")
                dropped_successfully = False
            else:
                print(f"  [OK] Old table '{mt}' is ABSENT from the database (Successfully merged!).")
                
        if dropped_successfully:
            print("\nSUCCESS: All 7 legacy heritage detail tables are absent from the database.")
            
        # 3. Check HERITAGE_PROFILE for form_data column
        print("\nChecking HERITAGE_PROFILE column structure:")
        hp_cols = {col['name']: col for col in inspector.get_columns('HERITAGE_PROFILE')}
        
        if 'form_data' in hp_cols:
            print("  [OK] 'form_data' column EXISTS in HERITAGE_PROFILE.")
            print(f"       Type: {hp_cols['form_data']['type']}")
        else:
            print("  [FAIL] 'form_data' column IS MISSING from HERITAGE_PROFILE!")
            
        # 4. Get all models registered in SQLAlchemy
        model_tables = db.metadata.tables
        
        # 5. Compare tables
        db_table_set = set(db_tables)
        model_table_set = set(model_tables.keys())
        
        missing_in_db = model_table_set - db_table_set
        extra_in_db = db_table_set - model_table_set
        common_tables = db_table_set & model_table_set
        
        if missing_in_db:
            print("\nWARNING: Tables defined in models but MISSING in database:")
            for t in sorted(missing_in_db):
                print(f"  - {t}")
        else:
            print("\nSUCCESS: All currently defined models have corresponding tables in the database.")
            
        if extra_in_db:
            print("\nINFO: Tables in database but NOT defined in active models:")
            for t in sorted(extra_in_db):
                print(f"  - {t}")
                
        # 6. Compare columns and types for common tables
        print("\n--- Detailed Table Schema Verification ---")
        discrepancies = []
        
        for table_name in sorted(common_tables):
            db_cols = {col['name']: col for col in inspector.get_columns(table_name)}
            model_table = model_tables[table_name]
            model_cols = model_table.columns
            
            db_col_names = set(db_cols.keys())
            model_col_names = set(model_cols.keys())
            
            missing_cols = model_col_names - db_col_names
            extra_cols = db_col_names - model_col_names
            common_cols = db_col_names & model_col_names
            
            table_status_printed = False
            
            if missing_cols:
                if not table_status_printed:
                    print(f"\nVerifying Table: {table_name}")
                    table_status_printed = True
                print(f"  [FAIL] Missing columns in DB: {', '.join(missing_cols)}")
                discrepancies.append((table_name, "missing_columns", list(missing_cols)))
            if extra_cols:
                if not table_status_printed:
                    print(f"\nVerifying Table: {table_name}")
                    table_status_printed = True
                print(f"  [WARN] Extra columns in DB: {', '.join(extra_cols)}")
                discrepancies.append((table_name, "extra_columns", list(extra_cols)))
                
            # Type and attribute verification for common columns
            type_mismatches = []
            for col_name in sorted(common_cols):
                db_col = db_cols[col_name]
                model_col = model_cols[col_name]
                
                db_type = str(db_col['type']).upper()
                model_type = str(model_col.type).upper()
                
                normalized_db = db_type
                normalized_model = model_type
                
                if "VARCHAR" in normalized_db or "TEXT" in normalized_db or "STRING" in normalized_db:
                    normalized_db = "TEXT/VARCHAR"
                if "VARCHAR" in normalized_model or "TEXT" in normalized_model or "STRING" in normalized_model:
                    normalized_model = "TEXT/VARCHAR"
                    
                if "INT" in normalized_db or "INTEGER" in normalized_db:
                    normalized_db = "INTEGER"
                if "INT" in normalized_model or "INTEGER" in normalized_model:
                    normalized_model = "INTEGER"
                    
                if "BOOLEAN" in normalized_db or "BOOL" in normalized_db:
                    normalized_db = "BOOLEAN"
                if "BOOLEAN" in normalized_model or "BOOL" in normalized_model:
                    normalized_model = "BOOLEAN"
                    
                if (normalized_db == "INTEGER" and normalized_model == "BOOLEAN") or (normalized_db == "BOOLEAN" and normalized_model == "INTEGER"):
                    pass
                elif normalized_db != normalized_model:
                    if not table_status_printed:
                        print(f"\nVerifying Table: {table_name}")
                        table_status_printed = True
                    print(f"  [WARN] Type mismatch for column '{col_name}': Model={model_type}, DB={db_type}")
                    type_mismatches.append((col_name, model_type, db_type))
            
            if type_mismatches:
                discrepancies.append((table_name, "type_mismatches", type_mismatches))
                
        if discrepancies:
            print(f"\nVerification completed with {len(discrepancies)} warnings/errors.")
        else:
            print("\nVerification completed successfully: DB matches active models perfectly!")

if __name__ == "__main__":
    verify_database()
