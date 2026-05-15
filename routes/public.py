from models import db, User, Attraction, Event, BarangayInfo
from modules.business.models import Establishment
from extensions import limiter
import os
from flask import Blueprint, render_template, request, url_for, current_app, make_response
from utils.logger_helper import log_entry, log_success
from utils.validators import validate_query_params
from modules.analytics.utils import record_view
import logging
from sqlalchemy import func
import json

public_bp = Blueprint("public", __name__)
logger = logging.getLogger(__name__)


@public_bp.route("/test-supabase")
def test_supabase():
    """
    Demonstrate using the Supabase Python client.
    """
    from flask import current_app
    supabase = current_app.supabase
    
    if not supabase:
        return "Supabase client not initialized. Check your environment variables.", 500
        
    try:
        # Using the same table name from the user's sample
        # Note: If 'todos' doesn't exist, this will error, but it demonstrates the API
        response = supabase.table('attraction').select("*").limit(5).execute()
        data = response.data
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500


@public_bp.route("/")
def index():
    """
    Render the home page with featured content.
    Optimized to use SQL-side random sampling and Redis caching.
    """
    logger.info("Home page accessed")
    record_view("page", page_name="home")

    featured_attractions = []
    featured_establishments = []
    redis = current_app.redis_client

    # Try to get from Cache
    if redis:
        try:
            cached_attr = redis.get("home_featured_attractions_v2")
            cached_est = redis.get("home_featured_establishments_v2")
            if cached_attr:
                featured_attractions = json.loads(cached_attr)
            if cached_est:
                featured_establishments = json.loads(cached_est)
        except Exception as e:
            logger.error(f"Redis cache error: {e}")

    # Fallback/Refresh
    if not featured_attractions:
        # Prioritize items marked with is_featured=True
        attractions = (
            Attraction.query.filter_by(status="approved")
            .order_by(Attraction.is_featured.desc(), func.random())
            .limit(6)
            .all()
        )
        featured_attractions = [a.to_dict() for a in attractions]
        if redis:
            redis.set("home_featured_attractions_v2", json.dumps(featured_attractions), ex=3600)

    if not featured_establishments:
        establishments = (
            Establishment.query.filter_by(status="approved")
            .order_by(Establishment.is_featured.desc(), func.random())
            .limit(6)
            .all()
        )
        featured_establishments = [e.to_dict() for e in establishments]
        if redis:
            redis.set("home_featured_establishments_v2", json.dumps(featured_establishments), ex=3600)

    return render_template(
        "pagez/index.html", 
        featured=featured_attractions,
        featured_establishments=featured_establishments
    )




@public_bp.route("/map")
def map_view():
    """
    Display the interactive map with all approved attractions.
    """
    logger.info("Interactive map page accessed")
    record_view("page", page_name="map")

    from utils.cache_helpers import cache_get, cache_set
    cache_key = "map_page_meta"
    
    # Try cache
    cached_meta = cache_get(cache_key)
    if cached_meta:
        return render_template(
            "pagez/map.html", 
            barangays=cached_meta["barangays"], 
            attractions_count=cached_meta["count"],
            mapbox_token=os.environ.get("mapbox_token", "")
        )

    # Get count of approved attractions for initial display
    attractions_count = Attraction.query.filter_by(status="approved").count()

    # Get unique barangays that have approved attractions
    barangays = (
        db.session.query(BarangayInfo.name)
        .join(Attraction, Attraction.barangay_id == BarangayInfo.id)
        .filter(Attraction.status == "approved")
        .distinct()
        .order_by(BarangayInfo.name)
        .all()
    )

    barangay_list = [b[0] for b in barangays]
    
    # Store in cache for 10 minutes
    cache_set(cache_key, {"barangays": barangay_list, "count": attractions_count}, ttl=600)

    logger.info("Map page loaded with attractions and barangays")
    return render_template(
        "pagez/map.html", 
        barangays=barangay_list, 
        attractions_count=attractions_count,
        mapbox_token=os.environ.get("mapbox_token", "")
    )


@public_bp.route("/v1/map")
def map_v2_view():
    """
    Display the version 2 interactive map with modern aesthetics.
    """
    logger.info("Interactive map v2 accessed")
    
    # Record view
    record_view("page", page_name="map_v2")
    
    # Get initial data
    attractions_count = Attraction.query.filter_by(status="approved").count()
    
    return render_template(
        "pagez/map_v2.html", 
        attractions_count=attractions_count,
        mapbox_token=os.environ.get("mapbox_token", "")
    )


