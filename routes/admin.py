"""
Admin routes with clean function design.

Dashboard helpers extracted for single responsibility.
Print statements replaced with logging helpers.
All related admin logic kept together in one file.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import (
    db,
    User,
    Attraction,
    Event,
    GalleryItem,
    PageView,
    Review,
    Favorite,
    EventInterest,
)
from extensions import limiter
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from sqlalchemy import func
from utils.logger_helper import (
    log_entry,
    log_query,
    log_success,
    log_error,
    log_render,
)
from typing import Dict, List, Tuple
import os
import logging

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
logger = logging.getLogger(__name__)


# === DASHBOARD HELPER FUNCTIONS ===

def _get_content_stats() -> Dict[str, int]:
    """
    Fetch basic content statistics.
    
    Returns:
        Dict with counts for attractions, events, gallery, reviews, favorites
    """
    return {
        "attractions": Attraction.query.count(),
        "events": Event.query.count(),
        "gallery": GalleryItem.query.count(),
        "reviews": Review.query.count(),
        "pending_reviews": Review.query.filter_by(status="pending").count(),
        "favorites": Favorite.query.count(),
    }


def _get_top_attractions(limit: int = 5) -> List[Dict[str, any]]:
    """
    Fetch most viewed attractions.
    
    Args:
        limit: Maximum number of attractions to return
        
    Returns:
        List of dicts with attraction name and view count
    """
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
    """
    Calculate engagement trends over specified days.
    
    Args:
        days: Number of days to analyze
        
    Returns:
        Dict with 'dates' and 'counts' lists for charting
    """
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
    """
    Fetch all items awaiting admin approval.
    
    Returns:
        Dict with pending users, gallery items, and reviews
    """
    return {
        "users": User.query.filter_by(is_approved=False, role="contributor").all(),
        "gallery": GalleryItem.query.filter_by(status="pending").all(),
        "reviews": Review.query.filter_by(status="pending").join(User).join(Attraction).all(),
    }


def _get_top_rated_attractions(limit: int = 5) -> List[Tuple[Attraction, float]]:
    """
    Fetch top-rated attractions based on average review rating.
    
    Args:
        limit: Maximum number of attractions to return
        
    Returns:
        List of tuples (Attraction, avg_rating)
    """
    return (
        db.session.query(Attraction, func.avg(Review.rating).label("avg_rating"))
        .join(Review)
        .group_by(Attraction.id)
        .order_by(func.avg(Review.rating).desc())
        .limit(limit)
        .all()
    )


def _get_recent_reviews(limit: int = 5) -> List[Review]:
    """
    Fetch most recent reviews for dashboard feed.
    
    Args:
        limit: Maximum number of reviews to return
        
    Returns:
        List of Review objects
    """
    return Review.query.order_by(Review.created_at.desc()).limit(limit).all()


# === ROUTE HANDLERS ===

@admin_bp.route("/dashboard")
@login_required
def admin_dashboard():
    """
    Display admin dashboard (clean refactored version).
    
    Orchestrates data fetching through focused helper functions.
    Each helper has single responsibility for stats, analytics, or pending items.
    
    Returns:
        Rendered dashboard with comprehensive admin data
    """
    log_entry("admin", "admin_dashboard", user=current_user.username)
    logger.info("Admin dashboard accessed")
    
    # Admin authorization
    if current_user.role != "admin":
        log_error("admin", "admin_dashboard", f"Access denied for role='{current_user.role}'")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "admin_dashboard", "Fetching dashboard data")
    
    # Gather all dashboard data via helpers
    stats = _get_content_stats()
    pending = _get_pending_items()
    top_attractions = _get_top_attractions()
    engagement_data = _get_engagement_data()
    recent_activity = _get_recent_reviews()
    top_rated = _get_top_rated_attractions()
    
    log_success(
        "admin",
        "admin_dashboard",
        f"Dashboard loaded with {stats['attractions']} attractions, {stats['events']} events"
    )
    logger.info(
        f"Dashboard data loaded: {stats['attractions']} attractions, "
        f"{stats['events']} events, {len(pending['users'])} pending users"
    )
    
    log_render("admin", "admin_dashboard", "admin/dashboard.html")
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


# === USER MANAGEMENT ===

@admin_bp.route("/users/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_user(id):
    """Approve pending contributor user."""
    log_entry("admin", "approve_user", id=id)
    logger.info(f"User approval requested for user ID {id}")
    
    if current_user.role != "admin":
        log_error("admin", "approve_user", f"Access denied for user ID={current_user.id}")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "approve_user", f"Fetching user ID {id}")
    user = User.query.get_or_404(id)
    user.is_approved = True
    db.session.commit()
    
    log_success("admin", "approve_user", f"User '{user.username}' approved")
    logger.info(f"User '{user.username}' (ID: {id}) approved successfully")
    
    flash(f"User {user.username} approved!")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/users/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_user(id):
    """Reject and delete pending contributor user."""
    log_entry("admin", "reject_user", id=id)
    logger.info(f"User rejection requested for user ID {id}")
    
    if current_user.role != "admin":
        log_error("admin", "reject_user", f"Access denied for user ID={current_user.id}")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "reject_user", f"Fetching user ID {id}")
    user = User.query.get_or_404(id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    log_success("admin", "reject_user", f"User '{username}' rejected and deleted")
    logger.info(f"User '{username}' (ID: {id}) rejected and deleted")
    
    flash(f"User {username} rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))


# === ATTRACTION MANAGEMENT ===

@admin_bp.route("/attractions")
@login_required
def admin_attractions():
    """Display attractions management page."""
    log_entry("admin", "admin_attractions")
    logger.info("Admin attractions management page accessed")
    
    if current_user.role != "admin":
        log_error("admin", "admin_attractions", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "admin_attractions", "Fetching all attractions")
    pending_attractions = Attraction.query.filter_by(status="pending").all()
    all_attractions = Attraction.query.order_by(Attraction.created_at.desc()).all()
    
    log_success(
        "admin",
        "admin_attractions",
        f"Loaded {len(all_attractions)} total, {len(pending_attractions)} pending"
    )
    logger.info(
        f"Attractions page loaded: {len(all_attractions)} total, {len(pending_attractions)} pending"
    )
    
    log_render("admin", "admin_attractions", "admin/attractions.html")
    return render_template(
        "admin/attractions.html",
        pending_attractions=pending_attractions,
        all_attractions=all_attractions,
    )


@admin_bp.route("/attractions/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_attraction(id):
    """Approve pending attraction."""
    log_entry("admin", "approve_attraction", id=id)
    logger.info(f"Attraction approval requested for ID {id}")
    
    if current_user.role != "admin":
        log_error("admin", "approve_attraction", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "approve_attraction", f"Fetching attraction ID {id}")
    attraction = Attraction.query.get_or_404(id)
    attraction.status = "approved"
    db.session.commit()
    
    log_success("admin", "approve_attraction", f"Attraction '{attraction.name}' approved")
    logger.info(f"Attraction '{attraction.name}' (ID: {id}) approved successfully")
    
    flash(f'Attraction "{attraction.name}" approved!')
    return redirect(url_for("admin.admin_attractions"))


@admin_bp.route("/attractions/delete/<int:id>")
@login_required
@limiter.limit("10 per minute")
def delete_attraction(id):
    """Delete attraction (admin or owner only)."""
    log_entry("admin", "delete_attraction", id=id)
    logger.info(f"Attraction deletion requested for ID {id}")
    
    log_query("admin", "delete_attraction", f"Fetching attraction ID {id}")
    attraction = Attraction.query.get_or_404(id)
    
    # Permission check
    if current_user.role != "admin" and attraction.user_id != current_user.id:
        log_error("admin", "delete_attraction", f"Access denied for user ID={current_user.id}")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    attraction_name = attraction.name
    db.session.delete(attraction)
    db.session.commit()
    
    log_success("admin", "delete_attraction", f"Attraction '{attraction_name}' deleted")
    logger.info(f"Attraction '{attraction_name}' (ID: {id}) deleted successfully")
    
    flash("Attraction deleted.")
    return redirect(url_for("admin.admin_attractions"))


@admin_bp.route("/attractions/edit/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def edit_attraction(id):
    """Edit attraction (admin or owner only)."""
    log_entry("admin", "edit_attraction", id=id, method=request.method)
    logger.info(f"Attraction edit requested for ID {id}")
    
    from flask import current_app
    
    log_query("admin", "edit_attraction", f"Fetching attraction ID {id}")
    attraction = Attraction.query.get_or_404(id)
    
    # Permission check
    if current_user.role != "admin" and attraction.user_id != current_user.id:
        log_error("admin", "edit_attraction", f"Access denied for user ID={current_user.id}")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    if request.method == "POST":
        attraction.name = request.form.get("name")
        attraction.category = request.form.get("category")
        attraction.description = request.form.get("description")
        attraction.lat = float(request.form.get("lat"))
        attraction.lng = float(request.form.get("lng"))
        
        # Handle image upload
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
                attraction.image_url = url_for("static", filename="uploads/" + filename)
        
        # Fallback to URL
        if request.form.get("image_url"):
            attraction.image_url = request.form.get("image_url")
        
        # Contributors require re-approval
        if current_user.role == "contributor":
            attraction.status = "pending"
        
        db.session.commit()
        
        log_success("admin", "edit_attraction", f"Attraction '{attraction.name}' updated")
        logger.info(f"Attraction '{attraction.name}' (ID: {id}) updated successfully")
        
        flash("Attraction updated.")
        return redirect(url_for("admin.admin_attractions"))
    
    log_render("admin", "edit_attraction", "admin/edit_attraction.html")
    return render_template("admin/edit_attraction.html", attraction=attraction)


# === EVENT MANAGEMENT ===

@admin_bp.route("/events")
@login_required
def admin_events():
    """Display events management page."""
    log_entry("admin", "admin_events")
    logger.info("Admin events management page accessed")
    
    if current_user.role != "admin":
        log_error("admin", "admin_events", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "admin_events", "Fetching all events")
    pending_events = Event.query.filter_by(status="pending").all()
    all_events = Event.query.order_by(Event.date.asc()).all()
    
    log_success(
        "admin",
        "admin_events",
        f"Loaded {len(all_events)} total, {len(pending_events)} pending"
    )
    logger.info(
        f"Events page loaded: {len(all_events)} total, {len(pending_events)} pending"
    )
    
    log_render("admin", "admin_events", "admin/events.html")
    return render_template(
        "admin/events.html", pending_events=pending_events, all_events=all_events
    )


@admin_bp.route("/events/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_event(id):
    """Approve pending event."""
    log_entry("admin", "approve_event", id=id)
    logger.info(f"Event approval requested for ID {id}")
    
    if current_user.role != "admin":
        log_error("admin", "approve_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "approve_event", f"Fetching event ID {id}")
    event = Event.query.get_or_404(id)
    event.status = "approved"
    db.session.commit()
    
    log_success("admin", "approve_event", f"Event '{event.title}' approved")
    logger.info(f"Event '{event.title}' (ID: {id}) approved successfully")
    
    flash(f'Event "{event.title}" approved!')
    return redirect(url_for("admin.admin_events"))


@admin_bp.route("/events/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_event(id):
    """Reject and delete pending event."""
    log_entry("admin", "reject_event", id=id)
    logger.info(f"Event rejection requested for ID {id}")
    
    if current_user.role != "admin":
        log_error("admin", "reject_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "reject_event", f"Fetching event ID {id}")
    event = Event.query.get_or_404(id)
    event_title = event.title
    db.session.delete(event)
    db.session.commit()
    
    log_success("admin", "reject_event", f"Event '{event_title}' rejected and deleted")
    logger.info(f"Event '{event_title}' (ID: {id}) rejected and deleted")
    
    flash(f'Event "{event_title}" rejected and removed.')
    return redirect(url_for("admin.admin_events"))


@admin_bp.route("/events/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def add_event():
    """Add new event (admin only)."""
    log_entry("admin", "add_event", user=current_user.username, method=request.method)
    logger.info(f"Add event page accessed by admin {current_user.username}")
    
    from flask import current_app
    
    if current_user.role != "admin":
        log_error("admin", "add_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    if request.method == "POST":
        image_url = request.form.get("image_url")
        
        # Handle file upload
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
                image_url = url_for("static", filename="uploads/" + filename)
        
        event = Event(
            title=request.form["title"],
            date=datetime.strptime(request.form["date"], "%Y-%m-%d"),
            location=request.form["location"],
            category=request.form["category"],
            description=request.form["description"],
            image_url=image_url,
            barangay=request.form.get("barangay", "Mangatarem"),
            user_id=current_user.id,
            status="approved",  # Admin events auto-approved
        )
        db.session.add(event)
        db.session.commit()
        
        log_success("admin", "add_event", f"New event '{event.title}' added by admin")
        logger.info(f"New event '{event.title}' added by admin {current_user.username}")
        
        flash("Event added successfully!")
        return redirect(url_for("admin.admin_events"))
    
    return render_template("admin/add_event.html")


@admin_bp.route("/events/edit/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def edit_event(id):
    """Edit existing event (admin only)."""
    log_entry("admin", "edit_event", id=id, method=request.method)
    logger.info(f"Event edit requested for ID {id}")
    
    from flask import current_app
    
    log_query("admin", "edit_event", f"Fetching event ID {id}")
    event = Event.query.get_or_404(id)
    
    if current_user.role != "admin":
        log_error("admin", "edit_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    if request.method =="POST":
        event.title = request.form["title"]
        event.date = datetime.strptime(request.form["date"], "%Y-%m-%d")
        event.location = request.form["location"]
        event.category = request.form["category"]
        event.description = request.form["description"]
        event.barangay = request.form.get("barangay", event.barangay)
        
        # Handle file upload
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
                event.image_url = url_for("static", filename="uploads/" + filename)
        
        # Fallback to URL
        if request.form.get("image_url") and not (
            "image" in request.files and request.files["image"].filename
        ):
            event.image_url = request.form.get("image_url")
        
        db.session.commit()
        
        log_success("admin", "edit_event", f"Event '{event.title}' updated")
        logger.info(f"Event '{event.title}' (ID: {id}) updated successfully")
        
        flash("Event updated successfully!")
        return redirect(url_for("admin.admin_events"))
    
    return render_template("admin/edit_event.html", event=event)


@admin_bp.route("/events/delete/<int:id>")
@login_required
@limiter.limit("10 per minute")
def delete_event(id):
    """Delete event (admin only)."""
    log_entry("admin", "delete_event", id=id)
    logger.info(f"Event deletion requested for ID {id}")
    
    if current_user.role != "admin":
        log_error("admin", "delete_event", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "delete_event", f"Fetching event ID {id}")
    event = Event.query.get_or_404(id)
    event_title = event.title
    db.session.delete(event)
    db.session.commit()
    
    log_success("admin", "delete_event", f"Event '{event_title}' deleted")
    logger.info(f"Event '{event_title}' (ID: {id}) deleted successfully")
    
    flash("Event deleted successfully!")
    return redirect(url_for("admin.admin_events"))


# === GALLERY MANAGEMENT ===

@admin_bp.route("/gallery/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_gallery(id):
    """Approve pending gallery item."""
    log_entry("admin", "approve_gallery", id=id)
    logger.info(f"Gallery item approval requested for ID {id}")
    
    if current_user.role != "admin":
        log_error("admin", "approve_gallery", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "approve_gallery", f"Fetching gallery item ID {id}")
    item = GalleryItem.query.get_or_404(id)
    item.status = "approved"
    db.session.commit()
    
    log_success("admin", "approve_gallery", f"Gallery item ID {id} approved")
    logger.info(f"Gallery item ID {id} approved successfully")
    
    flash("Gallery item approved!")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/gallery/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_gallery(id):
    """Reject and delete pending gallery item."""
    log_entry("admin", "reject_gallery", id=id)
    logger.info(f"Gallery item rejection requested for ID {id}")
    
    if current_user.role != "admin":
        log_error("admin", "reject_gallery", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    log_query("admin", "reject_gallery", f"Fetching gallery item ID {id}")
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    log_success("admin", "reject_gallery", f"Gallery item ID {id} rejected and deleted")
    logger.info(f"Gallery item ID {id} rejected and deleted")
    
    flash("Gallery item rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))


# === REVIEW MANAGEMENT ===

@admin_bp.route("/reviews/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_review(id):
    """Approve pending review."""
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    review = Review.query.get_or_404(id)
    review.status = "approved"
    db.session.commit()
    flash("Review approved!")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/reviews/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_review(id):
    """Reject and delete pending review."""
    if current_user.role != "admin":
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    flash("Review rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))


# === UTILITY FUNCTIONS ===

def allowed_file(filename: str) -> bool:
    """
    Check if file has allowed extension.
    
    Args:
        filename: Name of file to check
        
    Returns:
        True if extension is allowed, False otherwise
    """
    from flask import current_app
    
    ALLOWED_EXTENSIONS = current_app.config.get("ALLOWED_EXTENSIONS", {"png", "jpg", "jpeg", "gif", "mp4"})
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
