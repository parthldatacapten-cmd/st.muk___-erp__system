"""
Pydantic Schemas for User Management

Request/Response schemas for API validation.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    INSTITUTION_ADMIN = "institution_admin"
    FACULTY = "faculty"
    STUDENT = "student"
    PARENT = "parent"
    ACCOUNTANT = "accountant"
    RECEPTIONIST = "receptionist"


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ON_HOLD = "on_hold"


# ============= Institution Schemas =============

class InstitutionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    code: str = Field(..., min_length=3, max_length=50)
    board_type: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    city: Optional[str] = None
    state: Optional[str] = None


class InstitutionCreate(InstitutionBase):
    """Schema for creating a new institution."""
    admin_email: EmailStr
    admin_password: str = Field(..., min_length=8)
    admin_name: str


class InstitutionUpdate(BaseModel):
    """Schema for updating institution."""
    name: Optional[str] = None
    logo_url: Optional[str] = None
    address: Optional[str] = None
    theme_config: Optional[Dict[str, Any]] = None
    features_enabled: Optional[Dict[str, bool]] = None


class InstitutionResponse(InstitutionBase):
    id: int
    logo_url: Optional[str] = None
    affiliation_number: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============= User Schemas =============

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    gender: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8)
    role: UserRole
    institution_id: Optional[int] = None  # Auto-set for institution-scoped registration


class UserLogin(BaseModel):
    """Schema for login request."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[str] = None


class UserApprovalRequest(BaseModel):
    """Schema for approving/rejecting user."""
    approval_status: ApprovalStatus
    rejection_reason: Optional[str] = None


class Token(BaseModel):
    """Authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Decoded token data."""
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
    institution_id: Optional[int] = None


class UserResponse(UserBase):
    id: int
    institution_id: int
    role: UserRole
    is_active: bool
    email_verified: bool
    phone_verified: bool
    approval_status: ApprovalStatus
    avatar_url: Optional[str] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserWithInstitution(UserResponse):
    institution: InstitutionResponse
    
    model_config = ConfigDict(from_attributes=True)


# ============= Device Binding Schemas =============

class DeviceBindRequest(BaseModel):
    """Request to bind a new device (requires OTP)."""
    device_id: str
    device_name: str
    otp: str = Field(..., min_length=6, max_length=6)


class DeviceChangeResponse(BaseModel):
    remaining_changes: int
    next_change_allowed_at: Optional[datetime] = None
