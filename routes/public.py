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

    # Get count of approved attractions for initial display
    attractions_count = Attraction.query.filter_by(status="approved").count()

    # Record view
    record_view("page", page_name="map")

    # Get list of unique barangays from approved attractions for the filter
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

    logger.info(
        "Map page loaded with attractions and barangays"
    )
    return render_template(
        "pagez/map.html", 
        barangays=barangay_list, 
        attractions_count=attractions_count,
        mapbox_token=os.environ.get("mapbox_token", "")
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
    
    query = request.args.get("q", "").strip()
    category_filter = request.args.get("category", "")
    barangay_filter = request.args.get("barangay", "")

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

    # Apply Category Filter (only for attractions and events)
    if category_filter and category_filter != "all":
        attractions_query = attractions_query.filter(
            Attraction.category == category_filter
        )
        events_query = events_query.filter(Event.category == category_filter)
        # BarangayInfo doesn't have category, so we might hide/clear it when category filter is active
        if query and not (
            barangay_filter and barangay_filter != "all"
        ):  # Only clear if not filtering by barangay too
            pass

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

    # Fetch unique options for the filter dropdowns
    available_categories = (
        db.session.query(Attraction.category)
        .filter(Attraction.status == "approved")
        .distinct()
        .all()
    )
    # Also add event categories if different
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

    return render_template(
        "pagez/search_results.html",
        query=query,
        attractions=attractions,
        events=events,
        barangays_info=barangays_info,
        categories=all_categories,
        barangays=all_barangays,
        selected_category=category_filter,
        selected_barangay=barangay_filter,
    )


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


