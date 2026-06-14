import logging
from flask import redirect, url_for, flash, render_template, request
from flask_login import login_required, current_user
from extensions import db, limiter
from models import GalleryItem, AttractionReview, Announcement
from utils.logger_helper import log_entry, log_success, log_error
from utils.cache_helpers import cache_delete, invalidate_attraction_cache
from . import admin_bp

logger = logging.getLogger(__name__)


def _require_admin():
    """Return redirect if current user is not admin, else None."""
    if current_user.role != "admin":
        log_error("admin", "access", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    return None


# === GALLERY MODERATION ===

@admin_bp.route("/gallery/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_gallery(id):
    """Approve pending gallery item."""
    log_entry("admin", "approve_gallery", id=id)
    if (redir := _require_admin()):
        return redir
    item = GalleryItem.query.get_or_404(id)
    item.status = "approved"
    db.session.commit()
    log_success("admin", "approve_gallery", f"Gallery item ID {id} approved")
    flash("Gallery item approved!")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/gallery/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_gallery(id):
    """Reject and delete pending gallery item."""
    log_entry("admin", "reject_gallery", id=id)
    if (redir := _require_admin()):
        return redir
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    log_success("admin", "reject_gallery", f"Gallery item ID {id} rejected")
    flash("Gallery item rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))


# === REVIEW MODERATION ===

@admin_bp.route("/reviews")
@login_required
def reviews_list():
    """List all pending reviews for admin moderation."""
    log_entry("admin", "reviews_list")
    if (redir := _require_admin()):
        return redir

    status_filter = request.args.get("status", "pending")
    page = request.args.get("page", 1, type=int)

    from modules.auth.models import User
    from modules.attractions.models import Attraction

    query = (
        AttractionReview.query
        .join(User, AttractionReview.user_id == User.id)
        .join(Attraction, AttractionReview.attraction_id == Attraction.id)
        .order_by(AttractionReview.created_at.desc())
    )

    if status_filter != "all":
        query = query.filter(AttractionReview.status == status_filter)

    pagination = query.paginate(page=page, per_page=20, error_out=False)

    return render_template(
        "admin/reviews.html",
        reviews=pagination.items,
        pagination=pagination,
        status_filter=status_filter,
    )


@admin_bp.route("/reviews/approve/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("30 per minute")
def approve_review(id):
    """Approve pending review and invalidate detail cache."""
    log_entry("admin", "approve_review", id=id)
    if (redir := _require_admin()):
        return redir
    review = AttractionReview.query.get_or_404(id)
    review.status = "approved"
    db.session.commit()

    # Invalidate so the approved review shows on the public page
    cache_delete(f"attraction_detail_module:{review.attraction_id}")
    invalidate_attraction_cache(attraction_id=review.attraction_id)

    log_success("admin", "approve_review", f"Review ID {id} approved")
    flash("Review approved and is now publicly visible!")

    _next = request.args.get("next") or request.referrer or url_for("admin.reviews_list")
    return redirect(_next)


@admin_bp.route("/reviews/reject/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("30 per minute")
def reject_review(id):
    """Reject and delete a review."""
    log_entry("admin", "reject_review", id=id)
    if (redir := _require_admin()):
        return redir
    review = AttractionReview.query.get_or_404(id)
    attraction_id = review.attraction_id
    db.session.delete(review)
    db.session.commit()

    cache_delete(f"attraction_detail_module:{attraction_id}")

    log_success("admin", "reject_review", f"Review ID {id} rejected")
    flash("Review rejected and removed.")

    _next = request.args.get("next") or request.referrer or url_for("admin.reviews_list")
    return redirect(_next)


# === ANNOUNCEMENT MODERATION ===

@admin_bp.route("/announcements/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def admin_approve_announcement(id):
    """Approve a pending announcement."""
    log_entry("admin", "approve_announcement", id=id)
    if (redir := _require_admin()):
        return redir
    announcement = Announcement.query.get_or_404(id)
    announcement.status = "approved"
    db.session.commit()
    log_success("admin", "approve_announcement", f"Announcement ID {id} approved")
    flash("Announcement approved and published!")
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/announcements/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def admin_reject_announcement(id):
    """Reject and delete a pending announcement."""
    log_entry("admin", "reject_announcement", id=id)
    if (redir := _require_admin()):
        return redir
    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    log_success("admin", "reject_announcement", f"Announcement ID {id} rejected")
    flash("Announcement rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))
