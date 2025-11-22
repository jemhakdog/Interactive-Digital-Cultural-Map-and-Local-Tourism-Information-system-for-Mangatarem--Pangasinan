from flask import Blueprint, jsonify
from models import Attraction

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/attractions')
def api_attractions():
    """
    API endpoint to retrieve all approved attractions.
    
    Returns JSON array of attraction objects with properties:
    - id, name, category, barangay, description
    - lat, lng, image, rating
    
    Returns:
        JSON: List of approved attractions with their details.
    """
    attractions = Attraction.query.filter_by(status='approved').all()
    result = []
    for a in attractions:
        result.append({
            'id': a.id,
            'name': a.name,
            'category': a.category,
            'barangay': a.barangay,
            'description': a.description,
            'lat': a.lat,
            'lng': a.lng,
            'image': a.image_url,
            'rating': 4.5  # Placeholder rating until we implement reviews
        })
    return jsonify(result)
