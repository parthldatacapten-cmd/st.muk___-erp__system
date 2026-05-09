"""
Chat & Notification Database Models
Supports 1:1 chats, Group chats, System broadcasts, and Notifications
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class RoomType(str, enum.Enum):
    DIRECT = "DIRECT"  # 1:1 chat
    GROUP = "GROUP"    # Class/Staff group
    SYSTEM = "SYSTEM"  # Broadcasts


class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(200), nullable=True)  # For group chats
    room_type = Column(SQLEnum(RoomType), default=RoomType.DIRECT)
    institution_id = Column(String(50), ForeignKey("institutions.id"), nullable=False)
    created_by = Column(String(50), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    messages = relationship("Message", back_populates="room", cascade="all, delete-orphan")
    members = relationship("ChatMember", back_populates="room", cascade="all, delete-orphan")
    institution = relationship("Institution", back_populates="chat_rooms")


class ChatMember(Base):
    __tablename__ = "chat_members"
    
    id = Column(String(50), primary_key=True, index=True)
    room_id = Column(String(50), ForeignKey("chat_rooms.id"), nullable=False)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_read_at = Column(DateTime, nullable=True)
    
    room = relationship("ChatRoom", back_populates="members")
    user = relationship("User", back_populates="chat_memberships")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String(50), primary_key=True, index=True)
    room_id = Column(String(50), ForeignKey("chat_rooms.id"), nullable=False)
    sender_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="TEXT")  # TEXT, IMAGE, FILE, SYSTEM
    file_url = Column(String(500), nullable=True)
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    is_deleted = Column(Boolean, default=False)
    
    room = relationship("ChatRoom", back_populates="messages")
    sender = relationship("User", foreign_keys=[sender_id])
    reactions = relationship("MessageReaction", back_populates="message", cascade="all, delete-orphan")


class MessageReaction(Base):
    __tablename__ = "message_reactions"
    
    id = Column(String(50), primary_key=True, index=True)
    message_id = Column(String(50), ForeignKey("messages.id"), nullable=False)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    emoji = Column(String(10), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    message = relationship("Message", back_populates="reactions")


class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(String(50), primary_key=True, index=True)
    institution_id = Column(String(50), ForeignKey("institutions.id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50))  # FEE_DUE, ABSENT, HOMEWORK, EXAM, GENERAL
    priority = Column(String(20), default="NORMAL")  # LOW, NORMAL, HIGH, URGENT
    target_audience = Column(String(50))  # ALL, STUDENTS, PARENTS, TEACHERS, STAFF
    target_ids = Column(Text, nullable=True)  # JSON array of specific user IDs
    channel = Column(String(50))  # IN_APP, SMS, EMAIL, WHATSAPP, PUSH
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    created_by = Column(String(50), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    institution = relationship("Institution", back_populates="notifications")
    user_notifications = relationship("UserNotification", back_populates="notification", cascade="all, delete-orphan")


class UserNotification(Base):
    __tablename__ = "user_notifications"
    
    id = Column(String(50), primary_key=True, index=True)
    notification_id = Column(String(50), ForeignKey("notifications.id"), nullable=False)
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    notification = relationship("Notification", back_populates="user_notifications")
    user = relationship("User", back_populates="notifications")


# Add relationships to existing User model (to be imported in main models)
def extend_user_model(User):
    User.chat_memberships = relationship("ChatMember", back_populates="user")
    User.notifications = relationship("UserNotification", back_populates="user")
    User.sent_notifications = relationship("Notification", back_populates="creator")