@public_bp.route("/v1/events")
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


@public_bp.route("/v1/attractions/<int:id>")
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
    )


@public_bp.route("/v1/barangay")
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

    barangay_list.sort(key=lambda x: x["name"])
        
    return render_template(
        "pagez/barangays_v1.html", 
        barangays=barangay_list
    )




@public_bp.route("/search")
@limiter.limit("20 per minute")
@validate_query_params({
    'q': {'type': 'string', 'max_length': 200, 'required': False},
    'category': {'type': 'string', 'max_length': 50, 'required': False},
    'barangay': {'type': 'string', 'max_length': 50, 'required': False}
})
def search():
    """
    Unified search route for attractions, events, and barangays.
    Uses centralized validation via decorators.
    """
    log_entry("public", "search", args=request.args)
    
    query = request.args.get("q", "").strip().lower()
    category_filter = request.args.get("category", "all")
    barangay_filter = request.args.get("barangay", "all")

    from utils.cache_helpers import cache_get, cache_set
    
    # Only cache reasonable queries
    cache_key = None
    if len(query) <= 100:
        cache_key = f"search:{query}:{category_filter}:{barangay_filter}"
        cached_results = cache_get(cache_key)
        if cached_results:
            response = make_response(render_template(
                "pagez/search_results.html",
                **cached_results
            ))
            response.headers["X-Cache"] = "HIT"
            return response

    # Cache MISS - Execute queries
    # Start with base queries
    attractions_query = Attraction.query.filter_by(status="approved")
    events_query = Event.query.filter_by(status="approved")
    barangays_info_query = BarangayInfo.query

    # Apply Text Search if exists
    if query:
        search_terms = f"%{query}%"
        attractions_query = attractions_query.filter(
            (Attraction.name.ilike(search_terms))
            | (Attraction.description.ilike(search_terms))
            | (Attraction.category.ilike(search_terms))
        )
        events_query = events_query.filter(
            (Event.name.ilike(search_terms))
            | (Event.description.ilike(search_terms))
            | (Event.category.ilike(search_terms))
        )
        barangays_info_query = barangays_info_query.filter(
            BarangayInfo.name.ilike(search_terms)
        )

    # Apply Category Filter
    if category_filter and category_filter != "all":
        attractions_query = attractions_query.filter(
            Attraction.category == category_filter
        )
        events_query = events_query.filter(Event.category == category_filter)

    # Apply Barangay Filter
    if barangay_filter and barangay_filter != "all":
        attractions_query = attractions_query.join(BarangayInfo, Attraction.barangay_id == BarangayInfo.id).filter(
            BarangayInfo.name == barangay_filter
        )
        events_query = events_query.join(BarangayInfo, Event.barangay_id == BarangayInfo.id).filter(
            BarangayInfo.name == barangay_filter
        )
        barangays_info_query = barangays_info_query.filter(
            BarangayInfo.name == barangay_filter
        )

    # Execute queries
    attractions = attractions_query.all()
    events = events_query.all()
    barangays_info = (
        barangays_info_query.all()
        if query or (barangay_filter and barangay_filter != "all")
        else []
    )

    # Fetch unique options for dropdowns
    available_categories = (
        db.session.query(Attraction.category)
        .filter(Attraction.status == "approved")
        .distinct()
        .all()
    )
    event_categories = (
        db.session.query(Event.category)
        .filter(Event.status == "approved")
        .distinct()
        .all()
    )
    all_categories = sorted(
        list(
            set([c[0] for c in available_categories] + [c[0] for c in event_categories])
        )
    )

    available_barangays = (
        db.session.query(BarangayInfo.name)
        .join(Attraction, Attraction.barangay_id == BarangayInfo.id)
        .filter(Attraction.status == "approved")
        .distinct()
        .all()
    )
    all_barangays = sorted([b[0] for b in available_barangays if b[0] is not None])

    template_data = {
        "query": query,
        "attractions": attractions,
        "events": events,
        "barangays_info": barangays_info,
        "categories": all_categories,
        "barangays": all_barangays,
        "selected_category": category_filter,
        "selected_barangay": barangay_filter,
    }

    # Store in cache for 5 minutes if query is valid
    if cache_key:
        # Convert objects to dicts for caching
        serializable_data = {
            "query": query,
            "attractions": [a.to_dict() if hasattr(a, 'to_dict') else {'id': a.id, 'name': a.name} for a in attractions],
            "events": [e.to_dict() if hasattr(e, 'to_dict') else {'id': e.id, 'name': e.name} for e in events],
            "barangays_info": [b.to_dict() if hasattr(b, 'to_dict') else {'id': b.id, 'name': b.name} for b in barangays_info],
            "categories": all_categories,
            "barangays": all_barangays,
            "selected_category": category_filter,
            "selected_barangay": barangay_filter,
        }
        cache_set(cache_key, serializable_data, ttl=300)

    response = make_response(render_template(
        "pagez/search_results.html",
        **template_data
    ))
    response.headers["X-Cache"] = "MISS"
    return response


