import urllib.request
import urllib.parse
import json
import time

attractions = [
    {
        "name": "Daang Kalikasan",
        "query": "Daang Kalikasan, Mangatarem"
    },
    {
        "name": "Manleluag Spring Protected Landscape",
        "query": "Manleluag Hot Spring"
    },
    {
        "name": "St. Raymund de Penafort Church",
        "query": "Saint Raymund of Peñafort Parish Church, Mangatarem"
    },
    {
        "name": "Timmanguyob Falls",
        "query": "Timmanguyob Falls"
    },
    {
        "name": "Pacalat River",
        "query": "Pacalat, Mangatarem"
    },
    {
        "name": "Canding Falls",
        "query": "Canding Falls"
    },
    {
        "name": "Teraoka Farm",
        "query": "Teraoka Family Farm"
    }
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9"
}

results = {}

for attr in attractions:
    print(f"Querying for: {attr['name']}...")
    url = "https://nominatim.openstreetmap.org/search?q=" + urllib.parse.quote(attr['query']) + "&format=json&addressdetails=1&limit=5"
    req = urllib.request.Request(url, headers=headers)
    try:
        time.sleep(1.5)
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode())
            results[attr['name']] = data
            print(f"  Found {len(data)} results")
    except Exception as e:
        print(f"  Error: {e}")

with open("scratch/nominatim_all_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Finished!")
