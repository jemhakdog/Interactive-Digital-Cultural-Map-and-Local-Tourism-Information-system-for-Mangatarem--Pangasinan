from flask import Blueprint, jsonify, request, make_response
from models import Attraction, Establishment, db
from extensions import limiter
import logging
import math
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
    from models import BarangayInfo
    query = db.session.query(
        Attraction.id,
        Attraction.name,
        Attraction.category,
        BarangayInfo.name,
        Attraction.description,
        Attraction.latitude,
        Attraction.longitude,
        Attraction.image_url,
    ).join(BarangayInfo, Attraction.barangay_id == BarangayInfo.id).filter(Attraction.status == "approved")

    if category and category != "all":
        query = query.filter(Attraction.category == category)
    if barangay and barangay != "all":
        query = query.filter(BarangayInfo.name == barangay)

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
                "latitude": a[5],  # latitude
                "longitude": a[6],  # longitude
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
            item_dict["latitude"] = getattr(item, "latitude", None)
            item_dict["longitude"] = getattr(item, "longitude", None)
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


@api_bp.route("/establishments")
@limiter.limit("20 per minute")
def api_establishments():
    """
    API endpoint to retrieve approved establishments with pagination.

    Query Parameters:
    - page: Page number (default: 1)
    - per_page: Number of establishments per page (default: 20, max: 100)
    - type: Filter by type (inn/restaurant/cafe/fastfood)
    - price_range: Filter by price range (budget/moderate/premium)
    - barangay: Filter by barangay
    - lat: User latitude for distance sorting
    - lng: User longitude for distance sorting
    - radius: Search radius in km (default: 10)

    Returns JSON array of establishment objects.
    """
    logger.info("API endpoint /api/establishments called")

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)

    est_type = request.args.get("type")
    price_range = request.args.get("price_range")
    barangay = request.args.get("barangay")
    user_lat = request.args.get("lat", type=float)
    user_lng = request.args.get("lng", type=float)
    radius = request.args.get("radius", 10, type=float)

    query = Establishment.query.filter(Establishment.status == "approved")

    if est_type and est_type != "all":
        query = query.filter(Establishment.type == est_type)
    if price_range:
        query = query.filter(Establishment.price_range == price_range)
    if barangay and barangay != "all":
        from models import BarangayInfo
        query = query.join(BarangayInfo).filter(BarangayInfo.name == barangay)

    paginated_establishments = query.paginate(page=page, per_page=per_page, error_out=False)

    result = []
    for est in paginated_establishments.items:
        est_dict = {
            "id": est.id,
            "name": est.name,
            "type": est.type,
            "description": est.description or "",
            "address": est.address or "",
            "latitude": est.latitude,
            "longitude": est.longitude,
            "contact_number": est.contact_number,
            "price_range": est.price_range,
            "rating_avg": est.rating_avg or 0,
            "review_count": est.review_count or 0,
            "cover_image_url": est.cover_image_url,
            "logo_url": est.logo_url,
            "amenities": est.amenities or [],
            "barangay": est.barangay.name if est.barangay else None,
        }

        if user_lat and user_lng:
            dist = _haversine_distance(user_lat, user_lng, est.latitude, est.longitude)
            est_dict["distance"] = round(dist, 2)

        result.append(est_dict)

    if user_lat and user_lng:
        result.sort(key=lambda x: x.get("distance", float("inf")))
        result = [e for e in result if e.get("distance", float("inf")) <= radius]

    response_data = {
        "establishments": result,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": paginated_establishments.total,
            "pages": paginated_establishments.pages,
            "has_next": paginated_establishments.has_next,
            "has_prev": paginated_establishments.has_prev,
        },
    }

    logger.info(
        "Returning %d approved establishments (page %d/%d)",
        len(result), page, paginated_establishments.pages,
    )

    response = make_response(jsonify(response_data))
    response.headers["Cache-Control"] = "public, max-age=300"
    response.headers["Expires"] = (datetime.utcnow() + timedelta(minutes=5)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    return response


def _haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points using Haversine formula (returns km)."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


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
