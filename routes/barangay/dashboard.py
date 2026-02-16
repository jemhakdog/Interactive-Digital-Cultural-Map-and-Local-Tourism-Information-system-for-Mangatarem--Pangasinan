import logging
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Attraction, Event, GalleryItem
from . import barangay_bp

logger = logging.getLogger(__name__)

@barangay_bp.route("/dashboard")
@login_required
def barangay_dashboard():
    """Display the barangay contributor dashboard with content statistics."""
    logger.info("Barangay dashboard accessed by %s (%s)", current_user.username, current_user.barangay)

    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    stats = {
        "attractions": Attraction.query.filter_by(user_id=current_user.id).count(),
        "events": Event.query.filter_by(user_id=current_user.id).count(),
        "gallery": GalleryItem.query.filter_by(user_id=current_user.id).count(),
    }

    logger.info("Dashboard stats for %s: %s", current_user.username, stats)
    return render_template("barangay/dashboard.html", stats=stats)
