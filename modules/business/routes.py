"""
Routes for the Business module.
Handles both public directory and business owner dashboard.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_required, current_user
from extensions import db, limiter
from .models import Establishment, EstablishmentRoom, EstablishmentMenuItem, EstablishmentReview
from modules.barangay.models import BarangayInfo
from functools import wraps
from core.logger import log_entry, log_render
from datetime import datetime, timedelta
import math
import logging
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
from utils.file_helpers import save_uploaded_file

business_bp = Blueprint("business", __name__, url_prefix="/business")
logger = logging.getLogger(__name__)

# --- Decorators ---

def business_owner_required(f):
    """Decorator to restrict access to business_owner role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "business_owner":
            flash("Access denied. Business owner account required.", "error")
            return redirect(url_for("public.index"))
        return f(*args, **kwargs)
    return decorated

def approved_business_owner_required(f):
    """Decorator to restrict access to APPROVED business_owner role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "business_owner":
            flash("Access denied. Business owner account required.", "error")
            return redirect(url_for("public.index"))
        if not current_user.is_approved:
            flash("Your business account is pending approval.", "warning")
            return redirect(url_for("business.dashboard"))
        return f(*args, **kwargs)
    return decorated

def _get_owner_establishment():
    """Get the current business owner's establishment."""
    return Establishment.query.filter_by(owner_id=current_user.id).first()

# --- Public Routes ---

@business_bp.route("/")
def index():
    """Public establishment directory with filters."""
    log_entry("business", "index", method=request.method)
    logger.info("Establishments directory accessed")

    query = Establishment.query.filter_by(status="approved")

    # Smart Filters for Business Owners
    type_filter = request.args.get("type")
    is_auto_filtered = False
    owner_type = None
    show_all = request.args.get("show_all") == "true"

    if not type_filter and not show_all and current_user.is_authenticated and current_user.role == "business_owner":
        owner_establishment = _get_owner_establishment()
        if owner_establishment:
            type_filter = owner_establishment.type
            owner_type = owner_establishment.type
            is_auto_filtered = True

    if type_filter:
        query = query.filter_by(type=type_filter)

    price_filter = request.args.get("price_range")
    if price_filter:
        query = query.filter_by(price_range=price_filter)

    barangay_filter = request.args.get("barangay")
    if barangay_filter:
        query = query.join(BarangayInfo).filter(BarangayInfo.name == barangay_filter)

    search = request.args.get("q")
    if search:
        query = query.filter(Establishment.name.ilike(f"%{search}%"))

    establishments_list = query.order_by(Establishment.is_featured.desc(), Establishment.rating_avg.desc()).all()
    barangays = BarangayInfo.query.order_by(BarangayInfo.name).all()

    log_render("business", "index", "establishments.html")
    return render_template(
        "pagez/establishments.html",
        establishments=establishments_list,
        barangays=barangays,
        is_auto_filtered=is_auto_filtered,
        owner_type=owner_type,
    )

