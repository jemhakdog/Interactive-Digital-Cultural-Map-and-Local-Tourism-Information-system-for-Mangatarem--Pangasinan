from flask import Blueprint, render_template, jsonify, request
from models import db, User, Attraction, Event, GalleryItem, BarangayInfo, PageView
from flask_login import current_user
from extensions import limiter
from datetime import datetime
import logging

public_bp = Blueprint("public", __name__)
logger = logging.getLogger(__name__)


@public_bp.route("/")
def index():
    print("Host URL: ", request.host_url)
    """
    Render the home page with featured attractions.

    Displays the top 3 approved attractions as featured content.

    Returns:
        Rendered index template with featured attractions.
    """
    print(f"[PROGRESSIVE LOG] [public] > index > ENTRY")
    logger.info("Home page accessed")

    # Record view
    print(f"[PROGRESSIVE LOG] [public] > index > LOGIC: Recording view")
    record_view("page", page_name="home")

    # Get featured attractions (limit 3)
    print(f"[PROGRESSIVE LOG] [public] > index > QUERY: Fetching featured attractions")
    featured = Attraction.query.filter_by(status="approved").limit(3).all()

    print(
        f"[PROGRESSIVE LOG] [public] > index > SUCCESS: Displaying {len(featured)} featured attractions"
    )
    logger.info(f"Home page loaded with {len(featured)} featured attractions")

    print(f"[PROGRESSIVE LOG] [public] > index > RENDER: Rendering index.html")
    return render_template("public/index.html", featured=featured)


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
        print(f"[PROGRESSIVE LOG] [public] > record_view > ERROR: {e}")
        db.session.rollback()


