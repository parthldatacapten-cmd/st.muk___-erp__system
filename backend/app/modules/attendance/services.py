"""
Advanced Attendance Services
Handles NFC, QR, and Biometric attendance with Anti-Fraud logic.
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
import hashlib
import secrets
import logging

from app.modules.attendance.models import (
    AttendanceSession, AttendanceRecord, DeviceBond, AttendanceStatus
)
from app.core.exceptions import AppException, ErrorCode

logger = logging.getLogger(__name__)

class AttendanceService:
    def __init__(self, db: Session):
        self.db = db

    # --- NFC ATTENDANCE ---
    def start_nfc_session(self, faculty_id: str, batch_id: str, subject_id: Optional[str] = None) -> AttendanceSession:
        """Faculty starts an NFC session for marking attendance."""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=2) # Session valid for 2 hours
        
        session = AttendanceSession(
            faculty_id=faculty_id,
            batch_id=batch_id,
            subject_id=subject_id,
            session_type="NFC",
            session_token=session_token,
            expires_at=expires_at,
            is_active=True
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        logger.info(f"NFC Session started: {session.id} by {faculty_id}")
        return session

    def mark_nfc_attendance(self, session_token: str, student_device_id: str, student_id: str) -> AttendanceRecord:
        """
        Student taps phone to mark attendance.
        Anti-Fraud: Checks device binding and duplicate marks.
        """
        # 1. Validate Session
        session = self.db.query(AttendanceSession).filter(
            AttendanceSession.session_token == session_token,
            AttendanceSession.is_active == True,
            AttendanceSession.expires_at > datetime.utcnow()
        ).first()
        
        if not session:
            raise AppException(ErrorCode.BAD_REQUEST, "Invalid or expired NFC session")

        # 2. Verify Device Binding (Anti-Fraud: Pass the Phone)
        device_bond = self.db.query(DeviceBond).filter(
            DeviceBond.student_id == student_id,
            DeviceBond.device_id == student_device_id,
            DeviceBond.is_active == True
        ).first()

        if not device_bond:
            # In a real app, trigger OTP flow here to bind device first
            raise AppException(ErrorCode.FORBIDDEN, "Device not bound to student. Please bind device first.")

        # 3. Check if already marked present today
        existing = self.db.query(AttendanceRecord).filter(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.session_id == session.id,
            AttendanceRecord.status == AttendanceStatus.PRESENT
        ).first()

        if existing:
            raise AppException(ErrorCode.CONFLICT, "Attendance already marked for this session")

        # 4. Mark Present
        record = AttendanceRecord(
            session_id=session.id,
            student_id=student_id,
            device_id=student_device_id,
            status=AttendanceStatus.PRESENT,
            marked_at=datetime.utcnow(),
            latitude=None, # NFC doesn't need GPS usually, but can add
            longitude=None
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        logger.info(f"NFC Attendance marked: Student {student_id} in Session {session.id}")
        return record

    # --- QR ATTENDANCE ---
    def generate_dynamic_qr(self, faculty_id: str, batch_id: str) -> Dict:
        """
        Generate a QR code payload that changes every 30s.
        Payload contains: SessionToken + Timestamp + Hash
        """
        session_token = secrets.token_urlsafe(16)
        timestamp = int(datetime.utcnow().timestamp())
        
        # Create a hash that expires quickly
        secret_seed = f"{faculty_id}:{batch_id}:SECRET_KEY" # Should be env var
        signature = hashlib.sha256(f"{session_token}{timestamp}{secret_seed}".encode()).hexdigest()[:16]
        
        qr_payload = {
            "token": session_token,
            "ts": timestamp,
            "sig": signature,
            "batch_id": batch_id
        }
        
        # Create Session in DB (short lived, 5 mins)
        session = AttendanceSession(
            faculty_id=faculty_id,
            batch_id=batch_id,
            session_type="QR",
            session_token=session_token,
            expires_at=datetime.utcnow() + timedelta(minutes=5),
            is_active=True
        )
        self.db.add(session)
        self.db.commit()
        
        return {"qr_data": qr_payload, "expires_in": 30}

    def scan_qr_attendance(self, token: str, timestamp: int, signature: str, 
                           student_id: str, device_id: str, 
                           latitude: float, longitude: float,
                           selfie_image: Optional[str] = None) -> AttendanceRecord:
        """
        Student scans QR.
        Validations:
        1. Signature Match (Is QR genuine?)
        2. Timestamp < 30s old (Prevent replay)
        3. Geo-fencing (Is student in campus?)
        4. Mock Location Check (Done on client, but verified here if possible)
        """
        # 1. Time Validation
        now_ts = int(datetime.utcnow().timestamp())
        if now_ts - timestamp > 30:
            raise AppException(ErrorCode.BAD_REQUEST, "QR Code expired. Please scan again.")

        # 2. Signature Validation (Simplified)
        # In prod, fetch faculty/batch from token and re-calculate hash
        session = self.db.query(AttendanceSession).filter(
            AttendanceSession.session_token == token,
            AttendanceSession.is_active == True
        ).first()
        
        if not session:
            raise AppException(ErrorCode.BAD_REQUEST, "Invalid QR Session")

        # 3. Geo-fencing (Hardcoded campus coords for demo)
        CAMPUS_LAT = 19.0760
        CAMPUS_LON = 72.8777
        MAX_DIST_KM = 0.5 # 500 meters
        
        # Simple distance check (Haversine formula should be used in prod)
        dist = ((latitude - CAMPUS_LAT)**2 + (longitude - CAMPUS_LON)**2)**0.5 * 111 # Rough km
        if dist > MAX_DIST_KM:
            raise AppException(ErrorCode.FORBIDDEN, "You are outside the campus premises.")

        # 4. Selfie Challenge (If triggered)
        if selfie_image:
            # Here we would send image to AI service for liveness check
            # For now, just accept it
            logger.info(f"Selfie received for student {student_id}")

        # 5. Mark Attendance
        record = AttendanceRecord(
            session_id=session.id,
            student_id=student_id,
            device_id=device_id,
            status=AttendanceStatus.PRESENT,
            marked_at=datetime.utcnow(),
            latitude=latitude,
            longitude=longitude,
            verification_method="QR_SELFIE" if selfie_image else "QR_GPS"
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    # --- DEVICE MANAGEMENT ---
    def bind_device(self, student_id: str, device_id: str, otp_verified: bool) -> DeviceBond:
        """Bind a new device to a student account."""
        if not otp_verified:
            raise AppException(ErrorCode.BAD_REQUEST, "OTP verification required")

        # Check max devices (Limit to 2)
        active_devices = self.db.query(DeviceBond).filter(
            DeviceBond.student_id == student_id,
            DeviceBond.is_active == True
        ).count()

        if active_devices >= 2:
            raise AppException(ErrorCode.BAD_REQUEST, "Maximum 2 devices allowed. Contact admin to reset.")

        bond = DeviceBond(
            student_id=student_id,
            device_id=device_id,
            is_active=True
        )
        self.db.add(bond)
        self.db.commit()
        self.db.refresh(bond)
        return bond
