"""
Finance Business Logic Services
Handles fee collection, ledger updates, and immutable transaction rules.
"""
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modules.finance.models import (
    FeeHead, FeeStructure, FeeTransaction, StudentLedger, 
    ExpenseRequest, ExpenseTransaction, TransactionStatus
)
from app.modules.finance.schemas import (
    FeeCollectionCreate, FeeReversalCreate, ExpenseRequestCreate
)
from app.core.exceptions import AppException, ErrorCode
import logging

logger = logging.getLogger(__name__)

class FinanceService:
    def __init__(self, db: Session):
        self.db = db

    # --- FEE COLLECTION ---
    def collect_fee(self, payload: FeeCollectionCreate, institution_id: str) -> FeeTransaction:
        """
        Collect fee from student.
        CRITICAL: Creates an immutable record. Cannot be deleted later.
        """
        try:
            # 1. Validate Student & Structure
            student = self._get_student(payload.student_id)
            if not student:
                raise AppException(ErrorCode.NOT_FOUND, "Student not found")
            
            structure = self._get_active_structure(student.batch_id, payload.academic_year_id)
            if not structure:
                raise AppException(ErrorCode.BAD_REQUEST, "No fee structure defined for this batch/year")

            # 2. Calculate Due & Late Fees
            current_due = self.get_student_due(student.id)
            late_fee = 0.0
            if payload.is_late_fee_applicable:
                late_fee = self._calculate_late_fee(current_due, student.institution_id)

            total_amount = payload.amount + late_fee

            # 3. Create Transaction (Immutable)
            transaction = FeeTransaction(
                institution_id=institution_id,
                student_id=student.id,
                amount=total_amount,
                principal_amount=payload.amount,
                late_fee_amount=late_fee,
                payment_mode=payload.payment_mode,
                transaction_ref=payload.transaction_ref,
                cheque_number=payload.cheque_number,
                remarks=payload.remarks,
                status=TransactionStatus.COMPLETED,
                collected_by=payload.collected_by, # User ID of cashier
                is_reversed=False
            )
            
            self.db.add(transaction)
            self.db.flush() # Get ID before commit

            # 4. Update Student Ledger
            ledger_entry = StudentLedger(
                institution_id=institution_id,
                student_id=student.id,
                transaction_id=transaction.id,
                entry_type="CREDIT", # Money coming in
                amount=total_amount,
                balance_after=self._calculate_new_balance(student.id, total_amount, "CREDIT"),
                description=f"Fee collected via {payload.payment_mode}",
                posted_date=datetime.utcnow()
            )
            self.db.add(ledger_entry)

            self.db.commit()
            self.db.refresh(transaction)
            
            logger.info(f"Fee collected: {transaction.id} for Student {student.id}")
            return transaction

        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Database integrity error: {e}")
            raise AppException(ErrorCode.DATABASE_ERROR, "Failed to record transaction")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Unexpected error: {e}")
            raise e

    def reverse_transaction(self, payload: FeeReversalCreate, admin_user_id: str) -> FeeTransaction:
        """
        Reverse a transaction.
        CRITICAL: Does NOT delete the original record. Creates a negative entry.
        Requires mandatory reason.
        """
        if not payload.reason or len(payload.reason) < 10:
            raise AppException(ErrorCode.VALIDATION_ERROR, "Reversal reason must be at least 10 characters")

        original_txn = self.db.query(FeeTransaction).filter(
            FeeTransaction.id == payload.transaction_id,
            FeeTransaction.is_reversed == False
        ).first()

        if not original_txn:
            raise AppException(ErrorCode.NOT_FOUND, "Original transaction not found or already reversed")

        # 1. Mark Original as Reversed (Logical Delete)
        original_txn.is_reversed = True
        original_txn.reversed_at = datetime.utcnow()
        original_txn.reversed_by = admin_user_id

        # 2. Create Negative Transaction
        reverse_txn = FeeTransaction(
            institution_id=original_txn.institution_id,
            student_id=original_txn.student_id,
            amount=-original_txn.amount, # Negative amount
            principal_amount=-original_txn.principal_amount,
            late_fee_amount=-original_txn.late_fee_amount,
            payment_mode="REVERSAL",
            transaction_ref=f"REV-{original_txn.id}",
            remarks=f"REVERSED: {payload.reason}",
            status=TransactionStatus.REVERSED,
            collected_by=admin_user_id,
            is_reversed=False, # This is a new active record
            reverses_original_id=original_txn.id
        )
        self.db.add(reverse_txn)
        self.db.flush()

        # 3. Update Ledger with Debit Entry
        ledger_entry = StudentLedger(
            institution_id=original_txn.institution_id,
            student_id=original_txn.student_id,
            transaction_id=reverse_txn.id,
            entry_type="DEBIT", # Money going out (refund/adjustment)
            amount=original_txn.amount,
            balance_after=self._calculate_new_balance(original_txn.student_id, original_txn.amount, "DEBIT"),
            description=f"Transaction Reversed: {payload.reason}",
            posted_date=datetime.utcnow()
        )
        self.db.add(ledger_entry)

        self.db.commit()
        self.db.refresh(reverse_txn)
        
        logger.warning(f"Transaction {original_txn.id} reversed by {admin_user_id}. Reason: {payload.reason}")
        return reverse_txn

    def get_student_due(self, student_id: str) -> float:
        """Calculate total pending dues for a student."""
        # Sum of all defined fee structures - Sum of all paid transactions
        # Simplified logic for now
        ledgers = self.db.query(StudentLedger).filter(
            StudentLedger.student_id == student_id
        ).all()
        
        balance = sum(l.amount if l.entry_type == "DEBIT" else -l.amount for l in ledgers)
        return max(0, balance) # Dues cannot be negative

    def _calculate_new_balance(self, student_id: str, amount: float, type: str) -> float:
        current_due = self.get_student_due(student_id)
        if type == "CREDIT":
            return max(0, current_due - amount)
        else:
            return current_due + amount

    def _get_student(self, student_id: str):
        from app.modules.student.models import Student
        return self.db.query(Student).filter(Student.id == student_id).first()

    def _get_active_structure(self, batch_id: str, year_id: str):
        return self.db.query(FeeStructure).filter(
            FeeStructure.batch_id == batch_id,
            FeeStructure.academic_year_id == year_id,
            FeeStructure.is_active == True
        ).first()

    def _calculate_late_fee(self, due: float, institution_id: str) -> float:
        # Fetch institution config for late fee %
        return 0.0 # Placeholder
