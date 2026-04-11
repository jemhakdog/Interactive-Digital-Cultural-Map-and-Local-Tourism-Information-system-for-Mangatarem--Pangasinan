import logging
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db, limiter
from models import Attraction
from utils.logger_helper import log_entry, log_success, log_error
from utils.file_helpers import save_uploaded_file
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
        image_url = request.form.get("image_url")
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                image_url = uploaded_url
        
        attraction = Attraction(
            name=request.form.get("name"),
            category=request.form.get("category"),
            description=request.form.get("description"),
            latitude=float(request.form.get("latitude")),
            longitude=float(request.form.get("longitude")),
            image_url=image_url,
            user_id=current_user.id,
            barangay_id=1, # Admin submissions default to global/center
            status="approved",
        )
        db.session.add(attraction)
        db.session.commit()
        
        log_success("admin", "add_attraction", f"New attraction '{attraction.name}' added")
        flash("Attraction added successfully!")
        return redirect(url_for("admin.admin_attractions"))
    
    return render_template("admin/add_attraction.html")


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
        attraction.name = request.form.get("name")
        attraction.category = request.form.get("category")
        attraction.description = request.form.get("description")
        attraction.latitude = float(request.form.get("latitude"))
        attraction.longitude = float(request.form.get("longitude"))
        
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
    
    return render_template("admin/edit_attraction.html", attraction=attraction)
