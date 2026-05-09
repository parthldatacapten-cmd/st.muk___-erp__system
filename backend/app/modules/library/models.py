from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    books = relationship("Book", back_populates="author")


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    books = relationship("Book", back_populates="publisher")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    isbn = Column(String(20), unique=True, nullable=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=True)
    category = Column(String(50), nullable=False, index=True)  # Fiction, Science, Math, etc.
    rack_number = Column(String(20), nullable=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    price = Column(Float, nullable=True)
    cover_image_url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("Author", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    issues = relationship("BookIssue", back_populates="book")


class BookIssue(Base):
    __tablename__ = "book_issues"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    issue_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    fine_amount = Column(Float, default=0.0)
    fine_paid = Column(Boolean, default=False)
    status = Column(String(20), default="ISSUED")  # ISSUED, RETURNED, OVERDUE
    issued_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="issues")
    # Student relationship will be added when student module is imported


class LibraryFineConfig(Base):
    __tablename__ = "library_fine_config"

    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    fine_per_day = Column(Float, default=5.0)
    max_fine_cap = Column(Float, default=500.0)
    loan_period_days = Column(Integer, default=14)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
