from app import create_app

app = create_app()
with app.test_client() as client:
    res = client.get('/api/attractions?per_page=100')
    data = res.get_json()
    print("--- API Response Attractions ---")
    attractions = data.get("attractions", [])
    print(f"Total attractions returned by API: {len(attractions)}")
    for a in attractions:
        print(f"Name: {a['name']}")
        print(f"  osm_alternatives: {a.get('osm_alternatives')}")
