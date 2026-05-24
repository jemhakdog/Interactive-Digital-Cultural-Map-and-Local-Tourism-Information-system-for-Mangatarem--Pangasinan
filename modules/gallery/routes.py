"""
Routes for the Gallery module.
Extracted from routes/public.py.
"""

from flask import Blueprint, render_template, request
from models import db, GalleryItem, User
from core.logger import log_entry, log_query, log_render, log_success
import logging

gallery_bp = Blueprint("gallery", __name__, url_prefix="/gallery")
logger = logging.getLogger(__name__)

def record_view(view_type, item_id=None, page_name=None):
    """
    Shim for record_view (should ideally be moved to a shared service).
    """
    from modules.core.public_routes import record_view as public_record_view
    public_record_view(view_type, item_id, page_name)

@gallery_bp.route("/")
def index():
    """
    Display the photo and video gallery.
    """
    log_entry("gallery", "index")
    logger.info("Gallery page accessed")

    # Record view
    record_view("page", page_name="gallery")

    page = request.args.get('page', 1, type=int)
    per_page = 12

    log_query("gallery", "index", "Fetching approved gallery items with pagination")
    paginated = (
        GalleryItem.query.filter_by(status="approved")
        .order_by(GalleryItem.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    items = paginated.items

    # Get list of unique barangays from approved gallery items for the filter
    log_query("gallery", "index", "Fetching unique barangays for gallery")
    barangays = (
        db.session.query(User.barangay_id)
        .join(GalleryItem, User.id == GalleryItem.user_id)
        .filter(GalleryItem.status == "approved", User.barangay_id.is_not(None))
        .distinct()
        .order_by(User.barangay_id)
        .all()
    )

    barangay_list = [b[0] for b in barangays]

    log_success(
        "gallery",
        "index",
        f"Gallery loaded with {len(items)} items from {len(barangay_list)} barangays"
    )
    logger.info("Gallery page loaded")

    log_render("gallery", "index", "gallery.html")
    return render_template(
        "pagez/gallery.html", gallery_items=items, barangays=barangay_list, pagination=paginated
    )
