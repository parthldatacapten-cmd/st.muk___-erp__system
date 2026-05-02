# 13. API Design Specification - Phase 1 (MVP)

## 1. API Architecture Overview

### 1.1 Design Principles
- **RESTful**: Resource-based URLs with standard HTTP verbs
- **Stateless**: JWT authentication, no server-side sessions
- **Versioned**: All endpoints prefixed with `/api/v1/`
- **Consistent Response Format**: Standardized JSON structure
- **Error Handling**: RFC 7807 Problem Details format
- **Rate Limiting**: 100 requests/minute per user, 1000/minute for institute-level

### 1.2 Base URL Structure
```
Production: https://api.educore.in/api/v1/
Staging:    https://staging-api.educore.in/api/v1/
Local Dev:  http://localhost:8000/api/v1/
```

### 1.3 Technology Stack
- **Framework**: FastAPI (Python 3.11+)
- **Documentation**: Auto-generated OpenAPI 3.0 (Swagger UI + ReDoc)
- **Serialization**: Pydantic v2
- **Database ORM**: SQLAlchemy 2.0 (Async)
- **Caching**: Redis for rate limiting & session storage

---

## 2. Authentication & Authorization APIs

### 2.1 Login Flow
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin@stxaviers.edu.in",
  "password": "SecurePass123!",
  "role": "admin",
  "institution_id": "INST_2024_001"
}

Response 200 OK:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "usr_12345",
    "email": "admin@stxaviers.edu.in",
    "role": "admin",
    "institution_id": "INST_2024_001",
    "permissions": ["read:all", "write:all"]
  }
}
```

### 2.2 OTP Verification (2FA)
```http
POST /api/v1/auth/verify-otp
Content-Type: application/json

{
  "phone": "+919876543210",
  "otp": "123456",
  "device_id": "android_abc123xyz"
}

Response 200 OK:
{
  "access_token": "...",
  "device_bound": true,
  "message": "Device successfully bound to account"
}
```

### 2.3 Token Refresh
```http
POST /api/v1/auth/refresh
Authorization: Bearer <refresh_token>

Response 200 OK:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

### 2.4 Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>

Response 204 No Content
```

---

## 3. Core Module APIs

### 3.1 User Management

#### List Users (Paginated)
```http
GET /api/v1/users?role=faculty&page=1&limit=20&search=sharma
Authorization: Bearer <token>

Response 200 OK:
{
  "data": [
    {
      "id": "usr_67890",
      "name": "Prof. Rajesh Sharma",
      "email": "rajesh.sharma@stxaviers.edu.in",
      "role": "faculty",
      "department": "Physics",
      "employee_id": "EMP_2023_045",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "total_pages": 3
  }
}
```

#### Create User
```http
POST /api/v1/users
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Dr. Priya Patel",
  "email": "priya.patel@stxaviers.edu.in",
  "phone": "+919876543210",
  "role": "faculty",
  "department": "Chemistry",
  "employee_id": "EMP_2024_089",
  "password": "TempPass123!",
  "require_password_change": true
}

Response 201 Created:
{
  "id": "usr_99999",
  "message": "User created successfully. OTP sent to phone."
}
```

### 3.2 Student Admission

#### Submit Application
```http
POST /api/v1/admissions/apply
Content-Type: multipart/form-data

FormData:
- student_name: "Amit Kumar"
- dob: "2006-05-15"
- gender: "male"
- category: "general"
- stream: "science"
- father_name: "Suresh Kumar"
- mother_name: "Sunita Kumar"
- phone: "+919876543210"
- email: "amit.kumar@email.com"
- address: "123 MG Road, Pune, Maharashtra"
- aadhar_card: [file]
- marksheets: [file, file]
- photo: [file]

Response 201 Created:
{
  "application_id": "APP_2024_00123",
  "status": "pending_review",
  "message": "Application submitted. Reference ID sent via SMS."
}
```

#### Approve/Reject Application
```http
PATCH /api/v1/admissions/{application_id}/decision
Authorization: Bearer <token>
Content-Type: application/json

