from flask import Blueprint, jsonify, request
from models import Attraction
from extensions import limiter
import logging

api_bp = Blueprint("api", __name__, url_prefix="/api")
logger = logging.getLogger(__name__)


# === LEGACY API Endpoints (Redirecting to Modules) ===

@api_bp.route("/heritage/<heritage_type>")
@api_bp.route("/heritage/<heritage_type>/<int:item_id>")
@api_bp.route("/heritage/types")
def api_heritage_redirect(*args, **kwargs):
    """Redirect legacy heritage API calls to the new module."""
    return jsonify({"error": "Moved to /heritage/api"}), 301


@api_bp.route("/establishments")
def api_establishments_redirect():
    """Redirect legacy establishments API calls to the new module."""
    return jsonify({"error": "Moved to /business/api"}), 301


# === Attraction API (To be moved later or kept here if shared) ===

@api_bp.route("/attractions")
@limiter.limit("20 per minute")
def api_attractions():
    """
    API endpoint to retrieve approved attractions with pagination.
    """
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    barangay = request.args.get("barangay", "all")
    category = request.args.get("category", "all")
    
    from utils.cache_helpers import cache_get, cache_set
    cache_key = f"api_attractions:p{page}:pp{per_page}:b{barangay}:c{category}"
    
    # Try cache
    cached_data = cache_get(cache_key)
    if cached_data:
        response = jsonify(cached_data)
        response.headers["X-Cache"] = "HIT"
        return response
        
    query = Attraction.query.filter_by(status="approved")
    
    if barangay and barangay != "all":
        from models import BarangayInfo
        query = query.join(BarangayInfo).filter(BarangayInfo.name == barangay)
    
    if category and category != "all":
        query = query.filter_by(category=category)
        
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    result = []
    for attr in paginated.items:
        result.append({
            "id": attr.id,
            "name": attr.name,
            "category": attr.category,
            "description": attr.description,
            "latitude": attr.latitude,
            "longitude": attr.longitude,
            "barangay": attr.barangay.name if attr.barangay else None,
            "image_url": attr.image_url,
            "osm_alternatives": attr.osm_alternatives
        })
        
    payload = {
        "attractions": result,
        "pagination": {
            "page": page,
            "total": paginated.total,
            "pages": paginated.pages
        }
    }
    
    # Store in cache for 5 minutes
    cache_set(cache_key, payload, ttl=300)
    
    response = jsonify(payload)
    response.headers["X-Cache"] = "MISS"
    return response

@api_bp.route("/map-feedback", methods=["POST"])
def submit_map_feedback():
    """
    Accepts feedback from the interactive map.
    """
    try:
        data = request.get_json()
        if not data or not data.get("message") or not data.get("type"):
            return jsonify({"error": "Missing required fields"}), 400
            
        from models import MapFeedback
        from extensions import db
        
        attraction_id = data.get("attraction_id")
        if not attraction_id or attraction_id == "":
            attraction_id = None
            
        new_feedback = MapFeedback(
            attraction_id=attraction_id,
            feedback_type=data.get("type"),
            message=data.get("message")
        )
        
        db.session.add(new_feedback)
        db.session.commit()
        
        return jsonify({"message": "Feedback submitted successfully"}), 201
        
    except Exception as e:
        logger.error(f"Error submitting map feedback: {str(e)}")
        return jsonify({"error": "An internal error occurred"}), 500
