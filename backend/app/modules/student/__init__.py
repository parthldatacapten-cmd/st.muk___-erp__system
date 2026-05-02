"""
Student Management Module
Handles student lifecycle, academic hierarchy, and documents.
"""

from .models import (
    AcademicYear,
    Board,
    Stream,
    Course,
    Batch,
    Section,
    Student,
    Guardian,
    StudentDocument,
)
from .schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    GuardianCreate,
    GuardianResponse,
    BatchCreate,
    CourseCreate,
)
from .services import (
    create_student,
    get_student,
    enroll_student,
    upload_document,
    add_guardian,
)
from .routes import router

__all__ = [
    "AcademicYear",
    "Board",
    "Stream",
    "Course",
    "Batch",
    "Section",
    "Student",
    "Guardian",
    "StudentDocument",
    "StudentCreate",
    "StudentUpdate",
    "StudentResponse",
    "GuardianCreate",
    "GuardianResponse",
    "BatchCreate",
    "CourseCreate",
    "create_student",
    "get_student",
    "enroll_student",
    "upload_document",
    "add_guardian",
    "router",
]