{
  "decision": "approve",
  "batch_id": "BATCH_SCI_2024_01",
  "fee_structure_id": "FEE_SCI_REGULAR",
  "remarks": "All documents verified. Merit list rank: 45"
}

Response 200 OK:
{
  "student_id": "STU_2024_00123",
  "roll_number": "2024SCI045",
  "message": "Application approved. Student ID generated."
}
```

### 3.3 Attendance

#### Generate Dynamic QR
```http
POST /api/v1/attendance/sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "batch_id": "BATCH_SCI_2024_01",
  "subject_id": "SUB_PHY_101",
  "scheduled_start": "2024-10-15T10:00:00Z",
  "scheduled_end": "2024-10-15T11:30:00Z",
  "location": {
    "latitude": 18.5204,
    "longitude": 73.8567,
    "radius_meters": 100
  }
}

Response 201 Created:
{
  "session_id": "SES_20241015_001",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "qr_content": "https://educore.in/a/SES_20241015_001?tok=abc123",
  "valid_until": "2024-10-15T10:00:30Z",
  "refresh_interval_seconds": 30
}
```

#### Mark Attendance (Student)
```http
POST /api/v1/attendance/mark
Authorization: Bearer <token>
Content-Type: application/json

{
  "session_id": "SES_20241015_001",
  "scanned_qr_token": "abc123",
  "location": {
    "latitude": 18.5205,
    "longitude": 73.8568,
    "accuracy_meters": 15,
    "mock_location_detected": false
  },
  "device_id": "android_abc123xyz",
  "selfie_image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..." // Optional, if triggered
}

Response 200 OK:
{
  "status": "success",
  "attendance_id": "ATT_20241015_00123",
  "marked_at": "2024-10-15T10:05:23Z",
  "selfie_required_next_time": false
}

Response 403 Forbidden (Proxy detected):
{
  "error": "proxy_suspected",
  "message": "Attendance marked from different device. Selfie verification required.",
  "action_required": "upload_selfie"
}
```

#### Get Attendance Report
```http
GET /api/v1/attendance/batch/{batch_id}/report?from=2024-10-01&to=2024-10-31
Authorization: Bearer <token>

Response 200 OK:
{
  "batch_id": "BATCH_SCI_2024_01",
  "period": {
    "from": "2024-10-01",
    "to": "2024-10-31"
  },
  "summary": {
    "total_working_days": 22,
    "average_attendance_percent": 87.5
  },
  "students": [
    {
      "student_id": "STU_2024_00123",
      "name": "Amit Kumar",
      "present": 20,
      "absent": 2,
      "percentage": 90.9,
      "proxy_alerts": 0
    }
  ]
}
```

### 3.4 Fee Management

#### Create Fee Invoice
```http
POST /api/v1/fees/invoices
Authorization: Bearer <token>
Content-Type: application/json

{
  "student_id": "STU_2024_00123",
  "installment_number": 1,
  "due_date": "2024-11-30",
  "items": [
    {
      "description": "Tuition Fee - Semester 1",
      "amount": 45000,
      "tax_rate": 18,
      "tax_amount": 8100
    },
    {
      "description": "Library Fee",
      "amount": 2000,
      "tax_rate": 18,
      "tax_amount": 360
    }
  ],
  "discount": {
    "type": "scholarship",
    "amount": 5000,
    "reason": "Merit Scholarship - Rank 45"
  }
}

Response 201 Created:
{
  "invoice_id": "INV_2024_00123_01",
  "total_amount": 50460,
  "gst_number": "27ABCDE1234F1Z5",
  "pdf_url": "https://educore.in/invoices/INV_2024_00123_01.pdf"
}
```

#### Record Payment
```http
POST /api/v1/fees/payments
Authorization: Bearer <token>
Content-Type: application/json

