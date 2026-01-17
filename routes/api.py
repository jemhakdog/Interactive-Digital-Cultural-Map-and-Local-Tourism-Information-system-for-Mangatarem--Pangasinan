from flask import Blueprint, jsonify, request, make_response
from models import Attraction, db
from extensions import limiter
import logging
from datetime import datetime, timedelta

api_bp = Blueprint("api", __name__, url_prefix="/api")
logger = logging.getLogger(__name__)


@api_bp.route("/attractions")
@limiter.limit("20 per minute")
def api_attractions():
    """
    API endpoint to retrieve approved attractions with pagination.

    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Number of attractions per page (default: 20, max: 100)
    - category: Filter by category
    - barangay: Filter by barangay

    Returns JSON array of attraction objects with properties:
    - id, name, category, barangay, description
    - lat, lng, image, rating

    Returns:
        JSON: Paginated list of approved attractions with their details.
    """
    print(f"[PROGRESSIVE LOG] [api] > api_attractions > ENTRY")
    logger.info("API endpoint /api/attractions called")

    # Get pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", 20, type=int), 100
    )  # Cap at 100 per page

    # Get filter parameters
    category = request.args.get("category")
    barangay = request.args.get("barangay")

    print(
        f"[PROGRESSIVE LOG] [api] > api_attractions > QUERY: Fetching attractions with pagination (page={page}, per_page={per_page})"
    )

    # Build query with filters and only select needed columns
    query = db.session.query(
        Attraction.id,
        Attraction.name,
        Attraction.category,
        Attraction.barangay,
        Attraction.description,
        Attraction.lat,
        Attraction.lng,
        Attraction.image_url,
    ).filter(Attraction.status == "approved")

    if category and category != "all":
        query = query.filter(Attraction.category == category)
    if barangay and barangay != "all":
        query = query.filter(Attraction.barangay == barangay)

    # Paginate the results
    paginated_attractions = query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    result = []
    for a in paginated_attractions.items:
        result.append(
            {
                "id": a[0],  # id
                "name": a[1],  # name
                "category": a[2],  # category
                "barangay": a[3],  # barangay
                "description": a[4],  # description
                "lat": a[5],  # lat
                "lng": a[6],  # lng
                "image": a[7],  # image_url
                "rating": 4.5,  # Placeholder rating until we implement reviews
            }
        )

    response_data = {
        "attractions": result,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": paginated_attractions.total,
            "pages": paginated_attractions.pages,
            "has_next": paginated_attractions.has_next,
            "has_prev": paginated_attractions.has_prev,
        },
    }

    print(
        f"[PROGRESSIVE LOG] [api] > api_attractions > SUCCESS: Returning {len(result)} attractions (page {page}/{paginated_attractions.pages})"
    )
    logger.info(
        f"Returning {len(result)} approved attractions (page {page}/{paginated_attractions.pages})"
    )

    # Create response with caching headers
    response = make_response(jsonify(response_data))
    response.headers["Cache-Control"] = "public, max-age=300"  # Cache for 5 minutes
    response.headers["Expires"] = (datetime.utcnow() + timedelta(minutes=5)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    return response
