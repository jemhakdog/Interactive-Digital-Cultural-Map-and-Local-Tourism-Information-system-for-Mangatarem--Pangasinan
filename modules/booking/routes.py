from flask import Blueprint, jsonify, request, render_template, abort
from flask_login import login_required, current_user
from extensions import db
from datetime import datetime
from .models import BookableAsset, BookingSlot, Reservation
from models import Attraction, HeritageProfile

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

@booking_bp.route('/api/availability/<int:asset_id>', methods=['GET'])
def get_availability(asset_id):
    """Fetch availability for a bookable asset."""
    asset = BookableAsset.query.get_or_404(asset_id)
    if asset.status != 'active':
        return jsonify({'error': 'Asset is not available for booking'}), 400
        
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({'error': 'Date parameter is required'}), 400
        
    try:
        query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format (YYYY-MM-DD)'}), 400
        
    slot = BookingSlot.query.filter_by(bookable_asset_id=asset.id, date=query_date).first()
    
    # If slot doesn't exist yet for this date, assume full daily capacity is available
    if not slot:
        available = asset.daily_capacity
    else:
        available = slot.available_capacity
        
    return jsonify({
        'asset_id': asset.id,
        'date': date_str,
        'available_capacity': available,
        'daily_capacity': asset.daily_capacity
    })

@booking_bp.route('/api/reserve', methods=['POST'])
@login_required
def reserve_slot():
    """Create a reservation."""
    data = request.json
    asset_id = data.get('asset_id')
    date_str = data.get('date')
    party_size = int(data.get('party_size', 1))
    contact = data.get('contact', '')
    
    if not asset_id or not date_str:
        return jsonify({'error': 'Asset ID and date are required'}), 400
        
    try:
        reserve_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
        
    asset = BookableAsset.query.get_or_404(asset_id)
    if asset.status != 'active':
        return jsonify({'error': 'Asset is not available for booking'}), 400
        
    # Get or create the slot for this date
    slot = BookingSlot.query.filter_by(bookable_asset_id=asset.id, date=reserve_date).first()
    if not slot:
        slot = BookingSlot(
            bookable_asset_id=asset.id,
            date=reserve_date,
            total_capacity=asset.daily_capacity,
            booked_count=0
        )
        db.session.add(slot)
        db.session.flush() # To get slot.id
        
    if slot.available_capacity < party_size:
        return jsonify({'error': 'Not enough capacity available for this date'}), 400
        
    # Create the reservation
    reservation = Reservation(
        user_id=current_user.id,
        booking_slot_id=slot.id,
        party_size=party_size,
        primary_contact=contact,
        status='pending' if asset.requires_approval else 'confirmed'
    )
    
    # Update slot count
    slot.booked_count += party_size
    
    db.session.add(reservation)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'reservation_id': reservation.id,
        'status': reservation.status,
        'qr_token': reservation.qr_code_token
    })

@booking_bp.route('/admin/dashboard')
@login_required
def dashboard():
    """Admin/Owner dashboard for managing bookings."""
    # If business_owner, show their attractions' bookings
    # If barangay_admin (contributor), show their barangay's heritage/attractions bookings
    # For now, let's just fetch reservations related to assets they own/manage
    
    reservations = []
    
    if current_user.role == 'admin':
        reservations = Reservation.query.order_by(Reservation.created_at.desc()).all()
    elif current_user.role == 'contributor' and current_user.barangay_id:
        # Fetch reservations for this barangay
        reservations = Reservation.query.join(BookingSlot).join(BookableAsset).outerjoin(Attraction, BookableAsset.attraction_id == Attraction.id).outerjoin(HeritageProfile, BookableAsset.heritage_profile_id == HeritageProfile.id).filter(
            (Attraction.barangay_id == current_user.barangay_id) | 
            (HeritageProfile.barangay_id == current_user.barangay_id)
        ).order_by(Reservation.created_at.desc()).all()
    elif current_user.role == 'business_owner':
        # Fetch reservations for attractions owned by this user
        reservations = Reservation.query.join(BookingSlot).join(BookableAsset).join(Attraction, BookableAsset.attraction_id == Attraction.id).filter(
            Attraction.user_id == current_user.id
        ).order_by(Reservation.created_at.desc()).all()
    else:
        abort(403)
        
    return render_template('admin/booking_management.html', reservations=reservations)

@booking_bp.route('/api/admin/update_status', methods=['POST'])
@login_required
def update_status():
    """Update reservation status (approve/reject/check-in)."""
    # Needs authorization checks in a real scenario to ensure this user owns the asset
    if current_user.role not in ['admin', 'contributor', 'business_owner']:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.json
    res_id = data.get('reservation_id')
    new_status = data.get('status')
    
    if not res_id or not new_status:
        return jsonify({'error': 'Missing parameters'}), 400
        
    reservation = Reservation.query.get_or_404(res_id)
    old_status = reservation.status
    
    if new_status not in ['pending', 'confirmed', 'cancelled', 'attended', 'no-show']:
        return jsonify({'error': 'Invalid status'}), 400
        
    # Handle capacity if it's being cancelled
    if new_status == 'cancelled' and old_status != 'cancelled':
        reservation.slot.booked_count -= reservation.party_size
    elif old_status == 'cancelled' and new_status != 'cancelled':
        # Reactivating
        if reservation.slot.available_capacity < reservation.party_size:
             return jsonify({'error': 'Not enough capacity to reactivate'}), 400
        reservation.slot.booked_count += reservation.party_size
        
    reservation.status = new_status
    db.session.commit()
    
    return jsonify({'success': True, 'new_status': new_status})
