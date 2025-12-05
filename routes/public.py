from flask import Blueprint, render_template, jsonify
from models import db, User, Attraction, Event, GalleryItem, BarangayInfo

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """
    Render the home page with featured attractions.

    Displays the top 3 approved attractions as featured content.

    Returns:
        Rendered index template with featured attractions.
    """
    # Get featured attractions (limit 3)
    featured = Attraction.query.filter_by(status='approved').limit(3).all()
    return render_template('index.html', featured=featured)

@public_bp.route('/map')
def map_view():
    """
    Display the interactive map with all approved attractions.

    Provides a filterable map view showing all tourism spots and
    cultural attractions across Mangatarem's barangays.

    Returns:
        Rendered map template with list of barangays for filtering.
    """
    # Pass all approved attractions to the map
    attractions = Attraction.query.filter_by(status='approved').all()

    # Get list of unique barangays from approved attractions for the filter
    barangays = db.session.query(Attraction.barangay).filter(
        Attraction.status == 'approved',
        Attraction.barangay != None
    ).distinct().order_by(Attraction.barangay).all()

    barangay_list = [b[0] for b in barangays]

    return render_template('map.html', barangays=barangay_list)

@public_bp.route('/map1')
def map1_view():
    """
    Display the Google Maps version of the interactive map.

    Provides an alternative map view using Google Maps iframe 
    showing Mangatarem's tourism spots and cultural attractions.

    Returns:
        Rendered map1 template with list of barangays for filtering.
    """
    # Get list of unique barangays from approved attractions for the filter
    barangays = db.session.query(Attraction.barangay).filter(
        Attraction.status == 'approved',
        Attraction.barangay != None
    ).distinct().order_by(Attraction.barangay).all()

    barangay_list = [b[0] for b in barangays]

    return render_template('map1.html', barangays=barangay_list)

@public_bp.route('/attraction/<int:id>')
def attraction_detail(id):
    """
    Display detailed information about a specific attraction.

    Args:
        id: The ID of the attraction to display.

    Returns:
        Rendered detail template with attraction information.
    """
    attraction = Attraction.query.get_or_404(id)
    return render_template('detail.html', attraction=attraction)

@public_bp.route('/events')
def events():
    """
    Display all approved events in chronological order.

    Shows upcoming and ongoing cultural events and festivals
    across all barangays.

    Returns:
        Rendered events template with list of events.
    """
    events = Event.query.filter_by(status='approved').order_by(Event.date.asc()).all()
    return render_template('events.html', events=events)

@public_bp.route('/gallery')
def gallery():
    """
    Display the photo and video gallery.

    Shows all approved gallery items (photos and videos) from
    barangay contributors, sorted by upload date (newest first).

    Returns:
        Rendered gallery template with approved media items.
    """
    items = GalleryItem.query.filter_by(status='approved').order_by(GalleryItem.uploaded_at.desc()).all()

    # Get list of unique barangays from approved gallery items for the filter
    # We need to join with User table to get the barangay
    barangays = db.session.query(User.barangay).join(GalleryItem).filter(
        GalleryItem.status == 'approved',
        User.barangay != None
    ).distinct().order_by(User.barangay).all()

    barangay_list = [b[0] for b in barangays]

    return render_template('gallery.html', gallery_items=items, barangays=barangay_list)

@public_bp.route('/routes')
def routes():
    """
    Display suggested tourism routes.

    Returns:
        Rendered routes template.
    """
    return render_template('routes.html')

