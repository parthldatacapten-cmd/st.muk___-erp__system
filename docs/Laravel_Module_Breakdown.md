LARAVEL MODULE BREAKDOWN
PVG's College of Science & Commerce System
STEP 2: LARAVEL MODULE BREAKDOWN (PVGS)
ARCHITECTURAL PRINCIPLES
Modular (Domain-based), not controller-heavy
Business logic in Services, not Controllers
Authorization via Policies
Thin Controllers → Service → Model
Phase-1 focused (no premature optimization)
MODULE LIST (PHASE 1)
| Module | Priority
---|--------|---------
1 | Auth & Users | Core
2 | Roles & Permissions | Core
3 | Academic Structure | Core
4 | Student Management | Core
5 | Fees & Finance | Critical
6 | Timetable | High
7 | Attendance | High
8 | Lesson Planning | High
9 | Examination & Results | Medium
10 | Reports & NAAC | Medium
11 | Audit & Logs | Core

RECOMMENDED FOLDER STRUCTURE
app/
├── Modules/
│ ├── Auth/
│ ├── Users/
│ ├── Roles/
│ ├── Academics/
│ ├── Students/
│ ├── Fees/
│ ├── Timetable/
│ ├── Attendance/
│ ├── Lessons/
│ ├── Exams/
│ ├── Reports/
│ └── Audit/
├── Http/
│ └── Controllers/
├── Policies/
├── Services/
└── Models/

(You can use nwidart/laravel-modules or native structure — both work.)

MODULE-WISE BREAKDOWN
1. AUTH & USERS MODULE
Models:

User
Controllers:
LoginController
PasswordController
Services:
AuthService
Notes:
Laravel Breeze / Fortify recommended
No custom logic here
2. ROLES & PERMISSIONS MODULE
Models:

Role
Permission
RolePermission
UserRole
Services:
RoleService
PermissionService
Policies:
RolePolicy
PermissionPolicy
Notes:
Cache permissions aggressively
Middleware: check.permission
3. ACADEMIC STRUCTURE MODULE
Models:

Department
Program
AcademicPattern
AcademicUnit
SubjectMaster
SubjectOffering
SubjectComponent
FacultyAssignment
Services:
ProgramService
SubjectOfferingService
FacultyAssignmentService
Policies:
ProgramPolicy
SubjectPolicy
Notes:
Only Super Admin can mutate structure
4. STUDENT MANAGEMENT MODULE
Models:

Student
Category
StudentDocument
StudentProfileChange
Services:
AdmissionService
StudentProfileService
Policies:
StudentPolicy
Notes:
Admission workflow lives here
5. FEES & FINANCE MODULE (CRITICAL)
Models:

FeeStructure
FeeInstallment
StudentFee
FeePayment
Services:
FeeStructureService
InstallmentService
PaymentService
Policies:
FeePolicy
PaymentPolicy
Critical Logic:
Enforce installment order
Category-based assignment
6. TIMETABLE MODULE
Models:

Timetable
Lecture
Classroom
Services:
TimetableService
Policies:
TimetablePolicy
Key Rule:
Prevent time & faculty conflicts
7. ATTENDANCE MODULE
Models:

StudentAttendance
StaffAttendance
Services:
AttendanceService
Policies:
AttendancePolicy
Notes:
Heavy audit logging here
8. LESSON PLANNING MODULE
Models:

LessonChapter
LessonPlan
LessonPlanApproval
Services:
LessonPlanService
Policies:
LessonPlanPolicy
Notes:
Planned vs actual separation
9. EXAMINATION & RESULTS MODULE
Models:

Exam
Mark
Result
ResultTemplate
Services:
ExamService
ResultService
Policies:
ExamPolicy
ResultPolicy
10. REPORTS & NAAC MODULE
Models:

(Read-only / query-based)
Services:
ReportBuilderService
NaacReportService
Policies:
ReportPolicy
Notes:
Heavy use of query builders
Exports via Laravel Excel
11. AUDIT & LOGS MODULE
Models:

AuditLog
Services:
AuditService
Notes:
Global listener for model events
POLICY & AUTH STRATEGY
Gate for global permissions
Policies for entity-level access
Middleware:
auth
check.role
check.permission