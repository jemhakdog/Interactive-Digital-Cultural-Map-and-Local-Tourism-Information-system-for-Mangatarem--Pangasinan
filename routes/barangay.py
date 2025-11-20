from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Attraction, Event, GalleryItem, BarangayInfo
from datetime import datetime
from werkzeug.utils import secure_filename
import os

barangay_bp = Blueprint('barangay', __name__, url_prefix='/barangay')

@barangay_bp.route('/dashboard')
@login_required
def barangay_dashboard():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    stats = {
        'attractions': Attraction.query.filter_by(user_id=current_user.id).count(),
        'events': Event.query.filter_by(user_id=current_user.id).count(),
        'gallery': GalleryItem.query.filter_by(user_id=current_user.id).count()
    }
    
    return render_template('barangay/dashboard.html', stats=stats)

@barangay_bp.route('/attractions')
@login_required
def barangay_attractions():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    attractions = Attraction.query.filter_by(user_id=current_user.id).order_by(Attraction.created_at.desc()).all()
    return render_template('barangay/attractions.html', attractions=attractions)

@barangay_bp.route('/events')
@login_required
def barangay_events():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.date.asc()).all()
    return render_template('barangay/events.html', events=events)

@barangay_bp.route('/gallery')
@login_required
def barangay_gallery():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    gallery_items = GalleryItem.query.filter_by(user_id=current_user.id).order_by(GalleryItem.uploaded_at.desc()).all()
    return render_template('barangay/gallery.html', gallery_items=gallery_items)

@barangay_bp.route('/attractions/add', methods=['GET', 'POST'])
@login_required
def barangay_add_attraction():
    from flask import current_app
    
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
        
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
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
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/add_attraction.html')

@barangay_bp.route('/attractions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def barangay_edit_attraction(id):
    from flask import current_app
    
    attraction = Attraction.query.get_or_404(id)
    
    # Only allow editing own attractions
    if attraction.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay.barangay_dashboard'))
    
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
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                attraction.image_url = url_for('static', filename='uploads/' + filename)
        
        # Fallback to URL if provided and no file uploaded
        if request.form.get('image_url') and not ('image' in request.files and request.files['image'].filename):
            attraction.image_url = request.form.get('image_url')
        
        # Reset status to pending on edit
        attraction.status = 'pending'
        
        db.session.commit()
        flash('Attraction updated and submitted for approval.')
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/edit_attraction.html', attraction=attraction)

@barangay_bp.route('/attractions/delete/<int:id>')
@login_required
def barangay_delete_attraction(id):
    attraction = Attraction.query.get_or_404(id)
    
    # Only allow deleting own attractions
    if attraction.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay.barangay_dashboard'))
    
    db.session.delete(attraction)
    db.session.commit()
    flash('Attraction deleted.')
    return redirect(url_for('barangay.barangay_dashboard'))

@barangay_bp.route('/events/add', methods=['GET', 'POST'])
@login_required
def barangay_add_event():
    from flask import current_app
    
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
        
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
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
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/add_event.html')

@barangay_bp.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def barangay_edit_event(id):
    from flask import current_app
    
    event = Event.query.get_or_404(id)
    
    # Only allow editing own events
    if event.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay.barangay_dashboard'))
    
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
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                event.image_url = url_for('static', filename='uploads/' + filename)
        
        # Fallback to URL if provided and no file uploaded
        if request.form.get('image_url') and not ('image' in request.files and request.files['image'].filename):
            event.image_url = request.form.get('image_url')

        db.session.commit()
        
        # Reset status to pending on edit
        event.status = 'pending'
        db.session.commit()
        
        flash('Event updated and submitted for approval.')
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/edit_event.html', event=event)

@barangay_bp.route('/events/delete/<int:id>')
@login_required
def barangay_delete_event(id):
    event = Event.query.get_or_404(id)
    
    # Only allow deleting own events
    if event.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay.barangay_dashboard'))
    
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.')
    return redirect(url_for('barangay.barangay_dashboard'))

@barangay_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def barangay_profile_manage():
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
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
        return redirect(url_for('barangay.barangay_profile_manage'))
        
    return render_template('barangay/profile.html', info=info)

@barangay_bp.route('/gallery/add', methods=['GET', 'POST'])
@login_required
def barangay_add_gallery():
    from flask import current_app
    
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
        
    if request.method == 'POST':
        url = request.form.get('url')
        item_type = request.form.get('type', 'photo')
        
        # Handle file upload
        if 'media_file' in request.files:
            file = request.files['media_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                url = url_for('static', filename='uploads/' + filename)
                
                # Automatically detect type based on file extension
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in ['mp4', 'avi', 'mov', 'wmv']:
                    item_type = 'video'
                else:
                    item_type = 'photo'
        
        if not url:
            flash('Please provide a media file or URL.')
            return redirect(url_for('barangay.barangay_add_gallery'))
        
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
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/add_gallery.html')

@barangay_bp.route('/gallery/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def barangay_edit_gallery(id):
    from flask import current_app
    
    gallery_item = GalleryItem.query.get_or_404(id)
    
    # Only allow editing own gallery items
    if gallery_item.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay.barangay_dashboard'))
    
    if request.method == 'POST':
        gallery_item.caption = request.form.get('caption')
        
        # Handle file replacement
        if 'media_file' in request.files:
            file = request.files['media_file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
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
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/edit_gallery.html', gallery_item=gallery_item)

@barangay_bp.route('/gallery/delete/<int:id>')
@login_required
def barangay_delete_gallery(id):
    gallery_item = GalleryItem.query.get_or_404(id)
    
    # Only allow deleting own gallery items
    if gallery_item.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay.barangay_dashboard'))
    
    db.session.delete(gallery_item)
    db.session.commit()
    flash('Gallery item deleted.')
    return redirect(url_for('barangay.barangay_dashboard'))

def allowed_file(filename):
    from flask import current_app
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
