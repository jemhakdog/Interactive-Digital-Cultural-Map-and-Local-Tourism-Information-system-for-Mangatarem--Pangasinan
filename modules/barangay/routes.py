import logging
import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from extensions import db, limiter
from flask_login import login_required, current_user
from models import User
from modules.analytics.utils import record_view
from .models import BarangayInfo
from modules.attractions.models import Attraction
from modules.events.models import Event
from modules.gallery.models import GalleryItem
from utils.file_helpers import save_uploaded_file, detect_media_type
from utils.security import (
    validate_string_input, 
    validate_coordinates, 
    sanitize_html_input, 
    sanitize_url
)

barangay_bp = Blueprint("barangay", __name__, url_prefix="/barangay")
logger = logging.getLogger(__name__)


# --- Public Routes ---

@barangay_bp.route("/")
def index():
    """Display directory of all barangays with active contributors."""
    logger.info("Barangays directory page accessed")
    record_view("page", page_name="barangays_list")

    cache_key = "public_barangays_list"
    redis = current_app.redis_client

    if redis:
        try:
            cached_data = redis.get(cache_key)
            if cached_data:
                return render_template("pagez/barangays.html", barangays=json.loads(cached_data))
        except Exception as e:
            logger.error(f"Redis cache fetch error: {e}")

    barangay_ids_query = (
        db.session.query(User.barangay_id)
        .filter(
            User.role == "contributor", User.is_approved, User.barangay_id.is_not(None)
        )
        .distinct()
        .all()
    )
    barangay_ids = [b[0] for b in barangay_ids_query]

    if not barangay_ids:
        return render_template("pagez/barangays.html", barangays=[])

    all_attractions = (
        db.session.query(
            Attraction.barangay_id, 
            Attraction.name, 
            Attraction.category, 
            Attraction.image_url, 
            Attraction.latitude, 
            Attraction.longitude
        )
        .filter(
            Attraction.barangay_id.in_(barangay_ids), 
            Attraction.status == "approved"
        )
        .all()
    )

    from collections import defaultdict
    barangay_data = defaultdict(list)
    for a in all_attractions:
        barangay_data[a.barangay_id].append(a)

    barangay_infos = (
        db.session.query(BarangayInfo.id, BarangayInfo.name)
        .filter(BarangayInfo.id.in_(barangay_ids))
        .all()
    )
    barangay_map = {b.id: b.name for b in barangay_infos}

    barangay_list = []
    for brgy_id in barangay_ids:
        attractions = barangay_data.get(brgy_id, [])
        name = barangay_map.get(brgy_id, "Unknown")
        image_url = next((a.image_url for a in attractions if a.image_url), None)

        latitude, longitude = 15.9949, 120.4869 
        if attractions:
            latitude = sum(a.latitude for a in attractions) / len(attractions)
            longitude = sum(a.longitude for a in attractions) / len(attractions)

        tags = sorted(list(set(a.category for a in attractions if a.category)))

        barangay_list.append(
            {
                "name": name,
                "image_url": image_url,
                "latitude": latitude,
                "longitude": longitude,
                "tags": tags,
                "attraction_count": len(attractions),
            }
        )

    barangay_list.sort(key=lambda x: x["name"])

    if redis:
        try:
            redis.set(cache_key, json.dumps(barangay_list), ex=3600)
        except Exception as e:
            logger.error(f"Redis cache set error: {e}")

    return render_template("pagez/barangays.html", barangays=barangay_list)

