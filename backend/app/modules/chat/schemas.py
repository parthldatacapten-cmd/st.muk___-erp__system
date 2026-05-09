"""
Chat & Notification Pydantic Schemas
Validation models for API requests and responses
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


# === Chat Room Schemas ===
class ChatRoomBase(BaseModel):
    name: Optional[str] = None
    room_type: str = "DIRECT"  # DIRECT, GROUP, SYSTEM
    institution_id: str


class ChatRoomCreate(ChatRoomBase):
    member_ids: List[str] = []  # Initial members


class ChatRoomResponse(ChatRoomBase):
    id: str
    created_by: str
    created_at: datetime
    is_active: bool
    member_count: int = 0
    
    class Config:
        from_attributes = True


# === Message Schemas ===
class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    message_type: str = "TEXT"  # TEXT, IMAGE, FILE
    file_url: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    room_id: str
    sender_id: str
    sender_name: Optional[str] = None
    content: str
    message_type: str
    file_url: Optional[str] = None
    is_edited: bool
    edited_at: Optional[datetime] = None
    created_at: datetime
    reactions: List[dict] = []
    
    class Config:
        from_attributes = True


# === Notification Schemas ===
class NotificationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=2000)
    notification_type: str = "GENERAL"
    priority: str = "NORMAL"  # LOW, NORMAL, HIGH, URGENT
    target_audience: str = "ALL"  # ALL, STUDENTS, PARENTS, TEACHERS, STAFF
    target_ids: Optional[List[str]] = None  # Specific user IDs
    channel: str = "IN_APP"  # IN_APP, SMS, EMAIL, WHATSAPP, PUSH


class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    notification_type: str
    priority: str
    is_sent: bool
    sent_at: Optional[datetime] = None
    created_at: datetime
    created_by: str
    
    class Config:
        from_attributes = True


class UserNotificationResponse(BaseModel):
    id: str
    notification_id: str
    title: str
    message: str
    notification_type: str
    priority: str
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# === WebSocket Schemas ===
class WSMessage(BaseModel):
    action: str  # SEND_MESSAGE, MARK_READ, TYPING
    room_id: str
    content: Optional[str] = None
    message_id: Optional[str] = None


class WSResponse(BaseModel):
    type: str  # NEW_MESSAGE, MESSAGE_READ, USER_TYPING, ERROR
    data: dict
