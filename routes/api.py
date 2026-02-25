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
    logger.info("API endpoint /api/attractions called")

    # Get pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page = min(
        request.args.get("per_page", 20, type=int), 100
    )  # Cap at 100 per page

    # Get filter parameters
    category = request.args.get("category")
    barangay = request.args.get("barangay")

    logger.debug("Fetching attractions page=%d, per_page=%d", page, per_page)

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

    logger.info(
        "Returning %d approved attractions (page %d/%d)",
        len(result), page, paginated_attractions.pages,
    )

    # Create response with caching headers
    response = make_response(jsonify(response_data))
    response.headers["Cache-Control"] = "public, max-age=300"  # Cache for 5 minutes
    response.headers["Expires"] = (datetime.utcnow() + timedelta(minutes=5)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    return response


# === Heritage API Endpoints ===

@api_bp.route("/heritage/<heritage_type>")
@limiter.limit("20 per minute")
def api_heritage_list(heritage_type):
    """
    API endpoint to retrieve approved heritage items with pagination.

    URL Parameters:
    - heritage_type: One of natural, intangible, personality, institution, program

    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (default: 20, max: 100)
    - search: Search term for name/description fields

    Returns:
        JSON: Paginated list of approved heritage items.
    """
    from utils.heritage_registry import get_heritage_config

    config = get_heritage_config(heritage_type)
    if not config:
        return jsonify({"error": "Invalid heritage type"}), 404

    model = config["model"]
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    search_term = request.args.get("search", "")

    query = model.query.filter_by(status="approved")

    # Apply search filter on name field
    if search_term:
        name_field = config["name_field"]
        query = query.filter(
            getattr(model, name_field).ilike(f"%{search_term}%")
        )

    query = query.order_by(model.created_at.desc())
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    items = []
    for item in paginated.items:
        item_dict = {
            "id": item.id,
            config["name_field"]: getattr(item, config["name_field"]),
            "created_at": item.created_at.isoformat() if item.created_at else None,
        }
        # Add coordinates for mappable types
        if config.get("has_coords"):
            item_dict["lat"] = getattr(item, "lat", None)
            item_dict["lng"] = getattr(item, "lng", None)
        # Add photo if available
        photo = getattr(item, "photo_url", None) or getattr(item, "facade_photo_url", None)
        if photo:
            item_dict["photo_url"] = photo
        items.append(item_dict)

    response_data = {
        "heritage_type": heritage_type,
        "label": config["label"],
        "items": items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": paginated.total,
            "pages": paginated.pages,
            "has_next": paginated.has_next,
            "has_prev": paginated.has_prev,
        },
    }

    logger.info(
        "Returning %d approved %s items (page %d/%d)",
        len(items), config["label"], page, paginated.pages,
    )

    response = make_response(jsonify(response_data))
    response.headers["Cache-Control"] = "public, max-age=300"
    response.headers["Expires"] = (datetime.utcnow() + timedelta(minutes=5)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    return response


@api_bp.route("/heritage/<heritage_type>/<int:item_id>")
@limiter.limit("30 per minute")
def api_heritage_detail(heritage_type, item_id):
    """
    API endpoint to retrieve a single approved heritage item.

    Returns:
        JSON: Full heritage item details.
    """
    from datetime import date as date_type
    from utils.heritage_registry import get_heritage_config

    config = get_heritage_config(heritage_type)
    if not config:
        return jsonify({"error": "Invalid heritage type"}), 404

    model = config["model"]
    item = model.query.get_or_404(item_id)

    if item.status != "approved":
        return jsonify({"error": "Item not found"}), 404

    # Build full detail response
    result = {"id": item.id, "heritage_type": heritage_type}
    for field_name, label, field_type, required in config["fields"]:
        value = getattr(item, field_name, None)
        if isinstance(value, (date_type, datetime)):
            value = value.isoformat()
        result[field_name] = value

    result["created_at"] = item.created_at.isoformat() if item.created_at else None

    response = make_response(jsonify(result))
    response.headers["Cache-Control"] = "public, max-age=300"
    return response


@api_bp.route("/heritage/types")
@limiter.limit("30 per minute")
def api_heritage_types():
    """Return list of available heritage types with counts."""
    from utils.heritage_registry import get_all_types

    types = []
    for slug, config in get_all_types():
        model = config["model"]
        count = model.query.filter_by(status="approved").count()
        types.append({
            "slug": slug,
            "label": config["label"],
            "label_plural": config["label_plural"],
            "form": config["form"],
            "has_coords": config["has_coords"],
            "count": count,
        })

    response = make_response(jsonify({"types": types}))
    response.headers["Cache-Control"] = "public, max-age=300"
    return response
