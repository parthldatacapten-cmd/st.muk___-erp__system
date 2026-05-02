"""
User Management Models

Core models for user authentication, institutions (multi-tenancy), and roles.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..db.session import Base


class UserRole(enum.Enum):
    """System-wide roles."""
    SUPER_ADMIN = "super_admin"  # Platform owner
    INSTITUTION_ADMIN = "institution_admin"  # College/School principal
    FACULTY = "faculty"
    STUDENT = "student"
    PARENT = "parent"
    ACCOUNTANT = "accountant"
    RECEPTIONIST = "receptionist"


class ApprovalStatus(enum.Enum):
    """Approval workflow statuses."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ON_HOLD = "on_hold"


class Institution(Base):
    """
    Multi-tenant institution model.
    Each institution (school/college/coaching center) has isolated data.
    """
    __tablename__ = "institutions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # Short code for URL subdomain
    logo_url = Column(String(500))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    
    # Education board/type
    board_type = Column(String(50))  # CBSE, ICSE, State, University, Coaching
    affiliation_number = Column(String(100))  # CBSE/ICSE affiliation no
    
    # Branding & Customization
    theme_config = Column(JSON, default={})  # Colors, fonts, logo
    custom_domain = Column(String(255), unique=True)
    is_active = Column(Boolean, default=True)
    
    # Features enabled
    features_enabled = Column(JSON, default={
        "lms": True,
        "assessment": True,
        "attendance_nfc": True,
        "attendance_qr": True,
        "naac_reports": True,
        "payment_gateway": True,
    })
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="institution", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Institution {self.name} ({self.code})>"


class User(Base):
    """
    User model for all system users (admin, faculty, students, parents).
    Supports multi-tenancy via institution_id.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False, index=True)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    phone = Column(String(20), index=True)
    phone_verified = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    
    # Profile
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    full_name = Column(String(255))  # Computed field
    avatar_url = Column(String(500))
    gender = Column(String(20))
    date_of_birth = Column(DateTime)
    
    # Role & Permissions
    role = Column(SQLEnum(UserRole), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    is_super_admin = Column(Boolean, default=False)  # Platform-level admin
    
    # Device binding (anti-fraud)
    device_id = Column(String(255))  # Current logged-in device
    device_change_count = Column(Integer, default=0)
    last_device_change_at = Column(DateTime(timezone=True))
    
    # Approval workflow (for student/faculty registration)
    approval_status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING)
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    rejection_reason = Column(Text)
    
    # Metadata
    metadata = Column(JSON, default={})  # Extra fields based on role
    last_login_at = Column(DateTime(timezone=True))
    last_login_ip = Column(String(45))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    institution = relationship("Institution", back_populates="users")
    approved_users = relationship("User", remote_side=[id])
    
    def __repr__(self):
        return f"<User {self.email} ({self.role.value})>"


class Role(Base):
    """
    Custom role definitions for fine-grained permissions.
    Institutions can create custom roles beyond the base UserRole enum.
    """
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Permissions as JSON array
    permissions = Column(JSON, default=[])  # e.g., ["fees.create", "attendance.mark"]
    
    is_system_role = Column(Boolean, default=False)  # Cannot be deleted
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Role {self.name}>"