{
  "invoice_id": "INV_2024_00123_01",
  "payment_mode": "upi",
  "transaction_id": "UPI_1234567890_ABCDEF",
  "amount_paid": 50460,
  "payment_gateway_response": {
    "gateway": "razorpay",
    "order_id": "order_abc123",
    "payment_id": "pay_xyz789",
    "signature": "signature_hash"
  },
  "collected_by": "usr_receptionist_01",
  "collected_at": "2024-10-15T14:30:00Z"
}

Response 201 Created:
{
  "payment_id": "PAY_2024_00567",
  "receipt_number": "RCP_2024_00123",
  "receipt_pdf_url": "https://educore.in/receipts/RCP_2024_00123.pdf",
  "sms_sent": true
}
```

#### Reverse Payment (Immutable Ledger)
```http
POST /api/v1/fees/payments/{payment_id}/reverse
Authorization: Bearer <token>
Content-Type: application/json

{
  "reason": "Duplicate payment received. Original transaction to be refunded.",
  "refund_mode": "bank_transfer",
  "refund_account_details": {
    "account_number": "1234567890",
    "ifsc": "SBIN0001234",
    "account_holder": "Amit Kumar"
  },
  "approved_by": "usr_admin_01"
}

Response 200 OK:
{
  "reversal_id": "REV_2024_00012",
  "original_payment_id": "PAY_2024_00567",
  "status": "pending_refund",
  "audit_trail": {
    "original_record_preserved": true,
    "reversed_at": "2024-10-16T09:00:00Z",
    "reversed_by": "usr_admin_01"
  }
}
```

### 3.5 Examination & Assessment

#### Create Test
```http
POST /api/v1/exams/tests
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "JEE Mock Test - Physics #5",
  "subject_id": "SUB_PHY_101",
  "batch_id": "BATCH_SCI_2024_01",
  "duration_minutes": 180,
  "total_marks": 300,
  "marking_scheme": {
    "correct": 4,
    "incorrect": -1,
    "unattempted": 0,
    "partial_marks_enabled": false
  },
  "questions": [
    {
      "question_id": "Q_PHY_00123",
      "order": 1,
      "marks": 4
    },
    {
      "question_id": "Q_PHY_00456",
      "order": 2,
      "marks": 4
    }
  ],
  "scheduled_start": "2024-10-20T10:00:00Z",
  "scheduled_end": "2024-10-20T13:00:00Z",
  "randomize_questions": true,
  "randomize_options": true
}

Response 201 Created:
{
  "test_id": "TEST_2024_089",
  "student_count": 120,
  "hall_tickets_generated": true,
  "cbt_interface_url": "https://cbt.educore.in/test/TEST_2024_089"
}
```

#### Submit Test Answer (Student)
```http
POST /api/v1/exams/tests/{test_id}/submit
Authorization: Bearer <token>
Content-Type: application/json

{
  "responses": [
    {
      "question_id": "Q_PHY_00123",
      "selected_option": "B",
      "flagged_for_review": false
    },
    {
      "question_id": "Q_PHY_00456",
      "selected_option": null,
      "flagged_for_review": true
    }
  ],
  "time_taken_seconds": 10245,
  "submitted_at": "2024-10-20T12:50:45Z"
}

Response 200 OK:
{
  "submission_id": "SUB_2024_00123",
  "instant_score": 156,
  "percentile": 78.5,
  "all_india_rank": 2345,
  "answer_key_available_after": "2024-10-20T18:00:00Z"
}
```

#### Recalculate Scores (After Question Change)
```http
POST /api/v1/exams/tests/{test_id}/recalculate
Authorization: Bearer <token>
Content-Type: application/json

{
  "question_id": "Q_PHY_00789",
  "action": "mark_bonus",
  "reason": "Question statement had incorrect data. All students to receive full marks.",
  "trigger_recalculation": true
}

Response 202 Accepted:
{
  "job_id": "JOB_RECALC_20241020_001",
  "status": "processing",
  "affected_students": 120,
  "estimated_completion": "2024-10-20T15:05:00Z",
  "webhook_url": "https://educore.in/webhooks/recalc-complete"
}
```

### 3.6 LMS (Learning Management System)

#### Upload Study Material
```http
POST /api/v1/lms/materials
Authorization: Bearer <token>
Content-Type: multipart/form-data

