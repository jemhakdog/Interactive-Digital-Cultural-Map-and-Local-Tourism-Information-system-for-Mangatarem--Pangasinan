from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Attraction, Event, GalleryItem, BarangayInfo
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import logging

barangay_bp = Blueprint('barangay', __name__, url_prefix='/barangay')
logger = logging.getLogger(__name__)

@barangay_bp.route('/dashboard')
@login_required
def barangay_dashboard():
    """
    Display the barangay contributor dashboard.
    
    Shows statistics of attractions, events, and gallery items
    created by the current contributor user.
    
    Returns:
        Rendered barangay dashboard template with contributor's content statistics.
    """
    print(f"=== BARANGAY: Dashboard accessed by {current_user.username} ===")
    logger.info(f"Barangay dashboard accessed by {current_user.username} ({current_user.barangay})")
    
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    stats = {
        'attractions': Attraction.query.filter_by(user_id=current_user.id).count(),
        'events': Event.query.filter_by(user_id=current_user.id).count(),
        'gallery': GalleryItem.query.filter_by(user_id=current_user.id).count()
    }
    
    print(f"=== BARANGAY: Dashboard loaded with {stats['attractions']} attractions, {stats['events']} events ===")
    logger.info(f"Dashboard stats for {current_user.username}: {stats['attractions']} attractions, {stats['events']} events, {stats['gallery']} gallery items")
    
    return render_template('barangay/dashboard.html', stats=stats)

@barangay_bp.route('/attractions')
@login_required
def barangay_attractions():
    """
    Display all attractions created by the current contributor.
    
    Shows a list of the contributor's attractions with their approval status.
    
    Returns:
        Rendered attractions management template.
    """
    print(f"=== BARANGAY: Attractions page accessed by {current_user.username} ===")
    logger.info(f"Barangay attractions page accessed by {current_user.username}")
    
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    attractions = Attraction.query.filter_by(user_id=current_user.id).order_by(Attraction.created_at.desc()).all()
    
    print(f"=== BARANGAY: Displaying {len(attractions)} attractions ===")
    logger.info(f"Loaded {len(attractions)} attractions for {current_user.username}")
    
    return render_template('barangay/attractions.html', attractions=attractions)

@barangay_bp.route('/events')
@login_required
def barangay_events():
    """
    Display all events created by the current contributor.
    
    Shows a list of the contributor's events with their approval status.
    
    Returns:
        Rendered events management template.
    """
    print(f"=== BARANGAY: Events page accessed by {current_user.username} ===")
    logger.info(f"Barangay events page accessed by {current_user.username}")
    
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.date.asc()).all()
    
    print(f"=== BARANGAY: Displaying {len(events)} events ===")
    logger.info(f"Loaded {len(events)} events for {current_user.username}")
    
    return render_template('barangay/events.html', events=events)

@barangay_bp.route('/gallery')
@login_required
def barangay_gallery():
    """
    Display all gallery items created by the current contributor.
    
    Shows a list of the contributor's gallery items with their approval status.
    
    Returns:
        Rendered gallery management template.
    """
    print(f"=== BARANGAY: Gallery page accessed by {current_user.username} ===")
    logger.info(f"Barangay gallery page accessed by {current_user.username}")
    
    if current_user.role != 'contributor':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    gallery_items = GalleryItem.query.filter_by(user_id=current_user.id).order_by(GalleryItem.uploaded_at.desc()).all()
    
    print(f"=== BARANGAY: Displaying {len(gallery_items)} gallery items ===")
    logger.info(f"Loaded {len(gallery_items)} gallery items for {current_user.username}")
    
    return render_template('barangay/gallery.html', gallery_items=gallery_items)

@barangay_bp.route('/attractions/add', methods=['GET', 'POST'])
@login_required
def barangay_add_attraction():
    """
    Add a new attraction for the barangay.
    
    Contributors can create new attractions with details, location, and images.
    All new attractions are submitted with 'pending' status for admin approval.
    
    Returns:
        GET: Rendered add attraction form.
        POST: Redirect to dashboard after successful submission.
    """
    print(f"=== BARANGAY: Add attraction form accessed by {current_user.username} ===")
    logger.info(f"Add attraction page accessed by {current_user.username}")
    
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
        
        print(f"=== BARANGAY: New attraction '{attraction.name}' submitted by {current_user.username} ===")
        logger.info(f"New attraction '{attraction.name}' submitted by {current_user.username} for approval")
        
        flash('Attraction submitted for approval!')
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/add_attraction.html')

