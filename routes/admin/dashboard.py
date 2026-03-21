import logging
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from models import db, User, Attraction, Event, GalleryItem, AttractionReview, UserFavoriteAttraction, AnalyticsPageView
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
        "reviews": AttractionReview.query.count(),
        "pending_reviews": AttractionReview.query.filter_by(status="pending").count(),
        "favorites": UserFavoriteAttraction.query.count(),
    }


def _get_top_attractions(limit: int = 5) -> List[Dict[str, any]]:
    """Fetch most viewed attractions."""
    top_query = (
        db.session.query(Attraction.name, func.count(AnalyticsPageView.id).label("view_count"))
        .join(AnalyticsPageView, AnalyticsPageView.item_id == Attraction.id)
        .filter(AnalyticsPageView.view_type == "attraction")
        .group_by(Attraction.id)
        .order_by(func.count(AnalyticsPageView.id).desc())
        .limit(limit)
        .all()
    )
    return [{"name": name, "views": count} for name, count in top_query]


def _get_engagement_data(days: int = 7) -> Dict[str, List]:
    """Calculate engagement trends over specified days."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    daily_views_query = (
        db.session.query(
            func.date(AnalyticsPageView.timestamp).label("date"),
            func.count(AnalyticsPageView.id).label("count"),
        )
        .filter(AnalyticsPageView.timestamp >= cutoff_date)
        .group_by(func.date(AnalyticsPageView.timestamp))
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
        "reviews": AttractionReview.query.filter_by(status="pending").join(User, AttractionReview.user_id == User.id).join(Attraction, AttractionReview.attraction_id == Attraction.id).all(),
    }


def _get_top_rated_attractions(limit: int = 5) -> List[Tuple[Attraction, float]]:
    """Fetch top-rated attractions based on average review rating."""
    return (
        db.session.query(Attraction, func.avg(AttractionReview.rating).label("avg_rating"))
        .join(AttractionReview, Attraction.id == AttractionReview.attraction_id)
        .group_by(Attraction.id)
        .order_by(func.avg(AttractionReview.rating).desc())
        .limit(limit)
        .all()
    )


def _get_recent_reviews(limit: int = 5) -> List[AttractionReview]:
    """Fetch most recent reviews for dashboard feed."""
    return AttractionReview.query.order_by(AttractionReview.created_at.desc()).limit(limit).all()


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
