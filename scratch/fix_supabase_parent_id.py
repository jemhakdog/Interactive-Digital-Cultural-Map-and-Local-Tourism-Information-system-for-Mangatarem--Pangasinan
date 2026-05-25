import os
import psycopg2
from dotenv import load_dotenv

def fix_parent_id():
    load_dotenv()
    conn = psycopg2.connect(
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("dbname")
    )
    cur = conn.cursor()
    
    print("Adding parent_id column to ESTABLISHMENT_REVIEW...")
    try:
        cur.execute('ALTER TABLE "ESTABLISHMENT_REVIEW" ADD COLUMN IF NOT EXISTS parent_id INTEGER REFERENCES "ESTABLISHMENT_REVIEW"(id) ON DELETE CASCADE')
        conn.commit()
        print("Successfully added parent_id column!")
    except Exception as e:
        print(f"Error adding parent_id: {e}")
        conn.rollback()
        
    conn.close()

if __name__ == "__main__":
    fix_parent_id()
