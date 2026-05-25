import os
import sys
import psycopg2
from dotenv import load_dotenv

def run_migration_and_cleanup():
    load_dotenv()
    
    user = os.getenv("user", "").strip()
    password = os.getenv("password", "").strip()
    host = os.getenv("host", "").strip()
    port = os.getenv("port", "5432").strip()
    dbname = os.getenv("dbname", "").strip()
    
    if not all([user, host, dbname]):
        print("Supabase credentials missing in .env!")
        return
        
    print(f"Connecting to Supabase at: {host}...")
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=dbname
        )
        cursor = conn.cursor()
        
        # 1. Migrate the unique 'barangay' user if it doesn't exist in USER table
        print("\nChecking if unique user 'barangay' needs migration...")
        cursor.execute('SELECT id, username, email, password_hash, role, barangay, is_approved FROM "user" WHERE username = \'barangay\'')
        lower_user = cursor.fetchone()
        
        if lower_user:
            username, email, pwd_hash, role, barangay_name, is_approved = lower_user[1], lower_user[2], lower_user[3], lower_user[4], lower_user[5], lower_user[6]
            
            # Check if this email or username already exists in uppercase "USER"
            cursor.execute('SELECT id FROM "USER" WHERE username = %s OR email = %s', (username, email))
            existing_user = cursor.fetchone()
            
            if not existing_user:
                print(f"Migrating user '{username}' to uppercase 'USER' table...")
                
                # Set barangay_id to None to avoid foreign key constraint issues on lowercase tables
                barangay_id = None
                
                # Insert into "USER"
                cursor.execute(
                    'INSERT INTO "USER" (username, email, password, role, barangay_id, is_approved, is_superuser) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (username, email, pwd_hash, role, barangay_id, is_approved, False)
                )
                print(f"Successfully migrated user '{username}' (Email: {email}, Role: {role})!")
            else:
                print(f"User '{username}' or email '{email}' already exists in uppercase 'USER' table. Skipping user migration.")
        else:
            print("No 'barangay' user found in lowercase 'user' table.")
            
        # Commit the user migration
        conn.commit()
        
        # 2. Drop the 39 safe-to-drop and duplicate lowercase/legacy tables
        tables_to_drop = [
            # Legacy obsolete tables
            "page_view", "event_interest", "favorite", "review",
            
            # Lowercase duplicates
            "analytics_page_view", "attraction", "attraction_review", "barangay_info", 
            "database_audit_log", "establishment", "establishment_menu_item", 
            "establishment_review", "establishment_room", "event", "gallery_item", 
            "heritage_profile", "newsletter_subscriber", "password_reset_token", 
            "user", "user_event_interest", "user_favorite_attraction",
            
            # Legacy detail tables (Uppercase)
            "BUILT_HERITAGE_DETAIL", "MOVABLE_HERITAGE_DETAIL", "NATURAL_HERITAGE_DETAIL",
            "INTANGIBLE_HERITAGE_DETAIL", "PERSONALITY_DETAIL", "INSTITUTION_DETAIL", 
            "LGU_PROGRAM_DETAIL",
            
            # Legacy detail tables (Lowercase)
            "built_heritage_detail", "built_heritage_details",
            "movable_heritage_detail", "movable_heritage_details",
            "natural_heritage_detail", "natural_heritage_details",
            "intangible_heritage_detail", "intangible_heritage_details",
            "personality_detail", "personality_details",
            "institution_detail", "institution_details",
            "lgu_program_detail", "lgu_program_details"
        ]
        
        print("\nExecuting drops for 39 duplicate and legacy tables...")
        for table in tables_to_drop:
            try:
                # Use double quotes to handle lowercase names correctly in PostgreSQL
                cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
                print(f"  [DROPPED] Table: \"{table}\"")
            except Exception as e:
                print(f"  [ERROR] Failed to drop table \"{table}\": {e}")
                conn.rollback()
                
        # Commit all drops
        conn.commit()
        print("\nAll database tables cleaned up successfully!")
        
        # 3. List remaining tables in Supabase public schema to verify
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        remaining_tables = [row[0] for row in cursor.fetchall()]
        print(f"\nRemaining tables in Supabase database ({len(remaining_tables)}):")
        for t in remaining_tables:
            print(f"  - {t}")
            
        conn.close()
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    run_migration_and_cleanup()
