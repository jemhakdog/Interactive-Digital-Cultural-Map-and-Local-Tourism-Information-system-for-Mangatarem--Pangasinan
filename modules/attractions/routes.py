"""
Routes for the Attractions module.
Extracted from routes/public.py and routes/api.py.
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from extensions import db, limiter
from .models import Attraction, AttractionReview, ReviewPhoto
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
    from utils.cache_helpers import cache_get, cache_set

    log_query("attractions", "detail", f"Fetching attraction ID {id}")
    attraction = Attraction.query.get_or_404(id)
    
    # Record view
    _record_view("attraction", item_id=id)

    cache_key = f"attraction_detail_module:{id}"
    cached_data = cache_get(cache_key)
    
    if cached_data:
        return render_template(
            "pagez/detail.html",
            attraction=attraction,
            nearby=cached_data['nearby'],
            related_gallery=cached_data['related_gallery'],
            nearby_stay=cached_data['nearby_stay'],
            nearby_eat=cached_data['nearby_eat'],
        )

    # Cache MISS
    # Fetch nearby attractions (same barangay, approved, limit 3, excluding current)
    nearby_objs = (
        Attraction.query.filter(
            Attraction.barangay_id == attraction.barangay_id,
            Attraction.status == "approved",
            Attraction.id != attraction.id,
        )
        .limit(3)
        .all()
    )
    nearby = [n.to_dict() if hasattr(n, 'to_dict') else {'id': n.id, 'name': n.name, 'image_url': n.image_url} for n in nearby_objs]

    # Fetch related gallery items
    gallery_objs = (
        GalleryItem.query.join(User, GalleryItem.user_id == User.id)
        .filter(User.barangay_id == attraction.barangay_id, GalleryItem.status == "approved")
        .limit(6)
        .all()
    )
    related_gallery = [g.to_dict() if hasattr(g, 'to_dict') else {'id': g.id, 'url': g.url, 'caption': g.caption} for g in gallery_objs]

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
                est_data = est.to_dict() if hasattr(est, 'to_dict') else {'id': est.id, 'name': est.name, 'type': est.type, 'image_url': est.image_url}
                est_data['_distance'] = round(dist, 1)
                if est.type == "inn":
                    nearby_stay.append(est_data)
                else:
                    nearby_eat.append(est_data)
                    
        nearby_stay.sort(key=lambda x: x.get('_distance', 999))
        nearby_eat.sort(key=lambda x: x.get('_distance', 999))
        nearby_stay = nearby_stay[:3]
        nearby_eat = nearby_eat[:3]

    # Store in cache
    payload = {
        'nearby': nearby,
        'related_gallery': related_gallery,
        'nearby_stay': nearby_stay,
        'nearby_eat': nearby_eat
    }
    cache_set(cache_key, payload, ttl=900)

    # Check if favorited by current user
    is_favorite = False
    if current_user.is_authenticated:
        from modules.attractions.models import UserFavoriteAttraction
        is_favorite = UserFavoriteAttraction.query.filter_by(
            user_id=current_user.id, attraction_id=id
        ).first() is not None

    log_render("attractions", "detail", "detail.html")
    return render_template(
        "pagez/detail.html",
        attraction=attraction,
        nearby=nearby,
        related_gallery=related_gallery,
        nearby_stay=nearby_stay,
        nearby_eat=nearby_eat,
        is_favorite=is_favorite
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


# ─────────────────────────────────────────────
# REVIEWS API
# ─────────────────────────────────────────────

@attractions_bp.route("/<int:id>/reviews", methods=["GET"])
def get_reviews(id):
    """Return paginated approved reviews + rating summary for an attraction."""
    attraction = Attraction.query.get_or_404(id)
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 6, type=int), 20)

    pagination = (
        AttractionReview.query
        .filter_by(attraction_id=id, status="approved")
        .order_by(AttractionReview.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    reviews_data = [r.to_dict() for r in pagination.items]

    # Rating distribution (1–5)
    all_approved = (
        AttractionReview.query
        .with_entities(AttractionReview.rating)
        .filter_by(attraction_id=id, status="approved")
        .all()
    )
    ratings = [r.rating for r in all_approved]
    total = len(ratings)
    avg = round(sum(ratings) / total, 1) if total > 0 else 0
    distribution = {str(i): ratings.count(i) for i in range(1, 6)}

    return jsonify({
        "reviews": reviews_data,
        "summary": {
            "average": avg,
            "total": total,
            "distribution": distribution,
        },
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": pagination.total,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
    })


@attractions_bp.route("/<int:id>/reviews", methods=["POST"])
@login_required
@limiter.limit("10 per hour")
def post_review(id):
    """Submit a review (with optional photos) for an attraction.

    Accepts multipart/form-data:
        - rating  (int, 1-5, required)
        - comment (str, optional)
        - photos  (files, optional, max 5)
    """
    from utils.file_helpers import save_uploaded_file
    from utils.cache_helpers import cache_delete

    attraction = Attraction.query.get_or_404(id)

    # Validate rating
    rating = request.form.get("rating", type=int)
    if not rating or not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be between 1 and 5."}), 400

    comment = request.form.get("comment", "").strip() or None

    # Create review record (pending — admin must approve the text)
    review = AttractionReview(
        user_id=current_user.id,
        attraction_id=id,
        rating=rating,
        comment=comment,
        status="pending",
    )
    db.session.add(review)
    db.session.flush()  # get review.id before saving photos

    # Save uploaded photos immediately (no moderation)
    photo_files = request.files.getlist("photos")
    saved_photos = 0
    for photo in photo_files[:5]:  # max 5 photos
        if not photo or not photo.filename:
            continue
        url = save_uploaded_file(photo)
        if url:
            db.session.add(ReviewPhoto(review_id=review.id, url=url))
            saved_photos += 1

    db.session.commit()

    # Invalidate attraction detail cache
    cache_delete(f"attraction_detail_module:{id}")

    logger.info("Review %d posted for attraction %d by user %d", review.id, id, current_user.id)
    return jsonify({
        "success": True,
        "review_id": review.id,
        "photos_saved": saved_photos,
        "message": "Your review has been submitted and is pending approval. Thank you!",
    }), 201
