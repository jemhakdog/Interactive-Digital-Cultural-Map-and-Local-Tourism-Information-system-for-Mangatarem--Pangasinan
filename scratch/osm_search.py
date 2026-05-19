import requests
import json

def get_mangatarem_pois():
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Overpass QL query to find POIs in Mangatarem administrative boundary
    query = """
    [out:json][timeout:90];
    area["name"="Mangatarem"]["boundary"="administrative"]->.searchArea;
    (
      // Accommodations
      node["tourism"~"hotel|motel|guest_house|inn|resort|camp_site"](area.searchArea);
      way["tourism"~"hotel|motel|guest_house|inn|resort|camp_site"](area.searchArea);
      
      // Dining / Food
      node["amenity"~"restaurant|fast_food|cafe|food_court|pub|bar"](area.searchArea);
      way["amenity"~"restaurant|fast_food|cafe|food_court|pub|bar"](area.searchArea);
      
      // Swimming pools / Resorts
      node["leisure"~"swimming_pool|water_park|resort"](area.searchArea);
      way["leisure"~"swimming_pool|water_park|resort"](area.searchArea);
      
      // Places of Worship (Religious)
      node["amenity"="place_of_worship"](area.searchArea);
      way["amenity"="place_of_worship"](area.searchArea);
      
      // Tourist attractions / Historic
      node["tourism"="attraction"](area.searchArea);
      way["tourism"="attraction"](area.searchArea);
      node["historic"~"monument|memorial|ruins|heritage"](area.searchArea);
      way["historic"~"monument|memorial|ruins|heritage"](area.searchArea);
    );
    out center;
    """
    
    print("Querying OpenStreetMap Overpass API for Mangatarem, Pangasinan...")
    headers = {
        'User-Agent': 'InteractiveDigitalMapForMangatarem/1.0 (jemcarlo46@gmail.com)',
        'Referer': 'https://mangatarem.gov.ph'
    }
    response = requests.post(overpass_url, data={'data': query}, headers=headers)
    
    if response.status_code != 200:
        print(f"Error querying Overpass API: HTTP {response.status_code}")
        print(response.text)
        return []
        
    data = response.json()
    elements = data.get('elements', [])
    print(f"Successfully retrieved {len(elements)} elements from OSM.")
    
    pois = []
    for elem in elements:
        tags = elem.get('tags', {})
        name = tags.get('name')
        if not name:
            # Skip unnamed features
            continue
            
        # Get coordinates
        lat = elem.get('lat')
        lon = elem.get('lon')
        if lat is None or lon is None:
            # If way/relation, center coords are in 'center' field
            center = elem.get('center', {})
            lat = center.get('lat')
            lon = center.get('lon')
            
        if lat is None or lon is None:
            continue
            
        poi_type = "other"
        
        # Classify POI based on tags
        if 'tourism' in tags and tags['tourism'] in ['hotel', 'motel', 'guest_house', 'inn', 'resort']:
            poi_type = "accommodation"
        elif 'amenity' in tags and tags['amenity'] in ['restaurant', 'fast_food', 'cafe', 'food_court']:
            poi_type = "dining"
        elif 'amenity' in tags and tags['amenity'] == 'place_of_worship':
            poi_type = "religious"
        elif 'leisure' in tags and tags['leisure'] in ['swimming_pool', 'water_park', 'resort']:
            poi_type = "leisure"
        elif 'tourism' in tags and tags['tourism'] == 'attraction':
            poi_type = "attraction"
        elif 'historic' in tags:
            poi_type = "heritage"
            
        pois.append({
            'name': name,
            'lat': lat,
            'lon': lon,
            'category': poi_type,
            'tags': tags
        })
        
    return pois

if __name__ == "__main__":
    pois = get_mangatarem_pois()
    print(f"\nFound {len(pois)} named POIs:")
    for i, poi in enumerate(pois, 1):
        print(f"{i}. [{poi['category'].upper()}] {poi['name']} ({poi['lat']}, {poi['lon']})")
        print(f"   Tags: {list(poi['tags'].keys())}")
        
    # Save to a json file
    with open("scratch/osm_pois.json", "w", encoding="utf-8") as f:
        json.dump(pois, f, indent=2, ensure_ascii=False)
    print("\nSaved POIs to scratch/osm_pois.json")