FormData:
- batch_id: BATCH_SCI_2024_01
- subject_id: SUB_PHY_101
- chapter_id: CHAP_PHY_01
- title: "Electrostatics - Lecture Notes"
- description: "Comprehensive notes covering Coulomb's law, electric field, and potential"
- file_type: pdf
- file: [file]
- watermark_enabled: true
- drip_schedule:
    unlock_date: 2024-10-25
    prerequisite_chapter_ids: ["CHAP_PHY_00"]

Response 201 Created:
{
  "material_id": "MAT_2024_567",
  "storage_url": "https://cdn.educore.in/materials/MAT_2024_567.pdf",
  "watermark_applied": true,
  "unlock_date": "2024-10-25T00:00:00Z"
}
```

#### Stream Video (HLS)
```http
GET /api/v1/lms/videos/{video_id}/playlist.m3u8
Authorization: Bearer <token>

Response 200 OK:
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360
https://cdn.educore.in/videos/VID_123/360p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=1280x720
https://cdn.educore.in/videos/VID_123/720p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1920x1080
https://cdn.educore.in/videos/VID_123/1080p.m3u8
```

---

## 4. Error Handling Standards

### 4.1 Error Response Format (RFC 7807)
```json
{
  "type": "https://educore.in/errors/proxy-attendance-detected",
  "title": "Proxy Attendance Suspected",
  "status": 403,
  "detail": "Attendance marked from a different device than registered. Selfie verification required.",
  "instance": "/api/v1/attendance/mark",
  "trace_id": "req_abc123xyz789",
  "timestamp": "2024-10-15T10:05:23Z",
  "errors": [
    {
      "field": "device_id",
      "message": "Device mismatch. Registered device: android_xyz789, Current device: android_abc123"
    }
  ],
  "action_required": {
    "type": "upload_selfie",
    "endpoint": "/api/v1/attendance/verify-selfie",
    "method": "POST"
  }
}
```

### 4.2 Common HTTP Status Codes
| Code | Meaning | Usage Example |
|------|---------|---------------|
| 200 | OK | Successful GET, PATCH |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors, malformed JSON |
| 401 | Unauthorized | Missing or expired token |
| 403 | Forbidden | Insufficient permissions, proxy detected |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate entry, constraint violation |
| 422 | Unprocessable Entity | Business logic validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |

---

## 5. Rate Limiting & Throttling

### 5.1 Limits by Endpoint Category
| Category | Limit | Window | Burst |
|----------|-------|--------|-------|
| Authentication | 10 req/min | 1 min | 5 |
| Attendance Marking | 3 req/min | 1 min | 2 |
| Fee Payments | 20 req/min | 1 min | 10 |
| Exam Submission | 5 req/min | 1 min | 3 |
| File Uploads | 10 req/min | 1 min | 5 |
| General Queries | 100 req/min | 1 min | 50 |

### 5.2 Rate Limit Headers
```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1697380800
Retry-After: 60
```

### 5.3 Rate Limit Exceeded Response
```json
{
  "type": "https://educore.in/errors/rate-limit-exceeded",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "You have exceeded the rate limit of 100 requests per minute.",
  "retry_after": 60
}
```

---

## 6. Webhooks (Event Notifications)

### 6.1 Supported Events
| Event | Trigger | Payload Example |
|-------|---------|-----------------|
| `payment.success` | Fee payment completed | `{payment_id, student_id, amount, timestamp}` |
| `attendance.proxy_detected` | Suspicious attendance pattern | `{student_id, session_id, reason, device_info}` |
| `exam.recalculation_complete` | Score recalculation finished | `{test_id, affected_count, job_id}` |
| `admission.approved` | Student admission approved | `{application_id, student_id, batch_id}` |
| `fee.defaulter_threshold` | Student crosses 30 days overdue | `{student_id, outstanding_amount, days_overdue}` |

### 6.2 Webhook Registration
```http
POST /api/v1/webhooks/subscriptions
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://stxaviers.edu.in/webhooks/educore",
  "events": ["payment.success", "attendance.proxy_detected"],
  "secret": "whsec_abc123xyz789",
  "active": true
}