@barangay_bp.route("/<name>")
def profile(name):
    """Display a barangay's cultural and tourism profile page."""
    logger.info(f"Barangay profile page accessed for barangay '{name}'")
    record_view("page", page_name="barangay_profile")

    barangay_info = BarangayInfo.query.filter_by(name=name).first()
    barangay_id = barangay_info.id if barangay_info else None
    
    attractions = []
    events = []
    gallery_items = []

    if barangay_id:
        attractions = Attraction.query.filter_by(barangay_id=barangay_id, status="approved").all()
        events = (
            Event.query.filter_by(barangay_id=barangay_id, status="approved")
            .order_by(Event.date.asc())
            .all()
        )
        gallery_items = (
            GalleryItem.query.join(User, GalleryItem.user_id == User.id)
            .filter(User.barangay_id == barangay_id, GalleryItem.status == "approved")
            .order_by(GalleryItem.created_at.desc())
            .all()
        )

    center_latitude, center_longitude = 15.7890, 120.2856 
    map_assets = []
    coords_list = []

    for a in attractions:
        map_assets.append({
            "id": a.id,
            "name": a.name,
            "type": "attraction",
            "category": a.category,
            "description": a.description,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "image_url": a.image_url,
            "url": url_for('attractions.detail', id=a.id)
        })
        coords_list.append((a.latitude, a.longitude))

    for e in events:
        if e.latitude and e.longitude:
            map_assets.append({
                "id": e.id,
                "name": e.name,
                "type": "event",
                "category": e.category,
                "description": e.description,
                "latitude": e.latitude,
                "longitude": e.longitude,
                "image_url": e.image_url,
                "date": e.date.strftime('%B %d, %Y'),
                "url": "#" 
            })
            coords_list.append((e.latitude, e.longitude))

    if coords_list:
        center_latitude = sum(c[0] for c in coords_list) / len(coords_list)
        center_longitude = sum(c[1] for c in coords_list) / len(coords_list)

    return render_template(
        "pagez/barangay_profile.html",
        barangay_name=name,
        attractions=attractions,
        map_assets=map_assets,
        events=events,
        gallery_items=gallery_items,
        barangay_info=barangay_info,
        center_latitude=center_latitude,
        center_longitude=center_longitude,
    )

# --- Contributor Dashboard ---

@barangay_bp.route("/dashboard")
@login_required
def barangay_dashboard():
    """Display the barangay contributor dashboard."""
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    all_attractions = Attraction.query.filter_by(barangay_id=current_user.barangay_id).all()
    all_events = Event.query.filter_by(barangay_id=current_user.barangay_id).all()
    all_gallery = GalleryItem.query.filter_by(user_id=current_user.id).all()

    stats = {
        "total": len(all_attractions) + len(all_events),
        "approved": sum(1 for x in all_attractions + all_events if x.status == 'approved'),
        "pending": sum(1 for x in all_attractions + all_events if x.status == 'pending'),
        "rejected": sum(1 for x in all_attractions + all_events if x.status == 'rejected'),
        "gallery": len(all_gallery),
    }

    activity_items = []
    for attr in all_attractions:
        activity_items.append({'name': attr.name, 'type': 'Attraction', 'status': attr.status, 'date': attr.created_at, 'id': attr.id})
    for ev in all_events:
        activity_items.append({'name': ev.name, 'type': 'Event', 'status': ev.status, 'date': ev.created_at, 'id': ev.id})
    
    recent_activity = sorted(activity_items, key=lambda x: x['date'] if x['date'] else datetime.min, reverse=True)[:5]

    return render_template("barangay/dashboard.html", stats=stats, recent_activity=recent_activity)

# --- Contributor Profile Management ---

