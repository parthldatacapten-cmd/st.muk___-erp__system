"""
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
