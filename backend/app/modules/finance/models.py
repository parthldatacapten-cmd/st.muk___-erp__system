"""
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
