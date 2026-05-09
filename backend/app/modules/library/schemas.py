from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PublisherBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class PublisherCreate(PublisherBase):
    pass


class PublisherResponse(PublisherBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, max_length=20)
    author_id: int
    publisher_id: Optional[int] = None
    category: str = Field(..., min_length=1, max_length=50)
    rack_number: Optional[str] = None
    total_copies: int = Field(default=1, ge=1)
    price: Optional[float] = Field(None, ge=0)
    cover_image_url: Optional[str] = None
    description: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None
    category: Optional[str] = None
    rack_number: Optional[str] = None
    total_copies: Optional[int] = None
    price: Optional[float] = None
    cover_image_url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class BookResponse(BookBase):
    id: int
    available_copies: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    author: Optional[AuthorResponse] = None
    publisher: Optional[PublisherResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


class BookIssueBase(BaseModel):
    book_id: int
    student_id: int
    due_date: datetime


class BookIssueCreate(BookIssueBase):
    pass


class BookIssueResponse(BaseModel):
    id: int
    book_id: int
    student_id: int
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    fine_amount: float
    fine_paid: bool
    status: str
    created_at: datetime
    book: Optional[BookResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


class LibraryFineConfigBase(BaseModel):
    fine_per_day: float = Field(default=5.0, ge=0)
    max_fine_cap: float = Field(default=500.0, ge=0)
    loan_period_days: int = Field(default=14, ge=1)


class LibraryFineConfigCreate(LibraryFineConfigBase):
    institution_id: int


class LibraryFineConfigUpdate(BaseModel):
    fine_per_day: Optional[float] = None
    max_fine_cap: Optional[float] = None
    loan_period_days: Optional[int] = None
    is_active: Optional[bool] = None


class LibraryFineConfigResponse(LibraryFineConfigBase):
    id: int
    institution_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
