import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

print(f"Connecting to: {url}")

try:
    supabase: Client = create_client(url, key)
    # Try a simple query
    response = supabase.table('attraction').select("count", count="exact").limit(1).execute()
    print(f"Connection successful! Found {response.count} attractions.")
except Exception as e:
    print(f"Failed to connect: {e}")
