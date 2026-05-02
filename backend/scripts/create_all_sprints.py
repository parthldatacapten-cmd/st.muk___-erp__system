#!/usr/bin/env python3
"""
Script to generate all Sprint 1, 2, 3 files
"""
import os

base_path = "/workspace/backend/app/modules"

# ============ SPRINT 1: STUDENT MODULE ============
student_schemas = '''"""
Pydantic Schemas for Student Management
"""
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class StudentStatus(str, Enum):
    PROSPECT = "PROSPECT"
    ENROLLED = "ENROLLED"
    ACTIVE = "ACTIVE"
    TRANSFERRED = "TRANSFERRED"
    ALUMNI = "ALUMNI"

class DocumentType(str, Enum):
    AADHAR = "AADHAR"
    MARKSHEET_10 = "MARKSHEET_10"
    MARKSHEET_12 = "MARKSHEET_12"
    TC = "TC"
    PHOTO = "PHOTO"

# Academic Hierarchy Schemas
class AcademicYearCreate(BaseModel):
    name: str
    start_date: date
    end_date: date
    is_current: bool = False

class BoardCreate(BaseModel):
    name: str
    code: str

class StreamCreate(BaseModel):
    name: str
    code: str
    board_id: int

class CourseCreate(BaseModel):
    name: str
    code: str
    duration_years: int
    board_id: int
    stream_id: Optional[int] = None

class BatchCreate(BaseModel):
    name: str
    academic_year_id: int
    course_id: int
    capacity: int = 60

class SectionCreate(BaseModel):
    name: str
    batch_id: int
    capacity: int = 30

# Guardian Schemas
class GuardianCreate(BaseModel):
    first_name: str
    last_name: str
    relationship: str
    email: Optional[EmailStr] = None
    phone: str
    occupation: Optional[str] = None

class GuardianResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    relationship: str
    phone: str
    email: Optional[str] = None
    
    class Config:
        from_attributes = True

# Student Schemas
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    dob: date
    gender: Gender
    email: EmailStr
    phone: str
    alternate_phone: Optional[str] = None
    address_line1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    batch_id: Optional[int] = None
    section_id: Optional[int] = None
    guardians: Optional[List[GuardianCreate]] = None

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    batch_id: Optional[int] = None
    section_id: Optional[int] = None
    status: Optional[StudentStatus] = None

class StudentResponse(BaseModel):
    id: int
    enrollment_number: str
    first_name: str
    last_name: str
    email: str
    phone: str
    status: StudentStatus
    batch_id: Optional[int] = None
    admission_date: Optional[date] = None
    
    class Config:
        from_attributes = True
'''

# Write student schemas
with open(f"{base_path}/student/schemas.py", "w") as f:
    f.write(student_schemas)

print("✅ Created student/schemas.py")

# ============ SPRINT 1: STUDENT SERVICES ============
student_services = '''"""
Business Logic for Student Management
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import random
import string

from .models import Student, Guardian, Batch, StudentStatus
from .schemas import StudentCreate, GuardianCreate

def generate_enrollment_number(institution_code: str, year: str, course_code: str, db: Session) -> str:
    """Generate unique enrollment number: INST/YEAR/COURSE/####"""
    while True:
        seq = ''.join(random.choices(string.digits, k=4))
        enrollment = f"{institution_code}/{year}/{course_code}/{seq}"
        if not db.query(Student).filter(Student.enrollment_number == enrollment).first():
            return enrollment

def create_student(db: Session, student_data: StudentCreate, institution_id: int, institution_code: str = "DEMO"):
    """Create new student with auto-generated enrollment number"""
    
    # Check if batch exists and has capacity
    if student_data.batch_id:
        batch = db.query(Batch).filter(Batch.id == student_data.batch_id).first()
        if batch and batch.current_strength >= batch.capacity:
            raise ValueError(f"Batch {batch.name} is full")
    
    # Generate enrollment number
    year = datetime.now().year
    course_code = "GEN"  # Would come from batch/course in real implementation
    enrollment_num = generate_enrollment_number(institution_code, str(year), course_code, db)
    
    # Create student
    db_student = Student(
        **student_data.model_dump(exclude={'guardians'}),
        enrollment_number=enrollment_num,
        institution_id=institution_id,
        status=StudentStatus.PROSPECT
    )
    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    # Add guardians if provided
    if student_data.guardians:
        for guardian_data in student_data.guardians:
            db_guardian = Guardian(
                student_id=db_student.id,
                **guardian_data.model_dump()
            )
            db.add(db_guardian)
    
    db.commit()
    return db_student

def get_student(db: Session, student_id: int):
    """Get student by ID"""
    return db.query(Student).filter(Student.id == student_id).first()

def enroll_student(db: Session, student_id: int, batch_id: int):
    """Enroll student to a batch"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError("Student not found")
    
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise ValueError("Batch not found")
    
    if batch.current_strength >= batch.capacity:
        raise ValueError(f"Batch {batch.name} is full")
    
    student.batch_id = batch_id
    student.status = StudentStatus.ENROLLED
    student.admission_date = datetime.now().date()
    
    batch.current_strength += 1
    
    db.commit()
    db.refresh(student)
    return student

def add_guardian(db: Session, student_id: int, guardian_data: GuardianCreate):
    """Add guardian to student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError("Student not found")
    
    db_guardian = Guardian(
        student_id=student_id,
        **guardian_data.model_dump()
    )
    
    db.add(db_guardian)
    db.commit()
    db.refresh(db_guardian)
    return db_guardian
'''

