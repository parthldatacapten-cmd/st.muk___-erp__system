"""
Chat & Notification Business Logic
Handles messaging, room management, and notification broadcasting
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
import uuid
import json

from app.modules.chat.models import (
    ChatRoom, ChatMember, Message, MessageReaction,
    Notification, UserNotification, RoomType
)
from app.modules.chat.schemas import (
    ChatRoomCreate, MessageCreate, NotificationCreate
)


class ChatService:
    """Service for managing chat rooms and messages"""
    
    @staticmethod
    def create_direct_room(db: Session, institution_id: str, user1_id: str, user2_id: str) -> ChatRoom:
        """Create or retrieve a 1:1 chat room between two users"""
        # Check if room already exists
        existing_rooms = db.query(ChatRoom).filter(
            ChatRoom.institution_id == institution_id,
            ChatRoom.room_type == RoomType.DIRECT,
            ChatRoom.is_active == True
        ).all()
        
        for room in existing_rooms:
            members = [m.user_id for m in room.members]
            if set(members) == {user1_id, user2_id}:
                return room
        
        # Create new room
        room_id = f"room_{uuid.uuid4().hex[:12]}"
        room = ChatRoom(
            id=room_id,
            name=None,
            room_type=RoomType.DIRECT,
            institution_id=institution_id,
            created_by=user1_id,
            is_active=True
        )
        db.add(room)
        db.commit()
        db.refresh(room)
        
        # Add members
        member1 = ChatMember(room_id=room_id, user_id=user1_id)
        member2 = ChatMember(room_id=room_id, user_id=user2_id)
        db.add_all([member1, member2])
        db.commit()
        
        return room
    
    @staticmethod
    def create_group_room(db: Session, institution_id: str, name: str, 
                         created_by: str, member_ids: List[str]) -> ChatRoom:
        """Create a group chat room"""
        room_id = f"room_{uuid.uuid4().hex[:12]}"
        room = ChatRoom(
            id=room_id,
            name=name,
            room_type=RoomType.GROUP,
            institution_id=institution_id,
            created_by=created_by,
            is_active=True
        )
        db.add(room)
        db.commit()
        db.refresh(room)
        
        # Add all members including creator
        members = [ChatMember(room_id=room_id, user_id=user_id) for user_id in member_ids]
        if created_by not in member_ids:
            members.append(ChatMember(room_id=room_id, user_id=created_by))
        
        db.add_all(members)
        db.commit()
        
        return room
    
    @staticmethod
    def send_message(db: Session, room_id: str, sender_id: str, 
                    content: str, message_type: str = "TEXT",
                    file_url: Optional[str] = None) -> Message:
        """Send a message to a chat room"""
        message_id = f"msg_{uuid.uuid4().hex[:12]}"
        message = Message(
            id=message_id,
            room_id=room_id,
            sender_id=sender_id,
            content=content,
            message_type=message_type,
            file_url=file_url,
            is_edited=False,
            is_deleted=False
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        
        return message
    
    @staticmethod
    def get_room_messages(db: Session, room_id: str, limit: int = 50, 
                         offset: int = 0) -> List[Message]:
        """Get messages from a chat room"""
        messages = db.query(Message).filter(
            Message.room_id == room_id,
            Message.is_deleted == False
        ).order_by(Message.created_at.desc()).offset(offset).limit(limit).all()
        
        return list(reversed(messages))
    
    @staticmethod
    def mark_as_read(db: Session, room_id: str, user_id: str) -> bool:
        """Mark all messages in a room as read for a user"""
        membership = db.query(ChatMember).filter(
            ChatMember.room_id == room_id,
            ChatMember.user_id == user_id
        ).first()
        
        if membership:
            membership.last_read_at = datetime.utcnow()
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_user_rooms(db: Session, user_id: str, institution_id: str) -> List[ChatRoom]:
        """Get all chat rooms for a user"""
        rooms = db.query(ChatRoom).join(ChatMember).filter(
            ChatMember.user_id == user_id,
            ChatRoom.institution_id == institution_id,
            ChatRoom.is_active == True
        ).options(
            joinedload(ChatRoom.members),
            joinedload(ChatRoom.messages).load_only(Message.id, Message.created_at, Message.content)
        ).all()
        
        return rooms


class NotificationService:
    """Service for managing notifications"""
    
    @staticmethod
    def create_notification(db: Session, institution_id: str, title: str, 
                           message: str, notification_type: str,
                           priority: str, target_audience: str,
                           target_ids: Optional[List[str]], channel: str,
                           created_by: str) -> Notification:
        """Create a notification and queue it for delivery"""
        notif_id = f"notif_{uuid.uuid4().hex[:12]}"
        notification = Notification(
            id=notif_id,
            institution_id=institution_id,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            target_audience=target_audience,
            target_ids=json.dumps(target_ids) if target_ids else None,
            channel=channel,
            is_sent=False,
            created_by=created_by
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        # Create user notifications for target users
        NotificationService._create_user_notifications(db, notification, target_audience, target_ids)
        
        return notification
    
    @staticmethod
    def _create_user_notifications(db: Session, notification: Notification,
                                   target_audience: str, 
                                   target_ids: Optional[List[str]]):
        """Create individual user notification records"""
        from app.modules.student.models import Student
        from app.core.models import User
        
        user_ids = []
        
        if target_ids:
            user_ids = target_ids
        elif target_audience == "ALL":
            users = db.query(User).filter(
                User.institution_id == notification.institution_id,
                User.is_active == True
            ).all()
            user_ids = [u.id for u in users]
        elif target_audience == "TEACHERS":
            users = db.query(User).filter(
                User.institution_id == notification.institution_id,
                User.role == "TEACHER",
                User.is_active == True
            ).all()
            user_ids = [u.id for u in users]
        elif target_audience == "STUDENTS":
            students = db.query(Student).filter(
                Student.institution_id == notification.institution_id
            ).all()
            user_ids = [s.user_id for s in students if s.user_id]
        # Add more audience types as needed
        
        # Create user notification records
        user_notifs = [
            UserNotification(
                notification_id=notification.id,
                user_id=user_id
            ) for user_id in user_ids
        ]
        
        if user_notifs:
            db.add_all(user_notifs)
            db.commit()
    
    @staticmethod
    def get_user_notifications(db: Session, user_id: str, 
                              unread_only: bool = False,
                              limit: int = 20) -> List[UserNotification]:
        """Get notifications for a specific user"""
        query = db.query(UserNotification).filter(
            UserNotification.user_id == user_id
        ).join(Notification).order_by(Notification.created_at.desc())
        
        if unread_only:
            query = query.filter(UserNotification.is_read == False)
        
        return query.limit(limit).all()
    
    @staticmethod
    def mark_notification_read(db: Session, user_id: str, 
                               notification_id: str) -> bool:
        """Mark a notification as read"""
        user_notif = db.query(UserNotification).filter(
            UserNotification.user_id == user_id,
            UserNotification.notification_id == notification_id
        ).first()
        
        if user_notif:
            user_notif.is_read = True
            user_notif.read_at = datetime.utcnow()
            db.commit()
            return True
        return False
    
    @staticmethod
    def mark_all_read(db: Session, user_id: str) -> int:
        """Mark all notifications as read for a user"""
        count = db.query(UserNotification).filter(
            UserNotification.user_id == user_id,
            UserNotification.is_read == False
        ).update({
            UserNotification.is_read: True,
            UserNotification.read_at: datetime.utcnow()
        })
        db.commit()
        return count
