FUNCTIONAL REQUIREMENTS DOCUMENT (FRD)
PVG's College of Science & Commerce System
FRD – MODULE 2: ROLES & PERMISSIONS (RBAC)
2.1 Purpose
To ensure strict access control, data isolation between departments/programs, and role-based actions across the PVGS system.
This module prevents:

Cross-department data visibility (Animation vs CS issue)
Unauthorized edits
Operational confusion
2.2 Actors
Super Admin
Principal
HOD
Faculty
Accounts Staff
Student
Custom Roles (future)
2.3 Role Types
System Roles (Default)
These are pre-created and cannot be deleted:

Super Admin
Principal
HOD
Faculty
Accounts
Student
Custom Roles

Created by Super Admin
Based on permission sets
Example: "Exam Cell", "Office Staff"
2.4 Permission Model (Design Rule)
Permissions are defined at feature-action level:

View
Create
Edit
Delete
Approve
Export
Example:

attendance.mark
fees.installment.configure
lesson_plan.approve
2.5 Role Capabilities (High-Level)
Super Admin

Full access to all modules
Configure:
Academic structure
Roles & permissions
Fees rules
Sessions
No daily academic work
Principal (Observer Role)

Read-only access
Can view:
All reports
Staff attendance
Student attendance summaries
Fee collection summaries
Cannot:
Edit academic data
Modify fees
Approve lesson plans
(Permissions can be extended later on request)
HOD

Department-scoped access
Can:
View department programs
Approve lesson plans
View faculty workload
View attendance & results
Cannot:
Modify fees
Change academic structure
Faculty

Assignment-based access
Can:
View assigned subjects/components
Mark attendance
Create & update lesson plans
Enter marks
Cannot:
View other programs
Modify fees
Approve own plans
Accounts

Financial modules only
Can:
Configure fee structures
Define installments
View & export payment reports
Cannot:
Edit academic or attendance data
Student

Self-data access only
Can:
Apply for admission
Pay fees
View attendance & results
Cannot:
Edit approved academic records
View other students
2.6 Data Visibility Rules (CRITICAL)
Program-scoped visibility:

Users see only assigned programs
Department isolation:

Animation ≠ CS ≠ Commerce
Student data visible:

To faculty only if teaching that student
2.7 Approval Rules
Action
Approver
Lesson plan
HOD
Profile edits
Admin / Office
Fee adjustments
Accounts Head
Marks finalization
HOD / Exam Cell
2.8 Audit & Logs
All sensitive actions logged:

Who
When
Old vs new value
Mandatory for:

Attendance edits
Fees changes
Result changes
2.9 Outputs
Role-permission matrix
User access summary
Audit logs (exportable)