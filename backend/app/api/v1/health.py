"""Health check endpoints for monitoring."""
from fastapi import APIRouter, status
from sqlalchemy import text
from app.db.session import async_get_db
from redis import asyncio as aioredis
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", status_code=status.HTTP_200_OK)
async def health_check():
    """Basic health check - returns service status."""
    return {
        "status": "healthy",
        "service": "EduCore ERP Backend",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """Readiness check - verifies database and cache connections."""
    db_status = "unknown"
    redis_status = "unknown"
    
    # Check database connection
    try:
        async for db in async_get_db():
            await db.execute(text("SELECT 1"))
            db_status = "connected"
            break
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "disconnected"
    
    # Check Redis connection
    try:
        redis = aioredis.from_url(
            "redis://localhost:6379/0",
            encoding="utf-8",
            decode_responses=True
        )
        await redis.ping()
        redis_status = "connected"
        await redis.close()
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        redis_status = "disconnected"
    
    is_ready = db_status == "connected" and redis_status == "connected"
    
    return {
        "status": "ready" if is_ready else "not_ready",
        "checks": {
            "database": db_status,
            "cache": redis_status
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """Liveness check - simple ping to verify service is running."""
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }
