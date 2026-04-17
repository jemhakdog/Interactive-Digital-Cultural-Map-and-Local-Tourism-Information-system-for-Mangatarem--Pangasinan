import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Attraction
from utils.file_helpers import save_uploaded_file
from utils.security import validate_string_input, validate_float, validate_coordinates, sanitize_html_input
from . import barangay_bp

logger = logging.getLogger(__name__)

@barangay_bp.route("/attractions")
@login_required
def barangay_attractions():
    """Display all attractions created by the current contributor."""
    logger.info("Barangay attractions page accessed by %s", current_user.username)

    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    attractions = (
        Attraction.query.filter_by(barangay_id=current_user.barangay_id)
        .order_by(Attraction.created_at.desc())
        .all()
    )
    return render_template("barangay/attractions.html", attractions=attractions)


@barangay_bp.route("/attractions/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_add_attraction():
    """Add a new attraction (submitted as 'pending' for admin approval)."""
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    if request.method == "POST":
        name = request.form.get("name", "")
        description = request.form.get("description", "")
        category = request.form.get("category", "")
        lat_str = request.form.get("latitude", "")
        lng_str = request.form.get("longitude", "")

        # Validate name
        is_valid, error_msg = validate_string_input(name, max_length=200, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid name: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_attraction"))

        # Validate description
        is_valid, error_msg = validate_string_input(description, max_length=2000, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid description: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_attraction"))

        # Validate category
        is_valid, error_msg = validate_string_input(category, max_length=100, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid category: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_attraction"))

        # Validate coordinates
        try:
            lat = float(lat_str)
            lng = float(lng_str)
        except (ValueError, TypeError):
            flash("Invalid coordinates: latitude and longitude must be numeric.", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_attraction"))

        if not validate_coordinates(lat, lng):
            flash("Invalid coordinates: latitude/longitude out of range.", "error")
            return redirect(request.referrer or url_for("barangay.barangay_add_attraction"))

        image_url = request.form.get("image_url")
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                image_url = uploaded_url

        attraction = Attraction(
            name=name,
            category=category,
            description=sanitize_html_input(description),
            latitude=lat,
            longitude=lng,
            image_url=image_url,
            barangay_id=current_user.barangay_id,
            user_id=current_user.id,
            status="pending",
        )
        db.session.add(attraction)
        db.session.commit()

        logger.info("New attraction '%s' submitted by %s", attraction.name, current_user.username)
        flash("Attraction submitted for approval!")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/add_attraction.html")


@barangay_bp.route("/attractions/edit/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_edit_attraction(id):
    """Edit an attraction owned by the current contributor (resets to 'pending')."""
    attraction = Attraction.query.get_or_404(id)

    if attraction.barangay_id != current_user.barangay_id:
        flash("Access denied. This asset belongs to another barangay.")
        return redirect(url_for("barangay.barangay_dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "")
        description = request.form.get("description", "")
        category = request.form.get("category", "")
        lat_str = request.form.get("latitude", "")
        lng_str = request.form.get("longitude", "")

        # Validate name
        is_valid, error_msg = validate_string_input(name, max_length=200, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid name: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_attraction", id=attraction.id))

        # Validate description
        is_valid, error_msg = validate_string_input(description, max_length=2000, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid description: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_attraction", id=attraction.id))

        # Validate category
        is_valid, error_msg = validate_string_input(category, max_length=100, block_sql_injection=True)
        if not is_valid:
            flash(f"Invalid category: {error_msg}", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_attraction", id=attraction.id))

        # Validate coordinates
        try:
            lat = float(lat_str)
            lng = float(lng_str)
        except (ValueError, TypeError):
            flash("Invalid coordinates: latitude and longitude must be numeric.", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_attraction", id=attraction.id))

        if not validate_coordinates(lat, lng):
            flash("Invalid coordinates: latitude/longitude out of range.", "error")
            return redirect(request.referrer or url_for("barangay.barangay_edit_attraction", id=attraction.id))

        attraction.name = name
        attraction.category = category
        attraction.description = sanitize_html_input(description)
        attraction.latitude = lat
        attraction.longitude = lng

        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                attraction.image_url = uploaded_url

        if request.form.get("image_url") and not ("image" in request.files and request.files["image"].filename):
            attraction.image_url = request.form.get("image_url")

        attraction.status = "pending"
        db.session.commit()

        logger.info("Attraction '%s' (ID: %d) updated by %s", attraction.name, id, current_user.username)
        flash("Attraction updated and submitted for approval.")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/edit_attraction.html", attraction=attraction)


@barangay_bp.route("/attractions/delete/<int:id>")
@login_required
@limiter.limit("10 per minute")
def barangay_delete_attraction(id):
    """Delete an attraction owned by the current contributor."""
    attraction = Attraction.query.get_or_404(id)

    if attraction.barangay_id != current_user.barangay_id:
        flash("Access denied.")
        return redirect(url_for("barangay.barangay_dashboard"))

    attraction_name = attraction.name
    db.session.delete(attraction)
    db.session.commit()

    logger.info("Attraction '%s' (ID: %d) deleted by %s", attraction_name, id, current_user.username)
    flash("Attraction deleted.")
    return redirect(url_for("barangay.barangay_dashboard"))