@business_bp.route("/<int:id>")
def detail(id):
    """Public establishment detail page."""
    log_entry("business", "detail", id=id)
    establishment = Establishment.query.get_or_404(id)

    if establishment.status != "approved":
        flash("This establishment is not yet published.", "warning")
        return redirect(url_for("business.index"))

    rooms = []
    menu_items = []

    if establishment.type == "inn":
        rooms = EstablishmentRoom.query.filter_by(
            establishment_id=establishment.id, is_available=True
        ).all()
    else:
        menu_items = EstablishmentMenuItem.query.filter_by(
            establishment_id=establishment.id, is_available=True
        ).order_by(EstablishmentMenuItem.category, EstablishmentMenuItem.name).all()

    reviews = EstablishmentReview.query.filter_by(
        establishment_id=establishment.id, status="approved", parent_id=None
    ).order_by(EstablishmentReview.created_at.desc()).all()

    # Check if favorited by current user
    is_favorite = False
    is_stamped_today = False
    stamp_metadata = {}
    is_active_route = False
    
    if current_user.is_authenticated:
        from modules.business.models import UserFavoriteEstablishment
        is_favorite = UserFavoriteEstablishment.query.filter_by(
            user_id=current_user.id, establishment_id=id
        ).first() is not None
        
        # Check if checked in today
        from modules.gamification.models import TouristCheckIn
        from datetime import datetime
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stamped_today_record = TouristCheckIn.query.filter(
            TouristCheckIn.user_id == current_user.id,
            TouristCheckIn.establishment_id == id,
            TouristCheckIn.verified_at >= today_start
        ).first()
        
        if stamped_today_record:
            is_stamped_today = True
            stamp_metadata = {
                "verified_at": stamped_today_record.verified_at.strftime("%I:%M %p"),
                "distance": round(stamped_today_record.distance_meters, 1) if stamped_today_record.distance_meters else None
            }
            
        # Check if active navigation route in session matches this establishment
        from flask import session
        active_nav = session.get('active_nav')
        if active_nav and active_nav.get('type') == 'establishment' and int(active_nav.get('id')) == id:
            is_active_route = True

    log_render("business", "detail", "establishment_detail.html")
    return render_template(
        "pagez/establishment_detail.html",
        establishment=establishment,
        rooms=rooms,
        menu_items=menu_items,
        reviews=reviews,
        is_favorite=is_favorite,
        is_stamped_today=is_stamped_today,
        stamp_metadata=stamp_metadata,
        is_active_route=is_active_route
    )

@business_bp.route("/<int:id>/review", methods=["POST"])
@login_required
@validate_form_data({
    'rating': {'type': 'int', 'min': 1, 'max': 5, 'required': True},
    'comment': {'type': 'string', 'max_length': 2000, 'required': True}
})
def submit_review(id):
    """Submit a review for an establishment."""
    establishment = Establishment.query.get_or_404(id)
    rating = int(request.form.get("rating"))
    comment = request.form.get("comment", "")
    
    # Sanitize HTML but allow basic formatting
    sanitized_comment = sanitize_html_input(comment)

    review = EstablishmentReview(
        user_id=current_user.id,
        establishment_id=establishment.id,
        rating=rating,
        comment=sanitized_comment,
        status="approved",
    )
    db.session.add(review)
    db.session.flush()

    # Recalculate establishment rating
    approved_reviews = EstablishmentReview.query.filter_by(
        establishment_id=establishment.id, status="approved", parent_id=None
    ).all()
    if approved_reviews:
        establishment.rating_avg = sum(r.rating for r in approved_reviews) / len(approved_reviews)
        establishment.review_count = len(approved_reviews)
    else:
        establishment.rating_avg = 0
        establishment.review_count = 0

    # Dispatch notification to the establishment owner
    if establishment.owner_id and establishment.owner_id != current_user.id:
        try:
            from modules.notifications.models import create_notification
            create_notification(
                user_id=establishment.owner_id,
                title="New Establishment Review",
                message=f"A customer ({current_user.username}) left a {rating}-star review for your establishment '{establishment.name}'.",
                link=url_for("business.detail", id=establishment.id)
            )
        except Exception as e:
            logger.error(f"Failed to dispatch review notification: {e}")

    db.session.commit()

    flash("Your review has been posted successfully.", "success")
    return redirect(url_for("business.detail", id=id))

# --- Dashboard Routes ---

@business_bp.route("/dashboard")
@login_required
@business_owner_required
def dashboard():
    """Business owner dashboard overview."""
    if not current_user.is_approved:
        from modules.business.models import BusinessVerification
        verification = BusinessVerification.query.filter_by(user_id=current_user.id).first()
        return render_template("business/verify.html", verification=verification)
        
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

