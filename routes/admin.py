from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, Attraction, Event, GalleryItem, PageView
from extensions import limiter
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from sqlalchemy import func
import os
import logging

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
logger = logging.getLogger(__name__)


@admin_bp.route("/dashboard")
@login_required
def admin_dashboard():
    """
    Display the admin dashboard with statistics and pending approvals.

    Shows counts of attractions, events, and gallery items, along with
    pending user registrations and gallery items awaiting approval.
    Also shows analytics: most viewed attractions and engagement trends.

    Returns:
        Rendered admin dashboard template with stats and pending items.
    """
    print(
        f"[PROGRESSIVE LOG] [admin] > admin_dashboard > ENTRY: user='{current_user.username}'"
    )
    logger.info("Admin dashboard accessed")

    # Admin only
    if current_user.role != "admin":
        print(
            f"[PROGRESSIVE LOG] [admin] > admin_dashboard > ERROR: Access denied for role='{current_user.role}'"
        )
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(f"[PROGRESSIVE LOG] [admin] > admin_dashboard > QUERY: Fetching basic stats")
    stats = {
        "attractions": Attraction.query.count(),
        "events": Event.query.count(),
        "gallery": GalleryItem.query.count(),
    }

    # Analytics: Most Viewed Attractions
    top_attractions_query = (
        db.session.query(Attraction.name, func.count(PageView.id).label("view_count"))
        .join(PageView, PageView.item_id == Attraction.id)
        .filter(PageView.view_type == "attraction")
        .group_by(Attraction.id)
        .order_by(func.count(PageView.id).desc())
        .limit(5)
        .all()
    )

    top_attractions = [
        {"name": name, "views": count} for name, count in top_attractions_query
    ]

    # Analytics: Engagement Trends (Last 7 Days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    # SQLite has limited date functions, this works for many, but for SQLite specifically:
    # We might need to handle date extraction carefully if using SQLite directly.
    # Flask-SQLAlchemy usually handles dialects but func.date() in SQLite returns string 'YYYY-MM-DD'
    daily_views_query = (
        db.session.query(
            func.date(PageView.timestamp).label("date"),
            func.count(PageView.id).label("count"),
        )
        .filter(PageView.timestamp >= seven_days_ago)
        .group_by(func.date(PageView.timestamp))
        .all()
    )

    daily_views_dict = {str(d): c for d, c in daily_views_query}

    trend_dates = []
    trend_counts = []

    for i in range(6, -1, -1):
        d = (datetime.utcnow() - timedelta(days=i)).date()
        d_str = str(d)
        trend_dates.append(d.strftime("%b %d"))
        trend_counts.append(daily_views_dict.get(d_str, 0))

    engagement_data = {"dates": trend_dates, "counts": trend_counts}

    pending_users = User.query.filter_by(is_approved=False, role="contributor").all()
    pending_gallery = GalleryItem.query.filter_by(status="pending").all()

    print(
        f"[PROGRESSIVE LOG] [admin] > admin_dashboard > SUCCESS: Dashboard loaded with {stats['attractions']} attractions, {stats['events']} events"
    )
    logger.info(
        f"Dashboard data loaded: {stats['attractions']} attractions, {stats['events']} events, {len(pending_users)} pending users"
    )

    print(
        f"[PROGRESSIVE LOG] [admin] > admin_dashboard > RENDER: Rendering admin/dashboard.html"
    )
    return render_template(
        "admin/dashboard.html",
        stats=stats,
        pending_users=pending_users,
        pending_gallery=pending_gallery,
        top_attractions=top_attractions,
        engagement_data=engagement_data,
    )


@admin_bp.route("/users/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_user(id):
    """
    Approve a pending contributor user registration.

    Args:
        id: The ID of the user to approve.

    Returns:
        Redirect to admin dashboard with success message.
    """
    print(f"[PROGRESSIVE LOG] [admin] > approve_user > ENTRY: id={id}")
    logger.info(f"User approval requested for user ID {id}")

    if current_user.role != "admin":
        print(
            f"[PROGRESSIVE LOG] [admin] > approve_user > ERROR: Access denied for user ID={current_user.id}"
        )
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(f"[PROGRESSIVE LOG] [admin] > approve_user > QUERY: Fetching user ID {id}")
    user = User.query.get_or_404(id)
    user.is_approved = True
    db.session.commit()

    print(
        f"[PROGRESSIVE LOG] [admin] > approve_user > SUCCESS: User '{user.username}' approved"
    )
    logger.info(f"User '{user.username}' (ID: {id}) approved successfully")

    flash(f"User {user.username} approved!")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/users/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_user(id):
    """
    Reject and delete a pending contributor user registration.

    Args:
        id: The ID of the user to reject.

    Returns:
        Redirect to admin dashboard with confirmation message.
    """
    print(f"[PROGRESSIVE LOG] [admin] > reject_user > ENTRY: id={id}")
    logger.info(f"User rejection requested for user ID {id}")

    if current_user.role != "admin":
        print(
            f"[PROGRESSIVE LOG] [admin] > reject_user > ERROR: Access denied for user ID={current_user.id}"
        )
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(f"[PROGRESSIVE LOG] [admin] > reject_user > QUERY: Fetching user ID {id}")
    user = User.query.get_or_404(id)
    username = user.username
    db.session.delete(user)
    db.session.commit()

    print(
        f"[PROGRESSIVE LOG] [admin] > reject_user > SUCCESS: User '{username}' rejected and deleted"
    )
    logger.info(f"User '{username}' (ID: {id}) rejected and deleted")

    flash(f"User {username} rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/attractions")
@login_required
def admin_attractions():
    """
    Display the attractions management page for admins.

    Shows all attractions with pending items highlighted for review.

    Returns:
        Rendered attractions management template with pending and all attractions.
    """
    print(f"[PROGRESSIVE LOG] [admin] > admin_attractions > ENTRY")
    logger.info("Admin attractions management page accessed")

    if current_user.role != "admin":
        print(f"[PROGRESSIVE LOG] [admin] > admin_attractions > ERROR: Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(
        f"[PROGRESSIVE LOG] [admin] > admin_attractions > QUERY: Fetching all attractions"
    )
    pending_attractions = Attraction.query.filter_by(status="pending").all()
    all_attractions = Attraction.query.order_by(Attraction.created_at.desc()).all()

    print(
        f"[PROGRESSIVE LOG] [admin] > admin_attractions > SUCCESS: Loaded {len(all_attractions)} total, {len(pending_attractions)} pending"
    )
    logger.info(
        f"Attractions page loaded: {len(all_attractions)} total, {len(pending_attractions)} pending"
    )

    print(
        f"[PROGRESSIVE LOG] [admin] > admin_attractions > RENDER: Rendering admin/attractions.html"
    )
    return render_template(
        "admin/attractions.html",
        pending_attractions=pending_attractions,
        all_attractions=all_attractions,
    )


@admin_bp.route("/events")
@login_required
def admin_events():
    """
    Display the events management page for admins.

    Shows all events with pending items highlighted for review.

    Returns:
        Rendered events management template with pending and all events.
    """
    print(f"[PROGRESSIVE LOG] [admin] > admin_events > ENTRY")
    logger.info("Admin events management page accessed")

    if current_user.role != "admin":
        print(f"[PROGRESSIVE LOG] [admin] > admin_events > ERROR: Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(f"[PROGRESSIVE LOG] [admin] > admin_events > QUERY: Fetching all events")
    pending_events = Event.query.filter_by(status="pending").all()
    all_events = Event.query.order_by(Event.date.asc()).all()

    print(
        f"[PROGRESSIVE LOG] [admin] > admin_events > SUCCESS: Loaded {len(all_events)} total, {len(pending_events)} pending"
    )
    logger.info(
        f"Events page loaded: {len(all_events)} total, {len(pending_events)} pending"
    )

    print(
        f"[PROGRESSIVE LOG] [admin] > admin_events > RENDER: Rendering admin/events.html"
    )
    return render_template(
        "admin/events.html", pending_events=pending_events, all_events=all_events
    )


@admin_bp.route("/attractions/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_attraction(id):
    """
    Approve a pending attraction submission.

    Args:
        id: The ID of the attraction to approve.

    Returns:
        Redirect to attractions management page with success message.
    """
    print(f"[PROGRESSIVE LOG] [admin] > approve_attraction > ENTRY: id={id}")
    logger.info(f"Attraction approval requested for ID {id}")

    if current_user.role != "admin":
        print(f"[PROGRESSIVE LOG] [admin] > approve_attraction > ERROR: Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(
        f"[PROGRESSIVE LOG] [admin] > approve_attraction > QUERY: Fetching attraction ID {id}"
    )
    attraction = Attraction.query.get_or_404(id)
    attraction.status = "approved"
    db.session.commit()

    print(
        f"[PROGRESSIVE LOG] [admin] > approve_attraction > SUCCESS: Attraction '{attraction.name}' approved"
    )
    logger.info(f"Attraction '{attraction.name}' (ID: {id}) approved successfully")

    flash(f'Attraction "{attraction.name}" approved!')
    return redirect(url_for("admin.admin_attractions"))


@admin_bp.route("/attractions/delete/<int:id>")
@login_required
@limiter.limit("10 per minute")
def delete_attraction(id):
    """
    Delete an attraction from the system.

    Admins can delete any attraction, contributors can only delete their own.

    Args:
        id: The ID of the attraction to delete.

    Returns:
        Redirect to attractions management page with confirmation message.
    """
    print(f"[PROGRESSIVE LOG] [admin] > delete_attraction > ENTRY: id={id}")
    logger.info(f"Attraction deletion requested for ID {id}")

    print(
        f"[PROGRESSIVE LOG] [admin] > delete_attraction > QUERY: Fetching attraction ID {id}"
    )
    attraction = Attraction.query.get_or_404(id)

    # Check permission
    if current_user.role != "admin" and attraction.user_id != current_user.id:
        print(
            f"[PROGRESSIVE LOG] [admin] > delete_attraction > ERROR: Access denied for user ID={current_user.id}"
        )
        flash("Access denied.")
        return redirect(url_for("public.index"))

    attraction_name = attraction.name
    db.session.delete(attraction)
    db.session.commit()

    print(
        f"[PROGRESSIVE LOG] [admin] > delete_attraction > SUCCESS: Attraction '{attraction_name}' deleted"
    )
    logger.info(f"Attraction '{attraction_name}' (ID: {id}) deleted successfully")

    flash("Attraction deleted.")
    return redirect(url_for("admin.admin_attractions"))


@admin_bp.route("/attractions/edit/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def edit_attraction(id):
    """
    Edit an existing attraction.

    Admins can edit any attraction, contributors can only edit their own.
    When a contributor edits an attraction, its status resets to pending.

    Args:
        id: The ID of the attraction to edit.

    Returns:
        GET: Rendered edit attraction form.
        POST: Redirect to attractions page after successful update.
    """
    print(
        f"[PROGRESSIVE LOG] [admin] > edit_attraction > ENTRY: id={id}, method={request.method}"
    )
    logger.info(f"Attraction edit requested for ID {id}")

    from flask import current_app

    print(
        f"[PROGRESSIVE LOG] [admin] > edit_attraction > QUERY: Fetching attraction ID {id}"
    )
    attraction = Attraction.query.get_or_404(id)

    # Check permission
    if current_user.role != "admin" and attraction.user_id != current_user.id:
        print(
            f"[PROGRESSIVE LOG] [admin] > edit_attraction > ERROR: Access denied for user ID={current_user.id}"
        )
        flash("Access denied.")
        return redirect(url_for("public.index"))

    if request.method == "POST":
        print(
            f"[PROGRESSIVE LOG] [admin] > edit_attraction > LOGIC: Processing form data for '{request.form.get('name')}'"
        )
        attraction.name = request.form.get("name")
        attraction.category = request.form.get("category")
        attraction.description = request.form.get("description")
        attraction.lat = float(request.form.get("lat"))
        attraction.lng = float(request.form.get("lng"))

        # Handle Image Upload
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
                attraction.image_url = url_for("static", filename="uploads/" + filename)

        # Fallback to URL if provided and no file uploaded (or to update URL)
        if request.form.get("image_url"):
            attraction.image_url = request.form.get("image_url")

        if current_user.role == "contributor":
            print(
                f"[PROGRESSIVE LOG] [admin] > edit_attraction > LOGIC: Contributor edited, resetting status to pending"
            )
            attraction.status = "pending"

        db.session.commit()

        print(
            f"[PROGRESSIVE LOG] [admin] > edit_attraction > SUCCESS: Attraction '{attraction.name}' updated"
        )
        logger.info(f"Attraction '{attraction.name}' (ID: {id}) updated successfully")

        print(
            f"[PROGRESSIVE LOG] [admin] > edit_attraction > REDIRECT: Redirecting to admin.admin_attractions"
        )
        flash("Attraction updated.")
        return redirect(url_for("admin.admin_attractions"))

    print(
        f"[PROGRESSIVE LOG] [admin] > edit_attraction > RENDER: Rendering admin/edit_attraction.html"
    )
    return render_template("admin/edit_attraction.html", attraction=attraction)


@admin_bp.route("/events/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_event(id):
    """
    Approve a pending event submission.

    Args:
        id: The ID of the event to approve.

    Returns:
        Redirect to events management page with success message.
    """
    print(f"[PROGRESSIVE LOG] [admin] > approve_event > ENTRY: id={id}")
    logger.info(f"Event approval requested for ID {id}")

    if current_user.role != "admin":
        print(f"[PROGRESSIVE LOG] [admin] > approve_event > ERROR: Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(f"[PROGRESSIVE LOG] [admin] > approve_event > QUERY: Fetching event ID {id}")
    event = Event.query.get_or_404(id)
    event.status = "approved"
    db.session.commit()

    print(
        f"[PROGRESSIVE LOG] [admin] > approve_event > SUCCESS: Event '{event.title}' approved"
    )
    logger.info(f"Event '{event.title}' (ID: {id}) approved successfully")

    flash(f'Event "{event.title}" approved!')
    return redirect(url_for("admin.admin_events"))


@admin_bp.route("/events/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_event(id):
    """
    Reject and delete a pending event submission.

    Args:
        id: The ID of the event to reject.

    Returns:
        Redirect to events management page with confirmation message.
    """
    print(f"[PROGRESSIVE LOG] [admin] > reject_event > ENTRY: id={id}")
    logger.info(f"Event rejection requested for ID {id}")

    if current_user.role != "admin":
        print(f"[PROGRESSIVE LOG] [admin] > reject_event > ERROR: Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(f"[PROGRESSIVE LOG] [admin] > reject_event > QUERY: Fetching event ID {id}")
    event = Event.query.get_or_404(id)
    event_title = event.title
    db.session.delete(event)
    db.session.commit()

    print(
        f"[PROGRESSIVE LOG] [admin] > reject_event > SUCCESS: Event '{event_title}' rejected and deleted"
    )
    logger.info(f"Event '{event_title}' (ID: {id}) rejected and deleted")

    flash(f'Event "{event_title}" rejected and removed.')
    return redirect(url_for("admin.admin_events"))


@admin_bp.route("/gallery/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_gallery(id):
    """
    Approve a pending gallery item submission.

    Args:
        id: The ID of the gallery item to approve.

    Returns:
        Redirect to admin dashboard with success message.
    """
    print(f"[PROGRESSIVE LOG] [admin] > approve_gallery > ENTRY: id={id}")
    logger.info(f"Gallery item approval requested for ID {id}")

    if current_user.role != "admin":
        print(f"[PROGRESSIVE LOG] [admin] > approve_gallery > ERROR: Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(
        f"[PROGRESSIVE LOG] [admin] > approve_gallery > QUERY: Fetching gallery item ID {id}"
    )
    item = GalleryItem.query.get_or_404(id)
    item.status = "approved"
    db.session.commit()

    print(
        f"[PROGRESSIVE LOG] [admin] > approve_gallery > SUCCESS: Gallery item ID {id} approved"
    )
    logger.info(f"Gallery item ID {id} approved successfully")

    flash("Gallery item approved!")
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/gallery/reject/<int:id>")
@login_required
@limiter.limit("10 per minute")
def reject_gallery(id):
    """
    Reject and delete a pending gallery item submission.

    Args:
        id: The ID of the gallery item to reject.

    Returns:
        Redirect to admin dashboard with confirmation message.
    """
    print(f"[PROGRESSIVE LOG] [admin] > reject_gallery > ENTRY: id={id}")
    logger.info(f"Gallery item rejection requested for ID {id}")

    if current_user.role != "admin":
        print(f"[PROGRESSIVE LOG] [admin] > reject_gallery > ERROR: Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))

    print(
        f"[PROGRESSIVE LOG] [admin] > reject_gallery > QUERY: Fetching gallery item ID {id}"
    )
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()

    print(
        f"[PROGRESSIVE LOG] [admin] > reject_gallery > SUCCESS: Gallery item ID {id} rejected and deleted"
    )
    logger.info(f"Gallery item ID {id} rejected and deleted")

    flash("Gallery item rejected and removed.")
    return redirect(url_for("admin.admin_dashboard"))


def allowed_file(filename):
    """
    Check if a file has an allowed extension.

    Args:
        filename: The name of the file to check.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    from flask import current_app

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )
