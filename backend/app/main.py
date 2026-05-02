"""
EduCore ERP - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from .core.config import settings
from .core.exceptions import register_exception_handlers
from .core.logging_config import logger
from .api.v1.router import api_router
from .api.v1.health import router as health_router


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Indian Education Management ERP System",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
    )
    
    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add Prometheus metrics
    if not settings.DEBUG:
        Instrumentator().instrument(application).expose(application)
    
    # Register exception handlers
    register_exception_handlers(application)
    
    # Include health check router
    application.include_router(health_router, prefix="/api/v1")
    
    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    @application.on_event("startup")
    async def startup_event():
        """Log startup message."""
        logger.info("🚀 EduCore ERP Backend starting up...")
        logger.info(f"📌 Version: {settings.APP_VERSION}")
        logger.info(f"🔧 Debug Mode: {settings.DEBUG}")
        logger.info(f"🌍 Environment: {settings.ENVIRONMENT}")
    
    @application.on_event("shutdown")
    async def shutdown_event():
        """Log shutdown message."""
        logger.info("🛑 EduCore ERP Backend shutting down...")
    
    return application


app = create_application()
