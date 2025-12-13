from flask import Blueprint, jsonify
from models import Attraction
import logging

api_bp = Blueprint('api', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

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
    print("=== API: Fetching attractions ===")
    logger.info("API endpoint /api/attractions called")
    
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
    
    print(f"=== API: Returning {len(result)} attractions ===")
    logger.info(f"Returning {len(result)} approved attractions")
    return jsonify(result)