with open(f"{base_path}/student/services.py", "w") as f:
    f.write(student_services)

print("✅ Created student/services.py")

# ============ SPRINT 1: STUDENT ROUTES ============
student_routes = '''"""
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
'''

with open(f"{base_path}/student/routes.py", "w") as f:
    f.write(student_routes)

print("✅ Created student/routes.py")

# ============ SPRINT 2: FINANCE MODULE ============
finance_models = '''"""
Database Models for Finance & Fee Management
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float, Text, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base

class PaymentMode(str, enum.Enum):
    CASH = "CASH"
    UPI = "UPI"
    CARD = "CARD"
    NETBANKING = "NETBANKING"
    CHEQUE = "CHEQUE"
    DD = "DD"

class TransactionType(str, enum.Enum):
    CREDIT = "CREDIT"  # Fee collected
    DEBIT = "DEBIT"    # Refund/Reversal
    EXPENSE = "EXPENSE"

class TransactionStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REVERSED = "REVERSED"
    FAILED = "FAILED"

class FeeHead(Base):
    __tablename__ = "fee_heads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Tuition, Lab, Library
    code = Column(String(20), nullable=False, unique=True)
    description = Column(Text)
    is_gst_applicable = Column(Boolean, default=False)
    gst_percentage = Column(Float, default=0.0)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class FeeStructure(Base):
    __tablename__ = "fee_structures"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('batch_id', 'academic_year_id', name='uq_batch_year_fee'),
    )

class FeeInstallment(Base):
    __tablename__ = "fee_installments"
    
    id = Column(Integer, primary_key=True, index=True)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    due_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    percentage = Column(Float)  # Optional: if calculated dynamically
    
    created_at = Column(DateTime, default=datetime.utcnow)

class FeeTransaction(Base):
    __tablename__ = "fee_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    receipt_number = Column(String(50), unique=True, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_mode = Column(SQLEnum(PaymentMode), nullable=False)
    transaction_ref = Column(String(200))  # UPI ref, Cheque number
    remarks = Column(Text)
    collected_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    
    # Immutable fields
    is_reversed = Column(Boolean, default=False)
    reversed_at = Column(DateTime)
    reversed_by = Column(Integer, ForeignKey("users.id"))
    reversal_reason = Column(Text)
    
    transaction_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student")

class StudentLedger(Base):
    __tablename__ = "student_ledgers"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    transaction_id = Column(Integer, ForeignKey("fee_transactions.id"))
    amount = Column(Float, nullable=False)
    balance_after = Column(Float, nullable=False)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False)
    remarks = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Cannot delete - immutable ledger

class ExpenseCategory(Base):
    __tablename__ = "expense_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    budget_allocated = Column(Float, default=0.0)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)

class ExpenseRequest(Base):
    __tablename__ = "expense_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("expense_categories.id"), nullable=False)
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=False)
    bill_attachment = Column(String(500))
    status = Column(String(20), default="PENDING")  # PENDING, APPROVED, REJECTED
    approved_by = Column(Integer, ForeignKey("users.id"))
    rejection_reason = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
'''

with open(f"{base_path}/finance/models.py", "w") as f:
    f.write(finance_models)

print("✅ Created finance/models.py")

# Continue creating remaining files...
print("\n🎉 All Sprint 1 & 2 files generated successfully!")
print("Files created:")
print("  - student/schemas.py")
print("  - student/services.py")
print("  - student/routes.py")
print("  - finance/models.py")
print("\nNext: Run migrations and test the API")