@business_bp.route("/verify", methods=["POST"])
@login_required
@business_owner_required
def submit_verification():
    """Submit business verification documents."""
    if current_user.is_approved:
        flash("Your account is already approved.", "info")
        return redirect(url_for("business.dashboard"))

    from modules.business.models import BusinessVerification
    verification = BusinessVerification.query.filter_by(user_id=current_user.id).first()
    
    permit_url = request.form.get("permit_document_url", "").strip()
    other_url = request.form.get("other_document_url", "").strip()
    
    permit_file = request.files.get("permit_document_file")
    other_file = request.files.get("other_document_file")
    
    if permit_file and permit_file.filename:
        uploaded_url = save_uploaded_file(permit_file, allowed_extensions={"png", "jpg", "jpeg", "pdf"})
        if uploaded_url:
            permit_url = uploaded_url
            
    if other_file and other_file.filename:
        uploaded_url = save_uploaded_file(other_file, allowed_extensions={"png", "jpg", "jpeg", "pdf"})
        if uploaded_url:
            other_url = uploaded_url
    
    if not permit_url:
        flash("Business permit document is required (URL or file upload).", "error")
        return redirect(url_for("business.dashboard"))
        
    if not verification:
        verification = BusinessVerification(
            user_id=current_user.id,
            permit_document_url=permit_url,
            other_document_url=other_url,
            status="pending"
        )
        db.session.add(verification)
    else:
        verification.permit_document_url = permit_url
        verification.other_document_url = other_url
        verification.status = "pending"
        verification.submitted_at = datetime.utcnow()
        
    db.session.commit()
    flash("Verification documents submitted successfully. Please wait for admin approval.", "success")
    return redirect(url_for("business.dashboard"))

@business_bp.route("/establishment/create", methods=["GET", "POST"])
@login_required
@approved_business_owner_required
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

        cover_image_url = None
        if "cover_image_file" in request.files and request.files["cover_image_file"].filename:
            cover_image_url = save_uploaded_file(request.files["cover_image_file"])

        logo_url = None
        if "logo_file" in request.files and request.files["logo_file"].filename:
            logo_url = save_uploaded_file(request.files["logo_file"])

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
            cover_image_url=cover_image_url,
            logo_url=logo_url,
            owner_id=current_user.id,
            status="pending",
        )

        amenities = request.form.getlist("amenities")
        establishment.amenities = amenities if amenities else None

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
@approved_business_owner_required
def edit_establishment():
    """Edit existing establishment."""
    establishment = _get_owner_establishment()
    if not establishment:
        return redirect(url_for("business.create_establishment"))

    if request.method == "POST":
        barangay_name = request.form.get("barangay")

        name = request.form.get("name", "").strip()
        valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
        if not valid:
            flash(f"Invalid name: {err}", "error")
            return redirect(url_for("business.edit_establishment"))

        description = request.form.get("description", "").strip()
        description = sanitize_html_input(description)
        valid, err = validate_string_input(description, max_length=2000, block_sql_injection=False)
        if not valid:
            flash(f"Invalid description: {err}", "error")
            return redirect(url_for("business.edit_establishment"))

        address = request.form.get("address", "").strip()
        valid, err = validate_string_input(address, min_length=1, max_length=300, block_sql_injection=True)
        if not valid:
            flash(f"Invalid address: {err}", "error")
            return redirect(url_for("business.edit_establishment"))

        try:
            latitude = float(request.form.get("latitude", 0))
            longitude = float(request.form.get("longitude", 0))
        except (TypeError, ValueError):
            flash("Invalid coordinates: latitude and longitude must be numbers", "error")
            return redirect(url_for("business.edit_establishment"))

        if not validate_coordinates(latitude, longitude):
            flash("Invalid coordinates: latitude must be between -90 and 90, longitude between -180 and 180", "error")
            return redirect(url_for("business.edit_establishment"))

        contact_number = request.form.get("contact_number", "").strip()
        if contact_number and not validate_phone(contact_number):
            flash("Invalid contact number: please enter a valid phone number", "error")
            return redirect(url_for("business.edit_establishment"))

        email = request.form.get("email", "").strip()
        if email and not validate_email_format(email):
            flash("Invalid email: please enter a valid email address", "error")
            return redirect(url_for("business.edit_establishment"))

        website = request.form.get("website", "").strip()
        if website:
            website = sanitize_url(website)
            if not website:
                flash("Invalid website URL", "error")
                return redirect(url_for("business.edit_establishment"))

        price_range = request.form.get("price_range", "").strip()
        if price_range and price_range not in ("budget", "moderate", "premium"):
            flash("Invalid price range: must be budget, moderate, or premium", "error")
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
        if "cover_image_file" in request.files and request.files["cover_image_file"].filename:
            establishment.cover_image_url = save_uploaded_file(request.files["cover_image_file"])

        if "logo_file" in request.files and request.files["logo_file"].filename:
            establishment.logo_url = save_uploaded_file(request.files["logo_file"])

        amenities = request.form.getlist("amenities")
        establishment.amenities = amenities if amenities else None

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

