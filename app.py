from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Attraction, Event, GalleryItem, BarangayInfo
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here' # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mangatarem.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def seed_database():
    # Check if attractions exist
    if Attraction.query.first() is None:
        data_path = os.path.join(app.root_path, 'data', 'attractions.json')
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                data = json.load(f)
                for item in data:
                    attraction = Attraction(
                        name=item['name'],
                        category=item['category'],
                        barangay=item.get('barangay'),
                        description=item['description'],
                        lat=item['lat'],
                        lng=item['lng'],
                        image_url=item['image'],
                        status='approved'
                    )
                    db.session.add(attraction)
            db.session.commit()
            print("Database seeded with attractions.")

    # Create default admin if not exists
    if User.query.filter_by(username='admin').first() is None:
        admin = User(username='admin', email='admin@example.com', role='admin', is_approved=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin created.")

    # Create default contributor (Barangay Rep) if not exists
    if User.query.filter_by(username='barangay').first() is None:
        contributor = User(username='barangay', email='barangay@example.com', role='contributor', barangay='Poblacion', is_approved=True)
        contributor.set_password('barangay123')
        db.session.add(contributor)
        db.session.commit()
        print("Default contributor created.")

@app.route('/')
def index():
    # Get featured attractions (limit 3)
    featured = Attraction.query.filter_by(status='approved').limit(3).all()
    return render_template('index.html', featured=featured)

@app.route('/map')
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

@app.route('/attraction/<int:id>')
def attraction_detail(id):
    attraction = Attraction.query.get_or_404(id)
    return render_template('detail.html', attraction=attraction)

@app.route('/events')
def events():
    events = Event.query.filter_by(status='approved').order_by(Event.date.asc()).all()
    return render_template('events.html', events=events)

@app.route('/gallery')
def gallery():
    items = GalleryItem.query.filter_by(status='approved').order_by(GalleryItem.uploaded_at.desc()).all()
    return render_template('gallery.html', gallery_items=items)

@app.route('/routes')
def routes():
    return render_template('routes.html')

@app.route('/api/attractions')
def api_attractions():
    attractions = Attraction.query.filter_by(status='approved').all()
    result = []
    for a in attractions:
        result.append({
            'id': a.id,
            'name': a.name,
            'category': a.category,
            'barangay': a.barangay,
            'description': a.description,
            'lat': a.lat,
            'lng': a.lng,
            'image': a.image_url,
            'rating': 4.5 # Placeholder rating until we implement reviews
        })
    return jsonify(result)

@app.route('/barangays')
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

@app.route('/barangay/<name>')
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

# Auth Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if user.role == 'contributor' and not user.is_approved:
                flash('Your account is pending approval by the admin.')
                return redirect(url_for('login'))
                
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        barangay = request.form.get('barangay')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already exists.')
            return redirect(url_for('register'))
            
        user = User(username=username, email=email, role='contributor', barangay=barangay, is_approved=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please wait for admin approval.')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Admin Routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Admin only
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    stats = {
        'attractions': Attraction.query.count(),
        'events': Event.query.count(),
        'gallery': GalleryItem.query.count()
    }

    pending_users = User.query.filter_by(is_approved=False, role='contributor').all()
    pending_gallery = GalleryItem.query.filter_by(status='pending').all()
    
    return render_template('admin/dashboard.html', stats=stats, pending_users=pending_users, pending_gallery=pending_gallery)

@app.route('/admin/users/approve/<int:id>')
@login_required
def approve_user(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
        
    user = User.query.get_or_404(id)
    user.is_approved = True
    db.session.commit()
    flash(f'User {user.username} approved!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users/reject/<int:id>')
@login_required
def reject_user(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
        
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} rejected and removed.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/attractions')
@login_required
def admin_attractions():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    pending_attractions = Attraction.query.filter_by(status='pending').all()
    all_attractions = Attraction.query.order_by(Attraction.created_at.desc()).all()
    
    return render_template('admin/attractions.html', pending_attractions=pending_attractions, all_attractions=all_attractions)

@app.route('/admin/events')
@login_required
def admin_events():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    pending_events = Event.query.filter_by(status='pending').all()
    all_events = Event.query.order_by(Event.date.asc()).all()
    
    return render_template('admin/events.html', pending_events=pending_events, all_events=all_events)

@app.route('/admin/attractions/add', methods=['GET', 'POST'])
@login_required
def add_attraction():
    if current_user.role != 'contributor':
        flash('Access denied. Admins cannot create content directly.')
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        
        # Handle Image Upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = url_for('static', filename='uploads/' + filename)

        # Determine status: Admin = approved, Contributor = pending
        status = 'approved' if current_user.role == 'admin' else 'pending'

        attraction = Attraction(
            name=request.form.get('name'),
            category=request.form.get('category'),
            description=request.form.get('description'),
            lat=float(request.form.get('lat')),
            lng=float(request.form.get('lng')),
            image_url=image_url,
            status=status,
            user_id=current_user.id
        )
        db.session.add(attraction)
        db.session.commit()
        
        if status == 'pending':
            flash('Attraction submitted for approval!')
        else:
            flash('Attraction added successfully!')
            
        return redirect(url_for('barangay_dashboard'))
        
    return render_template('admin/add_attraction.html')

from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/admin/attractions/approve/<int:id>')
@login_required
def approve_attraction(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    attraction = Attraction.query.get_or_404(id)
    attraction.status = 'approved'
    db.session.commit()
    flash(f'Attraction "{attraction.name}" approved!')
    return redirect(url_for('admin_attractions'))

@app.route('/admin/attractions/delete/<int:id>')
@login_required
def delete_attraction(id):
    attraction = Attraction.query.get_or_404(id)
    
    # Check permission
    if current_user.role != 'admin' and attraction.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('index'))
    
    db.session.delete(attraction)
    db.session.commit()
    flash('Attraction deleted.')
    return redirect(url_for('admin_attractions'))

@app.route('/admin/attractions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_attraction(id):
    attraction = Attraction.query.get_or_404(id)
    
    # Check permission
    if current_user.role != 'admin' and attraction.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        attraction.name = request.form.get('name')
        attraction.category = request.form.get('category')
        attraction.description = request.form.get('description')
        attraction.lat = float(request.form.get('lat'))
        attraction.lng = float(request.form.get('lng'))
        
        # Handle Image Upload
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                attraction.image_url = url_for('static', filename='uploads/' + filename)
        
        # Fallback to URL if provided and no file uploaded (or to update URL)
        if request.form.get('image_url'):
             attraction.image_url = request.form.get('image_url')

        # Reset status to pending if edited by contributor
        if current_user.role == 'contributor':
            attraction.status = 'pending'

        db.session.commit()
        flash('Attraction updated.')
        return redirect(url_for('admin_attractions'))
        
    return render_template('admin/edit_attraction.html', attraction=attraction)

@app.route('/admin/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    if current_user.role != 'contributor':
        flash('Access denied. Admins cannot create content directly.')
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = url_for('static', filename='uploads/' + filename)

        # Determine status: Admin = approved, Contributor = pending
        status = 'approved' if current_user.role == 'admin' else 'pending'

        event = Event(
            title=request.form.get('title'),
            description=request.form.get('description'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d'),
            location=request.form.get('location'),
            image_url=image_url,
            user_id=current_user.id,
            status=status
        )
        db.session.add(event)
        db.session.commit()
        
        if status == 'pending':
            flash('Event submitted for approval!')
        else:
            flash('Event added successfully!')
        return redirect(url_for('barangay_dashboard'))
        
    return render_template('admin/add_event.html')

@app.route('/admin/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    
    # Check permission
    if current_user.role != 'admin' and event.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        event.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        event.location = request.form.get('location')
        
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    
    # Check permission
    if current_user.role != 'admin' and event.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('index'))
    
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.')
    return redirect(url_for('admin_events'))

@app.route('/admin/events/approve/<int:id>')
@login_required
def approve_event(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    event = Event.query.get_or_404(id)
    event.status = 'approved'
    db.session.commit()
    flash(f'Event "{event.title}" approved!')
    return redirect(url_for('admin_events'))

@app.route('/admin/events/reject/<int:id>')
@login_required
def reject_event(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash(f'Event "{event.title}" rejected and removed.')
    return redirect(url_for('admin_events'))

# =========================
# BARANGAY ROUTES
# =========================

@app.route('/barangay/dashboard')
@login_required
def barangay_dashboard():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    stats = {
        'attractions': Attraction.query.filter_by(user_id=current_user.id).count(),
        'events': Event.query.filter_by(user_id=current_user.id).count(),
        'gallery': GalleryItem.query.filter_by(user_id=current_user.id).count()
    }
    
    return render_template('barangay/dashboard.html', stats=stats)

@app.route('/barangay/attractions')
@login_required
def barangay_attractions():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    attractions = Attraction.query.filter_by(user_id=current_user.id).order_by(Attraction.created_at.desc()).all()
    return render_template('barangay/attractions.html', attractions=attractions)

@app.route('/barangay/events')
@login_required
def barangay_events():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.date.asc()).all()
    return render_template('barangay/events.html', events=events)

@app.route('/barangay/gallery')
@login_required
def barangay_gallery():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    gallery_items = GalleryItem.query.filter_by(user_id=current_user.id).order_by(GalleryItem.uploaded_at.desc()).all()
    return render_template('barangay/gallery.html', gallery_items=gallery_items)

@app.route('/barangay/attractions/add', methods=['GET', 'POST'])
@login_required
def barangay_add_attraction():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = url_for('static', filename='uploads/' + filename)
        
        attraction = Attraction(
            name=request.form['name'],
            category=request.form['category'],
            description=request.form['description'],
            lat=float(request.form['lat']),
            lng=float(request.form['lng']),
            image_url=image_url,
            barangay=current_user.barangay,
            user_id=current_user.id,
            status='pending'
        )
        db.session.add(attraction)
        db.session.commit()
        flash('Attraction submitted for approval!')
        return redirect(url_for('barangay_dashboard'))
        
    return render_template('barangay/add_attraction.html')

@app.route('/barangay/attractions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def barangay_edit_attraction(id):
    attraction = Attraction.query.get_or_404(id)
    
    # Only allow editing own attractions
    if attraction.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay_dashboard'))
    
    if request.method == 'POST':
        attraction.name = request.form['name']
        attraction.category = request.form['category']
        attraction.description = request.form['description']
        attraction.lat = float(request.form['lat'])
        attraction.lng = float(request.form['lng'])
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                attraction.image_url = url_for('static', filename='uploads/' + filename)
        
        # Fallback to URL if provided and no file uploaded
        if request.form.get('image_url') and not ('image' in request.files and request.files['image'].filename):
            attraction.image_url = request.form.get('image_url')
        
        # Reset status to pending on edit
        attraction.status = 'pending'
        
        db.session.commit()
        flash('Attraction updated and submitted for approval.')
        return redirect(url_for('barangay_dashboard'))
        
    return render_template('barangay/edit_attraction.html', attraction=attraction)

@app.route('/barangay/attractions/delete/<int:id>')
@login_required
def barangay_delete_attraction(id):
    attraction = Attraction.query.get_or_404(id)
    
    # Only allow deleting own attractions
    if attraction.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay_dashboard'))
    
    db.session.delete(attraction)
    db.session.commit()
    flash('Attraction deleted.')
    return redirect(url_for('barangay_dashboard'))

@app.route('/barangay/events/add', methods=['GET', 'POST'])
@login_required
def barangay_add_event():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = url_for('static', filename='uploads/' + filename)
        
        event = Event(
            title=request.form['title'],
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            location=request.form['location'],
            description=request.form['description'],
            image_url=image_url,
            barangay=current_user.barangay,
            user_id=current_user.id,
            status='pending'
        )
        db.session.add(event)
        db.session.commit()
        flash('Event submitted for approval!')
        return redirect(url_for('barangay_dashboard'))
        
    return render_template('barangay/add_event.html')

@app.route('/barangay/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def barangay_edit_event(id):
    event = Event.query.get_or_404(id)
    
    # Only allow editing own events
    if event.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay_dashboard'))
    
    if request.method == 'POST':
        event.title = request.form['title']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        event.location = request.form['location']
        event.description = request.form['description']
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                event.image_url = url_for('static', filename='uploads/' + filename)
        
        # Fallback to URL if provided and no file uploaded
        if request.form.get('image_url') and not ('image' in request.files and request.files['image'].filename):
            event.image_url = request.form.get('image_url')

        db.session.commit()
        
        # Reset status to pending on edit
        event.status = 'pending'
        db.session.commit()
        
        flash('Event updated and submitted for approval.')
        return redirect(url_for('barangay_dashboard'))
        
    return render_template('barangay/edit_event.html', event=event)

@app.route('/barangay/events/delete/<int:id>')
@login_required
def barangay_delete_event(id):
    event = Event.query.get_or_404(id)
    
    # Only allow deleting own events
    if event.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay_dashboard'))
    
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.')
    return redirect(url_for('barangay_dashboard'))

@app.route('/barangay/profile', methods=['GET', 'POST'])
@login_required
def barangay_profile_manage():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    info = BarangayInfo.query.filter_by(barangay_name=current_user.barangay).first()
    
    if request.method == 'POST':
        if not info:
            info = BarangayInfo(barangay_name=current_user.barangay, user_id=current_user.id)
            db.session.add(info)
            
        info.history = request.form.get('history')
        info.cultural_assets = request.form.get('cultural_assets')
        info.traditions = request.form.get('traditions')
        info.local_practices = request.form.get('local_practices')
        info.unique_features = request.form.get('unique_features')
        
        db.session.commit()
        flash('Barangay profile updated successfully!')
        return redirect(url_for('barangay_profile_manage'))
        
    return render_template('barangay/profile.html', info=info)

# =========================
# BARANGAY GALLERY ROUTES
# =========================

@app.route('/barangay/gallery/add', methods=['GET', 'POST'])
@login_required
def barangay_add_gallery():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        url = request.form.get('url')
        item_type = request.form.get('type', 'photo')
        
        # Handle file upload
        if 'media_file' in request.files:
            file = request.files['media_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                url = url_for('static', filename='uploads/' + filename)
                
                # Automatically detect type based on file extension
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in ['mp4', 'avi', 'mov', 'wmv']:
                    item_type = 'video'
                else:
                    item_type = 'photo'
        
        if not url:
            flash('Please provide a media file or URL.')
            return redirect(url_for('barangay_add_gallery'))
        
        gallery_item = GalleryItem(
            type=item_type,
            url=url,
            caption=request.form.get('caption'),
            user_id=current_user.id,
            status='pending'
        )
        db.session.add(gallery_item)
        db.session.commit()
        flash('Gallery item submitted for approval!')
        return redirect(url_for('barangay_dashboard'))
        
    return render_template('barangay/add_gallery.html')

@app.route('/barangay/gallery/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def barangay_edit_gallery(id):
    gallery_item = GalleryItem.query.get_or_404(id)
    
    # Only allow editing own gallery items
    if gallery_item.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay_dashboard'))
    
    if request.method == 'POST':
        gallery_item.caption = request.form.get('caption')
        
        # Handle file replacement
        if 'media_file' in request.files:
            file = request.files['media_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                gallery_item.url = url_for('static', filename='uploads/' + filename)
                
                # Update type based on new file
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in ['mp4', 'avi', 'mov', 'wmv']:
                    gallery_item.type = 'video'
                else:
                    gallery_item.type = 'photo'
        
        # Fallback to URL if provided and no file uploaded
        if request.form.get('url') and not ('media_file' in request.files and request.files['media_file'].filename):
            gallery_item.url = request.form.get('url')
        
        db.session.commit()
        
        # Reset status to pending on edit
        gallery_item.status = 'pending'
        db.session.commit()
        
        flash('Gallery item updated and submitted for approval.')
        return redirect(url_for('barangay_dashboard'))
        
    return render_template('barangay/edit_gallery.html', gallery_item=gallery_item)

@app.route('/barangay/gallery/delete/<int:id>')
@login_required
def barangay_delete_gallery(id):
    gallery_item = GalleryItem.query.get_or_404(id)
    
    # Only allow deleting own gallery items
    if gallery_item.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay_dashboard'))
    
    db.session.delete(gallery_item)
    db.session.commit()
    flash('Gallery item deleted.')
    return redirect(url_for('barangay_dashboard'))

@app.route('/admin/gallery/approve/<int:id>')
@login_required
def approve_gallery(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    item = GalleryItem.query.get_or_404(id)
    item.status = 'approved'
    db.session.commit()
    flash('Gallery item approved!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/gallery/reject/<int:id>')
@login_required
def reject_gallery(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('index'))
    
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Gallery item rejected and removed.')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True)
