"""
Routes for the Attractions module.
Extracted from routes/public.py and routes/api.py.
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from extensions import db, limiter
from .models import Attraction
from core.logger import log_entry, log_query, log_render
import logging
from datetime import datetime

attractions_bp = Blueprint("attractions", __name__, url_prefix="/attractions")
logger = logging.getLogger(__name__)

@attractions_bp.route("/<int:id>")
def detail(id):
    """
    Display detailed information about a specific attraction.
    """
    log_entry("attractions", "detail", id=id)
    logger.info("Attraction detail page accessed")

    from modules.auth.models import User
    from modules.gallery.models import GalleryItem
    from modules.business.models import Establishment
    from modules.analytics.models import AnalyticsPageView

    log_query("attractions", "detail", f"Fetching attraction ID {id}")
    attraction = Attraction.query.get_or_404(id)
    
    # Record view
    _record_view("attraction", item_id=id)

    # Fetch nearby attractions (same barangay, approved, limit 3, excluding current)
    nearby = (
        Attraction.query.filter(
            Attraction.barangay_id == attraction.barangay_id,
            Attraction.status == "approved",
            Attraction.id != attraction.id,
        )
        .limit(3)
        .all()
    )

    # Fetch related gallery items
    related_gallery = (
        GalleryItem.query.join(User, GalleryItem.user_id == User.id)
        .filter(User.barangay_id == attraction.barangay_id, GalleryItem.status == "approved")
        .limit(6)
        .all()
    )

    # Fetch nearby establishments
    nearby_stay = []
    nearby_eat = []
    if attraction.latitude and attraction.longitude:
        from core.geo import haversine_distance
        all_establishments = Establishment.query.filter_by(status="approved").all()
        for est in all_establishments:
            dist = haversine_distance(
                attraction.latitude, attraction.longitude,
                est.latitude, est.longitude
            )
            if dist <= 5.0:  # 5km radius
                est._distance = round(dist, 1)
                if est.type == "inn":
                    nearby_stay.append(est)
                else:
                    nearby_eat.append(est)
        nearby_stay.sort(key=lambda x: x._distance)
        nearby_eat.sort(key=lambda x: x._distance)
        nearby_stay = nearby_stay[:3]
        nearby_eat = nearby_eat[:3]

    log_render("attractions", "detail", "detail.html")
    return render_template(
        "pagez/detail.html",
        attraction=attraction,
        nearby=nearby,
        related_gallery=related_gallery,
        nearby_stay=nearby_stay,
        nearby_eat=nearby_eat,
    )

@attractions_bp.route("/api")
@limiter.limit("20 per minute")
def api_list():
    """
    API endpoint for attractions.
    """
    from modules.barangay.models import BarangayInfo
    
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    category = request.args.get("category")
    barangay = request.args.get("barangay")
    is_featured = request.args.get("is_featured")
    user_lat = request.args.get("lat", type=float)
    user_lng = request.args.get("lng", type=float)
    radius = request.args.get("radius", 10, type=float)

    query = db.session.query(
        Attraction.id,
        Attraction.name,
        Attraction.category,
        BarangayInfo.name.label("barangay_name"),
        Attraction.description,
        Attraction.latitude,
        Attraction.longitude,
        Attraction.image_url,
        Attraction.is_featured
    ).join(BarangayInfo, Attraction.barangay_id == BarangayInfo.id).filter(Attraction.status == "approved")

    if category and category != "all":
        query = query.filter(Attraction.category == category)
    if barangay and barangay != "all":
        query = query.filter(BarangayInfo.name == barangay)
    if is_featured:
        query = query.filter(Attraction.is_featured == (is_featured.lower() == 'true'))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    result = []
    for a in paginated.items:
        attr_dict = {
            "id": a.id,
            "name": a.name,
            "category": a.category,
            "barangay": a.barangay_name,
            "description": a.description,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "image": a.image_url,
            "is_featured": a.is_featured,
            "rating": 4.5,
        }

        if user_lat is not None and user_lng is not None:
            from core.geo import haversine_distance
            dist = haversine_distance(user_lat, user_lng, a.latitude, a.longitude)
            attr_dict["distance"] = round(dist, 2)
            if dist > radius:
                continue
        
        result.append(attr_dict)

    if user_lat is not None and user_lng is not None:
        result.sort(key=lambda x: x.get("distance", float("inf")))

    return jsonify({
        "attractions": result,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": paginated.total,
            "pages": paginated.pages,
            "has_next": paginated.has_next,
            "has_prev": paginated.has_prev,
        },
    })

def _record_view(view_type, item_id=None, page_name=None):
    """
    Internal helper for recording views (duplicate for now to ensure autonomy).
    """
    from modules.analytics.models import AnalyticsPageView
    from flask_login import current_user
    import threading

    app = current_app._get_current_object()
    user_id = current_user.id if current_user.is_authenticated else None

    def _async_record():
        with app.app_context():
            try:
                view = AnalyticsPageView(
                    view_type=view_type,
                    item_id=item_id,
                    page_name=page_name,
                    user_id=user_id,
                    timestamp=datetime.utcnow(),
                )
                db.session.add(view)
                db.session.commit()
            except Exception as e:
                logger.error(f"Analytics Error: {e}")
            finally:
                db.session.remove()

    threading.Thread(target=_async_record, daemon=True).start()
