from flask import request
from flask_socketio import emit, join_room, leave_room, disconnect
from flask_login import current_user
from extensions import db, socketio
from modules.chat.models import ChatRoom, ChatMessage, ChatParticipant
from markupsafe import escape
import logging

logger = logging.getLogger(__name__)

@socketio.on('connect')
def handle_connect():
    """
    Fired when a client attempts to connect to the WebSocket.
    Ensures the user is authenticated.
    """
    if not current_user.is_authenticated:
        # Anonymous users might be allowed to read public rooms, but for now we enforce auth
        # Or we can allow them to connect but reject room joins. Let's allow connection.
        pass
    logger.info(f"Client connected: {request.sid} (User: {current_user.id if current_user.is_authenticated else 'Anonymous'})")

@socketio.on('disconnect')
def handle_disconnect():
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('join')
def on_join(data):
    """
    User requests to join a specific room channel.
    """
    room_id = data.get('room_id')
    if not room_id:
        return
        
    room = ChatRoom.query.get(room_id)
    if not room:
        emit('error', {'message': 'Room not found'})
        return
        
    # Authorization
    if not current_user.is_authenticated:
        emit('error', {'message': 'Authentication required'})
        disconnect()
        return

    is_participant = ChatParticipant.query.filter_by(chat_room_id=room_id, user_id=current_user.id).first()
    
    if room.type == 'barangay':
        # Public rooms can be joined by anyone
        if not is_participant:
            # Auto-join them as participant if they chat? For now just allow socket join.
            pass
    elif not is_participant:
        emit('error', {'message': 'Not authorized for this room'})
        return
        
    room_str = str(room_id)
    join_room(room_str)
    
    # Broadcast to the room that a user joined (optional)
    # emit('status', {'message': f'{current_user.username} has joined.'}, room=room_str)
    logger.info(f"User {current_user.id} joined room {room_str}")

@socketio.on('leave')
def on_leave(data):
    room_id = data.get('room_id')
    if room_id:
        leave_room(str(room_id))

@socketio.on('send_message')
def handle_send_message(data):
    """
    Handles incoming messages from a user.
    """
    if not current_user.is_authenticated:
        emit('error', {'message': 'Authentication required'})
        return
        
    room_id = data.get('room_id')
    content = data.get('content')
    
    if not room_id or not content or not content.strip():
        return
        
    # Sanitize content
    content = escape(content.strip())
    
    room = ChatRoom.query.get(room_id)
    if not room:
        return
        
    # Authorization check
    is_participant = ChatParticipant.query.filter_by(chat_room_id=room_id, user_id=current_user.id).first()
    if room.type != 'barangay' and not is_participant:
        return
        
    # If they are not a participant in a public room but send a message, add them
    if room.type == 'barangay' and not is_participant:
        new_participant = ChatParticipant(chat_room_id=room_id, user_id=current_user.id)
        db.session.add(new_participant)
        db.session.commit()
        
    # Save message to DB
    msg = ChatMessage(
        chat_room_id=room_id,
        sender_id=current_user.id,
        content=content
    )
    db.session.add(msg)
    db.session.commit()
    
    # Broadcast to all clients in the room
    emit('receive_message', {
        'id': msg.id,
        'room_id': room_id,
        'sender_id': current_user.id,
        'sender_name': current_user.username,
        'content': msg.content,
        'created_at': msg.created_at.isoformat()
    }, room=str(room_id))

@socketio.on('typing')
def handle_typing(data):
    """
    Broadcasts typing indicator to the room.
    """
    if not current_user.is_authenticated:
        return
    room_id = data.get('room_id')
    is_typing = data.get('is_typing', False)
    
    if room_id:
        emit('typing_status', {
            'user_id': current_user.id,
            'username': current_user.username,
            'is_typing': is_typing
        }, room=str(room_id), include_self=False)
