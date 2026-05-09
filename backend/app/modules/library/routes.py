from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.auth import get_current_user
from app.modules.library.services import (
    AuthorService, PublisherService, BookService,
    LibraryFineConfigService
)
from app.modules.library.schemas import (
    AuthorCreate, AuthorResponse,
    PublisherCreate, PublisherResponse,
    BookCreate, BookUpdate, BookResponse,
    BookIssueCreate, BookIssueResponse,
    LibraryFineConfigCreate, LibraryFineConfigUpdate, LibraryFineConfigResponse
)

router = APIRouter(prefix="/api/v1/library", tags=["Library"])


# Author Endpoints
@router.post("/authors", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return AuthorService.create_author(db, author)


@router.get("/authors", response_model=List[AuthorResponse])
def get_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return AuthorService.get_authors(db, skip, limit)


# Publisher Endpoints
@router.post("/publishers", response_model=PublisherResponse)
def create_publisher(publisher: PublisherCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return PublisherService.create_publisher(db, publisher)


@router.get("/publishers", response_model=List[PublisherResponse])
def get_publishers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return PublisherService.get_publishers(db, skip, limit)


# Book Endpoints
@router.post("/books", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        return BookService.create_book(db, book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/books", response_model=List[BookResponse])
def get_books(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return BookService.get_books(db, skip, limit, category, search)


@router.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    book = BookService.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    book = BookService.update_book(db, book_id, book_update)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    success = BookService.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


# Book Issue Endpoints
@router.post("/books/{book_id}/issue", response_model=BookIssueResponse)
def issue_book(
    book_id: int,
    issue_data: BookIssueCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return BookService.issue_book(
            db=db,
            book_id=book_id,
            student_id=issue_data.student_id,
            due_date=issue_data.due_date,
            issued_by=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/issues/{issue_id}/return", response_model=BookIssueResponse)
def return_book(issue_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        return BookService.return_book(db, issue_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Fine Configuration Endpoints
@router.get("/config", response_model=LibraryFineConfigResponse)
def get_fine_config(institution_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    config = LibraryFineConfigService.get_config(db, institution_id)
    if not config:
        raise HTTPException(status_code=404, detail="Fine configuration not found")
    return config


@router.post("/config", response_model=LibraryFineConfigResponse)
def create_or_update_fine_config(
    config_data: LibraryFineConfigUpdate,
    institution_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return LibraryFineConfigService.create_or_update_config(db, institution_id, config_data)
