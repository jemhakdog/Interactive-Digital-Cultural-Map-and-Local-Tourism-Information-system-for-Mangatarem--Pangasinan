"""
Business owner dashboard routes.

Handles establishment CRUD, room management, and menu item management
for users with the 'business_owner' role.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Establishment, EstablishmentRoom, EstablishmentMenuItem, EstablishmentReview, BarangayInfo
from functools import wraps
import logging

business_bp = Blueprint("business", __name__, url_prefix="/business")
logger = logging.getLogger(__name__)


def business_owner_required(f):
    """Decorator to restrict access to business_owner role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "business_owner":
            flash("Access denied. Business owner account required.", "error")
            return redirect(url_for("public.index"))
        return f(*args, **kwargs)
    return decorated


def _get_owner_establishment():
    """Get the current business owner's establishment."""
    return Establishment.query.filter_by(owner_id=current_user.id).first()


@business_bp.route("/dashboard")
@login_required
@business_owner_required
def dashboard():
    """Business owner dashboard overview."""
    establishment = _get_owner_establishment()
    
    stats = {}
    if establishment:
        stats["total_reviews"] = EstablishmentReview.query.filter_by(
            establishment_id=establishment.id
        ).count()
        stats["pending_reviews"] = EstablishmentReview.query.filter_by(
            establishment_id=establishment.id, status="pending"
        ).count()
        stats["room_count"] = EstablishmentRoom.query.filter_by(
            establishment_id=establishment.id
        ).count()
        stats["menu_count"] = EstablishmentMenuItem.query.filter_by(
            establishment_id=establishment.id
        ).count()
    
    return render_template(
        "business/dashboard.html",
        establishment=establishment,
        stats=stats,
    )


@business_bp.route("/establishment/create", methods=["GET", "POST"])
@login_required
@business_owner_required
def create_establishment():
    """Create a new establishment listing."""
    existing = _get_owner_establishment()
    if existing:
        flash("You already have an establishment. Edit it instead.", "info")
        return redirect(url_for("business.edit_establishment"))

    if request.method == "POST":
        barangay_name = request.form.get("barangay")
        barangay = BarangayInfo.query.filter_by(name=barangay_name).first()
        if not barangay and barangay_name:
            barangay = BarangayInfo(name=barangay_name)
            db.session.add(barangay)
            db.session.flush()

        establishment = Establishment(
            name=request.form.get("name"),
            type=request.form.get("type"),
            description=request.form.get("description"),
            address=request.form.get("address"),
            latitude=float(request.form.get("latitude", 0)),
            longitude=float(request.form.get("longitude", 0)),
            barangay_id=barangay.id if barangay else None,
            contact_number=request.form.get("contact_number"),
            email=request.form.get("email"),
            website=request.form.get("website"),
            price_range=request.form.get("price_range"),
            cover_image_url=request.form.get("cover_image_url"),
            logo_url=request.form.get("logo_url"),
            owner_id=current_user.id,
            status="pending",
        )

        # Parse amenities from checkboxes
        amenities = request.form.getlist("amenities")
        establishment.amenities = amenities if amenities else None

        # Parse operating hours from form
        operating_hours = {}
        for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
            open_time = request.form.get(f"hours_{day}_open")
            close_time = request.form.get(f"hours_{day}_close")
            if open_time and close_time:
                operating_hours[day] = f"{open_time}-{close_time}"
        establishment.operating_hours = operating_hours if operating_hours else None

        db.session.add(establishment)
        db.session.commit()

        logger.info(f"Business owner '{current_user.username}' created establishment '{establishment.name}'")
        flash("Your establishment has been submitted for approval!", "success")
        return redirect(url_for("business.dashboard"))

    barangays = BarangayInfo.query.order_by(BarangayInfo.name).all()
    return render_template("business/edit_establishment.html", establishment=None, barangays=barangays)


