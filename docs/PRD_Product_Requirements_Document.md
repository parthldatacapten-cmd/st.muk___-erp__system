PRODUCT REQUIREMENTS DOCUMENT (PRD)
PVG's College of Science & Commerce – Academic & Administrative System
1. DOCUMENT METADATA
Product Name: PVGS Academic & Administrative System
Institution: PVG's College of Science & Commerce
Version: 1.0
Prepared By: [Your company/team]
Target Launch: Phase 1
System Nature: Independent, self-hosted (PVGS servers)

2. BACKGROUND & CONTEXT
2.1 Current Situation
PVGS currently uses an off-the-shelf system that:

Was partially configured
Was not adopted by faculty
Did not support PVGS's academic complexity
Lacked properly configured exams
Caused confusion in fees and scholarships
Failed to generate reliable NAAC data
As a result:

Many processes are manual
Reporting is difficult
Confidence in the system is low
2.2 Why a New System is Required
The new system must:

Fully replace the old system
Reflect actual academic workflows
Be easy for faculty to adopt
Be reliable for accounts & compliance
Support NAAC & management reporting
Avoid forced features like mobile apps or online exams
3. PRODUCT OBJECTIVES (WHAT SUCCESS LOOKS LIKE)
Primary Objectives
Centralize academic, fee, attendance, and result data
Eliminate ambiguity in fees & installments
Provide accurate, filterable NAAC reports
Give Principal & management full visibility (observer role)
Ensure data integrity with approvals & audit trails
Secondary Objectives
Improve faculty adoption
Reduce manual Excel work
Prepare system for future enhancements (mobile, QR, online exams)
4. SYSTEM SCOPE
4.1 In-Scope (Phase 1 – MUST HAVE)
The system will include:

Academic structure management
User roles & permission customization
Student admission & profile management
Fees, installments & scholarships
Student attendance
Staff attendance
Timetable & scheduling
Lesson planning (planned vs actual)
Examination results (no online exams)
Configurable result templates
NAAC & management reports
4.2 Out-of-Scope (Explicitly NOT in Phase 1)
Mobile application
QR / biometric attendance
Online examination conduction
Alumni management
Advanced analytics dashboards
(These may be considered in Phase 2 / 3)
5. KEY STAKEHOLDERS & USERS
5.1 Stakeholders
Principal / Head of Institution
Heads of Departments (HODs)
Accounts Department
Faculty Members
Students
System Super Admin
5.2 User Personas (High-Level)
Principal (Observer)

Wants high-level visibility
Needs reports, trends, summaries
Does NOT want to edit data
HOD

Manages academic delivery
Approves lesson plans & deviations
Oversees faculty performance
Faculty

Teaches assigned subjects
Marks attendance
Plans lessons
Submits marks
Accounts Staff

Manages fees & installments
Tracks payments & dues
Generates financial reports
Student

Applies for admission
Pays fees
Views attendance & results
Super Admin

Configures the system
Manages structure, roles & rules
No daily operations
6. HIGH-LEVEL FUNCTIONAL REQUIREMENTS
6.1 Academic Structure
Support UG & PG programs
Flexible academic pattern (semester/units)
Subject master reuse
Subject offerings per program & academic unit
Subject components (theory/lab/project)
6.2 Roles & Permissions
Role-based access control
Custom role creation
Program-scoped visibility
Assignment-based access (faculty → subjects)
6.3 Student Admission & Profiles
Online admission form
Application fee
Document upload
Approval workflow
Category (SC/ST/OBC/etc.) handling
Profile update requests with approval & audit trail
6.4 Fees & Finance
Program & year-wise fee structures
Ordered installments (sequence enforced)
Online & offline payments
Scholarships as adjustments (not fee items)
Installment-wise payment tracking
Accounts & management reports
6.5 Attendance
Student Attendance

Period / session-wise
Component-based
Timetable-linked
Edit window with audit trail
Defaulter identification
Staff Attendance

Daily manual attendance
Leave marking
Department-wise reports
Principal observer view
6.6 Lesson Planning
Chapter/module definition
Planned vs actual sessions
Deviation reasons
HOD approval
Reports for management
6.7 Examination & Results
Exam definition (internal/external/practical)
Component-wise marks entry
Excel/CSV upload
Result generation
Configurable result templates
Student result access
NAAC-ready result reports
6.8 Reporting & NAAC
Student strength reports
Category-wise data
Attendance summaries
Pass percentage reports
Program-wise & year-wise trends
Export to Excel/PDF
7. NON-FUNCTIONAL REQUIREMENTS
Web-based (desktop-first)
Hosted on PVGS servers
Secure role-based access
Full audit trail for sensitive actions
Scalable for future modules
Laravel-based backend
8. ASSUMPTIONS & CONSTRAINTS
Assumptions
Exams may be conducted offline
Faculty will use web interface
Academic structure can evolve
Constraints
No mobile app in Phase 1
No dependency on old system
Limited historical exam data
9. SUCCESS METRICS
100% fee installment clarity
Accurate attendance records
Reduced manual Excel usage
NAAC reports generated without rework
Principal able to review data without intervention
10. RISKS & MITIGATIONS
Risk
Mitigation
Faculty adoption
Simple UI, no forced mobile
Scope creep
PRD + FRD sign-off
Data inconsistency
Approval workflows + audit logs
NAAC format changes
Configurable reports
11. PHASE OVERVIEW
Phase 1: Core system (this PRD)
Phase 2: Optimization & automation
Phase 3: Enhancements (mobile, QR, online exams)
PRD STATUS
Once this PRD is:

Reviewed internally
Approved by decision makers
NO new features are added to Phase 1 without change approval
This is your scope shield.