@public_bp.route('/barangays')
def barangays():
    """
    Display directory of all barangays with active contributors.

    Shows a list of barangays that have approved contributors,
    with representative images from their attractions.

    Returns:
        Rendered barangays directory template with barangay list.
    """
    # Get list of barangays that have active contributors
    # We use a set to ensure uniqueness
    barangay_names = db.session.query(User.barangay).filter(
        User.role == 'contributor',
        User.is_approved == True,
        User.barangay != None
    ).distinct().all()

    barangay_list = []
    for b in barangay_names:
        name = b[0]
        # Get all approved attractions for this barangay to calculate metadata
        attractions = Attraction.query.filter(
            Attraction.barangay == name,
            Attraction.status == 'approved'
        ).all()

        # Find a representative image (first attraction with an image)
        image_url = None
        for attraction in attractions:
            if attraction.image_url:
                image_url = attraction.image_url
                break

        # Calculate center coordinates (centroid)
        lat = 15.9949 # Default
        lng = 120.4869 # Default
        if attractions:
            lat = sum(a.lat for a in attractions) / len(attractions)
            lng = sum(a.lng for a in attractions) / len(attractions)

        # Collect unique categories as tags
        tags = list(set(a.category for a in attractions))

        # Count attractions
        attraction_count = len(attractions)

        barangay_list.append({
            'name': name,
            'image_url': image_url,
            'lat': lat,
            'lng': lng,
            'tags': tags,
            'attraction_count': attraction_count
        })

    # Sort by name
    barangay_list.sort(key=lambda x: x['name'])

    return render_template('barangays.html', barangays=barangay_list)

@public_bp.route('/barangay/<name>')
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
    # Get all approved content for this barangay
    attractions = Attraction.query.filter_by(barangay=name, status='approved').all()
    events = Event.query.filter_by(barangay=name, status='approved').order_by(Event.date.asc()).all()

    # For gallery, we need to join with User since GalleryItem doesn't have barangay field
    gallery_items = GalleryItem.query.join(User).filter(
        User.barangay == name,
        GalleryItem.status == 'approved'
    ).order_by(GalleryItem.uploaded_at.desc()).all()

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
        attractions_json.append({
            'id': a.id,
            'name': a.name,
            'category': a.category,
            'barangay': a.barangay,
            'description': a.description,
            'lat': a.lat,
            'lng': a.lng,
            'image_url': a.image_url
        })

    return render_template('barangay_profile.html',
                         barangay_name=name,
                         attractions=attractions,
                         attractions_json=attractions_json,
                         events=events,
                         gallery_items=gallery_items,
                         barangay_info=barangay_info,
                         center_lat=center_lat,
                         center_lng=center_lng)

@public_bp.route('/sitemap.xml')
def sitemap():
    """
    Generate a dynamic sitemap.xml for SEO.

    Lists all static pages, approved attractions, and active barangays.

    Returns:
        XML response containing the sitemap.
    """
    from flask import make_response, url_for
    from datetime import datetime, timedelta

    host_components = url_for('public.index', _external=True).split('/')
    host_url = '/'.join(host_components[:3]) # e.g., http://localhost:5000

    pages = []
    ten_days_ago = (datetime.now() - timedelta(days=10)).date().isoformat()

    # Static pages
    static_urls = [
        'public.index',
        'public.map_view',
        'public.events',
        'public.gallery',
        'public.routes',
        'public.barangays'
    ]

    for url in static_urls:
        pages.append({
            'loc': url_for(url, _external=True),
            'lastmod': ten_days_ago,
            'changefreq': 'weekly',
            'priority': '0.8' if url == 'public.index' else '0.5'
        })

    # Dynamic pages: Attractions
    attractions = Attraction.query.filter_by(status='approved').all()
    for attraction in attractions:
        pages.append({
            'loc': url_for('public.attraction_detail', id=attraction.id, _external=True),
            'lastmod': attraction.created_at.date().isoformat() if attraction.created_at else ten_days_ago,
            'changefreq': 'monthly',
            'priority': '0.6'
        })

    # Dynamic pages: Barangays
    # Get unique barangays from users/attractions
    barangay_names = db.session.query(User.barangay).filter(
        User.role == 'contributor',
        User.is_approved == True,
        User.barangay != None
    ).distinct().all()

    for b in barangay_names:
        pages.append({
            'loc': url_for('public.barangay_profile', name=b[0], _external=True),
            'lastmod': ten_days_ago, # Ideally fetch latest update for barangay
            'changefreq': 'weekly',
            'priority': '0.7'
        })

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response



@public_bp.route('/google364b8336ce52ae86.html')
def verify_site():
    """
    Serve Google Search Console verification file.

    This route provides the verification file required by Google Search Console
    to verify ownership of the website. This is necessary for accessing
    Google Search Console features and improving site visibility in search results.

    Returns:
        Rendered verification template file.
    """
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
