"""
Routes for the Heritage module.
Extracted from routes/public.py.
"""

from flask import Blueprint, render_template, request, abort, jsonify, make_response
from core.logger import log_entry, log_render, log_success
from utils.security import validate_string_input
from modules.analytics.utils import record_view
from datetime import datetime, timedelta
import logging

heritage_bp = Blueprint("heritage", __name__, url_prefix="/heritage")
logger = logging.getLogger(__name__)

@heritage_bp.route("/")
def index():
    """
    Heritage catalog landing page.
    """
    from utils.heritage_registry import get_all_types

    log_entry("heritage", "index")
    logger.info("Heritage catalog page accessed")
    record_view("page", page_name="heritage")

    type_stats = {}
    for slug, config in get_all_types():
        model = config["model"]
        count = model.query.filter_by(status="approved").count()
        # Get a representative photo from the first approved item
        sample = model.query.filter_by(status="approved").first()
        photo = None
        if sample:
            photo = (
                getattr(sample, "photo_url", None)
                or getattr(sample, "facade_photo_url", None)
                or getattr(sample, "logo_url", None)
            )

        type_stats[slug] = {
            "label": config["label"],
            "label_plural": config["label_plural"],
            "form": config["form"],
            "has_coords": config["has_coords"],
            "count": count,
            "photo": photo,
        }

    log_success("heritage", "index", f"Heritage catalog loaded with {len(type_stats)} types")
    return render_template("pagez/heritage_index.html", heritage_types=type_stats)


@heritage_bp.route("/<heritage_type>")
def type_list(heritage_type):
    """
    Browse approved heritage items by type.
    """
    from utils.heritage_registry import get_heritage_config

    config = get_heritage_config(heritage_type)
    if not config:
        abort(404)

    log_entry("heritage", "type_list", heritage_type=heritage_type)
    logger.info(f"Heritage list page accessed for type '{heritage_type}'")
    record_view("page", page_name=f"heritage_{heritage_type}")

    model = config["model"]
    page = request.args.get("page", 1, type=int)
    per_page = 12
    raw_search = request.args.get("search", "").strip()
    
    # Validate search input
    is_valid, _ = validate_string_input(raw_search, max_length=200, block_sql_injection=True)
    search_term = raw_search[:200] if is_valid else ""

    query = model.query.filter_by(status="approved")
    if search_term:
        name_field = config["name_field"]
        query = query.filter(
            getattr(model, name_field).ilike(f"%{search_term}%")
        )

    paginated = query.order_by(model.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    log_success(
        "heritage", "type_list",
        f"Loaded {paginated.total} '{config['label']}' items (page {page})"
    )
    return render_template(
        "pagez/heritage_list.html",
        items=paginated.items,
        pagination=paginated,
        heritage_type=heritage_type,
        config=config,
        search_term=search_term,
    )


@heritage_bp.route("/<heritage_type>/<int:item_id>")
def detail(heritage_type, item_id):
    """Display detailed view of a single approved heritage item."""
    from utils.heritage_registry import get_heritage_config, get_display_name

    config = get_heritage_config(heritage_type)
    if not config:
        abort(404)

    model = config["model"]
    item = model.query.get_or_404(item_id)

    if item.status != "approved":
        abort(404)

    display_name = get_display_name(item, heritage_type)
    log_entry("heritage", "detail", heritage_type=heritage_type, id=item_id)
    logger.info(f"Heritage detail page for '{display_name}' (type: {heritage_type}, id: {item_id})")
    record_view("heritage", item_id=item_id, page_name=f"heritage_{heritage_type}")

    log_render("heritage", "detail", "heritage_detail.html")
    return render_template(
        "pagez/heritage_detail.html",
        item=item,
        heritage_type=heritage_type,
        config=config,
        display_name=display_name,
    )


# --- API Routes ---

@heritage_bp.route("/api/<heritage_type>")
def api_list(heritage_type):
    """API endpoint to retrieve approved heritage items with pagination."""
    from utils.heritage_registry import get_heritage_config

    config = get_heritage_config(heritage_type)
    if not config:
        return jsonify({"error": "Invalid heritage type"}), 404

    model = config["model"]
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    search_term = request.args.get("search", "")

    query = model.query.filter_by(status="approved")

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
        if config.get("has_coords"):
            item_dict["latitude"] = getattr(item, "latitude", None)
            item_dict["longitude"] = getattr(item, "longitude", None)
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

    response = make_response(jsonify(response_data))
    response.headers["Cache-Control"] = "public, max-age=300"
    response.headers["Expires"] = (datetime.utcnow() + timedelta(minutes=5)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )
    return response


@heritage_bp.route("/api/<heritage_type>/<int:item_id>")
def api_detail(heritage_type, item_id):
    """API endpoint to retrieve a single approved heritage item."""
    from datetime import date as date_type
    from utils.heritage_registry import get_heritage_config

    config = get_heritage_config(heritage_type)
    if not config:
        return jsonify({"error": "Invalid heritage type"}), 404

    model = config["model"]
    item = model.query.get_or_404(item_id)

    if item.status != "approved":
        return jsonify({"error": "Item not found"}), 404

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


@heritage_bp.route("/api/types")
def api_types():
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
