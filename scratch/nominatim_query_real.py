import urllib.request
import urllib.parse
import json

query = "Daang Kalikasan, Mangatarem"
url = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote(query) + "&format=json&addressdetails=1&limit=5"
req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9"
    }
)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("RAW NOMINATIM RESULTS:")
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
