import json
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
INPUT_FILE = os.path.join(DATA_DIR, 'scraped_attractions.json')

# Real OSM Nominatim results for "Daang Kalikasan, Mangatarem"
real_nominatim_results = [
  {
    "place_id": 259926937,
    "osm_type": "way",
    "osm_id": 924562642,
    "lat": 15.7916101,
    "lon": 120.2798642,
    "display_name": "Nature's Highway (Daang Kalikasan), Calvo, Purok 2, Umangan, Mangatarem, Pangasinan, Ilocos Region, 2413, Philippines",
    "address": {
      "road": "Daang Kalikasan (Nature's Highway)",
      "quarter": "Calvo",
      "hamlet": "Purok 2",
      "village": "Umangan",
      "town": "Mangatarem",
      "state": "Pangasinan",
      "region": "Ilocos Region",
      "postcode": "2413",
      "country": "Philippines"
    },
    "boundingbox": ["15.7839620", "15.7997179", "120.2754410", "120.2835449"]
  },
  {
    "place_id": 260113683,
    "osm_type": "way",
    "osm_id": 836743679,
    "lat": 15.7818073,
    "lon": 120.2717012,
    "display_name": "Nature's Highway (Daang Kalikasan), Parian, Mangatarem, Pangasinan, Ilocos Region, 2413, Philippines",
    "address": {
      "road": "Daang Kalikasan (Nature's Highway)",
      "village": "Parian",
      "town": "Mangatarem",
      "state": "Pangasinan",
      "region": "Ilocos Region",
      "postcode": "2413",
      "country": "Philippines"
    },
    "boundingbox": ["15.7797653", "15.7839620", "120.2679717", "120.2754410"]
  },
  {
    "place_id": 260265190,
    "osm_type": "way",
    "osm_id": 836743680,
    "lat": 15.7796569,
    "lon": 120.2678505,
    "display_name": "Nature's Highway (Daang Kalikasan), Muelang, Mangatarem, Pangasinan, Ilocos Region, 2413, Philippines",
    "address": {
      "road": "Daang Kalikasan (Nature's Highway)",
      "village": "Muelang",
      "town": "Mangatarem",
      "state": "Pangasinan",
      "region": "Ilocos Region",
      "postcode": "2413",
      "country": "Philippines"
    },
    "boundingbox": ["15.7795484", "15.7797653", "120.2677292", "120.2679717"]
  }
]

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found!")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        attractions = json.load(f)

    for attr in attractions:
        if "daang kalikasan" in attr.get('name', '').lower():
            print("Found Daang Kalikasan! Overwriting with actual OSM Nominatim geocoding results...")
            
            # Primary coordinates
            primary = real_nominatim_results[0]
            attr['latitude'] = primary['lat']
            attr['longitude'] = primary['lon']
            attr['osm_details'] = {
                "place_id": primary["place_id"],
                "osm_type": primary["osm_type"],
                "osm_id": primary["osm_id"],
                "display_name": primary["display_name"],
                "boundingbox": primary["boundingbox"],
                "address": primary["address"]
            }
            
            # Alternatives
            alternatives = []
            for alt in real_nominatim_results[1:]:
                alternatives.append({
                    "lat": alt["lat"],
                    "lon": alt["lon"],
                    "display_name": alt["display_name"],
                    "address": alt["address"]
                })
            attr['osm_alternatives'] = alternatives
            print("Successfully updated Daang Kalikasan in scraped_attractions.json!")

    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(attractions, f, indent=2, ensure_ascii=False)
    print("Done writing to file!")

if __name__ == "__main__":
    main()
