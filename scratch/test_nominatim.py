import urllib.request
import urllib.parse
import json

query = "Daang Kalikasan, Mangatarem, Pangasinan, Philippines"
url = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote(query) + "&format=json&addressdetails=1&limit=5"
req = urllib.request.Request(
    url,
    headers={"User-Agent": "MangataremHeritageProject/1.0 (contact: test@example.com)"}
)

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