@barangay_bp.route('/attractions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def barangay_edit_attraction(id):
    """
    Edit an existing attraction owned by the current contributor.
    
    Contributors can only edit their own attractions. After editing,
    the attraction status is reset to 'pending' for admin re-approval.
    
    Args:
        id: The ID of the attraction to edit.
    
    Returns:
        GET: Rendered edit attraction form.
        POST: Redirect to dashboard after successful update.
    """
    print(f"=== BARANGAY: Edit attraction ID {id} by {current_user.username} ===")
    logger.info(f"Edit attraction requested for ID {id} by {current_user.username}")
    
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
        
        print(f"=== BARANGAY: Attraction '{attraction.name}' updated by {current_user.username} ===")
        logger.info(f"Attraction '{attraction.name}' (ID: {id}) updated by {current_user.username} and resubmitted for approval")
        
        flash('Attraction updated and submitted for approval.')
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/edit_attraction.html', attraction=attraction)

@barangay_bp.route('/attractions/delete/<int:id>')
@login_required
def barangay_delete_attraction(id):
    """
    Delete an attraction owned by the current contributor.
    
    Contributors can only delete their own attractions.
    
    Args:
        id: The ID of the attraction to delete.
    
    Returns:
        Redirect to dashboard with confirmation message.
    """
    print(f"=== BARANGAY: Delete attraction ID {id} by {current_user.username} ===")
    logger.info(f"Delete attraction requested for ID {id} by {current_user.username}")
    
    attraction = Attraction.query.get_or_404(id)
    
    # Only allow deleting own attractions
    if attraction.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay.barangay_dashboard'))
    
    attraction_name = attraction.name
    db.session.delete(attraction)
    db.session.commit()
    
    print(f"=== BARANGAY: Attraction '{attraction_name}' deleted by {current_user.username} ===")
    logger.info(f"Attraction '{attraction_name}' (ID: {id}) deleted by {current_user.username}")
    
    flash('Attraction deleted.')
    return redirect(url_for('barangay.barangay_dashboard'))

@barangay_bp.route('/events/add', methods=['GET', 'POST'])
@login_required
def barangay_add_event():
    """
    Add a new event for the barangay.
    
    Contributors can create new events with details, dates, and images.
    All new events are submitted with 'pending' status for admin approval.
    
    Returns:
        GET: Rendered add event form.
        POST: Redirect to dashboard after successful submission.
    """
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
            category=request.form['category'],
            description=request.form['description'],
            image_url=image_url,
            barangay=current_user.barangay,
            user_id=current_user.id,
            status='pending'
        )
        db.session.add(event)
        db.session.commit()
        
        print(f"=== BARANGAY: New event '{event.title}' submitted by {current_user.username} ===")
        logger.info(f"New event '{event.title}' submitted by {current_user.username} for approval")
        
        flash('Event submitted for approval!')
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/add_event.html')

@barangay_bp.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def barangay_edit_event(id):
    """
    Edit an existing event owned by the current contributor.
    
    Contributors can only edit their own events. After editing,
    the event status is reset to 'pending' for admin re-approval.
    
    Args:
        id: The ID of the event to edit.
    
    Returns:
        GET: Rendered edit event form.
        POST: Redirect to dashboard after successful update.
    """
    print(f"=== BARANGAY: Edit event ID {id} by {current_user.username} ===")
    logger.info(f"Edit event requested for ID {id} by {current_user.username}")
    
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
        event.category = request.form['category']
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
        
        print(f"=== BARANGAY: Event '{event.title}' updated by {current_user.username} ===")
        logger.info(f"Event '{event.title}' (ID: {id}) updated by {current_user.username} and resubmitted for approval")
        
        flash('Event updated and submitted for approval.')
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/edit_event.html', event=event)

