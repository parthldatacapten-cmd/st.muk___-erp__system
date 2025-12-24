FUNCTIONAL REQUIREMENTS DOCUMENT (FRD)
PVG's College of Science & Commerce System
FRD – MODULE 7: EXAMINATION & RESULTS
7.1 Purpose
To manage exam structure, marks entry, result generation, and publishing, without forcing online exams.
This module supports:

UG & PG variations
Component-based evaluation
NAAC & university reporting
7.2 Actors
Exam Cell / Admin
Faculty
HOD
Principal (Observer)
Students
7.3 Exam Configuration
Exam Types

Internal Assessment
External / University Exam
Practical / Lab Exam
Project / Viva
Exam Definition Rules
Exams are defined per:

Program
Semester
Subject Offering
Component
Each exam has:

Exam type
Max marks
Passing marks
Weightage (if applicable)
7.4 Marks Entry
Faculty Marks Entry
Faculty enters marks only for:

Assigned components
Modes:

Manual entry
Excel upload (CSV/XLS)
Validation:

Cannot exceed max marks
Mandatory for all students (Absent = special flag)
Absent & Special Cases

Absent
Withheld
Re-exam / ATKT
Grace marks (if allowed)
All special cases must be:

Explicitly tagged
Logged
7.5 Result Calculation
Calculation Rules

Component-wise aggregation
Subject-wise total
Semester-wise result
Program-level result
Calculation rules must be:

Configurable per program
Stored version-wise (for audit)
7.6 Result Status & Approval
Result lifecycle:

Draft (faculty)
Submitted
Verified (HOD / Exam Cell)
Published
Only Published results visible to students.

7.7 Result Templates (IMPORTANT)
Each program can have:

Custom result format
Template controls:
Subject display order
Component breakdown
Grades / marks
Templates are reusable per program
This matches your requirement:
"Principal or decision makers will decide the format"

7.8 Student Result View
Students can:

View semester results
Download result sheet (PDF)
See:
Marks
Status (Pass/Fail/ATKT)
7.9 Reports
Pass / Fail summary
Subject-wise performance
Category-wise results
Faculty-wise performance
7.10 Audit & Controls
No deletion of published results
Any correction requires:
Reason
Re-approval
Full audit trail mandatory