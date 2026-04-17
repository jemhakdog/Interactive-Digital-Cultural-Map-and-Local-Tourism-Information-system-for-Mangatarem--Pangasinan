import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Attraction, BarangayInfo
from utils.logger_helper import log_entry, log_success, log_error
from utils.file_helpers import save_uploaded_file
from utils.security import validate_string_input, validate_float, validate_coordinates, sanitize_html_input, validate_integer
from . import admin_bp

logger = logging.getLogger(__name__)

@admin_bp.route("/attractions")
@login_required
def admin_attractions():
    """Display attractions management page with pagination."""
    log_entry("admin", "admin_attractions")
    
    if current_user.role != "admin":
        log_error("admin", "admin_attractions", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    paginated = Attraction.query.order_by(Attraction.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    all_attractions = paginated.items
    pending_attractions = Attraction.query.filter_by(status="pending").all()
    
    log_success("admin", "admin_attractions", f"Loaded {len(all_attractions)} attractions (Page {page})")
    return render_template(
        "admin/attractions.html",
        pending_attractions=pending_attractions,
        all_attractions=all_attractions,
        pagination=paginated,
    )


@admin_bp.route("/attractions/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def add_attraction():
    """Add new attraction (admin only)."""
    log_entry("admin", "add_attraction", method=request.method)
    
    if current_user.role != "admin":
        log_error("admin", "add_attraction", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")
        lat_str = request.form.get("latitude")
        lng_str = request.form.get("longitude")

        # Validate name
        valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
        if not valid:
            flash(f"Name: {err}", "error")
            return redirect(url_for("admin.add_attraction"))

        # Validate and sanitize description
        valid, err = validate_string_input(description, max_length=2000, block_sql_injection=True)
        if not valid:
            flash(f"Description: {err}", "error")
            return redirect(url_for("admin.add_attraction"))
        description = sanitize_html_input(description)

        # Validate category
        valid, err = validate_string_input(category, max_length=100, block_sql_injection=True)
        if not valid:
            flash(f"Category: {err}", "error")
            return redirect(url_for("admin.add_attraction"))

        # Validate coordinates
        valid_lat, lat_val, err_lat = validate_float(lat_str)
        valid_lng, lng_val, err_lng = validate_float(lng_str)
        if not valid_lat or not valid_lng:
            flash("Latitude and longitude must be valid numbers.", "error")
            return redirect(url_for("admin.add_attraction"))
        if not validate_coordinates(lat_val, lng_val):
            flash("Coordinates are out of range.", "error")
            return redirect(url_for("admin.add_attraction"))

        image_url = request.form.get("image_url")
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                image_url = uploaded_url

        attraction = Attraction(
            name=name,
            category=category,
            description=description,
            latitude=lat_val,
            longitude=lng_val,
            image_url=image_url,
            user_id=current_user.id,
            barangay_id=int(request.form.get("barangay_id", 1)),
            status="approved",
        )
        db.session.add(attraction)
        db.session.commit()

        log_success("admin", "add_attraction", f"New attraction '{attraction.name}' added")
        flash("Attraction added successfully!")
        return redirect(url_for("admin.admin_attractions"))
    
    barangays = BarangayInfo.query.order_by(BarangayInfo.name).all()
    return render_template("admin/add_attraction.html", barangays=barangays)


@admin_bp.route("/attractions/approve/<int:id>")
@login_required
@limiter.limit("10 per minute")
def approve_attraction(id):
    """Approve pending attraction."""
    log_entry("admin", "approve_attraction", id=id)
    
    if current_user.role != "admin":
        log_error("admin", "approve_attraction", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    attraction = Attraction.query.get_or_404(id)
    attraction.status = "approved"
    db.session.commit()
    
    log_success("admin", "approve_attraction", f"Attraction '{attraction.name}' approved")
    flash(f'Attraction "{attraction.name}" approved!')
    return redirect(url_for("admin.admin_attractions"))


@admin_bp.route("/attractions/delete/<int:id>")
@login_required
@limiter.limit("10 per minute")
def delete_attraction(id):
    """Delete attraction (admin or owner only)."""
    log_entry("admin", "delete_attraction", id=id)
    attraction = Attraction.query.get_or_404(id)
    
    if current_user.role != "admin" and attraction.user_id != current_user.id:
        log_error("admin", "delete_attraction", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    
    attraction_name = attraction.name
    db.session.delete(attraction)
    db.session.commit()
    
    log_success("admin", "delete_attraction", f"Attraction '{attraction_name}' deleted")
    flash("Attraction deleted.")
    return redirect(url_for("admin.admin_attractions"))


@admin_bp.route("/attractions/edit/<int:id>", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def edit_attraction(id):
    """Edit attraction (admin or owner only)."""
    log_entry("admin", "edit_attraction", id=id, method=request.method)
    attraction = Attraction.query.get_or_404(id)
    
    if current_user.role != "admin" and attraction.user_id != current_user.id:
        log_error("admin", "edit_attraction", "Access denied")
        flash("Access denied.")
        return redirect(url_for("public.index"))
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")
        barangay_id_str = request.form.get("barangay_id")
        lat_str = request.form.get("latitude")
        lng_str = request.form.get("longitude")

        # Validate name
        valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
        if not valid:
            flash(f"Name: {err}", "error")
            return redirect(url_for("admin.edit_attraction", id=id))

        # Validate and sanitize description
        valid, err = validate_string_input(description, max_length=2000, block_sql_injection=True)
        if not valid:
            flash(f"Description: {err}", "error")
            return redirect(url_for("admin.edit_attraction", id=id))
        description = sanitize_html_input(description)

        # Validate category
        valid, err = validate_string_input(category, max_length=100, block_sql_injection=True)
        if not valid:
            flash(f"Category: {err}", "error")
            return redirect(url_for("admin.edit_attraction", id=id))

        # Validate coordinates
        valid_lat, lat_val, err_lat = validate_float(lat_str)
        valid_lng, lng_val, err_lng = validate_float(lng_str)
        if not valid_lat or not valid_lng:
            flash("Latitude and longitude must be valid numbers.", "error")
            return redirect(url_for("admin.edit_attraction", id=id))
        if not validate_coordinates(lat_val, lng_val):
            flash("Coordinates are out of range.", "error")
            return redirect(url_for("admin.edit_attraction", id=id))

        if barangay_id_str:
            valid_bar, barangay_id, err_bar = validate_integer(barangay_id_str, min_value=1)
            if not valid_bar:
                flash("Invalid barangay ID.", "error")
                return redirect(url_for("admin.edit_attraction", id=id))
            attraction.barangay_id = barangay_id

        attraction.name = name
        attraction.category = category
        attraction.description = description
        attraction.latitude = lat_val
        attraction.longitude = lng_val

        # Handle image upload
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                attraction.image_url = uploaded_url

        if request.form.get("image_url"):
            attraction.image_url = request.form.get("image_url")

        # Contributors require re-approval
        if current_user.role == "contributor":
            attraction.status = "pending"

        db.session.commit()
        log_success("admin", "edit_attraction", f"Attraction '{attraction.name}' updated")
        flash("Attraction updated.")
        return redirect(url_for("admin.admin_attractions"))
    
    barangays = BarangayInfo.query.order_by(BarangayInfo.name).all()
    return render_template("admin/edit_attraction.html", attraction=attraction, barangays=barangays)
