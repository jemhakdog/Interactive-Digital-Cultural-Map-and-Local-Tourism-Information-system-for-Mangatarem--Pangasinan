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
    
    barangay = request.args.get("barangay")
    category = request.args.get("category")
    
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
            "image_url": attr.image_url
        })
        
    return jsonify({
        "attractions": result,
        "pagination": {
            "page": page,
            "total": paginated.total,
            "pages": paginated.pages
        }
    })