@barangay_bp.route("/profile", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_profile_manage():
    """Manage the barangay's cultural and tourism profile information."""
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    info = current_user.barangay
    if not info:
        flash("No barangay assigned to your account.", "error")
        return redirect(url_for("barangay.barangay_dashboard"))

    if request.method == "POST":
        fields = ["mission", "vision", "history", "cultural_assets", "traditions", "local_practices", "unique_features"]
        for field in fields:
            val = request.form.get(field, "")
            is_valid, err = validate_string_input(val, max_length=5000, block_sql_injection=True)
            if not is_valid:
                flash(f"Invalid {field}: {err}", "error")
                return redirect(url_for("barangay.barangay_profile_manage"))
            setattr(info, field, sanitize_html_input(val))
        
        if not info.user_id:
            info.user_id = current_user.id

        db.session.commit()
        flash("Barangay profile updated successfully!")
        return redirect(url_for("barangay.barangay_profile_manage"))

    return render_template("barangay/profile.html", info=info)

# --- Contributor Attraction CRUD ---

@barangay_bp.route("/attractions")
@login_required
def barangay_attractions():
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    attractions = Attraction.query.filter_by(barangay_id=current_user.barangay_id).order_by(Attraction.created_at.desc()).all()
    return render_template("barangay/attractions.html", attractions=attractions)

@barangay_bp.route("/attractions/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_add_attraction():
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    if request.method == "POST":
        name = request.form.get("name", "")
        description = request.form.get("description", "")
        category = request.form.get("category", "")
        lat_str = request.form.get("latitude", "")
        lng_str = request.form.get("longitude", "")

        is_valid, err = validate_string_input(name, max_length=200)
        if not is_valid:
            flash(f"Invalid name: {err}", "error")
            return redirect(url_for("barangay.barangay_add_attraction"))

        try:
            lat, lng = float(lat_str), float(lng_str)
            if not validate_coordinates(lat, lng):
                raise ValueError
        except (ValueError, TypeError):
            flash("Invalid coordinates.", "error")
            return redirect(url_for("barangay.barangay_add_attraction"))

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
        flash("Attraction submitted for approval!")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/add_attraction.html")

# --- Contributor Event CRUD ---

@barangay_bp.route("/events")
@login_required
def barangay_events():
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    events = Event.query.filter_by(barangay_id=current_user.barangay_id).order_by(Event.date.asc()).all()
    return render_template("barangay/events.html", events=events)

@barangay_bp.route("/events/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_add_event():
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        location = request.form.get("location", "")
        category = request.form.get("category", "")
        date_str = request.form.get("date", "")

        try:
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            flash("Invalid date format.", "error")
            return redirect(url_for("barangay.barangay_add_event"))

        image_url = request.form.get("image_url")
        if "image" in request.files:
            uploaded_url = save_uploaded_file(request.files["image"])
            if uploaded_url:
                image_url = uploaded_url

        event = Event(
            name=title,
            date=event_date,
            location=location,
            category=category,
            description=sanitize_html_input(description),
            image_url=image_url,
            barangay_id=current_user.barangay_id,
            user_id=current_user.id,
            status="pending",
        )
        db.session.add(event)
        db.session.commit()
        flash("Event submitted for approval!")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/add_event.html")

# --- Contributor Gallery CRUD ---

@barangay_bp.route("/gallery")
@login_required
def barangay_gallery():
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    gallery_items = GalleryItem.query.filter_by(user_id=current_user.id).order_by(GalleryItem.uploaded_at.desc()).all()
    return render_template("barangay/gallery.html", gallery_items=gallery_items)

@barangay_bp.route("/gallery/add", methods=["GET", "POST"])
@login_required
@limiter.limit("10 per minute")
def barangay_add_gallery():
    if current_user.role != "contributor":
        flash("Access denied.")
        return redirect(url_for("public.index"))

    if request.method == "POST":
        url = request.form.get("url")
        caption = request.form.get("caption", "")
        item_type = request.form.get("type", "photo")

        if "media_file" in request.files:
            uploaded_url = save_uploaded_file(request.files["media_file"])
            if uploaded_url:
                url = uploaded_url
                item_type = detect_media_type(request.files["media_file"].filename)

        if not url:
            flash("Please provide media.", "error")
            return redirect(url_for("barangay.barangay_add_gallery"))

        gallery_item = GalleryItem(
            type=item_type,
            url=sanitize_url(url),
            caption=sanitize_html_input(caption),
            user_id=current_user.id,
            status="pending",
        )
        db.session.add(gallery_item)
        db.session.commit()
        flash("Gallery item submitted for approval!")
        return redirect(url_for("barangay.barangay_dashboard"))

    return render_template("barangay/add_gallery.html")
