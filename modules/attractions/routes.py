"""
Routes for the Attractions module.
Extracted from routes/public.py and routes/api.py.
"""

from flask import Blueprint, request, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from extensions import db, limiter
from .models import Attraction, AttractionReview, ReviewPhoto
import logging
from datetime import datetime

attractions_bp = Blueprint("attractions", __name__, url_prefix="/attractions")
logger = logging.getLogger(__name__)

@attractions_bp.route("/<int:id>")
def detail(id):
    """Redirect legacy attraction detail view to modern v1 version."""
    logger.info(f"Redirecting legacy /attractions/{id} to /v1/attractions/{id}")
    return redirect(url_for("public_v1.attraction_detail_v1_view", id=id, **request.args), code=302)

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
    """Return paginated approved reviews (root only) + replies + rating summary for an attraction."""
    Attraction.query.get_or_404(id)
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 6, type=int), 20)

    # Paginate approved root reviews only
    pagination = (
        AttractionReview.query
        .filter_by(attraction_id=id, parent_id=None, status="approved")
        .order_by(AttractionReview.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    reviews_data = []
    for r in pagination.items:
        r_dict = r.to_dict()
        
        # Query replies (approved always, plus pending for the logged-in user)
        replies_query = AttractionReview.query.filter_by(attraction_id=id, parent_id=r.id)
        if current_user.is_authenticated:
            replies = replies_query.filter(
                (AttractionReview.status == "approved") |
                ((AttractionReview.status == "pending") & (AttractionReview.user_id == current_user.id))
            ).order_by(AttractionReview.created_at.asc()).all()
        else:
            replies = replies_query.filter_by(status="approved").order_by(AttractionReview.created_at.asc()).all()
            
        r_dict["replies"] = [reply.to_dict() for reply in replies]
        reviews_data.append(r_dict)

    # Fetch user's own pending root reviews if logged in
    pending_reviews_data = []
    if current_user.is_authenticated:
        pending_root = (
            AttractionReview.query
            .filter_by(attraction_id=id, parent_id=None, user_id=current_user.id, status="pending")
            .order_by(AttractionReview.created_at.desc())
            .all()
        )
        for r in pending_root:
            r_dict = r.to_dict()
            # User's own pending root reviews will only have their own pending replies (if any)
            replies = AttractionReview.query.filter_by(
                attraction_id=id, 
                parent_id=r.id, 
                user_id=current_user.id, 
                status="pending"
            ).order_by(AttractionReview.created_at.asc()).all()
            r_dict["replies"] = [reply.to_dict() for reply in replies]
            pending_reviews_data.append(r_dict)

    # Rating distribution (1–5) - only counts root reviews
    all_approved = (
        AttractionReview.query
        .with_entities(AttractionReview.rating)
        .filter(
            AttractionReview.attraction_id == id,
            AttractionReview.status == "approved",
            AttractionReview.parent_id.is_(None),
            AttractionReview.rating.is_not(None)
        )
        .all()
    )
    ratings = [r.rating for r in all_approved]
    total = len(ratings)
    avg = round(sum(ratings) / total, 1) if total > 0 else 0
    distribution = {str(i): ratings.count(i) for i in range(1, 6)}

    return jsonify({
        "reviews": reviews_data,
        "pending_reviews": pending_reviews_data,
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
    """Submit a review or reply (with optional photos) for an attraction.

    Accepts multipart/form-data:
        - parent_id (int, optional, for replies)
        - rating    (int, 1-5, required unless parent_id present)
        - comment   (str, optional)
        - photos    (files, optional, max 5)
    """
    from utils.file_helpers import save_uploaded_file
    from utils.cache_helpers import cache_delete, invalidate_attraction_cache

    Attraction.query.get_or_404(id)
    parent_id = request.form.get("parent_id", type=int)

    # Parse and validate comment
    comment = request.form.get("comment", "").strip() or None

    rating = None
    if parent_id:
        # Replying to another review: verify parent exists and is root
        parent = AttractionReview.query.get_or_404(parent_id)
        if parent.parent_id is not None:
            return jsonify({"error": "Cannot reply to a sub-reply."}), 400
        if parent.attraction_id != id:
            return jsonify({"error": "Parent review does not match this attraction."}), 400
    else:
        # Validate rating for root reviews
        rating = request.form.get("rating", type=int)
        if not rating or not (1 <= rating <= 5):
            return jsonify({"error": "Rating must be between 1 and 5."}), 400

    # Create review/reply record (pending — admin must approve)
    review = AttractionReview(
        user_id=current_user.id,
        attraction_id=id,
        rating=rating,
        comment=comment,
        parent_id=parent_id,
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
    invalidate_attraction_cache(attraction_id=id)

    logger.info("Review/Reply %d posted for attraction %d by user %d", review.id, id, current_user.id)
    return jsonify({
        "success": True,
        "review_id": review.id,
        "photos_saved": saved_photos,
        "message": "Your post has been submitted and is pending approval. Thank you!",
    }), 201
