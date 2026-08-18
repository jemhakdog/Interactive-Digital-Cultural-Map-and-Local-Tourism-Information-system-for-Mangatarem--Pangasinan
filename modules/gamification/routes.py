"""
Routes for the Gamification Module.
Handles QR scanning, GPS location validation, badge unlocking, and merchant voucher generation.
"""

import math
import logging
from datetime import datetime
from sqlalchemy import insert
from flask import render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import login_required, current_user
from extensions import db, limiter
from . import gamification_bp
from .models import AchievementBadge, UserPassport, TouristCheckIn
from models import Attraction, Establishment

logger = logging.getLogger(__name__)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points
    on the Earth in meters using the Haversine formula.
    """
    R = 6371000.0 # Earth's radius in meters
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    
    return R * c



@gamification_bp.route("/scan/<type_>/<int:id_>")
@login_required
def scan_qr(type_, id_):
    """
    Renders the physical QR check-in scanner page.
    Automatically identifies target landmark or merchant spot.
    Security: Only accessible if they are actively navigating to this destination on the map.
    """
    # Active Navigation Guard
    active_nav = session.get('active_nav')
    if not active_nav or str(active_nav.get('id')) != str(id_) or active_nav.get('type') != type_:
        flash("Access Denied. You must start active navigation on the map to this destination to access check-in stamps.", "warning")
        return redirect(url_for("public_v1.map_v2_view", route_to=id_, type=type_))

    target_name = "Unknown Spot"
    if type_ == "attraction":
        spot = Attraction.query.get_or_404(id_)
        target_name = spot.name
    elif type_ == "establishment":
        spot = Establishment.query.get_or_404(id_)
        target_name = spot.name
    else:
        flash("Invalid QR code scanned.", "error")
        return redirect(url_for("public.index"))

    return render_template(
        "gamification/qr_scanner.html",
        target_type=type_,
        target_id=id_,
        target_name=target_name
    )


@gamification_bp.route("/api/start-navigation", methods=["POST"])
@login_required
def start_navigation():
    """
    Backend active navigation route lock.
    Enforces that stamp validation is only accessible during active navigation.
    """
    data = request.get_json() or {}
    target_id = data.get("id")
    target_type = data.get("type", "attraction")
    
    if not target_id:
        return jsonify({"success": False, "message": "Missing destination ID."}), 400
        
    session['active_nav'] = {
        "id": int(target_id),
        "type": target_type,
        "timestamp": datetime.utcnow().isoformat()
    }
    return jsonify({"success": True, "message": "Active navigation route locked in session."})


@gamification_bp.route("/api/stop-navigation", methods=["POST"])
@login_required
def stop_navigation():
    """
    Unlocks active navigation state upon exiting map directions.
    """
    session.pop('active_nav', None)
    return jsonify({"success": True, "message": "Active navigation route cleared."})



@gamification_bp.route("/api/checkin", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def verify_checkin():
    """
    GPS-validated QR Check-in Endpoint.
    Compares tourist browser coordinates vs. official target coordinates.
    Threshold constraint: 50 meters.
    """
    data = request.get_json() or {}
    target_type = data.get("type") # 'attraction' or 'establishment'
    target_id = data.get("id")
    user_lat = data.get("latitude")
    user_lon = data.get("longitude")

    if not all([target_type, target_id, user_lat, user_lon]):
        return jsonify({"success": False, "message": "Missing coordinates or spot details."}), 400

    try:
        user_lat = float(user_lat)
        user_lon = float(user_lon)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Coordinates must be numbers."}), 400

    # Get official coordinates
    target_lat = None
    target_lon = None
    spot_name = "Unknown"

    if target_type == "attraction":
        spot = Attraction.query.get(target_id)
        if spot:
            target_lat = spot.latitude
            target_lon = spot.longitude
            spot_name = spot.name
    elif target_type == "establishment":
        spot = Establishment.query.get(target_id)
        if spot:
            target_lat = spot.latitude
            target_lon = spot.longitude
            spot_name = spot.name

    if not target_lat or not target_lon:
        return jsonify({"success": False, "message": "Target landmark has no registered coordinates."}), 400

    # Haversine Geolocation Check-in Validation
    distance = haversine_distance(user_lat, user_lon, target_lat, target_lon)
    
    # 50-meter threshold
    MAX_THRESHOLD = 50.0
    if distance > MAX_THRESHOLD:
        return jsonify({
            "success": False,
            "message": f"Verification failed. You are {int(distance)}m away from '{spot_name}'. Must be within 50m to check in."
        }), 400

    # Check if user already checked in at this spot (soft UX check).
    existing = TouristCheckIn.query.filter_by(
        user_id=current_user.id,
        attraction_id=(target_id if target_type == "attraction" else None),
        establishment_id=(target_id if target_type == "establishment" else None),
    ).first()

    if existing:
        return jsonify({
            "success": True,
            "message": f"Welcome back! You already checked in at '{spot_name}' today.",
            "already_checked_in": True
        })

    # Atomically insert check-in. ON CONFLICT DO NOTHING prevents TOCTOU races:
    # even if two concurrent requests both pass the query above, only one insert succeeds.
    if target_type == "attraction":
        conflict_cols = ['user_id', 'attraction_id']
    else:
        conflict_cols = ['user_id', 'establishment_id']

    db.session.execute(
        insert(TouristCheckIn)
        .values(
            user_id=current_user.id,
            attraction_id=(target_id if target_type == "attraction" else None),
            establishment_id=(target_id if target_type == "establishment" else None),
            latitude=user_lat,
            longitude=user_lon,
            distance_meters=distance,
        )
        .on_conflict_do_nothing(index_elements=conflict_cols)
    )
    db.session.flush()

    # ---- Badge Unlock Logic ----
    unlocked_badges = []
    
    # Get all badges the user has NOT unlocked yet
    unlocked_badge_ids = [p.badge_id for p in current_user.passports]
    available_badges = AchievementBadge.query.filter(
        ~AchievementBadge.id.in_(unlocked_badge_ids) if unlocked_badge_ids else True
    ).all()

    # Get all checked in attraction and establishment IDs for this user
    visited_attraction_ids = {c.attraction_id for c in current_user.check_ins if c.attraction_id}
    
    for badge in available_badges:
        required_ids = badge.target_locations # list of required attraction IDs
        # Check if user has checked in to all required locations
        if required_ids and all(req_id in visited_attraction_ids for req_id in required_ids):
            # Unlock badge (ON CONFLICT prevents duplicate rewards from race conditions)
            db.session.execute(
                insert(UserPassport)
                .values(user_id=current_user.id, badge_id=badge.id)
                .on_conflict_do_nothing(index_elements=['user_id', 'badge_id'])
            )
            unlocked_badges.append({
                "title": badge.title,
                "description": badge.description,
                "badge_image_url": badge.badge_image_url,
                "reward_promo": badge.reward_promo
            })

    db.session.commit()
    logger.info(f"User '{current_user.username}' checked in at '{spot_name}'. Unlocked {len(unlocked_badges)} badges.")

    return jsonify({
        "success": True,
        "message": f"Stamp awarded! Checked in successfully at '{spot_name}'!",
        "distance": int(distance),
        "unlocked_badges": unlocked_badges
    })


@gamification_bp.route("/my-passport")
@login_required
def view_passport():
    """
    Renders the beautiful glassmorphic tourist passport dashboard,
    listing unlocked stamps, badge achievements, and LGU merchant coupon discounts.
    """
    # Fetch all badges
    badges = AchievementBadge.query.all()
    
    # Map unlocked badge IDs
    unlocked_badge_ids = {p.badge_id for p in current_user.passports}
    
    # Calculate progress percentages for locked badges
    visited_attraction_ids = {c.attraction_id for c in current_user.check_ins if c.attraction_id}
    
    badges_data = []
    unlocked_coupons = []
    
    for badge in badges:
        is_unlocked = badge.id in unlocked_badge_ids
        
        # Calculate progress
        req_ids = badge.target_locations or []
        completed_reqs = sum(1 for req_id in req_ids if req_id in visited_attraction_ids)
        total_reqs = len(req_ids)
        progress_pct = int((completed_reqs / total_reqs) * 100) if total_reqs > 0 else 0
        
        badges_data.append({
            "badge": badge,
            "is_unlocked": is_unlocked,
            "progress_pct": progress_pct,
            "completed_reqs": completed_reqs,
            "total_reqs": total_reqs
        })
        
        if is_unlocked and badge.reward_promo:
            unlocked_coupons.append({
                "badge_title": badge.title,
                "promo": badge.reward_promo
            })
            
    # Fetch recent check-ins
    recent_checkins = TouristCheckIn.query.filter_by(user_id=current_user.id).order_by(TouristCheckIn.verified_at.desc()).limit(5).all()

    return render_template(
        "gamification/passport_dashboard.html",
        badges_data=badges_data,
        unlocked_coupons=unlocked_coupons,
        recent_checkins=recent_checkins
    )

