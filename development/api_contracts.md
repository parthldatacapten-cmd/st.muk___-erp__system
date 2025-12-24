# API Contracts & Specifications

## Overview
This document defines the REST API contracts for the PVGS Academic & Administrative System. All APIs follow RESTful conventions with JSON responses.

## API Standards

### Base URL
```
https://api.pvgs.edu/v1
```

### Authentication
- **Type**: Bearer Token (Laravel Sanctum)
- **Header**: `Authorization: Bearer {token}`
- **Token Expiry**: 24 hours

### Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful",
  "errors": null,
  "meta": {
    "pagination": {},
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### Error Response Format
```json
{
  "success": false,
  "data": null,
  "message": "Error message",
  "errors": {
    "field_name": ["Error description"]
  },
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

## Authentication APIs

### 1. Login
**POST** `/auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "device_name": "web"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "user_type": "student",
      "roles": ["student"]
    },
    "token": "bearer_token_here",
    "token_type": "Bearer"
  },
  "message": "Login successful"
}
```

### 2. Logout
**POST** `/auth/logout`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### 3. Get Current User
**GET** `/auth/user`

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "user_type": "student",
    "profile": {
      "student_id": "STU001",
      "program": "BSc Computer Science",
      "batch": "2023-2026"
    }
  }
}
```

## Student Management APIs

### 1. Get All Students
**GET** `/students`

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 15)
- `program_id`: Filter by program
- `batch_id`: Filter by batch
- `status`: Filter by status (active, inactive, graduated)
- `search`: Search by name or student ID

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "student_id": "STU001",
      "user": {
        "name": "John Doe",
        "email": "john@example.com"
      },
      "program": {
        "name": "BSc Computer Science"
      },
      "batch": {
        "name": "2023-2026"
      },
      "status": "active"
    }
  ],
  "meta": {
    "pagination": {
      "current_page": 1,
      "per_page": 15,
      "total": 150,
      "last_page": 10
    }
  }
}
```

### 2. Get Student Details
**GET** `/students/{id}`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "student_id": "STU001",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "2000-01-01",
    "gender": "male",
    "address": "123 Main St, City",
    "phone": "+1234567890",
    "emergency_contact": "+0987654321",
    "program": {
      "id": 1,
      "name": "BSc Computer Science",
      "duration_years": 3
    },
    "batch": {
      "id": 1,
      "name": "2023-2026"
    },
    "enrollments": [
      {
        "semester": "Semester 1",
        "subjects": ["Mathematics", "Physics"]
      }
    ],
    "status": "active",
    "created_at": "2023-06-01T00:00:00Z"
  }
}
```

### 3. Create Student
**POST** `/students`

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "date_of_birth": "2000-01-01",
  "gender": "male",
  "address": "123 Main St, City",
  "emergency_contact": "+0987654321",
  "program_id": 1,
  "batch_id": 1
}
```

### 4. Update Student
**PUT** `/students/{id}`

**Request:** Same as create, plus optional fields

### 5. Delete Student
**DELETE** `/students/{id}`

## Academic Structure APIs

### 1. Get Programs
**GET** `/programs`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "program_code": "BSC_CS",
      "program_name": "BSc Computer Science",
      "description": "Bachelor of Science in Computer Science",
      "duration_years": 3,
      "total_semesters": 6,
      "total_fees": 150000.00,
      "is_active": true
    }
  ]
}
```

### 2. Get Subjects by Program
**GET** `/programs/{program_id}/subjects`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "subject_code": "CS101",
      "subject_name": "Introduction to Programming",
      "credits": 4,
      "type": "both",
      "theory_marks": 60,
      "practical_marks": 40,
      "is_active": true
    }
  ]
}
```

## Attendance APIs

### 1. Mark Attendance
**POST** `/attendance`

**Request:**
```json
{
  "subject_id": 1,
  "batch_id": 1,
  "faculty_id": 1,
  "attendance_date": "2024-01-01",
  "start_time": "09:00",
  "end_time": "10:00",
  "session_type": "theory",
  "topic": "Introduction to Programming",
  "students": [
    {
      "student_id": 1,
      "status": "present"
    },
    {
      "student_id": 2,
      "status": "absent",
      "remarks": "Medical leave"
    }
  ]
}
```

### 2. Get Attendance Report
**GET** `/attendance/report`

**Query Parameters:**
- `student_id`: Filter by student
- `subject_id`: Filter by subject
- `batch_id`: Filter by batch
- `start_date`: Start date (YYYY-MM-DD)
- `end_date`: End date (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "data": {
    "student": {
      "name": "John Doe",
      "student_id": "STU001"
    },
    "subject": {
      "name": "Mathematics"
    },
    "total_sessions": 30,
    "present_count": 28,
    "absent_count": 2,
    "attendance_percentage": 93.33,
    "records": [
      {
        "date": "2024-01-01",
        "status": "present",
        "topic": "Algebra"
      }
    ]
  }
}
```

## Financial APIs

