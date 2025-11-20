from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, Attraction, Event, GalleryItem
from datetime import datetime
from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    # Admin only
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    stats = {
        'attractions': Attraction.query.count(),
        'events': Event.query.count(),
        'gallery': GalleryItem.query.count()
    }

    pending_users = User.query.filter_by(is_approved=False, role='contributor').all()
    pending_gallery = GalleryItem.query.filter_by(status='pending').all()
    
    return render_template('admin/dashboard.html', stats=stats, pending_users=pending_users, pending_gallery=pending_gallery)

@admin_bp.route('/users/approve/<int:id>')
@login_required
def approve_user(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
        
    user = User.query.get_or_404(id)
    user.is_approved = True
    db.session.commit()
    flash(f'User {user.username} approved!')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/users/reject/<int:id>')
@login_required
def reject_user(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
        
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} rejected and removed.')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/attractions')
@login_required
def admin_attractions():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    pending_attractions = Attraction.query.filter_by(status='pending').all()
    all_attractions = Attraction.query.order_by(Attraction.created_at.desc()).all()
    
    return render_template('admin/attractions.html', pending_attractions=pending_attractions, all_attractions=all_attractions)

@admin_bp.route('/events')
@login_required
def admin_events():
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    pending_events = Event.query.filter_by(status='pending').all()
    all_events = Event.query.order_by(Event.date.asc()).all()
    
    return render_template('admin/events.html', pending_events=pending_events, all_events=all_events)

@admin_bp.route('/attractions/approve/<int:id>')
@login_required
def approve_attraction(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    attraction = Attraction.query.get_or_404(id)
    attraction.status = 'approved'
    db.session.commit()
    flash(f'Attraction "{attraction.name}" approved!')
    return redirect(url_for('admin.admin_attractions'))

@admin_bp.route('/attractions/delete/<int:id>')
@login_required
def delete_attraction(id):
    attraction = Attraction.query.get_or_404(id)
    
    # Check permission
    if current_user.role != 'admin' and attraction.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    db.session.delete(attraction)
    db.session.commit()
    flash('Attraction deleted.')
    return redirect(url_for('admin.admin_attractions'))

@admin_bp.route('/attractions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_attraction(id):
    from flask import current_app
    
    attraction = Attraction.query.get_or_404(id)
    
    # Check permission
    if current_user.role != 'admin' and attraction.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
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
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                attraction.image_url = url_for('static', filename='uploads/' + filename)
        
        # Fallback to URL if provided and no file uploaded (or to update URL)
        if request.form.get('image_url'):
             attraction.image_url = request.form.get('image_url')

        # Reset status to pending if edited by contributor
        if current_user.role == 'contributor':
            attraction.status = 'pending'

        db.session.commit()
        flash('Attraction updated.')
        return redirect(url_for('admin.admin_attractions'))
        
    return render_template('admin/edit_attraction.html', attraction=attraction)

@admin_bp.route('/events/approve/<int:id>')
@login_required
def approve_event(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    event = Event.query.get_or_404(id)
    event.status = 'approved'
    db.session.commit()
    flash(f'Event "{event.title}" approved!')
    return redirect(url_for('admin.admin_events'))

@admin_bp.route('/events/reject/<int:id>')
@login_required
def reject_event(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash(f'Event "{event.title}" rejected and removed.')
    return redirect(url_for('admin.admin_events'))

@admin_bp.route('/gallery/approve/<int:id>')
@login_required
def approve_gallery(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    item = GalleryItem.query.get_or_404(id)
    item.status = 'approved'
    db.session.commit()
    flash('Gallery item approved!')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/gallery/reject/<int:id>')
@login_required
def reject_gallery(id):
    if current_user.role != 'admin':
        flash('Access denied.')
        return redirect(url_for('public.index'))
    
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Gallery item rejected and removed.')
    return redirect(url_for('admin.admin_dashboard'))

def allowed_file(filename):
    from flask import current_app
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
