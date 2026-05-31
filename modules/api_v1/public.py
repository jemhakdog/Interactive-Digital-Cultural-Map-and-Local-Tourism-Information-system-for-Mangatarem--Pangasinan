import os
import logging
from flask import Blueprint, render_template, current_app
from models import db, User, Attraction, Event, BarangayInfo, UserFavoriteAttraction
from utils.logger_helper import log_entry
from modules.analytics.utils import record_view
import json

public_v1_bp = Blueprint("public_v1", __name__, url_prefix="/v1")
logger = logging.getLogger(__name__)


@public_v1_bp.route("/map")
def map_v2_view():
    """
    Display the version 2 interactive map with modern aesthetics.
    """
    logger.info("Interactive map v2 accessed")
    
    # Record view
    record_view("page", page_name="map_v2")
    
    # Get initial data
    attractions_count = Attraction.query.filter_by(status="approved").count()
    
    checked_in_today_attractions = []
    checked_in_today_establishments = []
    
    from flask_login import current_user
    if current_user.is_authenticated:
        from modules.gamification.models import TouristCheckIn
        from datetime import datetime
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_checkins = TouristCheckIn.query.filter(
            TouristCheckIn.user_id == current_user.id,
            TouristCheckIn.verified_at >= today_start
        ).all()
        checked_in_today_attractions = [c.attraction_id for c in today_checkins if c.attraction_id]
        checked_in_today_establishments = [c.establishment_id for c in today_checkins if c.establishment_id]
    
    return render_template(
        "pagez/map_v2.html", 
        attractions_count=attractions_count,
        mapbox_token=os.environ.get("mapbox_token", ""),
        checked_in_today_attractions=checked_in_today_attractions,
        checked_in_today_establishments=checked_in_today_establishments
    )


@public_v1_bp.route("/map-dashboard")
def map_dashboard_view():
    """
    Display the dark-themed desktop Map Dashboard (Map V3).
    """
    logger.info("Interactive Map Dashboard accessed")
    record_view("page", page_name="map_dashboard")
    
    # Get data for widgets
    from modules.heritage.models import HeritageProfile
    from modules.business.models import Establishment
    
    attractions_count = Attraction.query.filter_by(status="approved").count()
    heritage_count = HeritageProfile.query.filter_by(status="approved").count()
    events_count = Event.query.filter_by(status="approved").count()
    est_count = Establishment.query.filter_by(status="approved").count()
    
    # Recent elements
    recent_attractions = Attraction.query.filter_by(status="approved").order_by(Attraction.created_at.desc()).limit(4).all()
    
    return render_template(
        "pagez/map_dashboard.html",
        attractions_count=attractions_count,
        heritage_count=heritage_count,
        events_count=events_count,
        est_count=est_count,
        recent_attractions=recent_attractions,
        mapbox_token=os.environ.get("mapbox_token", "")
    )


@public_v1_bp.route("/events")
def events_v2_view():
    """
    Display the version 2 events listing with premium mobile-first aesthetics.
    """
    logger.info("Events v2 listing accessed")
    
    # Record view
    record_view("page", page_name="events_v2")
    
    # Fetch approved events in chronological order
    events = Event.query.filter_by(status="approved").order_by(Event.date.asc()).all()
    
    return render_template(
        "pagez/events_v2.html", 
        events=events
    )


@public_v1_bp.route("/lgu-events")
def lgu_events_view():
    """
    Display the scraped LGU events from Mangatarem website.
    """
    logger.info("LGU Scraped Events listing accessed")
    record_view("page", page_name="lgu_events")
    
    events_path = os.path.join(current_app.root_path, 'data', 'scraped_events.json')
    scraped_events = []
    if os.path.exists(events_path):
        with open(events_path, 'r', encoding='utf-8') as f:
            try:
                scraped_events = json.load(f)
            except Exception as e:
                logger.error(f"Error parsing scraped events JSON: {e}")
                
    return render_template(
        "pagez/lgu_events.html", 
        events=scraped_events
    )


