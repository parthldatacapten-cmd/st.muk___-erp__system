"""
Database Models for Student & Academic Management
"""
from datetime import date, datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Enum as SQLEnum,
    UniqueConstraint,
    Text,
    Float,
)
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base


# ============== ENUMS ==============
class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class StudentStatus(str, enum.Enum):
    PROSPECT = "PROSPECT"  # Inquiry/Registered but not enrolled
    ENROLLED = "ENROLLED"  # Enrolled to batch
    ACTIVE = "ACTIVE"  # Currently studying
    TRANSFERRED = "TRANSFERRED"
    ALUMNI = "ALUMNI"
    DROPPED_OUT = "DROPPED_OUT"


class DocumentType(str, enum.Enum):
    AADHAR = "AADHAR"
    BIRTH_CERTIFICATE = "BIRTH_CERTIFICATE"
    MARKSHEET_10 = "MARKSHEET_10"
    MARKSHEET_12 = "MARKSHEET_12"
    TC = "TC"  # Transfer Certificate
    PHOTO = "PHOTO"
    OTHER = "OTHER"


# ============== ACADEMIC HIERARCHY ==============
class AcademicYear(Base):
    __tablename__ = "academic_years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)  # e.g., "2024-2025"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_current = Column(Boolean, default=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    batches = relationship("Batch", back_populates="academic_year")


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # CBSE, ICSE, State Board, University
    code = Column(String(20), nullable=False, unique=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    courses = relationship("Course", back_populates="board")


class Stream(Base):
    __tablename__ = "streams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Science, Commerce, Arts, Engineering
    code = Column(String(20), nullable=False)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    courses = relationship("Course", back_populates="stream")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)  # Class 12 Science, B.Tech CSE, MBA
    code = Column(String(50), nullable=False)
    duration_years = Column(Integer, nullable=False)
    stream_id = Column(Integer, ForeignKey("streams.id"))
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    board = relationship("Board", back_populates="courses")
    stream = relationship("Stream", back_populates="courses")
    batches = relationship("Batch", back_populates="course")


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # 2024-A, FYBCOM-A
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    capacity = Column(Integer, nullable=False, default=60)
    current_strength = Column(Integer, default=0)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('name', 'institution_id', name='uq_batch_name_institution'),
    )

    # Relationships
    academic_year = relationship("AcademicYear", back_populates="batches")
    course = relationship("Course", back_populates="batches")
    sections = relationship("Section", back_populates="batch")
    students = relationship("Student", back_populates="batch")


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # Div A, Div B, Section 1
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    capacity = Column(Integer, default=30)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    batch = relationship("Batch", back_populates="sections")
    students = relationship("Student", back_populates="section")


# ============== STUDENT MODEELS ==============
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Info
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    email = Column(String(200), unique=True, index=True)
    phone = Column(String(20), nullable=False)
    alternate_phone = Column(String(20))
    
    # Address
    address_line1 = Column(String(200))
    address_line2 = Column(String(200))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    
    # Academic Info
    enrollment_number = Column(String(50), unique=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    section_id = Column(Integer, ForeignKey("sections.id"))
    status = Column(SQLEnum(StudentStatus), default=StudentStatus.PROSPECT)
    admission_date = Column(Date)
    
    # Institutional Link
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # Optional: if student has login
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    batch = relationship("Batch", back_populates="students")
    section = relationship("Section", back_populates="students")
    guardians = relationship("Guardian", back_populates="student", cascade="all, delete-orphan")
    documents = relationship("StudentDocument", back_populates="student", cascade="all, delete-orphan")


class Guardian(Base):
    __tablename__ = "guardians"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Guardian Info
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    relationship = Column(String(50), nullable=False)  # Father, Mother, Guardian
    email = Column(String(200))
    phone = Column(String(20), nullable=False)
    occupation = Column(String(100))
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    student = relationship("Student", back_populates="guardians")


class StudentDocument(Base):
    __tablename__ = "student_documents"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)  # MinIO path
    file_size = Column(Integer)  # in bytes
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    student = relationship("Student", back_populates="documents")
