from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List, Optional

from app.modules.library.models import (
    Author, Publisher, Book, BookIssue, LibraryFineConfig
)
from app.modules.library.schemas import (
    AuthorCreate, PublisherCreate, BookCreate, BookUpdate,
    BookIssueCreate, LibraryFineConfigCreate, LibraryFineConfigUpdate
)


class AuthorService:
    @staticmethod
    def create_author(db: Session, author: AuthorCreate) -> Author:
        db_author = Author(**author.model_dump())
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author
    
    @staticmethod
    def get_authors(db: Session, skip: int = 0, limit: int = 100) -> List[Author]:
        return db.query(Author).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_author(db: Session, author_id: int) -> Optional[Author]:
        return db.query(Author).filter(Author.id == author_id).first()


class PublisherService:
    @staticmethod
    def create_publisher(db: Session, publisher: PublisherCreate) -> Publisher:
        db_publisher = Publisher(**publisher.model_dump())
        db.add(db_publisher)
        db.commit()
        db.refresh(db_publisher)
        return db_publisher
    
    @staticmethod
    def get_publishers(db: Session, skip: int = 0, limit: int = 100) -> List[Publisher]:
        return db.query(Publisher).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_publisher(db: Session, publisher_id: int) -> Optional[Publisher]:
        return db.query(Publisher).filter(Publisher.id == publisher_id).first()


class BookService:
    @staticmethod
    def create_book(db: Session, book: BookCreate) -> Book:
        # Check if ISBN already exists
        if book.isbn:
            existing = db.query(Book).filter(Book.isbn == book.isbn).first()
            if existing:
                raise ValueError("Book with this ISBN already exists")
        
        db_book = Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    
    @staticmethod
    def get_books(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Book]:
        query = db.query(Book).filter(Book.is_active == True)
        
        if category:
            query = query.filter(Book.category == category)
        
        if search:
            query = query.filter(
                (Book.title.ilike(f"%{search}%")) | 
                (Book.isbn.ilike(f"%{search}%"))
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_book(db: Session, book_id: int) -> Optional[Book]:
        return db.query(Book).filter(Book.id == book_id).first()
    
    @staticmethod
    def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Optional[Book]:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return None
        
        update_data = book_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        db.commit()
        db.refresh(db_book)
        return db_book
    
    @staticmethod
    def delete_book(db: Session, book_id: int) -> bool:
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return False
        
        db_book.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def issue_book(
        db: Session, 
        book_id: int, 
        student_id: int, 
        due_date: datetime,
        issued_by: int
    ) -> BookIssue:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError("Book not found")
        
        if book.available_copies <= 0:
            raise ValueError("No copies available for issue")
        
        # Create issue record
        issue = BookIssue(
            book_id=book_id,
            student_id=student_id,
            due_date=due_date,
            issued_by=issued_by,
            status="ISSUED"
        )
        db.add(issue)
        
        # Decrease available copies
        book.available_copies -= 1
        
        db.commit()
        db.refresh(issue)
        return issue
    
    @staticmethod
    def return_book(db: Session, issue_id: int) -> BookIssue:
        issue = db.query(BookIssue).filter(BookIssue.id == issue_id).first()
        if not issue:
            raise ValueError("Issue record not found")
        
        if issue.status == "RETURNED":
            raise ValueError("Book already returned")
        
        # Calculate fine
        config = db.query(LibraryFineConfig).filter(
            LibraryFineConfig.institution_id == 1  # TODO: Get from context
        ).first()
        
        fine_amount = 0.0
        if issue.return_date is None and issue.due_date < datetime.utcnow():
            days_overdue = (datetime.utcnow() - issue.due_date).days
            if config:
                fine_amount = min(days_overdue * config.fine_per_day, config.max_fine_cap)
        
        # Update issue record
        issue.return_date = datetime.utcnow()
        issue.status = "RETURNED"
        issue.fine_amount = fine_amount
        
        # Increase available copies
        book = db.query(Book).filter(Book.id == issue.book_id).first()
        if book:
            book.available_copies += 1
        
        db.commit()
        db.refresh(issue)
        return issue


class LibraryFineConfigService:
    @staticmethod
    def get_config(db: Session, institution_id: int) -> Optional[LibraryFineConfig]:
        return db.query(LibraryFineConfig).filter(
            LibraryFineConfig.institution_id == institution_id,
            LibraryFineConfig.is_active == True
        ).first()
    
    @staticmethod
    def create_or_update_config(
        db: Session, 
        institution_id: int, 
        config_data: LibraryFineConfigUpdate
    ) -> LibraryFineConfig:
        config = db.query(LibraryFineConfig).filter(
            LibraryFineConfig.institution_id == institution_id
        ).first()
        
        if config:
            update_data = config_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(config, field, value)
            db.commit()
            db.refresh(config)
        else:
            config = LibraryFineConfig(
                institution_id=institution_id,
                **config_data.model_dump()
            )
            db.add(config)
            db.commit()
            db.refresh(config)
        
        return config
