import logging
from flask import redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import GalleryItem, Review
from utils.logger_helper import log_entry, log_success, log_error
from . import admin_bp

logger = logging.getLogger(__name__)

# === GALLERY MODERATION ===

@admin_bp.route("/gallery/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_gallery(id):
    """Approve pending gallery item."""
    log_entry("admin", "approve_gallery", id=id)
    
    if current_user.role != "admin":
        log_error("admin", "approve_gallery", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
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
    
    if current_user.role != "admin":
        log_error("admin", "reject_gallery", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    log_success("admin", "reject_gallery", f"Gallery item ID {id} rejected")
    flash("Gallery item rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))


# === REVIEW MODERATION ===

@admin_bp.route("/reviews/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_review(id):
    """Approve pending review."""
    log_entry("admin", "approve_review", id=id)
    
    if current_user.role != "admin":
        log_error("admin", "approve_review", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    review = Review.query.get_or_404(id)
    review.status = "approved"
    db.session.commit()
    
    log_success("admin", "approve_review", f"Review ID {id} approved")
    flash("Review approved!")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/reviews/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_review(id):
    """Reject and delete pending review."""
    log_entry("admin", "reject_review", id=id)
    
    if current_user.role != "admin":
        log_error("admin", "reject_review", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    
    log_success("admin", "reject_review", f"Review ID {id} rejected")
    flash("Review rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))
