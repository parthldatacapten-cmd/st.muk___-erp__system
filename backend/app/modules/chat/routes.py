"""
Chat & Notification API Routes
REST endpoints and WebSocket handler for real-time messaging
"""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.models import User
from app.modules.chat.services import ChatService, NotificationService
from app.modules.chat.schemas import (
    ChatRoomCreate, ChatRoomResponse, MessageCreate, MessageResponse,
    NotificationCreate, NotificationResponse, UserNotificationResponse,
    WSMessage, WSResponse
)

router = APIRouter()


# === Chat Room Endpoints ===

@router.post("/rooms", response_model=ChatRoomResponse)
def create_chat_room(
    room_data: ChatRoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new chat room (direct or group)"""
    if room_data.room_type == "DIRECT":
        if len(room_data.member_ids) != 1:
            raise HTTPException(status_code=400, message="Direct chat must have exactly 1 other member")
        return ChatService.create_direct_room(
            db=db,
            institution_id=current_user.institution_id,
            user1_id=current_user.id,
            user2_id=room_data.member_ids[0]
        )
    else:
        return ChatService.create_group_room(
            db=db,
            institution_id=current_user.institution_id,
            name=room_data.name or "Group Chat",
            created_by=current_user.id,
            member_ids=room_data.member_ids
        )


@router.get("/rooms", response_model=List[ChatRoomResponse])
def get_my_rooms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all chat rooms for the current user"""
    rooms = ChatService.get_user_rooms(db, current_user.id, current_user.institution_id)
    return rooms


@router.get("/rooms/{room_id}/messages", response_model=List[MessageResponse])
def get_room_messages(
    room_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get messages from a specific chat room"""
    # Verify user is member of room
    from app.modules.chat.models import ChatMember
    membership = db.query(ChatMember).filter(
        ChatMember.room_id == room_id,
        ChatMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this room")
    
    messages = ChatService.get_room_messages(db, room_id, limit, offset)
    return messages


@router.post("/rooms/{room_id}/messages", response_model=MessageResponse)
def send_message(
    room_id: str,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a message to a chat room"""
    # Verify membership
    from app.modules.chat.models import ChatMember
    membership = db.query(ChatMember).filter(
        ChatMember.room_id == room_id,
        ChatMember.user_id == current_user.id
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this room")
    
    message = ChatService.send_message(
        db=db,
        room_id=room_id,
        sender_id=current_user.id,
        content=message_data.content,
        message_type=message_data.message_type,
        file_url=message_data.file_url
    )
    
    return message


@router.post("/rooms/{room_id}/read")
def mark_room_read(
    room_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all messages in a room as read"""
    success = ChatService.mark_as_read(db, room_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Room membership not found")
    return {"status": "success"}


# === Notification Endpoints ===

@router.get("/notifications", response_model=List[UserNotificationResponse])
def get_notifications(
    unread_only: bool = False,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get notifications for the current user"""
    return NotificationService.get_user_notifications(
        db, current_user.id, unread_only, limit
    )


@router.post("/notifications/{notif_id}/read")
def mark_notification_read(
    notif_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a specific notification as read"""
    success = NotificationService.mark_notification_read(db, current_user.id, notif_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "success"}


@router.post("/notifications/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark all notifications as read"""
    count = NotificationService.mark_all_read(db, current_user.id)
    return {"status": "success", "marked_count": count}


@router.post("/broadcast", response_model=NotificationResponse)
def broadcast_notification(
    notif_data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Broadcast a notification to users (Admin/Teacher only)"""
    if current_user.role not in ["ADMIN", "TEACHER", "INSTITUTION_ADMIN"]:
        raise HTTPException(status_code=403, detail="Not authorized to broadcast")
    
    return NotificationService.create_notification(
        db=db,
        institution_id=current_user.institution_id,
        title=notif_data.title,
        message=notif_data.message,
        notification_type=notif_data.notification_type,
        priority=notif_data.priority,
        target_audience=notif_data.target_audience,
        target_ids=notif_data.target_ids,
        channel=notif_data.channel,
        created_by=current_user.id
    )


# === WebSocket Endpoint for Real-Time Chat ===

@router.websocket("/ws/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: str,
    db: Session = Depends(get_db),
    token: str = Query(...)
):
    """WebSocket endpoint for real-time chat"""
    # Authenticate user from token
    from app.core.auth import verify_token
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if not user_id:
            await websocket.close(code=1008)
            return
        current_user = db.query(User).filter(User.id == user_id).first()
        if not current_user:
            await websocket.close(code=1008)
            return
    except Exception:
        await websocket.close(code=1008)
        return
    
    # Verify room membership
    from app.modules.chat.models import ChatMember
    membership = db.query(ChatMember).filter(
        ChatMember.room_id == room_id,
        ChatMember.user_id == current_user.id
    ).first()
    
    if not membership:
        await websocket.close(code=1008)
        return
    
    await websocket.accept()
    
    # Store connection in application state for broadcasting
    # Note: For production, use Redis pub/sub for multi-worker setups
    await websocket.send_json({
        "type": "CONNECTED",
        "data": {"room_id": room_id}
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            action = message_data.get("action")
            
            if action == "SEND_MESSAGE":
                content = message_data.get("content")
                if content:
                    message = ChatService.send_message(
                        db=db,
                        room_id=room_id,
                        sender_id=current_user.id,
                        content=content
                    )
                    # Broadcast to all connected clients in room
                    await websocket.send_json({
                        "type": "NEW_MESSAGE",
                        "data": {
                            "id": message.id,
                            "sender_id": message.sender_id,
                            "content": message.content,
                            "created_at": message.created_at.isoformat()
                        }
                    })
            
            elif action == "MARK_READ":
                ChatService.mark_as_read(db, room_id, current_user.id)
                await websocket.send_json({
                    "type": "MESSAGE_READ",
                    "data": {"user_id": current_user.id}
                })
            
            elif action == "TYPING":
                await websocket.send_json({
                    "type": "USER_TYPING",
                    "data": {"user_id": current_user.id}
                })
    
    except WebSocketDisconnect:
        # Handle disconnect
        pass
    except Exception as e:
        await websocket.send_json({
            "type": "ERROR",
            "data": {"message": str(e)}
        })
