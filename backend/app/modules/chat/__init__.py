"""
Chat & Notification Module
Real-time messaging, group chats, and system notifications
"""
from fastapi import APIRouter

from .routes import router as chat_router

router = APIRouter(prefix="/chat", tags=["Chat & Notifications"])
router.include_router(chat_router)

__all__ = ["router"]
