"""
Authentication Endpoints

Login, logout, token refresh, device binding.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ...db.session import get_db
from ...models.user import User, Institution, ApprovalStatus
from ...schemas.user import (
    Token,
    UserCreate,
    UserResponse,
    UserLogin,
    DeviceBindRequest,
    DeviceChangeResponse,
    InstitutionCreate,
)
from ...core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from ...core.config import settings

router = APIRouter()


@router.post("/register/institution", response_model=dict, status_code=status.HTTP_201_CREATED)
def register_institution(institution_data: InstitutionCreate, db: Session = Depends(get_db)):
    """
    Register a new institution (school/college/coaching center).
    Creates the institution and admin user in one transaction.
    """
    from ...models.user import UserRole
    
    # Check if institution code already exists
    existing = db.query(Institution).filter(
        Institution.code == institution_data.code
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Institution code already exists"
        )
    
    # Check if admin email already exists
    existing_admin = db.query(User).filter(
        User.email == institution_data.admin_email
    ).first()
    
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create institution
    institution = Institution(
        name=institution_data.name,
        code=institution_data.code,
        board_type=institution_data.board_type,
        email=institution_data.email,
        phone=institution_data.phone,
        city=institution_data.city,
        state=institution_data.state,
        is_active=True,
    )
    
    db.add(institution)
    db.flush()  # Get institution ID
    
    # Create admin user
    admin_user = User(
        institution_id=institution.id,
        email=institution_data.admin_email,
        hashed_password=get_password_hash(institution_data.admin_password),
        first_name=institution_data.admin_name.split()[0],
        last_name=" ".join(institution_data.admin_name.split()[1:]) if len(institution_data.admin_name.split()) > 1 else "",
        role=UserRole.INSTITUTION_ADMIN,
        is_active=True,
        email_verified=True,  # Auto-verify for initial admin
        approval_status=ApprovalStatus.APPROVED,
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    return {
        "message": "Institution registered successfully",
        "institution_id": institution.id,
        "admin_user_id": admin_user.id,
    }


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login.
    Returns access token and refresh token.
    """
    # Find user by email (username field in form_data)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    if user.approval_status != ApprovalStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account approval pending. Status: {user.approval_status.value}"
        )
    
    # Generate tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "role": user.role.value,
            "institution_id": user.institution_id,
        },
        expires_delta=access_token_expires,
    )
    
    refresh_token = create_refresh_token(
        data={
            "sub": user.email,
            "user_id": user.id,
        }
    )
    
    # Update last login
    user.last_login_at = None  # Will be updated by DB trigger or manually
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token."""
    payload = verify_token(refresh_token, token_type="refresh")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Generate new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "role": user.role.value,
            "institution_id": user.institution_id,
        },
        expires_delta=access_token_expires,
    )
    
    # Generate new refresh token (rotate)
    new_refresh_token = create_refresh_token(
        data={
            "sub": user.email,
            "user_id": user.id,
        }
    )
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/device/bind", response_model=DeviceChangeResponse)
def bind_device(
    device_data: DeviceBindRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Bind a new device to user account.
    Requires OTP verification.
    Enforces MAX_DEVICE_CHANGES_PER_SEMESTER limit.
    """
    from datetime import datetime, timedelta
    
    # TODO: Verify OTP against sent OTP
    # For now, we'll skip actual OTP verification in this scaffold
    
    # Check device change limit
    semester_start = datetime.utcnow() - timedelta(days=180)
    
    if current_user.last_device_change_at and current_user.last_device_change_at > semester_start:
        if current_user.device_change_count >= settings.MAX_DEVICE_CHANGES_PER_SEMESTER:
            next_allowed = current_user.last_device_change_at + timedelta(days=180)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Maximum device changes ({settings.MAX_DEVICE_CHANGES_PER_SEMESTER}) reached this semester. Next allowed: {next_allowed}"
            )
    
    # Update device binding
    old_device = current_user.device_id
    current_user.device_id = device_data.device_id
    current_user.device_change_count += 1
    current_user.last_device_change_at = datetime.utcnow()
    
    db.commit()
    
    remaining_changes = settings.MAX_DEVICE_CHANGES_PER_SEMESTER - current_user.device_change_count
    
    return DeviceChangeResponse(
        remaining_changes=remaining_changes,
    )


# Dependency to get current user
async def get_current_active_user(
    token: str = Depends(OAuth2PasswordRequestForm),
    db: Session = Depends(get_db),
) -> User:
    """Get current authenticated user."""
    # This is a simplified version - actual implementation would parse Bearer token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # TODO: Implement proper token extraction from Authorization header
    # For now, this is a placeholder
    raise credentials_exception
