"""
User Management Endpoints

CRUD operations for users, approval workflows.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...db.session import get_db
from ...models.user import User, UserRole, ApprovalStatus
from ...schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserApprovalRequest,
    UserWithInstitution,
)
from ...core.security import get_password_hash

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.
    Requires institution admin or super admin privileges.
    """
    # Check if email already exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        institution_id=user_data.institution_id,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        gender=user_data.gender,
        role=user_data.role,
        approval_status=ApprovalStatus.PENDING,  # Requires approval
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    role: UserRole = None,
    db: Session = Depends(get_db),
):
    """List users with optional role filter."""
    query = db.query(User)
    
    if role:
        query = query.filter(User.role == role)
    
    users = query.offset(skip).limit(limit).all()
    
    return users


@router.get("/{user_id}", response_model=UserWithInstitution)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID with institution details."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
):
    """Update user profile."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/{user_id}/approve", response_model=UserResponse)
def approve_user(
    user_id: int,
    approval_request: UserApprovalRequest,
    db: Session = Depends(get_db),
):
    """Approve or reject user registration."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.approval_status = approval_request.approval_status
    
    if approval_request.approval_status == ApprovalStatus.REJECTED:
        if not approval_request.rejection_reason:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rejection reason is required"
            )
        user.rejection_reason = approval_request.rejection_reason
    elif approval_request.approval_status == ApprovalStatus.APPROVED:
        user.approved_at = None  # Will be set by DB trigger or manually
        user.rejection_reason = None
    
    db.commit()
    db.refresh(user)
    
    return user
