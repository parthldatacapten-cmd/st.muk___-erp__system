"""
EduCore ERP - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from .core.config import settings
from .api.v1.router import api_router


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
    
    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_PREFIX)
    
    @application.get("/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": settings.APP_VERSION}
    
    return application


app = create_application()
