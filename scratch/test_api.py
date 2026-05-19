import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()
with app.test_client() as client:
    response = client.get('/business/api')
    print("API Status Code:", response.status_code)
    data = response.get_json()
    print("Establishments in API:")
    for est in data.get('establishments', []):
        print(f"- {est['name']} (ID: {est['id']}, Type: {est['type']}, Lat: {est['latitude']}, Lng: {est['longitude']}, Barangay: {est['barangay']})")
