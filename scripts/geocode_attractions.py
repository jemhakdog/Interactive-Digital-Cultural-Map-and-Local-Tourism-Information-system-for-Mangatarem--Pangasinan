import json
import os
import sys
import time
import requests

# Set file paths
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
INPUT_FILE = os.path.join(DATA_DIR, 'scraped_attractions.json')

# Compliant custom User-Agent utilizing a real project email to bypass Nominatim's spam filter
HEADERS = {
    "User-Agent": "InteractiveMangataremCulturalMap/1.0 (zani31349@gmail.com)"
}

def query_nominatim(queries):
    """
    Sequentially query Nominatim with fallback options, rate-limited at 1.5 seconds per request.
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    
    for query in queries:
        print(f"  [HTTP] Querying Nominatim for: '{query}'...")
        params = {
            "q": query,
            "format": "json",
            "addressdetails": 1,
            "limit": 5
        }
        
        try:
            # Strictly respect Nominatim usage policy (1 request per second max)
            time.sleep(1.5)
            
            response = requests.get(base_url, headers=HEADERS, params=params, timeout=10)
            if response.status_code == 200:
                results = response.json()
                if results:
                    print(f"  [SUCCESS] Found {len(results)} matches for '{query}'!")
                    return results
            else:
                print(f"  [WARN] Nominatim HTTP Error {response.status_code} for query '{query}'")
        except Exception as e:
            print(f"  [ERROR] Network error geocoding '{query}': {e}")
            
    return []

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERROR] Input file {INPUT_FILE} not found!")
        sys.exit(1)
        
    print(f"[START] Loading attractions from {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        attractions = json.load(f)
        
    print(f"[INFO] Found {len(attractions)} attractions to geocode.")
    
    updated_count = 0
    
    for attr in attractions:
        name = attr.get('name')
        print(f"\n[GEOCODE] Processing attraction: '{name}'")
        
        # Build optimized query sequential search and custom hardcoded fallbacks
        queries = []
        hardcoded_fallback = None
        
        if "daang kalikasan" in name.lower():
            queries = [
                "Daang Kalikasan, Calvo, Umangan, Mangatarem",
                "Daang Kalikasan",
                "Daang Kalikasan, Mangatarem"
            ]
        elif "pacalat" in name.lower():
            queries = [
                "Pacalat River, Mangatarem",
                "Pacalat, Mangatarem"
            ]
        elif "manleluag" in name.lower():
            queries = [
                "Manleluag Hot Spring",
                "Manleluag Spring, Mangatarem",
                "Manleluag Protected Landscape",
                "Manleluag"
            ]
        elif "canding" in name.lower():
            queries = [
                "Canding Falls",
                "Canding Falls, San Clemente",
                "Kanding Falls, Mangatarem"
            ]
        elif "timmanguyob" in name.lower():
            queries = [
                "Timmanguyob Falls",
                "Timmanguyob, San Clemente"
            ]
            # Precise coordinates obtained through research (border Maasin, San Clemente)
            hardcoded_fallback = {
                "lat": 15.643861,
                "lon": 120.282089,
                "display_name": "Timmanguyob Falls, Maasin, San Clemente, Tarlac / Border Mangatarem, Pangasinan"
            }
        elif "teraoka" in name.lower():
            queries = [
                "Teraoka Family Farm, Mangatarem",
                "Teraoka Agri-Tourism",
                "Cabaluyan, Mangatarem"
            ]
            
        # Execute geocoding
        results = query_nominatim(queries)
        
        if results:
            primary = results[0]
            lat = float(primary.get('lat'))
            lon = float(primary.get('lon'))
            
            attr['latitude'] = lat
            attr['longitude'] = lon
            
            # Save full primary details in OSM format
            attr['osm_details'] = {
                "place_id": primary.get("place_id"),
                "osm_type": primary.get("osm_type"),
                "osm_id": primary.get("osm_id"),
                "display_name": primary.get("display_name"),
                "boundingbox": primary.get("boundingbox"),
                "address": primary.get("address", {})
            }
            
            # Save alternative matches (like different barangay matching options)
            alternatives = []
            for alt in results[1:]:
                alternatives.append({
                    "lat": float(alt.get('lat')),
                    "lon": float(alt.get('lon')),
                    "display_name": alt.get("display_name"),
                    "address": alt.get("address", {})
                })
            attr['osm_alternatives'] = alternatives
            
            print(f"  [SAVED] Assigned coordinates: ({lat}, {lon})")
            updated_count += 1
            
        elif hardcoded_fallback:
            # Fall back to high-accuracy hardcoded research coords if Nominatim lacks it entirely
            lat = hardcoded_fallback["lat"]
            lon = hardcoded_fallback["lon"]
            display_name = hardcoded_fallback["display_name"]
            
            attr['latitude'] = lat
            attr['longitude'] = lon
            attr['osm_details'] = {
                "place_id": "hardcoded_fallback",
                "osm_type": "node",
                "display_name": display_name,
                "address": {"county": "Mangatarem/San Clemente", "state": "Pangasinan/Tarlac"}
            }
            attr['osm_alternatives'] = []
            
            print(f"  [SAVED] Assigned research coordinates: ({lat}, {lon})")
            updated_count += 1
            
        else:
            print("  [KEEP] No results found across all fallbacks. Keeping original coordinates.")
            if 'latitude' not in attr:
                attr['latitude'] = None
                attr['longitude'] = None
                attr['osm_details'] = None
                attr['osm_alternatives'] = []
                
    # Save the updated attractions back to file
    print(f"\n[SAVING] Writing updated dataset back to {INPUT_FILE}...")
    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(attractions, f, indent=2, ensure_ascii=False)
        
    print(f"[FINISHED] Geocoded and updated {updated_count}/{len(attractions)} attractions successfully!")

if __name__ == "__main__":
    main()
