"""Admin routes for establishing management (approval, rejection, deletion)."""

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Establishment, EstablishmentReview
from . import admin_bp
import logging

logger = logging.getLogger(__name__)


def admin_required(f):
    """Reuse existing admin check pattern."""
    from functools import wraps
    from flask_login import current_user

    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Access denied.", "error")
            return redirect(url_for("public.index"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/establishments")
@login_required
@admin_required
def manage_establishments():
    """List all establishments with status filter."""
    status = request.args.get("status", "all")

    query = Establishment.query
    if status != "all":
        query = query.filter_by(status=status)

    establishments = query.order_by(Establishment.created_at.desc()).all()

    pending_count = Establishment.query.filter_by(status="pending").count()

    return render_template(
        "admin/establishments.html",
        establishments=establishments,
        current_status=status,
        pending_count=pending_count,
    )


@admin_bp.route("/establishments/<int:id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_establishment(id):
    """Approve an establishment listing."""
    est = Establishment.query.get_or_404(id)
    est.status = "approved"
    db.session.commit()
    logger.info(f"Establishment '{est.name}' approved by admin")
    flash(f"'{est.name}' has been approved and is now live.", "success")
    return redirect(url_for("admin.manage_establishments"))


@admin_bp.route("/establishments/<int:id>/reject", methods=["POST"])
@login_required
@admin_required
def reject_establishment(id):
    """Reject an establishment listing."""
    est = Establishment.query.get_or_404(id)
    est.status = "rejected"
    db.session.commit()
    logger.info(f"Establishment '{est.name}' rejected by admin")
    flash(f"'{est.name}' has been rejected.", "warning")
    return redirect(url_for("admin.manage_establishments"))


@admin_bp.route("/establishments/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_establishment(id):
    """Delete an establishment."""
    est = Establishment.query.get_or_404(id)
    name = est.name
    db.session.delete(est)
    db.session.commit()
    logger.info(f"Establishment '{name}' deleted by admin")
    flash(f"'{name}' has been deleted.", "success")
    return redirect(url_for("admin.manage_establishments"))


@admin_bp.route("/establishment-reviews")
@login_required
@admin_required
def manage_establishment_reviews():
    """Manage establishment reviews (approve/reject)."""
    status = request.args.get("status", "pending")
    query = EstablishmentReview.query
    if status != "all":
        query = query.filter_by(status=status)

    reviews = query.order_by(EstablishmentReview.created_at.desc()).all()

    return render_template(
        "admin/establishment_reviews.html",
        reviews=reviews,
        current_status=status,
    )


@admin_bp.route("/establishment-reviews/<int:id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_establishment_review(id):
    """Approve an establishment review and recalculate ratings."""
    review = EstablishmentReview.query.get_or_404(id)
    review.status = "approved"
    db.session.commit()

    # Recalculate establishment rating
    est = review.establishment
    approved_reviews = EstablishmentReview.query.filter_by(
        establishment_id=est.id, status="approved"
    ).all()
    if approved_reviews:
        est.rating_avg = sum(r.rating for r in approved_reviews) / len(approved_reviews)
        est.review_count = len(approved_reviews)
    else:
        est.rating_avg = 0
        est.review_count = 0
    db.session.commit()

    flash("Review approved.", "success")
    return redirect(url_for("admin.manage_establishment_reviews"))


@admin_bp.route("/establishment-reviews/<int:id>/reject", methods=["POST"])
@login_required
@admin_required
def reject_establishment_review(id):
    """Reject an establishment review."""
    review = EstablishmentReview.query.get_or_404(id)
    review.status = "rejected"
    db.session.commit()
    flash("Review rejected.", "success")
    return redirect(url_for("admin.manage_establishment_reviews"))
