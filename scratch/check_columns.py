import os
import psycopg2
from dotenv import load_dotenv

def check_cols():
    load_dotenv()
    conn = psycopg2.connect(
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),
        database=os.getenv("dbname")
    )
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM "ESTABLISHMENT_REVIEW" LIMIT 1')
    print("ESTABLISHMENT_REVIEW columns:", [d[0] for d in cur.description])
    
    conn.close()

if __name__ == "__main__":
    check_cols()
