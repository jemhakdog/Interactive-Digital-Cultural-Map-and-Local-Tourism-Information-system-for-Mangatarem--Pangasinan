import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("mapbox_token")

attractions = [
    "Daang Kalikasan",
    "Pacalat River",
    "Manleluag Spring Protected Landscape",
    "Canding Falls",
    "Timmanguyob Falls",
    "Teraoka Farm"
]

for name in attractions:
    print(f"\nGeocoding '{name}'...")
    # Mapbox Geocoding prefers URL-encoded queries in the path
    query = f"{name}, Mangatarem, Pangasinan, Philippines"
    encoded_query = quote(query)
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{encoded_query}.json"
    
    params = {
        "access_token": token,
        "limit": 5
    }
    
    try:
        r = requests.get(url, params=params, timeout=5)
        if r.status_code == 200:
            data = r.json()
            features = data.get("features", [])
            print(f"Status 200, matches: {len(features)}")
            for idx, feat in enumerate(features[:3]):
                lon, lat = feat["center"]
                print(f"  Match {idx+1}: {feat['place_name']}")
                print(f"    Coords: ({lat}, {lon})")
        else:
            print(f"Status {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