@barangay_bp.route('/events/delete/<int:id>')
@login_required
def barangay_delete_event(id):
    """
    Delete an event owned by the current contributor.
    
    Contributors can only delete their own events.
    
    Args:
        id: The ID of the event to delete.
    
    Returns:
        Redirect to dashboard with confirmation message.
    """
    print(f"=== BARANGAY: Delete event ID {id} by {current_user.username} ===")
    logger.info(f"Delete event requested for ID {id} by {current_user.username}")
    
    event = Event.query.get_or_404(id)
    
    # Only allow deleting own events
    if event.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay.barangay_dashboard'))
    
    event_title = event.title
    db.session.delete(event)
    db.session.commit()
    
    print(f"=== BARANGAY: Event '{event_title}' deleted by {current_user.username} ===")
    logger.info(f"Event '{event_title}' (ID: {id}) deleted by {current_user.username}")
    
    flash('Event deleted.')
    return redirect(url_for('barangay.barangay_dashboard'))

@barangay_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def barangay_profile_manage():
    """
    Manage the barangay's cultural and tourism profile information.
    
    Contributors can update their barangay's history, cultural assets,
    traditions, local practices, and unique features.
    
    Returns:
        GET: Rendered profile management form.
        POST: Redirect to profile page after successful update.
    """
    print(f"=== BARANGAY: Profile management accessed by {current_user.username} ===")
    logger.info(f"Barangay profile management page accessed by {current_user.username}")
    
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
        
        print(f"=== BARANGAY: Profile updated for {current_user.barangay} by {current_user.username} ===")
        logger.info(f"Barangay profile for {current_user.barangay} updated by {current_user.username}")
        
        flash('Barangay profile updated successfully!')
        return redirect(url_for('barangay.barangay_profile_manage'))
        
    return render_template('barangay/profile.html', info=info)

@barangay_bp.route('/gallery/add', methods=['GET', 'POST'])
@login_required
def barangay_add_gallery():
    """
    Add a new gallery item (photo or video) for the barangay.
    
    Contributors can upload media files or provide URLs. Media type is
    automatically detected. All items are submitted with 'pending' status.
    
    Returns:
        GET: Rendered add gallery form.
        POST: Redirect to dashboard after successful submission.
    """
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
        
        print(f"=== BARANGAY: New gallery item ({item_type}) submitted by {current_user.username} ===")
        logger.info(f"New gallery item (type: {item_type}) submitted by {current_user.username} for approval")
        
        flash('Gallery item submitted for approval!')
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/add_gallery.html')

@barangay_bp.route('/gallery/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def barangay_edit_gallery(id):
    """
    Edit an existing gallery item owned by the current contributor.
    
    Contributors can only edit their own gallery items. After editing,
    the item status is reset to 'pending' for admin re-approval.
    
    Args:
        id: The ID of the gallery item to edit.
    
    Returns:
        GET: Rendered edit gallery form.
        POST: Redirect to dashboard after successful update.
    """
    print(f"=== BARANGAY: Edit gallery item ID {id} by {current_user.username} ===")
    logger.info(f"Edit gallery item requested for ID {id} by {current_user.username}")
    
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
        
        print(f"=== BARANGAY: Gallery item (ID: {id}) updated by {current_user.username} ===")
        logger.info(f"Gallery item ID {id} updated by {current_user.username} and resubmitted for approval")
        
        flash('Gallery item updated and submitted for approval.')
        return redirect(url_for('barangay.barangay_dashboard'))
        
    return render_template('barangay/edit_gallery.html', gallery_item=gallery_item)

@barangay_bp.route('/gallery/delete/<int:id>')
@login_required
def barangay_delete_gallery(id):
    """
    Delete a gallery item owned by the current contributor.
    
    Contributors can only delete their own gallery items.
    
    Args:
        id: The ID of the gallery item to delete.
    
    Returns:
        Redirect to dashboard with confirmation message.
    """
    print(f"=== BARANGAY: Delete gallery item ID {id} by {current_user.username} ===")
    logger.info(f"Delete gallery item requested for ID {id} by {current_user.username}")
    
    gallery_item = GalleryItem.query.get_or_404(id)
    
    # Only allow deleting own gallery items
    if gallery_item.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('barangay.barangay_dashboard'))
    
    db.session.delete(gallery_item)
    db.session.commit()
    
    print(f"=== BARANGAY: Gallery item deleted by {current_user.username} ===")
    logger.info(f"Gallery item ID {id} deleted by {current_user.username}")
    
    flash('Gallery item deleted.')
    return redirect(url_for('barangay.barangay_dashboard'))

def allowed_file(filename):
    """
    Check if a file has an allowed extension.
    
    Args:
        filename: The name of the file to check.
    
    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    from flask import current_app
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
