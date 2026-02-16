import logging
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from models import db, User, Attraction, Event, GalleryItem, Review, Favorite, PageView
from utils.logger_helper import log_entry, log_success, log_error
from . import admin_bp

logger = logging.getLogger(__name__)

# === DASHBOARD HELPER FUNCTIONS ===

def _get_content_stats() -> Dict[str, int]:
    """Fetch basic content statistics."""
    return {
        "attractions": Attraction.query.count(),
        "events": Event.query.count(),
        "gallery": GalleryItem.query.count(),
        "reviews": Review.query.count(),
        "pending_reviews": Review.query.filter_by(status="pending").count(),
        "favorites": Favorite.query.count(),
    }


def _get_top_attractions(limit: int = 5) -> List[Dict[str, any]]:
    """Fetch most viewed attractions."""
    top_query = (
        db.session.query(Attraction.name, func.count(PageView.id).label("view_count"))
        .join(PageView, PageView.item_id == Attraction.id)
        .filter(PageView.view_type == "attraction")
        .group_by(Attraction.id)
        .order_by(func.count(PageView.id).desc())
        .limit(limit)
        .all()
    )
    return [{"name": name, "views": count} for name, count in top_query]


def _get_engagement_data(days: int = 7) -> Dict[str, List]:
    """Calculate engagement trends over specified days."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    daily_views_query = (
        db.session.query(
            func.date(PageView.timestamp).label("date"),
            func.count(PageView.id).label("count"),
        )
        .filter(PageView.timestamp >= cutoff_date)
        .group_by(func.date(PageView.timestamp))
        .all()
    )
    daily_views_dict = {str(d): c for d, c in daily_views_query}
    
    trend_dates = []
    trend_counts = []
    for i in range(days - 1, -1, -1):
        d = (datetime.utcnow() - timedelta(days=i)).date()
        d_str = str(d)
        trend_dates.append(d.strftime("%b %d"))
        trend_counts.append(daily_views_dict.get(d_str, 0))
    return {"dates": trend_dates, "counts": trend_counts}


def _get_pending_items() -> Dict[str, any]:
    """Fetch all items awaiting admin approval."""
    return {
        "users": User.query.filter_by(is_approved=False, role="contributor").all(),
        "gallery": GalleryItem.query.filter_by(status="pending").all(),
        "reviews": Review.query.filter_by(status="pending").join(User, Review.user_id == User.id).join(Attraction, Review.attraction_id == Attraction.id).all(),
    }


def _get_top_rated_attractions(limit: int = 5) -> List[Tuple[Attraction, float]]:
    """Fetch top-rated attractions based on average review rating."""
    return (
        db.session.query(Attraction, func.avg(Review.rating).label("avg_rating"))
        .join(Review, Attraction.id == Review.attraction_id)
        .group_by(Attraction.id)
        .order_by(func.avg(Review.rating).desc())
        .limit(limit)
        .all()
    )


def _get_recent_reviews(limit: int = 5) -> List[Review]:
    """Fetch most recent reviews for dashboard feed."""
    return Review.query.order_by(Review.created_at.desc()).limit(limit).all()


# === ROUTE HANDLERS ===

@admin_bp.route("/dashboard")
@login_required
def admin_dashboard():
    """Display admin dashboard."""
    log_entry("admin", "admin_dashboard", user=current_user.username)
    
    if current_user.role != "admin":
        log_error("admin", "admin_dashboard", f"Access denied for role='{current_user.role}'")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    # Gather data via helpers
    stats = _get_content_stats()
    pending = _get_pending_items()
    top_attractions = _get_top_attractions()
    engagement_data = _get_engagement_data()
    recent_activity = _get_recent_reviews()
    top_rated = _get_top_rated_attractions()
    
    log_success("admin", "admin_dashboard", "Dashboard data loaded successfully")
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        pending_users=pending["users"],
        pending_gallery=pending["gallery"],
        pending_reviews=pending["reviews"],
        top_attractions=top_attractions,
        engagement_data=engagement_data,
        recent_activity=recent_activity,
        top_rated=top_rated,
    )
