"""
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
