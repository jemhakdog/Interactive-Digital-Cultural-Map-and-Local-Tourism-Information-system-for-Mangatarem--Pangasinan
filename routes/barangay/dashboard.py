import logging
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Attraction, Event, GalleryItem
from . import barangay_bp

logger = logging.getLogger(__name__)

@barangay_bp.route("/dashboard")
@login_required
def barangay_dashboard():
    """Display the barangay contributor dashboard with community-wide statistics."""
    logger.info("Barangay dashboard accessed by %s (%s)", current_user.username, current_user.barangay_id)

    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    # 1. Fetch community-wide aggregates
    # We query by barangay_id to represent the "Ownership" paradigm
    all_attractions = Attraction.query.filter_by(barangay_id=current_user.barangay_id).all()
    all_events = Event.query.filter_by(barangay_id=current_user.barangay_id).all()
    all_gallery = GalleryItem.query.filter_by(user_id=current_user.id).all() # Gallery usually stays personal/curated

    total_assets = len(all_attractions) + len(all_events)
    
    stats = {
        "total": total_assets,
        "approved": sum(1 for x in all_attractions + all_events if x.status == 'approved'),
        "pending": sum(1 for x in all_attractions + all_events if x.status == 'pending'),
        "rejected": sum(1 for x in all_attractions + all_events if x.status == 'rejected'),
        "gallery": len(all_gallery),
    }

    # 2. Compile Recent Activity (Latest 5 items from the Barangay)
    activity_items = []
    # Add attractions
    for attr in all_attractions:
        activity_items.append({
            'name': attr.name,
            'type': 'Attraction',
            'status': attr.status,
            'date': attr.created_at,
            'id': attr.id
        })
    # Add events
    for ev in all_events:
        activity_items.append({
            'name': ev.name,
            'type': 'Event',
            'status': ev.status,
            'date': ev.created_at,
            'id': ev.id
        })
    
    # Sort activity by date descending
    recent_activity = sorted(activity_items, key=lambda x: x['date'] if x['date'] else datetime.min, reverse=True)[:5]

    logger.info("Dashboard community-wide stats for %s: %s", current_user.username, stats)
    return render_template("barangay/dashboard.html", stats=stats, recent_activity=recent_activity)