Response 201 Created:
{
  "subscription_id": "WH_SUB_001",
  "verification_token": "verify_abc123"
}
```

### 6.3 Webhook Signature Verification
```python
# Python example for verifying webhook signature
import hmac
import hashlib

def verify_webhook(payload: str, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

---

## 7. Versioning Strategy

### 7.1 URL Versioning
- All endpoints prefixed with `/api/v{version}/`
- Current version: `v1`
- Deprecation policy: 6 months notice before retiring a version

### 7.2 Backward Compatibility Rules
1. **Never break existing clients**: Add new fields, don't remove old ones
2. **Use optional fields**: New features get optional parameters
3. **Deprecation headers**: Mark deprecated fields with `X-Deprecated` header
4. **Changelog**: Maintain `/api/changelog.json` with all changes

### 7.3 Deprecation Example
```http
GET /api/v1/users/123
X-Deprecated: true
X-Deprecation-Notice: "Field 'phone' is deprecated. Use 'phones[0].number' instead."
X-Sunset-Date: "2025-04-30"
```

---

## 8. API Documentation & Testing

### 8.1 Auto-Generated Docs
- **Swagger UI**: `https://api.educore.in/docs`
- **ReDoc**: `https://api.educore.in/redoc`
- **OpenAPI JSON**: `https://api.educore.in/openapi.json`

### 8.2 Postman Collection
- Published collection: `EduCore ERP API v1`
- Environment variables for dev/staging/prod
- Pre-request scripts for JWT token refresh

### 8.3 Testing Strategy
| Type | Tool | Coverage Target |
|------|------|-----------------|
| Unit Tests | pytest | 90%+ |
| Integration Tests | pytest + TestClient | All critical paths |
| Contract Tests | Schemathesis | OpenAPI compliance |
| Load Tests | k6 | 1000 concurrent users |
| Security Tests | OWASP ZAP | Zero critical vulnerabilities |

---

## 9. Security Best Practices

### 9.1 Input Validation
- All inputs validated with Pydantic models
- SQL injection prevention via SQLAlchemy ORM
- XSS prevention via output encoding
- File upload restrictions (type, size, virus scan)

### 9.2 Authentication
- JWT tokens with RS256 signing
- Short-lived access tokens (1 hour)
- Long-lived refresh tokens (7 days, rotating)
- Device binding for sensitive operations

### 9.3 Authorization
- Role-Based Access Control (RBAC)
- Resource-level permissions
- Audit logging for all write operations

### 9.4 Data Protection
- HTTPS everywhere (TLS 1.3)
- Encryption at rest for sensitive data (AES-256)
- PII masking in logs
- GDPR-compliant data export/delete endpoints

---

## 10. Monitoring & Observability

### 10.1 Logging Standards
```json
{
  "timestamp": "2024-10-15T10:05:23Z",
  "level": "INFO",
  "service": "educore-api",
  "trace_id": "abc123xyz789",
  "span_id": "def456",
  "method": "POST",
  "path": "/api/v1/attendance/mark",
  "status_code": 200,
  "duration_ms": 145,
  "user_id": "usr_student_00123",
  "institution_id": "INST_2024_001"
}
```

### 10.2 Metrics to Track
- Request rate (req/s)
- Error rate (%)
- P50/P95/P99 latency
- Database query performance
- Cache hit ratio
- Rate limit violations

### 10.3 Alerting Rules
| Metric | Threshold | Action |
|--------|-----------|--------|
| Error Rate | >5% for 5 min | Page on-call engineer |
| P99 Latency | >2s for 10 min | Investigate performance |
| Database CPU | >80% for 15 min | Scale up DB |
| Failed Logins | >100/min from single IP | Block IP, security alert |

---

**Document Status**: ✅ Complete  
**Next Step**: Implement API endpoints following these specifications  
**Approval Required**: Tech lead sign-off before Sprint 1 development
