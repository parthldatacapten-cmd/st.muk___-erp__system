"""
Attendance Routes
Endpoints for NFC, QR, and Device Management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.modules.attendance.services import AttendanceService
from app.modules.attendance.schemas import (
    NFCSessionCreate, NFCMarkCreate, 
    QRGenerateResponse, QRScanCreate, 
    DeviceBindCreate, AttendanceRecordResponse
)
from app.core.security import get_current_user
from app.modules.user.models import User

router = APIRouter(prefix="/api/v1/attendance", tags=["Attendance"])

@router.post("/nfc/session", response_model=dict)
def start_nfc_session(
    payload: NFCSessionCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Faculty starts an NFC session."""
    service = AttendanceService(db)
    session = service.start_nfc_session(
        faculty_id=current_user.id,
        batch_id=payload.batch_id,
        subject_id=payload.subject_id
    )
    return {"session_id": session.id, "token": session.session_token, "expires_at": session.expires_at}

@router.post("/nfc/mark", response_model=AttendanceRecordResponse)
def mark_nfc(
    payload: NFCMarkCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Student taps to mark attendance."""
    service = AttendanceService(db)
    record = service.mark_nfc_attendance(
        session_token=payload.session_token,
        student_device_id=payload.device_id,
        student_id=current_user.id
    )
    return record

@router.get("/qr/generate", response_model=QRGenerateResponse)
def generate_qr(
    batch_id: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Generate dynamic QR code for projector."""
    service = AttendanceService(db)
    result = service.generate_dynamic_qr(
        faculty_id=current_user.id,
        batch_id=batch_id
    )
    return result

@router.post("/qr/scan", response_model=AttendanceRecordResponse)
def scan_qr(
    payload: QRScanCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Student scans QR code."""
    service = AttendanceService(db)
    record = service.scan_qr_attendance(
        token=payload.token,
        timestamp=payload.ts,
        signature=payload.sig,
        student_id=current_user.id,
        device_id=payload.device_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        selfie_image=payload.selfie_image
    )
    return record

@router.post("/device/bind")
def bind_device(
    payload: DeviceBindCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Bind a new device to student account (requires OTP)."""
    service = AttendanceService(db)
    bond = service.bind_device(
        student_id=current_user.id,
        device_id=payload.device_id,
        otp_verified=payload.otp_verified
    )
    return {"status": "success", "message": "Device bound successfully"}