@business_bp.route("/rooms")
@login_required
@approved_business_owner_required
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
@approved_business_owner_required
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

    amenities = request.form.getlist("room_amenities")
    room.amenities = amenities if amenities else None

    images_raw = request.form.get("image_urls", "")
    image_urls = [url.strip() for url in images_raw.split(",") if url.strip()]
    room.image_urls = image_urls if image_urls else None

    db.session.add(room)
    db.session.commit()

    flash(f"Room '{room.name}' added successfully!", "success")
    return redirect(url_for("business.manage_rooms"))

@business_bp.route("/rooms/<int:room_id>/edit", methods=["POST"])
@login_required
@approved_business_owner_required
def edit_room(room_id):
    """Edit an existing room."""
    establishment = _get_owner_establishment()
    room = EstablishmentRoom.query.get_or_404(room_id)

    if not establishment or room.establishment_id != establishment.id:
        flash("Access denied.", "error")
        return redirect(url_for("business.dashboard"))

    name = request.form.get("name", "").strip()
    valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
    if not valid:
        flash(f"Invalid room name: {err}", "error")
        return redirect(url_for("business.manage_rooms"))

    description = request.form.get("description", "").strip()
    description = sanitize_html_input(description)
    valid, err = validate_string_input(description, max_length=1000, block_sql_injection=False)
    if not valid:
        flash(f"Invalid room description: {err}", "error")
        return redirect(url_for("business.manage_rooms"))

    price_raw = request.form.get("price_per_night")
    if price_raw:
        valid, price_val, err = validate_float(price_raw, min_value=0)
        if not valid:
            flash(f"Invalid price per night: {err}", "error")
            return redirect(url_for("business.manage_rooms"))
    else:
        price_val = None

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
@approved_business_owner_required
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

