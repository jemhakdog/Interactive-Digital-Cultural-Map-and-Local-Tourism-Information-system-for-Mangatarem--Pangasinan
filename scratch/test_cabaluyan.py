import requests

url = "https://nominatim.openstreetmap.org/search"
headers = {
    "User-Agent": "InteractiveMangataremCulturalMap/1.0 (zani31349@gmail.com)"
}

query = "Cabaluyan, Mangatarem, Pangasinan"
params = {
    "q": query,
    "format": "json",
    "addressdetails": 1,
    "limit": 1
}

r = requests.get(url, headers=headers, params=params)
if r.status_code == 200:
    data = r.json()
    if data:
        print(f"Cabaluyan found: {data[0].get('display_name')}")
        print(f"Coords: ({data[0].get('lat')}, {data[0].get('lon')})")
    else:
        print("Cabaluyan not found.")
else:
    print(f"Error {r.status_code}: {r.text}")
