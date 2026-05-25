import os
import sys
import psycopg2
from dotenv import load_dotenv

def audit_and_prepare_cleanup():
    load_dotenv()
    
    user = os.getenv("user", "").strip()
    password = os.getenv("password", "").strip()
    host = os.getenv("host", "").strip()
    port = os.getenv("port", "5432").strip()
    dbname = os.getenv("dbname", "").strip()
    
    if not all([user, host, dbname]):
        print("Supabase credentials missing in .env!")
        return
        
    print(f"Connecting to Supabase host to audit rows: {host}...")
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=dbname
        )
        cursor = conn.cursor()
        
        # 1. Get all tables in public schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\nAuditing row counts for {len(tables)} tables:")
        row_counts = {}
        for t in tables:
            try:
                # Use double quotes to preserve case-sensitivity in PostgreSQL
                cursor.execute(f'SELECT COUNT(*) FROM "{t}"')
                count = cursor.fetchone()[0]
                row_counts[t] = count
                print(f"  - \"{t}\": {count} rows")
            except Exception as e:
                print(f"  - \"{t}\": Error querying rows ({e})")
                conn.rollback()
                
        # 2. Analyze duplicates
        print("\n--- DUPLICATE TABLE ANALYSIS ---")
        
        duplicates = [
            ("ANALYTICS_PAGE_VIEW", "analytics_page_view"),
            ("ATTRACTION", "attraction"),
            ("ATTRACTION_REVIEW", "attraction_review"),
            ("BARANGAY_INFO", "barangay_info"),
            ("DATABASE_AUDIT_LOG", "database_audit_log"),
            ("ESTABLISHMENT", "establishment"),
            ("ESTABLISHMENT_MENU_ITEM", "establishment_menu_item"),
            ("ESTABLISHMENT_REVIEW", "establishment_review"),
            ("ESTABLISHMENT_ROOM", "establishment_room"),
            ("EVENT", "event"),
            ("GALLERY_ITEM", "gallery_item"),
            ("HERITAGE_PROFILE", "heritage_profile"),
            ("NEWSLETTER_SUBSCRIBER", "newsletter_subscriber"),
            ("PASSWORD_RESET_TOKEN", "password_reset_token"),
            ("USER", "user"),
            ("USER_EVENT_INTEREST", "user_event_interest"),
            ("USER_FAVORITE_ATTRACTION", "user_favorite_attraction")
        ]
        
        safe_to_drop_lowercase = []
        action_required = []
        
        for upper, lower in duplicates:
            u_count = row_counts.get(upper, 0)
            l_count = row_counts.get(lower, 0)
            
            print(f"Comparison: \"{upper}\" ({u_count} rows) vs \"{lower}\" ({l_count} rows)")
            
            if l_count == 0:
                safe_to_drop_lowercase.append(lower)
            else:
                action_required.append((upper, lower, u_count, l_count))
                
        # 3. Analyze legacy detail tables
        legacy_tables = [
            'BUILT_HERITAGE_DETAIL', 'built_heritage_detail', 'built_heritage_details',
            'MOVABLE_HERITAGE_DETAIL', 'movable_heritage_detail', 'movable_heritage_details',
            'NATURAL_HERITAGE_DETAIL', 'natural_heritage_detail', 'natural_heritage_details',
            'INTANGIBLE_HERITAGE_DETAIL', 'intangible_heritage_detail', 'intangible_heritage_details',
            'PERSONALITY_DETAIL', 'personality_detail', 'personality_details',
            'INSTITUTION_DETAIL', 'institution_detail', 'institution_details',
            'LGU_PROGRAM_DETAIL', 'lgu_program_detail', 'lgu_program_details',
            'page_view', 'event_interest', 'favorite', 'review'
        ]
        
        print("\n--- LEGACY TABLES ANALYSIS ---")
        safe_to_drop_legacy = []
        legacy_action_required = []
        
        for lt in legacy_tables:
            if lt in row_counts:
                count = row_counts[lt]
                print(f"Legacy table \"{lt}\": {count} rows")
                if count == 0:
                    safe_to_drop_legacy.append(lt)
                else:
                    legacy_action_required.append((lt, count))
                    
        # 4. Summary & Recommendations
        print("\n=== CLEANUP RECOMMENDATION SUMMARY ===")
        print(f"1. Safe to drop immediately (0 rows): {len(safe_to_drop_lowercase) + len(safe_to_drop_legacy)} tables")
        for t in sorted(safe_to_drop_lowercase + safe_to_drop_legacy):
            print(f"   - DROP TABLE \"{t}\" CASCADE;")
            
        if action_required or legacy_action_required:
            print("\n🚨 WARNING: Data migration or review required for the following tables before dropping:")
            for upper, lower, u_count, l_count in action_required:
                print(f"   - Lowercase table \"{lower}\" has {l_count} rows, while Uppercase \"{upper}\" has {u_count} rows.")
            for lt, count in legacy_action_required:
                print(f"   - Legacy table \"{lt}\" has {count} rows. Data must be merged/imported to HeritageProfile.form_data.")
        else:
            print("\n🎉 Excellent! All duplicate and legacy tables are empty and can be safely dropped without data loss.")
            
        conn.close()
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")

if __name__ == "__main__":
    audit_and_prepare_cleanup()
