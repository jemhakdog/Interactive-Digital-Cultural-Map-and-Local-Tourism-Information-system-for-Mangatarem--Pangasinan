from flask import Blueprint, jsonify, request, render_template, abort
from flask_login import login_required, current_user
from extensions import db
from modules.chat.models import ChatRoom, ChatMessage, ChatParticipant
from models import BarangayInfo, Establishment

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

@chat_bp.route('/', methods=['GET'])
@login_required
def chat_index():
    """
    Renders the main chat interface or returns a list of active rooms for the user.
    """
    # Fetch rooms the current user is a participant of
    participants = ChatParticipant.query.filter_by(user_id=current_user.id).all()
    room_ids = [p.chat_room_id for p in participants]
    rooms = ChatRoom.query.filter(ChatRoom.id.in_(room_ids)).all()
    
    # If API request, return JSON
    if request.headers.get('Accept') == 'application/json':
        room_data = []
        for r in rooms:
            name = f"Room {r.id}"
            if r.type == 'barangay' and r.barangay:
                name = f"{r.barangay.name} Community Hub"
            elif r.type == 'business' and r.establishment:
                name = r.establishment.name
            
            room_data.append({
                "id": r.id,
                "type": r.type,
                "name": name,
                "created_at": r.created_at.isoformat()
            })
        return jsonify({"status": "success", "rooms": room_data})
        
    return render_template('chat/index.html', rooms=rooms)

@chat_bp.route('/<int:room_id>', methods=['GET'])
@login_required
def chat_room(room_id):
    """
    Fetches the history of a specific chat room.
    """
    room = ChatRoom.query.get_or_404(room_id)
    
    # Simple Authorization check: User must be a participant or it must be a public barangay room
    is_participant = ChatParticipant.query.filter_by(chat_room_id=room_id, user_id=current_user.id).first()
    if not is_participant and room.type != 'barangay':
        abort(403, description="You are not authorized to view this private room.")
        
    # Pagination for historical messages
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    messages_query = ChatMessage.query.filter_by(chat_room_id=room_id).order_by(ChatMessage.created_at.desc())
    paginated_messages = messages_query.paginate(page=page, per_page=per_page, error_out=False)
    
    if request.headers.get('Accept') == 'application/json':
        msg_data = []
        for msg in paginated_messages.items:
            msg_data.append({
                "id": msg.id,
                "sender_id": msg.sender_id,
                "sender_name": msg.sender.username if msg.sender else "System",
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
                "is_system_msg": msg.is_system_msg
            })
        # Reverse to return chronological order for the frontend
        msg_data.reverse()
        
        return jsonify({
            "status": "success",
            "room_id": room_id,
            "messages": msg_data,
            "has_next": paginated_messages.has_next,
            "has_prev": paginated_messages.has_prev,
            "page": page
        })
        
    return render_template('chat/room.html', room=room)
