import requests
import time

url = "https://nominatim.openstreetmap.org/search"
headers = {
    "User-Agent": "InteractiveMangataremCulturalMap/1.0 (zani31349@gmail.com)"
}

test_scenarios = {
    "Pacalat River": [
        "Pacalat River, Mangatarem",
        "Pacalat, Mangatarem",
        "Pacalat River"
    ],
    "Manleluag Spring Protected Landscape": [
        "Manleluag Spring Protected Landscape, Mangatarem",
        "Manleluag Protected Landscape",
        "Manleluag Spring",
        "Manleluag"
    ],
    "Canding Falls": [
        "Canding Falls, Mangatarem",
        "Canding, Mangatarem",
        "Canding Falls",
        "Kanding Falls"
    ],
    "Timmanguyob Falls": [
        "Timmanguyob Falls, Mangatarem",
        "Timmanguyob Falls",
        "Timmanguyob, Mangatarem",
        "Timmanguyob"
    ],
    "Teraoka Farm": [
        "Teraoka Family Farm, Mangatarem",
        "Teraoka Farm",
        "Teraoka, Mangatarem",
        "Teraoka"
    ]
}

for name, queries in test_scenarios.items():
    print("\n==========================================")
    print(f"Testing scenarios for: {name}")
    print("==========================================")
    
    for query in queries:
        time.sleep(1.5)
        print(f"Querying: '{query}'...")
        params = {
            "q": query,
            "format": "json",
            "addressdetails": 1,
            "limit": 3
        }
        try:
            r = requests.get(url, headers=headers, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json()
                print(f"  Result count: {len(data)}")
                if data:
                    for i, item in enumerate(data[:2]):
                        print(f"    Match {i+1}: {item.get('display_name')}")
                        print(f"      Coords: ({item.get('lat')}, {item.get('lon')})")
                    break  # Found matches for this query, move to next scenario
            else:
                print(f"  Error: {r.status_code}")
        except Exception as e:
            print(f"  Exception: {e}")
