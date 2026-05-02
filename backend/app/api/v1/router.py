"""
API Router for v1 endpoints
"""

from fastapi import APIRouter
from .endpoints import auth, institutions, users

api_router = APIRouter()

# Authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Institution endpoints (multi-tenancy)
api_router.include_router(institutions.router, prefix="/institutions", tags=["Institutions"])

# User management endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])