@public_v1_bp.route("/attractions/<int:id>")
def attraction_detail_v1_view(id):
    """
    Display detailed information about a specific attraction (modernized mobile-first design).
    """
    log_entry("public", "attraction_detail_v1", id=id)
    logger.info("Attraction detail v1 page accessed")

    from modules.auth.models import User
    from modules.gallery.models import GalleryItem
    from modules.business.models import Establishment
    from utils.cache_helpers import cache_get, cache_set

    logger.debug(f"Fetching attraction ID {id}")
    attraction = Attraction.query.get_or_404(id)
    
    # Record view
    record_view("attraction", item_id=id)

    # Check if favorited by current user
    is_favorite = False
    is_visited = False
    is_stamped_today = False
    stamp_metadata = {}
    is_active_route = False

    from flask import session
    from datetime import datetime
    from flask_login import current_user
    if current_user.is_authenticated:
        from models import VisitorLog
        is_favorite = UserFavoriteAttraction.query.filter_by(
            user_id=current_user.id, attraction_id=id
        ).first() is not None
        is_visited = VisitorLog.query.filter_by(
            visitor_user_id=current_user.id,
            target_type="attraction",
            target_id=id
        ).first() is not None

        # Check if checked in today
        from modules.gamification.models import TouristCheckIn
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        stamped_today_record = TouristCheckIn.query.filter(
            TouristCheckIn.user_id == current_user.id,
            TouristCheckIn.attraction_id == id,
            TouristCheckIn.verified_at >= today_start
        ).first()
        
        if stamped_today_record:
            is_stamped_today = True
            stamp_metadata = {
                "verified_at": stamped_today_record.verified_at.strftime("%I:%M %p"),
                "distance": round(stamped_today_record.distance_meters, 1) if stamped_today_record.distance_meters else None
            }
            
        # Check if active navigation route in session matches this attraction
        active_nav = session.get('active_nav')
        if active_nav and active_nav.get('type') == 'attraction' and int(active_nav.get('id')) == id:
            is_active_route = True

    cache_key = f"attraction_detail_v1:{id}"
    cached_data = cache_get(cache_key)
    
    if cached_data:
        # Template can handle dicts for nearby/gallery/establishments
        return render_template(
            "pagez/detail_v1.html",
            attraction=attraction,
            nearby=cached_data['nearby'],
            related_gallery=cached_data['related_gallery'],
            nearby_stay=cached_data['nearby_stay'],
            nearby_eat=cached_data['nearby_eat'],
            is_favorite=is_favorite,
            is_visited=is_visited,
            is_stamped_today=is_stamped_today,
            stamp_metadata=stamp_metadata,
            is_active_route=is_active_route,
        )

    # Cache MISS - Fetch data
    # Fetch nearby attractions (same barangay, approved, limit 3, excluding current)
    nearby_objs = (
        Attraction.query.filter(
            Attraction.barangay_id == attraction.barangay_id,
            Attraction.status == "approved",
            Attraction.id != attraction.id,
        )
        .limit(3)
        .all()
    )
    nearby = [n.to_dict() if hasattr(n, 'to_dict') else {'id': n.id, 'name': n.name, 'image_url': n.image_url} for n in nearby_objs]

    # Fetch related gallery items
    gallery_objs = (
        GalleryItem.query.join(User, GalleryItem.user_id == User.id)
        .filter(User.barangay_id == attraction.barangay_id, GalleryItem.status == "approved")
        .limit(6)
        .all()
    )
    related_gallery = [g.to_dict() if hasattr(g, 'to_dict') else {'id': g.id, 'url': g.url, 'caption': g.caption} for g in gallery_objs]

    # Fetch nearby establishments
    nearby_stay = []
    nearby_eat = []
    if attraction.latitude and attraction.longitude:
        from core.geo import haversine_distance
        all_establishments = Establishment.query.filter_by(status="approved").all()
        for est in all_establishments:
            dist = haversine_distance(
                attraction.latitude, attraction.longitude,
                est.latitude, est.longitude
            )
            if dist <= 5.0:  # 5km radius
                est_data = est.to_dict() if hasattr(est, 'to_dict') else {'id': est.id, 'name': est.name, 'type': est.type, 'image_url': est.image_url}
                est_data['_distance'] = round(dist, 1)
                if est.type == "inn":
                    nearby_stay.append(est_data)
                else:
                    nearby_eat.append(est_data)
                    
        nearby_stay.sort(key=lambda x: x.get('_distance', 999))
        nearby_eat.sort(key=lambda x: x.get('_distance', 999))
        nearby_stay = nearby_stay[:3]
        nearby_eat = nearby_eat[:3]

    # Store in cache for 15 minutes
    payload = {
        'nearby': nearby,
        'related_gallery': related_gallery,
        'nearby_stay': nearby_stay,
        'nearby_eat': nearby_eat
    }
    cache_set(cache_key, payload, ttl=900)

    return render_template(
        "pagez/detail_v1.html",
        attraction=attraction,
        nearby=nearby,
        related_gallery=related_gallery,
        nearby_stay=nearby_stay,
        nearby_eat=nearby_eat,
        is_favorite=is_favorite,
        is_visited=is_visited,
        is_stamped_today=is_stamped_today,
        stamp_metadata=stamp_metadata,
        is_active_route=is_active_route,
    )


@public_v1_bp.route("/barangay")
def barangays_v1_view():
    """
    Display the version 1 mobile-optimized barangay directory.
    Uses aggregated data from contributors and attractions.
    """
    logger.info("Barangay v1 listing accessed")
    record_view("page", page_name="barangays_v1")
    
    # Get all barangay IDs that have approved contributors
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
        return render_template("pagez/barangays_v1.html", barangays=[])

    # Fetch approved attractions for these barangays to derive images and tags
    all_attractions = (
        db.session.query(
            Attraction.barangay_id, 
            Attraction.name, 
            Attraction.category, 
            Attraction.image_url
        )
        .filter(
            Attraction.barangay_id.in_(barangay_ids), 
            Attraction.status == "approved"
        )
        .all()
    )

    from collections import defaultdict
    barangay_data_map = defaultdict(list)
    for a in all_attractions:
        barangay_data_map[a.barangay_id].append(a)

    barangay_infos = (
        db.session.query(BarangayInfo.id, BarangayInfo.name, BarangayInfo.image_url if hasattr(BarangayInfo, 'image_url') else db.literal(None).label('image_url'))
        .filter(BarangayInfo.id.in_(barangay_ids))
        .all()
    )
    
    barangay_list = []
    for brgy in barangay_infos:
        attractions = barangay_data_map.get(brgy.id, [])
        
        # Determine representative image: Use BarangayInfo image if exists, else first attraction image
        image_url = getattr(brgy, 'image_url', None)
        if not image_url and attractions:
            image_url = next((a.image_url for a in attractions if a.image_url), None)

        tags = sorted(list(set(a.category for a in attractions if a.category)))
        
        barangay_list.append({
            "name": brgy.name,
            "image_url": image_url,
            "tags": tags,
            "attraction_count": len(attractions),
        })
        print(barangay_list)

    barangay_list.sort(key=lambda x: x["name"])
        
    return render_template(
        "pagez/barangays_v1.html", 
        barangays=barangay_list
    )
