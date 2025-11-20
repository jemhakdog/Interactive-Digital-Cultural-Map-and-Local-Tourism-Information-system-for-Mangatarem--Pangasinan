from flask import Blueprint, render_template, jsonify
from models import db, User, Attraction, Event, GalleryItem, BarangayInfo

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    # Get featured attractions (limit 3)
    featured = Attraction.query.filter_by(status='approved').limit(3).all()
    return render_template('index.html', featured=featured)

@public_bp.route('/map')
def map_view():
    # Pass all approved attractions to the map
    attractions = Attraction.query.filter_by(status='approved').all()
    
    # Get list of unique barangays from approved attractions for the filter
    barangays = db.session.query(Attraction.barangay).filter(
        Attraction.status == 'approved',
        Attraction.barangay != None
    ).distinct().order_by(Attraction.barangay).all()
    
    barangay_list = [b[0] for b in barangays]
    
    return render_template('map.html', barangays=barangay_list)

@public_bp.route('/attraction/<int:id>')
def attraction_detail(id):
    attraction = Attraction.query.get_or_404(id)
    return render_template('detail.html', attraction=attraction)

@public_bp.route('/events')
def events():
    events = Event.query.filter_by(status='approved').order_by(Event.date.asc()).all()
    return render_template('events.html', events=events)

@public_bp.route('/gallery')
def gallery():
    items = GalleryItem.query.filter_by(status='approved').order_by(GalleryItem.uploaded_at.desc()).all()
    return render_template('gallery.html', gallery_items=items)

@public_bp.route('/routes')
def routes():
    return render_template('routes.html')

@public_bp.route('/barangays')
def barangays():
    # Get list of barangays that have active contributors
    # We use a set to ensure uniqueness
    barangays = db.session.query(User.barangay).filter(
        User.role == 'contributor', 
        User.is_approved == True,
        User.barangay != None
    ).distinct().all()
    
    # Convert list of tuples to list of strings
    barangay_list = [b[0] for b in barangays]
    return render_template('barangays.html', barangays=barangay_list)

@public_bp.route('/barangay/<name>')
def barangay_profile(name):
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