@public_bp.route("/routes")
def routes():
    """
    Display suggested tourism routes.

    Returns:
        Rendered routes template.
    """
    logger.info("Tourism routes page accessed")
    logger.info("Rendering routes.html")
    return render_template("pagez/routes.html")









@public_bp.route("/sitemap.xml")
def sitemap():
    """
    Generate a dynamic sitemap.xml for SEO.

    Lists all static pages, approved attractions, and active barangays.

    Returns:
        XML response containing the sitemap.
    """
    from datetime import datetime

    # host_url = "/".join(host_components[:3])  # e.g., http://localhost:5000

    pages = []
    import subprocess
    import os

    def get_last_commit_date():
        """
        Get the last commit date from git history.

        Attempts to read from the production source repository path first,
        then falls back to the current directory (for dev environment).
        Returns today's date if git command fails.
        """
        source_repo = "/home/GoMangatarem/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan"
        try:
            cmd = ["git", "log", "-1", "--format=%cd", "--date=iso"]

            # Check if production path exists
            if os.path.exists(source_repo):
                cmd = [
                    "git",
                    "-C",
                    source_repo,
                    "log",
                    "-1",
                    "--format=%cd",
                    "--date=iso",
                ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # The date comes back like "2023-10-27 10:00:00 +0000", verify/parse if needed
            # For simplicity, we just want the date part YYYY-MM-DD
            # Simple ISO date format from git log is usually YYYY-MM-DD HH:MM:SS +/-TZ
            return result.stdout.strip().split(" ")[0]
        except Exception:
            # Fallback to today's date if anything fails
            return datetime.now().date().isoformat()

    last_update = get_last_commit_date()

    # Static pages
    static_urls = [
        "public.index",
        "public.map_view",
        "events.index",
        "gallery.index",
        "public.routes",
        "barangay.index",
        "heritage.index",
    ]

    for url in static_urls:
        pages.append(
            {
                "loc": url_for(url, _external=True),
                "lastmod": last_update,
                "changefreq": "weekly",
                "priority": "0.8" if url == "pagez.index" else "0.5",
            }
        )

    # Dynamic pages: Attractions
    attractions = Attraction.query.filter_by(status="approved").all()
    for attraction in attractions:
        pages.append(
            {
                "loc": url_for(
                    "attractions.detail", id=attraction.id, _external=True
                ),
                "lastmod": attraction.created_at.date().isoformat()
                if attraction.created_at
                else last_update,
                "changefreq": "monthly",
                "priority": "0.6",
            }
        )

    # Dynamic pages: Barangays
    # Get unique barangays from users/attractions
    barangay_names = (
        db.session.query(User.barangay_id)
        .filter(
            User.role == "contributor", User.is_approved, User.barangay_id.is_not(None)
        )
        .distinct()
        .all()
    )

    for b in barangay_names:
        pages.append(
            {
                "loc": url_for("barangay.profile", name=b[0], _external=True),
                "lastmod": last_update,  # Ideally fetch latest update for barangay
                "changefreq": "weekly",
                "priority": "0.7",
            }
        )

    log_success("public", "sitemap", f"Sitemap generated with {len(pages)} pages")
    logger.info(f"Sitemap.xml generated with {len(pages)} total pages")

    sitemap_xml = render_template("sitemap.xml", pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


@public_bp.route("/google364b8336ce52ae86.html")
def verify_site():
    """
    Serve Google Search Console verification file.
    """
    log_entry("public", "verify_site")
    logger.info("Google Search Console verification file accessed")
    return render_template("google364b8336ce52ae86.html")


@public_bp.route("/robots.txt")
def robots():
    """
    Serve robots.txt file.
    """
    sitemap_url = url_for("public.sitemap", _external=True)

    robots_txt = f"""User-agent: *
Allow: /
Disallow: /admin/
Disallow: /barangay-admin/
Disallow: /user/
Disallow: /pull
Disallow: /pull/

Sitemap: {sitemap_url}
"""
    response = make_response(robots_txt)
    response.headers["Content-Type"] = "text/plain"
    return response


