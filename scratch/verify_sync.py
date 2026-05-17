from app import create_app
from models import Attraction

app = create_app()
with app.app_context():
    daang = Attraction.query.filter(Attraction.name.like('%Daang%')).first()
    if daang:
        print(f"Name: {daang.name}")
        print(f"Primary Lat/Lng: ({daang.latitude}, {daang.longitude})")
        print(f"OSM Alternatives Type: {type(daang.osm_alternatives)}")
        print(f"OSM Alternatives Content: {daang.osm_alternatives}")
    else:
        print("Daang Kalikasan attraction not found in DB.")
