"""
Business owner dashboard routes.

Handles establishment CRUD, room management, and menu item management
for users with the 'business_owner' role.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Establishment, EstablishmentRoom, EstablishmentMenuItem, EstablishmentReview, BarangayInfo
from functools import wraps
from utils.validators import validate_form_data
from utils.security import (
    validate_string_input,
    validate_email_format,
    validate_float,
    validate_integer,
    sanitize_html_input,
    validate_coordinates,
    validate_phone,
    sanitize_url,
)
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
@validate_form_data({
    "name": {"type": "string", "required": True, "min_length": 1, "max_length": 200},
    "description": {"type": "string", "max_length": 2000},
    "address": {"type": "string", "required": True, "min_length": 1, "max_length": 300},
    "latitude": {"type": "float", "required": True},
    "longitude": {"type": "float", "required": True},
    "contact_number": {"type": "string", "max_length": 20},
    "email": {"type": "string", "max_length": 100},
    "website": {"type": "string", "max_length": 200},
    "price_range": {"type": "string", "max_length": 10}
})
def create_establishment():
    """Create a new establishment listing."""
    existing = _get_owner_establishment()
    if existing:
        flash("You already have an establishment. Edit it instead.", "info")
        return redirect(url_for("business.edit_establishment"))

    if request.method == "POST":
        # Data is already validated by decorator
        name = request.form.get("name")
        description = sanitize_html_input(request.form.get("description", ""))
        address = request.form.get("address")
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
        contact_number = request.form.get("contact_number")
        email = request.form.get("email")
        website = sanitize_url(request.form.get("website", ""))
        price_range = request.form.get("price_range")
        barangay_name = request.form.get("barangay")

        barangay = BarangayInfo.query.filter_by(name=barangay_name).first()
        if not barangay and barangay_name:
            barangay = BarangayInfo(name=barangay_name)
            db.session.add(barangay)
            db.session.flush()

        establishment = Establishment(
            name=name,
            type=request.form.get("type"),
            description=description,
            address=address,
            latitude=latitude,
            longitude=longitude,
            barangay_id=barangay.id if barangay else None,
            contact_number=contact_number,
            email=email,
            website=website,
            price_range=price_range,
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

        # Validate name
        name = request.form.get("name", "").strip()
        valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
        if not valid:
            flash(f"Invalid name: {err}", "error")
            return redirect(url_for("business.edit_establishment"))

        # Validate description (sanitize HTML)
        description = request.form.get("description", "").strip()
        description = sanitize_html_input(description)
        valid, err = validate_string_input(description, max_length=2000, block_sql_injection=False)
        if not valid:
            flash(f"Invalid description: {err}", "error")
            return redirect(url_for("business.edit_establishment"))

        # Validate address
        address = request.form.get("address", "").strip()
        valid, err = validate_string_input(address, min_length=1, max_length=300, block_sql_injection=True)
        if not valid:
            flash(f"Invalid address: {err}", "error")
            return redirect(url_for("business.edit_establishment"))

        # Validate coordinates
        try:
            latitude = float(request.form.get("latitude", 0))
            longitude = float(request.form.get("longitude", 0))
        except (TypeError, ValueError):
            flash("Invalid coordinates: latitude and longitude must be numbers", "error")
            return redirect(url_for("business.edit_establishment"))

        if not validate_coordinates(latitude, longitude):
            flash("Invalid coordinates: latitude must be between -90 and 90, longitude between -180 and 180", "error")
            return redirect(url_for("business.edit_establishment"))

        # Validate contact number
        contact_number = request.form.get("contact_number", "").strip()
        if contact_number and not validate_phone(contact_number):
            flash("Invalid contact number: please enter a valid phone number", "error")
            return redirect(url_for("business.edit_establishment"))

        # Validate email
        email = request.form.get("email", "").strip()
        if email and not validate_email_format(email):
            flash("Invalid email: please enter a valid email address", "error")
            return redirect(url_for("business.edit_establishment"))

        # Validate website
        website = request.form.get("website", "").strip()
        if website:
            website = sanitize_url(website)
            if not website:
                flash("Invalid website URL", "error")
                return redirect(url_for("business.edit_establishment"))

        # Validate price range
        price_range = request.form.get("price_range", "").strip()
        if price_range and price_range not in ("$", "$$", "$$$"):
            flash("Invalid price range: must be $, $$, or $$$", "error")
            return redirect(url_for("business.edit_establishment"))

        barangay = BarangayInfo.query.filter_by(name=barangay_name).first()
        if not barangay and barangay_name:
            barangay = BarangayInfo(name=barangay_name)
            db.session.add(barangay)
            db.session.flush()

        establishment.name = name
        establishment.type = request.form.get("type")
        establishment.description = description
        establishment.address = address
        establishment.latitude = latitude
        establishment.longitude = longitude
        establishment.barangay_id = barangay.id if barangay else None
        establishment.contact_number = contact_number
        establishment.email = email
        establishment.website = website
        establishment.price_range = price_range
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
@validate_form_data({
    "name": {"type": "string", "required": True, "min_length": 1, "max_length": 200},
    "description": {"type": "string", "max_length": 1000},
    "price_per_night": {"type": "float", "min_value": 0},
    "capacity": {"type": "integer", "min_value": 1, "max_value": 100}
})
def add_room():
    """Add a new room to the establishment."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Create your establishment first.", "warning")
        return redirect(url_for("business.create_establishment"))

    # Data is already validated by decorator
    name = request.form.get("name")
    description = sanitize_html_input(request.form.get("description", ""))
    price_val = float(request.form.get("price_per_night")) if request.form.get("price_per_night") else None
    capacity_val = int(request.form.get("capacity", 2))

    room = EstablishmentRoom(
        establishment_id=establishment.id,
        name=name,
        description=description,
        price_per_night=price_val,
        capacity=capacity_val,
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

    # Validate name
    name = request.form.get("name", "").strip()
    valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
    if not valid:
        flash(f"Invalid room name: {err}", "error")
        return redirect(url_for("business.manage_rooms"))

    # Validate description
    description = request.form.get("description", "").strip()
    description = sanitize_html_input(description)
    valid, err = validate_string_input(description, max_length=1000, block_sql_injection=False)
    if not valid:
        flash(f"Invalid room description: {err}", "error")
        return redirect(url_for("business.manage_rooms"))

    # Validate price
    price_raw = request.form.get("price_per_night")
    if price_raw:
        valid, price_val, err = validate_float(price_raw, min_value=0)
        if not valid:
            flash(f"Invalid price per night: {err}", "error")
            return redirect(url_for("business.manage_rooms"))
    else:
        price_val = None

    # Validate capacity
    capacity_raw = request.form.get("capacity")
    valid, capacity_val, err = validate_integer(capacity_raw if capacity_raw else 2, min_value=1, max_value=100)
    if not valid:
        flash(f"Invalid capacity: {err}", "error")
        return redirect(url_for("business.manage_rooms"))

    room.name = name
    room.description = description
    room.price_per_night = price_val
    room.capacity = capacity_val
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

    # Validate name
    name = request.form.get("name", "").strip()
    valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
    if not valid:
        flash(f"Invalid menu item name: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    # Validate description
    description = request.form.get("description", "").strip()
    description = sanitize_html_input(description)
    valid, err = validate_string_input(description, max_length=1000, block_sql_injection=False)
    if not valid:
        flash(f"Invalid menu item description: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    # Validate price
    price_raw = request.form.get("price")
    if price_raw:
        valid, price_val, err = validate_float(price_raw, min_value=0)
        if not valid:
            flash(f"Invalid price: {err}", "error")
            return redirect(url_for("business.manage_menu"))
    else:
        price_val = None

    # Validate category
    category = request.form.get("category", "").strip()
    valid, err = validate_string_input(category, min_length=1, max_length=100, block_sql_injection=True)
    if not valid:
        flash(f"Invalid category: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    item = EstablishmentMenuItem(
        establishment_id=establishment.id,
        name=name,
        description=description,
        price=price_val,
        category=category,
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

    # Validate name
    name = request.form.get("name", "").strip()
    valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
    if not valid:
        flash(f"Invalid menu item name: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    # Validate description
    description = request.form.get("description", "").strip()
    description = sanitize_html_input(description)
    valid, err = validate_string_input(description, max_length=1000, block_sql_injection=False)
    if not valid:
        flash(f"Invalid menu item description: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    # Validate price
    price_raw = request.form.get("price")
    if price_raw:
        valid, price_val, err = validate_float(price_raw, min_value=0)
        if not valid:
            flash(f"Invalid price: {err}", "error")
            return redirect(url_for("business.manage_menu"))
    else:
        price_val = None

    # Validate category
    category = request.form.get("category", "").strip()
    valid, err = validate_string_input(category, min_length=1, max_length=100, block_sql_injection=True)
    if not valid:
        flash(f"Invalid category: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    item.name = name
    item.description = description
    item.price = price_val
    item.category = category
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
