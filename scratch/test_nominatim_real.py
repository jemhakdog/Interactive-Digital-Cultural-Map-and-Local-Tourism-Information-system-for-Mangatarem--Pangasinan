import requests
import time

url = "https://nominatim.openstreetmap.org/search"
headers = {
    # Using a real contact email as required by OSM policy to avoid automated spam blocks
    "User-Agent": "InteractiveMangataremCulturalMap/1.0 (zani31349@gmail.com)"
}

attractions = [
    "Daang Kalikasan",
    "Pacalat River",
    "Manleluag Spring Protected Landscape",
    "Canding Falls",
    "Timmanguyob Falls",
    "Teraoka Farm"
]

for name in attractions:
    print(f"\nQuerying '{name}'...")
    query = f"{name}, Mangatarem, Pangasinan, Philippines"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 3
    }
    
    # Strictly respect Nominatim rate limits (at least 1.2 seconds between requests)
    time.sleep(1.5)
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"Status Code: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Matches: {len(data)}")
            if data:
                print(f"  Match 1: {data[0].get('display_name')}")
                print(f"  Coords: ({data[0].get('lat')}, {data[0].get('lon')})")
        else:
            print(f"Response: {r.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