@public_bp.route("/map")
def map_view():
    """
    Display the interactive map with all approved attractions.

    Provides a filterable map view showing all tourism spots and
    cultural attractions across Mangatarem's barangays.

    Returns:
        Rendered map template with list of barangays for filtering.
    """
    print(f"[PROGRESSIVE LOG] [public] > map_view > ENTRY")
    logger.info("Interactive map page accessed")

    # Get count of approved attractions for initial display
    print(
        f"[PROGRESSIVE LOG] [public] > map_view > QUERY: Counting approved attractions"
    )
    attractions_count = Attraction.query.filter_by(status="approved").count()

    # Record view
    record_view("page", page_name="map")

    # Get list of unique barangays from approved attractions for the filter
    print(f"[PROGRESSIVE LOG] [public] > map_view > QUERY: Fetching unique barangays")
    barangays = (
        db.session.query(Attraction.barangay)
        .filter(Attraction.status == "approved", Attraction.barangay != None)
        .distinct()
        .order_by(Attraction.barangay)
        .all()
    )

    barangay_list = [b[0] for b in barangays]

    print(
        f"[PROGRESSIVE LOG] [public] > map_view > SUCCESS: Map loaded with {attractions_count} attractions, {len(barangay_list)} barangays"
    )
    logger.info(
        f"Map page loaded with {attractions_count} attractions and {len(barangay_list)} barangays"
    )

    print(f"[PROGRESSIVE LOG] [public] > map_view > RENDER: Rendering map.html")
    return render_template(
        "public/map.html", barangays=barangay_list, attractions_count=attractions_count
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
    print(f"[PROGRESSIVE LOG] [public] > attraction_detail > ENTRY: id={id}")
    logger.info(f"Attraction detail page accessed for ID {id}")

    print(
        f"[PROGRESSIVE LOG] [public] > attraction_detail > QUERY: Fetching attraction ID {id}"
    )
    attraction = Attraction.query.get_or_404(id)
    # Record view
    record_view("attraction", item_id=id)

    print(
        f"[PROGRESSIVE LOG] [public] > attraction_detail > SUCCESS: Displaying attraction '{attraction.name}'"
    )
    logger.info(f"Showing attraction '{attraction.name}' (ID: {id})")

    print(
        f"[PROGRESSIVE LOG] [public] > attraction_detail > RENDER: Rendering detail.html"
    )
    return render_template("public/detail.html", attraction=attraction)


@public_bp.route("/events")
def events():
    """
    Display all approved events in chronological order.

    Shows upcoming and ongoing cultural events and festivals
    across all barangays.

    Returns:
        Rendered events template with list of events.
    """
    print(f"[PROGRESSIVE LOG] [public] > events > ENTRY")
    logger.info("Events page accessed")

    # Record view
    record_view("page", page_name="events")

    print(f"[PROGRESSIVE LOG] [public] > events > QUERY: Fetching approved events")
    events = Event.query.filter_by(status="approved").order_by(Event.date.asc()).all()

    print(
        f"[PROGRESSIVE LOG] [public] > events > SUCCESS: Displaying {len(events)} approved events"
    )
    logger.info(f"Events page loaded with {len(events)} approved events")

    print(f"[PROGRESSIVE LOG] [public] > events > RENDER: Rendering events.html")
    return render_template("public/events.html", events=events)


@public_bp.route("/gallery")
def gallery():
    """
    Display the photo and video gallery.

    Shows all approved gallery items (photos and videos) from
    barangay contributors, sorted by upload date (newest first).

    Returns:
        Rendered gallery template with approved media items.
    """
    print(f"[PROGRESSIVE LOG] [public] > gallery > ENTRY")
    logger.info("Gallery page accessed")

    # Record view
    record_view("page", page_name="gallery")

    print(
        f"[PROGRESSIVE LOG] [public] > gallery > QUERY: Fetching approved gallery items"
    )
    items = (
        GalleryItem.query.filter_by(status="approved")
        .order_by(GalleryItem.uploaded_at.desc())
        .all()
    )

    # Get list of unique barangays from approved gallery items for the filter
    print(
        f"[PROGRESSIVE LOG] [public] > gallery > QUERY: Fetching unique barangays for gallery"
    )
    barangays = (
        db.session.query(User.barangay)
        .join(GalleryItem)
        .filter(GalleryItem.status == "approved", User.barangay != None)
        .distinct()
        .order_by(User.barangay)
        .all()
    )

    barangay_list = [b[0] for b in barangays]

    print(
        f"[PROGRESSIVE LOG] [public] > gallery > SUCCESS: Gallery loaded with {len(items)} items from {len(barangay_list)} barangays"
    )
    logger.info(f"Gallery page loaded with {len(items)} approved items")

    print(f"[PROGRESSIVE LOG] [public] > gallery > RENDER: Rendering gallery.html")
    return render_template(
        "public/gallery.html", gallery_items=items, barangays=barangay_list
    )


@public_bp.route("/search")
@limiter.limit("20 per minute")
def search():
    """
    Search for attractions and events with advanced filtering.
    Args:
        q (str): The search query.
        category (str): Filter by category (Nature, Historical, etc.)
        barangay (str): Filter by barangay location.
    """
    print(
        f"[PROGRESSIVE LOG] [public] > search > ENTRY: q='{request.args.get('q', '')}', category='{request.args.get('category', '')}', barangay='{request.args.get('barangay', '')}'"
    )
    logger.info(f"Search page accessed with query: {request.args.get('q', '')}")

    query = request.args.get("q", "")
    category_filter = request.args.get("category", "")
    barangay_filter = request.args.get("barangay", "")

    # Start with base approved query
    print(
        f"[PROGRESSIVE LOG] [public] > search > QUERY: Initializing attractions and events base queries"
    )
    attractions_query = Attraction.query.filter_by(status="approved")
    events_query = Event.query.filter_by(status="approved")

    # Apply Text Search if exists
    if query:
        print(
            f"[PROGRESSIVE LOG] [public] > search > LOGIC: Applying text search for '{query}'"
        )
        attractions_query = attractions_query.filter(
            (Attraction.name.ilike(f"%{query}%"))
            | (Attraction.description.ilike(f"%{query}%"))
        )
        events_query = events_query.filter(
            (Event.title.ilike(f"%{query}%")) | (Event.description.ilike(f"%{query}%"))
        )

    # Apply Category Filter
    if category_filter and category_filter != "all":
        print(
            f"[PROGRESSIVE LOG] [public] > search > LOGIC: Applying category filter '{category_filter}'"
        )
        attractions_query = attractions_query.filter(
            Attraction.category == category_filter
        )
        events_query = events_query.filter(Event.category == category_filter)

    # Apply Barangay Filter
    if barangay_filter and barangay_filter != "all":
        print(
            f"[PROGRESSIVE LOG] [public] > search > LOGIC: Applying barangay filter '{barangay_filter}'"
        )
        attractions_query = attractions_query.filter(
            Attraction.barangay == barangay_filter
        )
        events_query = events_query.filter(Event.barangay == barangay_filter)

    print(f"[PROGRESSIVE LOG] [public] > search > QUERY: Executing filtered queries")
    attractions = attractions_query.all()
    events = events_query.all()

    # Fetch unique options for the filter dropdowns
    print(
        f"[PROGRESSIVE LOG] [public] > search > QUERY: Fetching filter context (categories, barangays)"
    )
    available_categories = db.session.query(Attraction.category).distinct().all()
    available_barangays = (
        db.session.query(Attraction.barangay)
        .filter(Attraction.barangay != None)
        .distinct()
        .all()
    )

    print(
        f"[PROGRESSIVE LOG] [public] > search > SUCCESS: Found {len(attractions)} attractions, {len(events)} events"
    )
    logger.info(
        f"Search results: {len(attractions)} attractions, {len(events)} events for query '{query}'"
    )

    print(
        f"[PROGRESSIVE LOG] [public] > search > RENDER: Rendering search_results.html"
    )
    return render_template(
        "public/search_results.html",
        query=query,
        attractions=attractions,
        events=events,
        categories=[c[0] for c in available_categories],
        barangays=[b[0] for b in available_barangays],
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
    print(f"[PROGRESSIVE LOG] [public] > routes > ENTRY")
    logger.info("Tourism routes page accessed")
    print(f"[PROGRESSIVE LOG] [public] > routes > RENDER: Rendering routes.html")
    return render_template("public/routes.html")


@public_bp.route("/barangays")
def barangays():
    """
    Display directory of all barangays with active contributors.

    Shows a list of barangays that have approved contributors,
    with representative images from their attractions.

    Returns:
        Rendered barangays directory template with barangay list.
    """
    print(f"[PROGRESSIVE LOG] [public] > barangays > ENTRY")
    logger.info("Barangays directory page accessed")

    # Record view
    record_view("page", page_name="barangays_list")

    # Get list of barangays that have active contributors
    print(
        f"[PROGRESSIVE LOG] [public] > barangays > QUERY: Fetching list of approved contributors' barangays"
    )
    # We use a set to ensure uniqueness
    barangay_names = (
        db.session.query(User.barangay)
        .filter(
            User.role == "contributor", User.is_approved == True, User.barangay != None
        )
        .distinct()
        .all()
    )

    print(
        f"[PROGRESSIVE LOG] [public] > barangays > LOGIC: Processing metadata for {len(barangay_names)} barangays"
    )
    barangay_list = []
    for b in barangay_names:
        name = b[0]
        # Get all approved attractions for this barangay to calculate metadata
        attractions = Attraction.query.filter(
            Attraction.barangay == name, Attraction.status == "approved"
        ).all()

        # Find a representative image (first attraction with an image)
        image_url = None
        for attraction in attractions:
            if attraction.image_url:
                image_url = attraction.image_url
                break

        # Calculate center coordinates (centroid)
        lat = 15.9949  # Default
        lng = 120.4869  # Default
        if attractions:
            lat = sum(a.lat for a in attractions) / len(attractions)
            lng = sum(a.lng for a in attractions) / len(attractions)

        # Collect unique categories as tags
        tags = list(set(a.category for a in attractions))

        # Count attractions
        attraction_count = len(attractions)

        barangay_list.append(
            {
                "name": name,
                "image_url": image_url,
                "lat": lat,
                "lng": lng,
                "tags": tags,
                "attraction_count": attraction_count,
            }
        )

    # Sort by name
    barangay_list.sort(key=lambda x: x["name"])

    print(
        f"[PROGRESSIVE LOG] [public] > barangays > SUCCESS: Loaded {len(barangay_list)} barangays"
    )
    logger.info(f"Barangays directory page loaded with {len(barangay_list)} barangays")

    print(f"[PROGRESSIVE LOG] [public] > barangays > RENDER: Rendering barangays.html")
    return render_template("public/barangays.html", barangays=barangay_list)


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
    print(f"[PROGRESSIVE LOG] [public] > barangay_profile > ENTRY: name='{name}'")
    logger.info(f"Barangay profile page accessed for barangay '{name}'")

    # Record view
    record_view(
        "page", page_name="barangay_profile", item_id=None
    )  # We could count specific barangays if we had IDs

    # Get all approved content for this barangay
    print(
        f"[PROGRESSIVE LOG] [public] > barangay_profile > QUERY: Fetching attractions, events, gallery, and info for '{name}'"
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
    print(
        f"[PROGRESSIVE LOG] [public] > barangay_profile > LOGIC: Calculating map center"
    )
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
        f"[PROGRESSIVE LOG] [public] > barangay_profile > SUCCESS: Profile for '{name}' loaded ({len(attractions)} attractions, {len(events)} events)"
    )
    logger.info(
        f"Barangay profile for '{name}': {len(attractions)} attractions, {len(events)} events, {len(gallery_items)} gallery items"
    )

    print(
        f"[PROGRESSIVE LOG] [public] > barangay_profile > RENDER: Rendering barangay_profile.html"
    )
    return render_template(
        "public/barangay_profile.html",
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
    from datetime import datetime, timedelta

    host_components = url_for("public.index", _external=True).split("/")
    host_url = "/".join(host_components[:3])  # e.g., http://localhost:5000

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
        except Exception as e:
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
                "priority": "0.8" if url == "public.index" else "0.5",
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
            User.role == "contributor", User.is_approved == True, User.barangay != None
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
        f"[PROGRESSIVE LOG] [public] > sitemap > SUCCESS: Sitemap generated with {len(pages)} pages"
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
    print(f"[PROGRESSIVE LOG] [public] > verify_site > ENTRY")
    logger.info("Google Search Console verification file accessed")
    return render_template("google364b8336ce52ae86.html")


# @public_bp.route('/robots.txt')
# def robots():
#     """
#     Generate robots.txt configuration.

#     Returns:
#         Text response with robots.txt content.
#     """
#     from flask import make_response, url_for

#     sitemap_url = url_for('public.sitemap', _external=True)

#     robots_txt = f"""User-agent: *
# Allow: /
# Disallow: /admin/
# Disallow: /barangay-admin/
# Disallow: /pull
# Disallow: /pull/
# Sitemap: {sitemap_url}
# """
#     response = make_response(robots_txt)
#     response.headers["Content-Type"] = "text/plain"
#     return response
