from flask import Blueprint, render_template, request
from models import db, User, Attraction, Event, GalleryItem, BarangayInfo, PageView
from flask_login import current_user
from extensions import limiter
from datetime import datetime
import logging

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
    Render the home page with featured attractions.
    """
    logger.info("Home page accessed")

    # Record view
    record_view("page", page_name="home")

    # Get featured attractions (limit 3)
    featured = Attraction.query.filter_by(status="approved").limit(3).all()

    logger.info(f"Home page loaded with {len(featured)} featured attractions")
    return render_template("pagez/index.html", featured=featured)


def record_view(view_type, item_id=None, page_name=None):
    """
    Helper function to record a page view.
    """
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        view = PageView(
            view_type=view_type,
            item_id=item_id,
            page_name=page_name,
            user_id=user_id,
            timestamp=datetime.utcnow(),
        )
        db.session.add(view)
        db.session.commit()
    except Exception as e:
        # Silently fail to not disrupt user experience
        logger.error(f"Error recording view: {e}")
        db.session.rollback()


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
    barangays = (
        db.session.query(Attraction.barangay)
        .filter(Attraction.status == "approved", Attraction.barangay.is_not(None))
        .distinct()
        .order_by(Attraction.barangay)
        .all()
    )

    barangay_list = [b[0] for b in barangays]

    logger.info(
        f"Map page loaded with {attractions_count} attractions and {len(barangay_list)} barangays"
    )
    return render_template(
        "pagez/map.html", barangays=barangay_list, attractions_count=attractions_count
    )


@public_bp.route("/attraction/<int:id>")
def attraction_detail(id):
    """
    Display detailed information about a specific attraction.

    Args:
        id: The ID of the attraction to display.

    Returns:
        Rendered detail template with attraction information.
    """
    print(f"[PROGRESSIVE LOG] [pagez] > attraction_detail > ENTRY: id={id}")
    logger.info(f"Attraction detail page accessed for ID {id}")

    print(
        f"[PROGRESSIVE LOG] [pagez] > attraction_detail > QUERY: Fetching attraction ID {id}"
    )
    attraction = Attraction.query.get_or_404(id)
    # Record view
    record_view("attraction", item_id=id)

    # Fetch nearby attractions (same barangay, approved, limit 3, excluding current)
    nearby = (
        Attraction.query.filter(
            Attraction.barangay == attraction.barangay,
            Attraction.status == "approved",
            Attraction.id != attraction.id,
        )
        .limit(3)
        .all()
    )

    # Fetch related gallery items (if any, matching by barangay since we don't have direct link in GalleryItem)
    # Note: GalleryItem joins with User to check for barangay
    related_gallery = (
        GalleryItem.query.join(User)
        .filter(User.barangay == attraction.barangay, GalleryItem.status == "approved")
        .limit(6)
        .all()
    )

    print(
        f"[PROGRESSIVE LOG] [pagez] > attraction_detail > SUCCESS: Displaying attraction '{attraction.name}', Found {len(nearby)} nearby places"
    )
    logger.info(f"Showing attraction '{attraction.name}' (ID: {id})")

    print(
        "[PROGRESSIVE LOG] [pagez] > attraction_detail > RENDER: Rendering detail.html"
    )
    return render_template(
        "pagez/detail.html",
        attraction=attraction,
        nearby=nearby,
        related_gallery=related_gallery,
    )


@public_bp.route("/events")
def events():
    """
    Display all approved events in chronological order.

    Shows upcoming and ongoing cultural events and festivals
    across all barangays.

    Returns:
        Rendered events template with list of events.
    """
    print("[PROGRESSIVE LOG] [pagez] > events > ENTRY")
    logger.info("Events page accessed")

    # Record view
    record_view("page", page_name="events")

    print("[PROGRESSIVE LOG] [pagez] > events > QUERY: Fetching approved events")
    events = Event.query.filter_by(status="approved").order_by(Event.date.asc()).all()

    print(
        f"[PROGRESSIVE LOG] [pagez] > events > SUCCESS: Displaying {len(events)} approved events"
    )
    logger.info(f"Events page loaded with {len(events)} approved events")

    print("[PROGRESSIVE LOG] [pagez] > events > RENDER: Rendering events.html")
    return render_template("pagez/events.html", events=events)


@public_bp.route("/gallery")
def gallery():
    """
    Display the photo and video gallery.

    Shows all approved gallery items (photos and videos) from
    barangay contributors, sorted by upload date (newest first).

    Returns:
        Rendered gallery template with approved media items.
    """
    print("[PROGRESSIVE LOG] [pagez] > gallery > ENTRY")
    logger.info("Gallery page accessed")

    # Record view
    record_view("page", page_name="gallery")

    print(
        "[PROGRESSIVE LOG] [pagez] > gallery > QUERY: Fetching approved gallery items"
    )
    items = (
        GalleryItem.query.filter_by(status="approved")
        .order_by(GalleryItem.uploaded_at.desc())
        .all()
    )

    # Get list of unique barangays from approved gallery items for the filter
    print(
        "[PROGRESSIVE LOG] [pagez] > gallery > QUERY: Fetching unique barangays for gallery"
    )
    barangays = (
        db.session.query(User.barangay)
        .join(GalleryItem)
        .filter(GalleryItem.status == "approved", User.barangay is not None)
        .distinct()
        .order_by(User.barangay)
        .all()
    )

    barangay_list = [b[0] for b in barangays]

    print(
        f"[PROGRESSIVE LOG] [pagez] > gallery > SUCCESS: Gallery loaded with {len(items)} items from {len(barangay_list)} barangays"
    )
    logger.info(f"Gallery page loaded with {len(items)} approved items")

    print("[PROGRESSIVE LOG] [pagez] > gallery > RENDER: Rendering gallery.html")
    return render_template(
        "pagez/gallery.html", gallery_items=items, barangays=barangay_list
    )


@public_bp.route("/search")
@limiter.limit("20 per minute")
def search():
    """
    Search for attractions, events, and barangay info with advanced filtering.
    """
    print(
        f"[PROGRESSIVE LOG] [pagez] > search > ENTRY: q='{request.args.get('q', '')}', category='{request.args.get('category', '')}', barangay='{request.args.get('barangay', '')}'"
    )
    logger.info(f"Search page accessed with query: {request.args.get('q', '')}")

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
            (Event.title.ilike(search_terms))
            | (Event.description.ilike(search_terms))
            | (Event.category.ilike(search_terms))
        )
        barangays_info_query = barangays_info_query.filter(
            (BarangayInfo.barangay_name.ilike(search_terms))
            | (BarangayInfo.history.ilike(search_terms))
            | (BarangayInfo.cultural_assets.ilike(search_terms))
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
        attractions_query = attractions_query.filter(
            Attraction.barangay == barangay_filter
        )
        events_query = events_query.filter(Event.barangay == barangay_filter)
        barangays_info_query = barangays_info_query.filter(
            BarangayInfo.barangay_name == barangay_filter
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
        db.session.query(Attraction.barangay)
        .filter(Attraction.status == "approved", Attraction.barangay.is_not(None))
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


@public_bp.route("/barangays")
def barangays():
    """
    Display directory of all barangays with active contributors.
    """
    logger.info("Barangays directory page accessed")

    # Record view
    record_view("page", page_name="barangays_list")

    # Get list of barangays that have active contributors
    barangay_names_query = (
        db.session.query(User.barangay)
        .filter(
            User.role == "contributor", User.is_approved, User.barangay.is_not(None)
        )
        .distinct()
        .all()
    )
    barangay_names = [b[0] for b in barangay_names_query]

    if not barangay_names:
        return render_template("pagez/barangays.html", barangays=[])

    # Optimize: Fetch all relevant attractions in one query instead of a loop
    all_attractions = Attraction.query.filter(
        Attraction.barangay.in_(barangay_names), Attraction.status == "approved"
    ).all()

    # Group attractions by barangay
    from collections import defaultdict

    barangay_data = defaultdict(list)
    for a in all_attractions:
        barangay_data[a.barangay].append(a)

    barangay_list = []
    for name in barangay_names:
        attractions = barangay_data.get(name, [])

        # Find a representative image
        image_url = next((a.image_url for a in attractions if a.image_url), None)

        # Calculate center coordinates (centroid)
        lat, lng = 15.9949, 120.4869  # Default
        if attractions:
            lat = sum(a.lat for a in attractions) / len(attractions)
            lng = sum(a.lng for a in attractions) / len(attractions)

        # Collect unique categories as tags
        tags = list(set(a.category for a in attractions))

        barangay_list.append(
            {
                "name": name,
                "image_url": image_url,
                "lat": lat,
                "lng": lng,
                "tags": tags,
                "attraction_count": len(attractions),
            }
        )

    # Sort by name
    barangay_list.sort(key=lambda x: x["name"])

    logger.info(f"Barangays directory page loaded with {len(barangay_list)} barangays")
    return render_template("pagez/barangays.html", barangays=barangay_list)


@public_bp.route("/barangay/<name>")
def barangay_profile(name):
    """
    Display a barangay's cultural and tourism profile page.

    Shows all approved attractions, events, gallery items, and
    cultural information for a specific barangay.

    Args:
        name: The name of the barangay.

    Returns:
        Rendered barangay profile template with all content for the barangay.
    """
    print(f"[PROGRESSIVE LOG] [pagez] > barangay_profile > ENTRY: name='{name}'")
    logger.info(f"Barangay profile page accessed for barangay '{name}'")

    # Record view
    record_view(
        "page", page_name="barangay_profile", item_id=None
    )  # We could count specific barangays if we had IDs

    # Get all approved content for this barangay
    print(
        f"[PROGRESSIVE LOG] [pagez] > barangay_profile > QUERY: Fetching attractions, events, gallery, and info for '{name}'"
    )
    attractions = Attraction.query.filter_by(barangay=name, status="approved").all()
    events = (
        Event.query.filter_by(barangay=name, status="approved")
        .order_by(Event.date.asc())
        .all()
    )

    # For gallery, we need to join with User since GalleryItem doesn't have barangay field
    gallery_items = (
        GalleryItem.query.join(User)
        .filter(User.barangay == name, GalleryItem.status == "approved")
        .order_by(GalleryItem.uploaded_at.desc())
        .all()
    )

    # Get barangay info (cultural assets, traditions, etc.)
    barangay_info = BarangayInfo.query.filter_by(barangay_name=name).first()

    # Calculate center coordinates for map (average of all attraction coordinates)
    center_lat, center_lng = 15.9949, 120.4869  # Default: Mangatarem coordinates
    if attractions:
        center_lat = sum(a.lat for a in attractions) / len(attractions)
        center_lng = sum(a.lng for a in attractions) / len(attractions)

    # Convert attractions to dictionaries for JSON serialization
    attractions_json = []
    for a in attractions:
        attractions_json.append(
            {
                "id": a.id,
                "name": a.name,
                "category": a.category,
                "barangay": a.barangay,
                "description": a.description,
                "lat": a.lat,
                "lng": a.lng,
                "image_url": a.image_url,
            }
        )

    print(
        f"[PROGRESSIVE LOG] [pagez] > barangay_profile > SUCCESS: Profile for '{name}' loaded ({len(attractions)} attractions, {len(events)} events)"
    )
    logger.info(
        f"Barangay profile for '{name}': {len(attractions)} attractions, {len(events)} events, {len(gallery_items)} gallery items"
    )

    logger.info(f"Rendering barangay_profile.html")
    return render_template(
        "pagez/barangay_profile.html",
        barangay_name=name,
        attractions=attractions,
        attractions_json=attractions_json,
        events=events,
        gallery_items=gallery_items,
        barangay_info=barangay_info,
        center_lat=center_lat,
        center_lng=center_lng,
    )


@public_bp.route("/sitemap.xml")
def sitemap():
    """
    Generate a dynamic sitemap.xml for SEO.

    Lists all static pages, approved attractions, and active barangays.

    Returns:
        XML response containing the sitemap.
    """
    from flask import make_response, url_for
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
        "public.events",
        "public.gallery",
        "public.routes",
        "public.barangays",
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
                    "public.attraction_detail", id=attraction.id, _external=True
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
        db.session.query(User.barangay)
        .filter(
            User.role == "contributor", User.is_approved, User.barangay.is_not(None)
        )
        .distinct()
        .all()
    )

    for b in barangay_names:
        pages.append(
            {
                "loc": url_for("public.barangay_profile", name=b[0], _external=True),
                "lastmod": last_update,  # Ideally fetch latest update for barangay
                "changefreq": "weekly",
                "priority": "0.7",
            }
        )

    print(
        f"[PROGRESSIVE LOG] [pagez] > sitemap > SUCCESS: Sitemap generated with {len(pages)} pages"
    )
    logger.info(f"Sitemap.xml generated with {len(pages)} total pages")

    sitemap_xml = render_template("sitemap.xml", pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


@public_bp.route("/google364b8336ce52ae86.html")
def verify_site():
    """
    Serve Google Search Console verification file.

    This route provides the verification file required by Google Search Console
    to verify ownership of the website. This is necessary for accessing
    Google Search Console features and improving site visibility in search results.

    Returns:
        Rendered verification template file.
    """
    print(f"[PROGRESSIVE LOG] [pagez] > verify_site > ENTRY")
    logger.info("Google Search Console verification file accessed")
    return render_template("google364b8336ce52ae86.html")


@public_bp.route("/robots.txt")
def robots():
    """
    Generate robots.txt configuration.

    Returns:
        Text response with robots.txt content.
    """
    from flask import make_response, url_for

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
