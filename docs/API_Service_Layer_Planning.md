API & SERVICE LAYER PLANNING
PVG's College of Science & Commerce System
ARCHITECTURE PRINCIPLES
Controller = thin
Business logic = Service layer
DB writes = transactional
RBAC enforced at policy/middleware level
Audit logs mandatory for sensitive actions
No cross-ERP dependencies
1. AUTH & ROLES MODULE
APIs

POST /api/auth/login
POST /api/auth/logout
GET /api/auth/me
GET /api/roles
POST /api/roles
PUT /api/roles/{id}
GET /api/permissions
POST /api/roles/{roleId}/permissions
Services

AuthService
RoleService
PermissionService
Key Rules

Principal role = read-only
Faculty restricted by department
Role changes are audited
2. ADMISSION & STUDENT PROFILE MODULE
APIs

POST /api/admissions/apply
POST /api/admissions/upload-documents
GET /api/admissions/{id}
POST /api/students
GET /api/students/{id}
PUT /api/students/{id}
PUT /api/students/{id}/editable-fields
Services

AdmissionService
StudentService
StudentProfileService
Transactions

Admission creation
Document upload + linking
Profile updates (audit logged)
3. FEES & INSTALLMENTS MODULE (CRITICAL)
APIs

GET /api/fee-structures
POST /api/fee-structures
POST /api/students/{id}/assign-fee-structure
GET /api/students/{id}/fee-ledger
POST /api/fees/pay
GET /api/fees/payments
Services

FeeStructureService
StudentFeeService
InstallmentService
PaymentService
Hard Rules (Service-Enforced)

Cannot pay installment 2 before 1
Fee reassignment without permission
Every reassignment logged
Scholarship does NOT change amounts
4. SCHOLARSHIP TRACKING MODULE (NO MONEY LOGIC)
APIs

POST /api/students/{id}/scholarship/apply
POST /api/scholarship/{id}/verify
GET /api/students/{id}/scholarship
Services

ScholarshipApplicationService
ScholarshipVerificationService
Rules

Scholarship = eligibility + documents only
Fee structure assigned manually
Verification by Student Section only
5. ACADEMICS (PROGRAMS, SUBJECTS, COMPONENTS)
APIs

GET /api/programs
POST /api/programs
GET /api/subjects
POST /api/subjects
POST /api/subjects/{id}/components
Services

ProgramService
AcademicStructureService
SubjectComponentService
Key Support

Same subject in multiple programs
Different codes per program/semester
Theory / Practical / Project separation
6. ATTENDANCE (STUDENT + STAFF)
APIs

POST /api/attendance/mark
GET /api/attendance/report
POST /api/staff-attendance/mark
Services

AttendanceService
TimetableValidationService
Critical Validations

Teacher double-booking
Class double-booking
Period-wise & day-wise support
7. LESSON PLANNING MODULE
APIs

POST /api/lesson-plans
PUT /api/lesson-plans/{id}
POST /api/lesson-plans/{id}/actuals
GET /api/lesson-plans/review
Services

LessonPlanService
LessonActualService
LessonReviewService
Core Logic

Planned vs Actual
Editable schedules
HOD approval & review
Historical comparison (NAAC-ready)
8. EXAMINATION & RESULTS MODULE
APIs

POST /api/results/upload
GET /api/results/student/{id}
GET /api/results/templates
POST /api/results/templates
Services

ResultService
ResultTemplateService
ATKTService
Notes

Exams may be offline
System stores marks, results, ATKT flags
Calculation formulas configurable
9. REPORTS & NAAC MODULE
APIs

POST /api/reports/generate
GET /api/reports/download
Services

ReportBuilderService
NAACReportService
Features

Dynamic columns
Filters
Category / gender / program wise
Export (Excel / PDF)
10. SYSTEM CONFIGURATION
APIs

GET /api/settings
PUT /api/settings
POST /api/audit/logs
GET /api/audit/logs
Services

SystemSettingService
AuditLogService
TRANSACTION STRATEGY (IMPORTANT)
Wrap these in DB transactions:

Admission + documents
Fee assignment
Fee payment
Scholarship verification
Attendance marking (bulk)
Result upload
CROSS-CUTTING SERVICES
Service
Purpose
ValidationService
Central rules
AuthorizationService
Role checks
AuditLogService
Compliance
NotificationService
SMS / Email (Phase 2)
STATUS CHECK
Area
Ready
APIs
Defined
Services
Clear
Business rules
Enforced
Laravel suitability
Excellent
PVG constraints
Respected