@business_bp.route("/establishment/edit", methods=["GET", "POST"])
@login_required
@business_owner_required
def edit_establishment():
    """Edit existing establishment."""
    establishment = _get_owner_establishment()
    if not establishment:
        return redirect(url_for("business.create_establishment"))

    if request.method == "POST":
        barangay_name = request.form.get("barangay")
        barangay = BarangayInfo.query.filter_by(name=barangay_name).first()
        if not barangay and barangay_name:
            barangay = BarangayInfo(name=barangay_name)
            db.session.add(barangay)
            db.session.flush()

        establishment.name = request.form.get("name")
        establishment.type = request.form.get("type")
        establishment.description = request.form.get("description")
        establishment.address = request.form.get("address")
        establishment.latitude = float(request.form.get("latitude", 0))
        establishment.longitude = float(request.form.get("longitude", 0))
        establishment.barangay_id = barangay.id if barangay else None
        establishment.contact_number = request.form.get("contact_number")
        establishment.email = request.form.get("email")
        establishment.website = request.form.get("website")
        establishment.price_range = request.form.get("price_range")
        establishment.cover_image_url = request.form.get("cover_image_url")
        establishment.logo_url = request.form.get("logo_url")

        # Parse amenities
        amenities = request.form.getlist("amenities")
        establishment.amenities = amenities if amenities else None

        # Parse operating hours
        operating_hours = {}
        for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]:
            open_time = request.form.get(f"hours_{day}_open")
            close_time = request.form.get(f"hours_{day}_close")
            if open_time and close_time:
                operating_hours[day] = f"{open_time}-{close_time}"
        establishment.operating_hours = operating_hours if operating_hours else None

        db.session.commit()
        logger.info(f"Establishment '{establishment.name}' updated by owner '{current_user.username}'")
        flash("Establishment updated successfully!", "success")
        return redirect(url_for("business.dashboard"))

    barangays = BarangayInfo.query.order_by(BarangayInfo.name).all()
    return render_template("business/edit_establishment.html", establishment=establishment, barangays=barangays)


# === Room Management ===

@business_bp.route("/rooms")
@login_required
@business_owner_required
def manage_rooms():
    """List and manage rooms for inn/hotel."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Create your establishment first.", "warning")
        return redirect(url_for("business.create_establishment"))

    rooms = EstablishmentRoom.query.filter_by(establishment_id=establishment.id).all()
    return render_template("business/manage_rooms.html", establishment=establishment, rooms=rooms)


@business_bp.route("/rooms/add", methods=["POST"])
@login_required
@business_owner_required
def add_room():
    """Add a new room to the establishment."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Create your establishment first.", "warning")
        return redirect(url_for("business.create_establishment"))

    room = EstablishmentRoom(
        establishment_id=establishment.id,
        name=request.form.get("name"),
        description=request.form.get("description"),
        price_per_night=float(request.form.get("price_per_night", 0)) if request.form.get("price_per_night") else None,
        capacity=int(request.form.get("capacity", 2)),
        is_available=request.form.get("is_available") == "on",
    )

    # Parse amenities
    amenities = request.form.getlist("room_amenities")
    room.amenities = amenities if amenities else None

    # Parse image URLs (comma-separated)
    images_raw = request.form.get("image_urls", "")
    image_urls = [url.strip() for url in images_raw.split(",") if url.strip()]
    room.image_urls = image_urls if image_urls else None

    db.session.add(room)
    db.session.commit()

    flash(f"Room '{room.name}' added successfully!", "success")
    return redirect(url_for("business.manage_rooms"))


@business_bp.route("/rooms/<int:room_id>/edit", methods=["POST"])
@login_required
@business_owner_required
def edit_room(room_id):
    """Edit an existing room."""
    establishment = _get_owner_establishment()
    room = EstablishmentRoom.query.get_or_404(room_id)

    if not establishment or room.establishment_id != establishment.id:
        flash("Access denied.", "error")
        return redirect(url_for("business.dashboard"))

    room.name = request.form.get("name")
    room.description = request.form.get("description")
    room.price_per_night = float(request.form.get("price_per_night", 0)) if request.form.get("price_per_night") else None
    room.capacity = int(request.form.get("capacity", 2))
    room.is_available = request.form.get("is_available") == "on"

    amenities = request.form.getlist("room_amenities")
    room.amenities = amenities if amenities else None

    images_raw = request.form.get("image_urls", "")
    image_urls = [url.strip() for url in images_raw.split(",") if url.strip()]
    room.image_urls = image_urls if image_urls else None

    db.session.commit()
    flash(f"Room '{room.name}' updated!", "success")
    return redirect(url_for("business.manage_rooms"))


@business_bp.route("/rooms/<int:room_id>/delete", methods=["POST"])
@login_required
@business_owner_required
def delete_room(room_id):
    """Delete a room."""
    establishment = _get_owner_establishment()
    room = EstablishmentRoom.query.get_or_404(room_id)

    if not establishment or room.establishment_id != establishment.id:
        flash("Access denied.", "error")
        return redirect(url_for("business.dashboard"))

    db.session.delete(room)
    db.session.commit()
    flash("Room deleted.", "success")
    return redirect(url_for("business.manage_rooms"))


