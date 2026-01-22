
import os
from dotenv import load_dotenv
from utils.db_manager import get_database_uri

# Load ACTUAL .env file
load_dotenv()

# Mock VERCEL to True to see what happens in Vercel mode
os.environ["VERCEL"] = "1"
os.environ["DB_PROVIDER"] = "supabase"

print(f"DEBUG: host env var: '{os.getenv('host')}'")
print(f"DEBUG: user env var: '{os.getenv('user')}'")

uri = get_database_uri()
print(f"DEBUG: Constructed URI: {uri}")
