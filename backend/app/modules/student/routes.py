"""
API Routes for Student Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.core.security import get_current_user
from .schemas import StudentCreate, StudentUpdate, StudentResponse, GuardianCreate, GuardianResponse, BatchCreate
from .services import create_student, get_student, enroll_student, add_guardian
from .models import Student

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def register_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Register a new student"""
    institution_id = current_user.get("institution_id")
    institution_code = current_user.get("institution_code", "DEMO")
    
    try:
        student = create_student(db, student_data, institution_id, institution_code)
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create student")

@router.get("/{student_id}", response_model=StudentResponse)
def get_student_details(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get student details by ID"""
    student = get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/{student_id}/enroll")
def enroll_student_to_batch(
    student_id: int,
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Enroll student to a batch"""
    try:
        student = enroll_student(db, student_id, batch_id)
        return {"message": "Student enrolled successfully", "student": student}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{student_id}/guardians", response_model=GuardianResponse)
def add_student_guardian(
    student_id: int,
    guardian_data: GuardianCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add guardian to student"""
    try:
        guardian = add_guardian(db, student_id, guardian_data)
        return guardian
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