# === Menu Item Management ===

@business_bp.route("/menu")
@login_required
@business_owner_required
def manage_menu():
    """List and manage menu items for restaurant/cafe."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Create your establishment first.", "warning")
        return redirect(url_for("business.create_establishment"))

    items = EstablishmentMenuItem.query.filter_by(establishment_id=establishment.id).order_by(
        EstablishmentMenuItem.category, EstablishmentMenuItem.name
    ).all()

    # Group by category
    from collections import defaultdict
    grouped = defaultdict(list)
    for item in items:
        grouped[item.category or "Other"].append(item)

    return render_template(
        "business/manage_menu.html",
        establishment=establishment,
        items=items,
        grouped_items=dict(grouped),
    )


@business_bp.route("/menu/add", methods=["POST"])
@login_required
@business_owner_required
def add_menu_item():
    """Add a new menu item."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Create your establishment first.", "warning")
        return redirect(url_for("business.create_establishment"))

    item = EstablishmentMenuItem(
        establishment_id=establishment.id,
        name=request.form.get("name"),
        description=request.form.get("description"),
        price=float(request.form.get("price", 0)) if request.form.get("price") else None,
        category=request.form.get("category"),
        image_url=request.form.get("image_url"),
        is_available=request.form.get("is_available") == "on",
        is_bestseller=request.form.get("is_bestseller") == "on",
    )

    db.session.add(item)
    db.session.commit()
    flash(f"Menu item '{item.name}' added!", "success")
    return redirect(url_for("business.manage_menu"))


@business_bp.route("/menu/<int:item_id>/edit", methods=["POST"])
@login_required
@business_owner_required
def edit_menu_item(item_id):
    """Edit an existing menu item."""
    establishment = _get_owner_establishment()
    item = EstablishmentMenuItem.query.get_or_404(item_id)

    if not establishment or item.establishment_id != establishment.id:
        flash("Access denied.", "error")
        return redirect(url_for("business.dashboard"))

    item.name = request.form.get("name")
    item.description = request.form.get("description")
    item.price = float(request.form.get("price", 0)) if request.form.get("price") else None
    item.category = request.form.get("category")
    item.image_url = request.form.get("image_url")
    item.is_available = request.form.get("is_available") == "on"
    item.is_bestseller = request.form.get("is_bestseller") == "on"

    db.session.commit()
    flash(f"Menu item '{item.name}' updated!", "success")
    return redirect(url_for("business.manage_menu"))


@business_bp.route("/menu/<int:item_id>/delete", methods=["POST"])
@login_required
@business_owner_required
def delete_menu_item(item_id):
    """Delete a menu item."""
    establishment = _get_owner_establishment()
    item = EstablishmentMenuItem.query.get_or_404(item_id)

    if not establishment or item.establishment_id != establishment.id:
        flash("Access denied.", "error")
        return redirect(url_for("business.dashboard"))

    db.session.delete(item)
    db.session.commit()
    flash("Menu item deleted.", "success")
    return redirect(url_for("business.manage_menu"))


@business_bp.route("/reviews")
@login_required
@business_owner_required
def view_reviews():
    """View reviews for the business owner's establishment."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Create your establishment first.", "warning")
        return redirect(url_for("business.create_establishment"))

    reviews = EstablishmentReview.query.filter_by(
        establishment_id=establishment.id
    ).order_by(EstablishmentReview.created_at.desc()).all()

    return render_template(
        "business/reviews.html",
        establishment=establishment,
        reviews=reviews,
    )

@business_bp.route("/browse")
@login_required
@business_owner_required
def browse_peers():
    """Browse other approved establishments of the same type."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Please create your establishment profile first to browse peers.", "info")
        return redirect(url_for("business.create_establishment"))

    # Mapping for friendly labels
    type_labels = {
        "inn": "Inns & Lodges",
        "restaurant": "Restaurants",
        "cafe": "Cafés",
        "fastfood": "Fast Food Establishments"
    }
    type_label = type_labels.get(establishment.type, establishment.type.title() + "s")

    # Get approved establishments of the same type, excluding own
    peers = Establishment.query.filter_by(
        type=establishment.type,
        status="approved"
    ).filter(Establishment.id != (establishment.id if establishment else 0)).order_by(
        Establishment.is_featured.desc(), 
        Establishment.rating_avg.desc()
    ).all()

    return render_template(
        "business/browse_peers.html",
        establishment=establishment,
        peers=peers,
        type_label=type_label
    )
