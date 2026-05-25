import os
import sys
import psycopg2
from dotenv import load_dotenv

def inspect_records():
    load_dotenv()
    
    user = os.getenv("user", "").strip()
    password = os.getenv("password", "").strip()
    host = os.getenv("host", "").strip()
    port = os.getenv("port", "5432").strip()
    dbname = os.getenv("dbname", "").strip()
    
    if not all([user, host, dbname]):
        print("Supabase credentials missing!")
        return
        
    print(f"Connecting to Supabase to inspect records: {host}...")
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=dbname
        )
        cursor = conn.cursor()
        
        # 1. Inspect "user" vs "USER"
        print("\n=== USER COMPARISON ===")
        cursor.execute('SELECT id, username, email, role FROM "USER"')
        upper_users = cursor.fetchall()
        print(f"Uppercase \"USER\" table ({len(upper_users)} records):")
        for u in upper_users:
            print(f"  - ID: {u[0]}, Username: {u[1]}, Email: {u[2]}, Role: {u[3]}")
            
        cursor.execute('SELECT id, username, email, role FROM "user"')
        lower_users = cursor.fetchall()
        print(f"\nLowercase \"user\" table ({len(lower_users)} records):")
        for u in lower_users:
            print(f"  - ID: {u[0]}, Username: {u[1]}, Email: {u[2]}, Role: {u[3]}")
            
        # 2. Inspect "attraction" vs "ATTRACTION"
        print("\n=== ATTRACTION COMPARISON ===")
        cursor.execute('SELECT id, name, category, status FROM "ATTRACTION"')
        upper_attrs = cursor.fetchall()
        print(f"Uppercase \"ATTRACTION\" table ({len(upper_attrs)} records):")
        for a in upper_attrs:
            print(f"  - ID: {a[0]}, Name: {a[1]}, Category: {a[2]}, Status: {a[3]}")
            
        cursor.execute('SELECT id, name, category, status FROM "attraction"')
        lower_attrs = cursor.fetchall()
        print(f"\nLowercase \"attraction\" table ({len(lower_attrs)} records):")
        for a in lower_attrs:
            print(f"  - ID: {a[0]}, Name: {a[1]}, Category: {a[2]}, Status: {a[3]}")
            
        # 3. Inspect "page_view"
        print("\n=== PAGE VIEW DATA ===")
        cursor.execute('SELECT COUNT(*) FROM "page_view"')
        pv_count = cursor.fetchone()[0]
        print(f"Legacy \"page_view\" table has {pv_count} rows.")
        if pv_count > 0:
            cursor.execute('SELECT page_url, timestamp LIMIT 5')
            try:
                pvs = cursor.fetchall()
                print("First 5 page views in legacy table:")
                for pv in pvs:
                    print(f"  - URL: {pv[0]}, Timestamp: {pv[1]}")
            except Exception as e:
                print(f"  Could not print rows: {e}")
                
        conn.close()
    except Exception as e:
        print(f"Error inspecting: {e}")

if __name__ == "__main__":
    inspect_records()