### 1. Get Student Fees
**GET** `/students/{student_id}/fees`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "fee_category": "Tuition Fee",
      "total_amount": 50000.00,
      "paid_amount": 25000.00,
      "pending_amount": 25000.00,
      "status": "partial",
      "due_date": "2024-02-01",
      "installments": [
        {
          "number": 1,
          "amount": 25000.00,
          "due_date": "2024-01-01",
          "status": "paid"
        },
        {
          "number": 2,
          "amount": 25000.00,
          "due_date": "2024-02-01",
          "status": "pending"
        }
      ]
    }
  ]
}
```

### 2. Process Payment
**POST** `/payments`

**Request:**
```json
{
  "student_id": 1,
  "fee_id": 1,
  "amount": 25000.00,
  "payment_method": "online",
  "transaction_id": "TXN123456",
  "payment_date": "2024-01-01",
  "remarks": "First installment payment"
}
```

## Examination APIs

### 1. Get Exam Schedule
**GET** `/exams/schedule`

**Query Parameters:**
- `batch_id`: Filter by batch
- `subject_id`: Filter by subject
- `start_date`: Start date
- `end_date`: End date

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "subject": {
        "name": "Mathematics",
        "code": "MATH101"
      },
      "exam_name": "Mid Semester Exam",
      "exam_type": "internal",
      "exam_date": "2024-02-15",
      "start_time": "10:00",
      "duration_minutes": 120,
      "total_marks": 100,
      "passing_marks": 40
    }
  ]
}
```

### 2. Submit Exam Results
**POST** `/exams/{exam_id}/results`

**Request:**
```json
{
  "results": [
    {
      "student_id": 1,
      "marks_obtained": 85,
      "remarks": "Good performance"
    },
    {
      "student_id": 2,
      "marks_obtained": 92,
      "remarks": "Excellent"
    }
  ]
}
```

### 3. Get Student Results
**GET** `/students/{student_id}/results`

**Query Parameters:**
- `semester_id`: Filter by semester
- `exam_type`: Filter by exam type

**Response:**
```json
{
  "success": true,
  "data": {
    "student": {
      "name": "John Doe",
      "student_id": "STU001"
    },
    "semester": "Semester 1",
    "results": [
      {
        "subject": "Mathematics",
        "exam_type": "internal",
        "marks_obtained": 85,
        "total_marks": 100,
        "percentage": 85.00,
        "grade": "A",
        "status": "pass"
      }
    ],
    "semester_gpa": 8.5,
    "overall_status": "pass"
  }
}
```

## Reporting APIs

### 1. Get NAAC Report
**GET** `/reports/naac/{report_type}`

**Path Parameters:**
- `report_type`: curriculum, teaching, evaluation, research, etc.

**Query Parameters:**
- `academic_year`: Academic year
- `program_id`: Specific program

### 2. Get Attendance Summary
**GET** `/reports/attendance/summary`

**Query Parameters:**
- `batch_id`: Batch ID
- `subject_id`: Subject ID
- `start_date`: Start date
- `end_date`: End date

### 3. Get Financial Report
**GET** `/reports/financial/summary`

**Query Parameters:**
- `start_date`: Start date
- `end_date`: End date
- `program_id`: Program filter

## Dashboard APIs

### 1. Get Student Dashboard
**GET** `/dashboard/student`

**Response:**
```json
{
  "success": true,
  "data": {
    "profile": {
      "name": "John Doe",
      "student_id": "STU001",
      "program": "BSc CS",
      "batch": "2023-2026"
    },
    "attendance": {
      "today_percentage": 95.5,
      "monthly_percentage": 92.3,
      "total_sessions": 120,
      "present_count": 110
    },
    "fees": {
      "total_pending": 25000.00,
      "next_due_date": "2024-02-01",
      "next_installment": 25000.00
    },
    "upcoming_exams": [
      {
        "subject": "Mathematics",
        "date": "2024-02-15",
        "time": "10:00 AM"
      }
    ],
    "recent_results": [
      {
        "subject": "Physics",
        "marks": 88,
        "grade": "A"
      }
    ]
  }
}
```

### 2. Get Faculty Dashboard
**GET** `/dashboard/faculty`

### 3. Get Admin Dashboard
**GET** `/dashboard/admin`

## File Upload APIs

### 1. Upload Document
**POST** `/documents/upload`

**Content-Type:** `multipart/form-data`

**Form Data:**
- `file`: File to upload
- `document_type`: student_photo, mark_sheet, etc.
- `student_id`: Associated student ID (if applicable)

**Response:**
```json
{
  "success": true,
  "data": {
    "file_path": "uploads/students/STU001/photo.jpg",
    "file_url": "https://api.pvgs.edu/storage/uploads/students/STU001/photo.jpg",
    "file_name": "photo.jpg",
    "file_size": 1024000
  },
  "message": "File uploaded successfully"
}
```

## Notification APIs

### 1. Get Notifications
**GET** `/notifications`

**Query Parameters:**
- `type`: fee_due, exam_schedule, result_published, etc.
- `read`: true/false
- `page`: Page number

### 2. Mark Notification Read
**PUT** `/notifications/{id}/read`

## Rate Limiting

### API Limits:
- **General APIs**: 1000 requests per hour per user
- **File Upload**: 50 uploads per hour per user
- **Report Generation**: 100 reports per hour per user

### Headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1609459200
```

## Versioning

### API Versioning:
- **Current Version**: v1
- **Version Header**: `Accept: application/vnd.pvgs.v1+json`
- **URL Versioning**: `/v1/` prefix

### Backward Compatibility:
- Maintain v1 for 2 years after v2 release
- Deprecation warnings in response headers
- Migration guides provided

This API contract provides a comprehensive specification for all PVGS system endpoints with consistent request/response formats and error handling.