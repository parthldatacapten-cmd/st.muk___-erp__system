"""
Database Models - EduCore ERP

This module contains all SQLAlchemy models for the application.
Models are organized by domain:
- users: User authentication and management
- institutions: Multi-tenancy support
- students: Student information and profiles
- academics: Courses, batches, subjects, timetables
- attendance: NFC, QR, biometric attendance records
- assessments: Exams, questions, results
- finance: Fees, payments, expenses, payroll
- lms: Courses, videos, assignments, resources
- compliance: NAAC, NEP reports and data
"""

from .user import User, Institution, Role
# Additional models will be added in subsequent commits

__all__ = [
    "User",
    "Institution", 
    "Role",
]