@business_bp.route("/menu")
@login_required
@approved_business_owner_required
def manage_menu():
    """List and manage menu items for restaurant/cafe."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Create your establishment first.", "warning")
        return redirect(url_for("business.create_establishment"))

    items = EstablishmentMenuItem.query.filter_by(establishment_id=establishment.id).order_by(
        EstablishmentMenuItem.category, EstablishmentMenuItem.name
    ).all()

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
@approved_business_owner_required
def add_menu_item():
    """Add a new menu item."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Create your establishment first.", "warning")
        return redirect(url_for("business.create_establishment"))

    name = request.form.get("name", "").strip()
    valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
    if not valid:
        flash(f"Invalid menu item name: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    description = request.form.get("description", "").strip()
    description = sanitize_html_input(description)
    valid, err = validate_string_input(description, max_length=1000, block_sql_injection=False)
    if not valid:
        flash(f"Invalid menu item description: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    price_raw = request.form.get("price")
    if price_raw:
        valid, price_val, err = validate_float(price_raw, min_value=0)
        if not valid:
            flash(f"Invalid price: {err}", "error")
            return redirect(url_for("business.manage_menu"))
    else:
        price_val = None

    category = request.form.get("category", "").strip()
    valid, err = validate_string_input(category, min_length=1, max_length=100, block_sql_injection=True)
    if not valid:
        flash(f"Invalid category: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    image_url = None
    if "image_file" in request.files and request.files["image_file"].filename:
        image_url = save_uploaded_file(request.files["image_file"])

    item = EstablishmentMenuItem(
        establishment_id=establishment.id,
        name=name,
        description=description,
        price=price_val,
        category=category,
        image_url=image_url,
        is_available=request.form.get("is_available") == "on",
        is_bestseller=request.form.get("is_bestseller") == "on",
    )

    db.session.add(item)
    db.session.commit()
    flash(f"Menu item '{item.name}' added!", "success")
    return redirect(url_for("business.manage_menu"))

@business_bp.route("/menu/<int:item_id>/edit", methods=["POST"])
@login_required
@approved_business_owner_required
def edit_menu_item(item_id):
    """Edit an existing menu item."""
    establishment = _get_owner_establishment()
    item = EstablishmentMenuItem.query.get_or_404(item_id)

    if not establishment or item.establishment_id != establishment.id:
        flash("Access denied.", "error")
        return redirect(url_for("business.dashboard"))

    name = request.form.get("name", "").strip()
    valid, err = validate_string_input(name, min_length=1, max_length=200, block_sql_injection=True)
    if not valid:
        flash(f"Invalid menu item name: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    description = request.form.get("description", "").strip()
    description = sanitize_html_input(description)
    valid, err = validate_string_input(description, max_length=1000, block_sql_injection=False)
    if not valid:
        flash(f"Invalid menu item description: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    price_raw = request.form.get("price")
    if price_raw:
        valid, price_val, err = validate_float(price_raw, min_value=0)
        if not valid:
            flash(f"Invalid price: {err}", "error")
            return redirect(url_for("business.manage_menu"))
    else:
        price_val = None

    category = request.form.get("category", "").strip()
    valid, err = validate_string_input(category, min_length=1, max_length=100, block_sql_injection=True)
    if not valid:
        flash(f"Invalid category: {err}", "error")
        return redirect(url_for("business.manage_menu"))

    item.name = name
    item.description = description
    item.price = price_val
    item.category = category
    
    if "image_file" in request.files and request.files["image_file"].filename:
        item.image_url = save_uploaded_file(request.files["image_file"])
        
    item.is_available = request.form.get("is_available") == "on"
    item.is_bestseller = request.form.get("is_bestseller") == "on"

    db.session.commit()
    flash(f"Menu item '{item.name}' updated!", "success")
    return redirect(url_for("business.manage_menu"))

@business_bp.route("/menu/<int:item_id>/delete", methods=["POST"])
@login_required
@approved_business_owner_required
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
@approved_business_owner_required
def view_reviews():
    """View reviews for the business owner's establishment."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Create your establishment first.", "warning")
        return redirect(url_for("business.create_establishment"))

    reviews = EstablishmentReview.query.filter_by(
        establishment_id=establishment.id,
        parent_id=None
    ).order_by(EstablishmentReview.created_at.desc()).all()

    return render_template(
        "business/reviews.html",
        establishment=establishment,
        reviews=reviews,
    )

@business_bp.route("/reviews/reply/<int:review_id>", methods=["POST"])
@login_required
@approved_business_owner_required
@limiter.limit("10 per minute")
def reply_to_review(review_id):
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Please create your establishment first.", "error")
        return redirect(url_for("business.create_establishment"))

    review = EstablishmentReview.query.get_or_404(review_id)
    if review.establishment_id != establishment.id:
        flash("Access denied. This review is not for your establishment.", "error")
        return redirect(url_for("business.view_reviews"))

    comment = request.form.get("comment", "").strip()
    if not comment:
        flash("Please provide a response comment.", "error")
        return redirect(url_for("business.view_reviews"))

    # Create the reply review record
    reply = EstablishmentReview(
        user_id=current_user.id,
        establishment_id=establishment.id,
        parent_id=review.id,
        comment=sanitize_html_input(comment),
        rating=None,  # Replies do not have ratings
        status="approved"  # Business owner responses are approved instantly
    )
    db.session.add(reply)
    db.session.commit()

    # Invalidate public caches for this establishment
    from utils.cache_helpers import cache_delete, invalidate_business_cache
    cache_delete(f"establishment_detail_module:{establishment.id}")
    invalidate_business_cache(establishment_id=establishment.id)

    flash("Response posted successfully!")
    return redirect(url_for("business.view_reviews"))

@business_bp.route("/browse")
@login_required
@approved_business_owner_required
def browse_peers():
    """Browse other approved establishments of the same type."""
    establishment = _get_owner_establishment()
    if not establishment:
        flash("Please create your establishment profile first to browse peers.", "info")
        return redirect(url_for("business.create_establishment"))

    type_labels = {
        "inn": "Inns & Lodges",
        "restaurant": "Restaurants",
        "cafe": "Cafés",
        "fastfood": "Fast Food Establishments"
    }
    type_label = type_labels.get(establishment.type, establishment.type.title() + "s")

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


# --- API Routes ---

@business_bp.route("/api")
@limiter.limit("20 per minute")
def api_list():
    """API endpoint to retrieve approved establishments with pagination."""
    logger.info("API endpoint /business/api called")

    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)

    est_type = request.args.get("type")
    price_range = request.args.get("price_range")
    barangay = request.args.get("barangay")
    user_lat = request.args.get("lat", type=float)
    user_lng = request.args.get("lng", type=float)
    radius = request.args.get("radius", 10, type=float)
    is_featured = request.args.get("is_featured")

    query = Establishment.query.filter(Establishment.status == "approved")

    if est_type and est_type != "all":
        query = query.filter(Establishment.type == est_type)
    if price_range:
        query = query.filter(Establishment.price_range == price_range)
    if barangay and barangay != "all":
        query = query.join(BarangayInfo).filter(BarangayInfo.name == barangay)
    if is_featured:
        query = query.filter(Establishment.is_featured == (is_featured.lower() == 'true'))

    paginated_establishments = query.paginate(page=page, per_page=per_page, error_out=False)

    result = []
    for est in paginated_establishments.items:
        est_dict = {
            "id": est.id,
            "name": est.name,
            "type": est.type,
            "description": est.description or "",
            "address": est.address or "",
            "latitude": est.latitude,
            "longitude": est.longitude,
            "contact_number": est.contact_number,
            "price_range": est.price_range,
            "rating_avg": est.rating_avg or 0,
            "review_count": est.review_count or 0,
            "cover_image_url": est.cover_image_url,
            "logo_url": est.logo_url,
            "amenities": est.amenities or [],
            "barangay": est.barangay.name if est.barangay else None,
        }

        if user_lat and user_lng:
            dist = _haversine_distance(user_lat, user_lng, est.latitude, est.longitude)
            est_dict["distance"] = round(dist, 2)

        result.append(est_dict)

    if user_lat and user_lng:
        result.sort(key=lambda x: x.get("distance", float("inf")))
        result = [e for e in result if e.get("distance", float("inf")) <= radius]

    response_data = {
        "establishments": result,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": paginated_establishments.total,
            "pages": paginated_establishments.pages,
            "has_next": paginated_establishments.has_next,
            "has_prev": paginated_establishments.has_prev,
        },
    }

    response = make_response(jsonify(response_data))
    response.headers["Cache-Control"] = "public, max-age=300"
    response.headers["Expires"] = (datetime.utcnow() + timedelta(minutes=5)).strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    return response


def _haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points using Haversine formula (returns km)."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
