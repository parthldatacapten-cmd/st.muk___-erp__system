"""
Institution Endpoints

CRUD operations for institutions (multi-tenancy).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...db.session import get_db
from ...models.user import Institution
from ...schemas.user import InstitutionCreate, InstitutionUpdate, InstitutionResponse

router = APIRouter()


@router.get("/", response_model=List[InstitutionResponse])
def list_institutions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all active institutions."""
    institutions = db.query(Institution).filter(
        Institution.is_active == True
    ).offset(skip).limit(limit).all()
    
    return institutions


@router.get("/{institution_id}", response_model=InstitutionResponse)
def get_institution(institution_id: int, db: Session = Depends(get_db)):
    """Get institution by ID."""
    institution = db.query(Institution).filter(
        Institution.id == institution_id,
        Institution.is_active == True
    ).first()
    
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
    
    return institution


@router.put("/{institution_id}", response_model=InstitutionResponse)
def update_institution(
    institution_id: int,
    institution_update: InstitutionUpdate,
    db: Session = Depends(get_db),
):
    """Update institution details."""
    institution = db.query(Institution).filter(
        Institution.id == institution_id
    ).first()
    
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
    
    # Update fields
    update_data = institution_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(institution, field, value)
    
    db.commit()
    db.refresh(institution)
    
    return institution
