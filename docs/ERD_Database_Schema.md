ERD – DATABASE SCHEMA (ATKT MERGED)
PVG's College of Science & Commerce System
ERD DESIGN PRINCIPLES (LOCKED)
Program-driven academic rules
Semester-based subjects
Component-aware evaluation
ATKT/backlog is derived, not manually edited
Scholarships are tracking-only
Fees are manually assigned, rule-enforced
NAAC reporting is first-class
CORE ACADEMIC STRUCTURE
1. programs
programs

id
name (B.Sc CS, B.Sc Animation, etc.)
level (UG / PG)
department_id
duration_years
is_active
2. academic_years
academic_years

id
name (2024-25)
is_current
3. semesters
semesters

id
program_id
academic_year_id
semester_number (1..6)
year_number (1..3 / 1..2)
Supports:

2 semesters per year
Program-specific sequencing
4. subjects
subjects

id
name
subject_code
program_id
semester_id
credits
Same subject name can exist in:

Multiple programs
Different codes
Different semesters
5. subject_components
subject_components

id
subject_id
component_type (THEORY / PRACTICAL / PROJECT)
max_marks
pass_marks
Component-wise evaluation
Component-wise ATKT

STUDENT & ADMISSION
6. students
students

id
admission_number
prn_number
program_id
category_id
scholarship_applied (Yes / No)
status (ACTIVE / LEFT / COMPLETED)
7. student_admissions
student_admissions

id
student_id
academic_year_id
admission_date
EXAMINATION, RESULTS & ATKT (CORE CHANGE)
8. exam_results
exam_results

id
student_id
program_id
semester_id
subject_id
subject_component_id
marks_obtained
max_marks
pass_marks
result_status (PASS / FAIL)
exam_attempt (REGULAR / ATKT / REVAL)
Source of truth for:

Pass / fail
Backlog creation
Promotion logic
9. student_backlogs (DERIVED TABLE)
student_backlogs

id
student_id
program_id
semester_id
subject_id
subject_component_id
academic_year_id
backlog_status (ACTIVE / CLEARED)
cleared_exam_result_id
No manual editing
System-maintained only

10. atkt_rules (PROGRAM-CONFIGURABLE)
atkt_rules

id
program_id
academic_level (UG / PG)
max_active_backlogs
scope (SEMESTER / YEAR)
component_wise (Yes / No)
promotion_allowed (Yes / No)
effective_from_year
effective_to_year
Different rules per program
Historical accuracy for NAAC

11. student_promotions
student_promotions

id
student_id
from_semester_id
to_semester_id
promotion_status (PROMOTED / PROMOTED_WITH_ATKT / NOT_PROMOTED)
calculated_on
Stored snapshot
No recalculation surprises

FEES & SCHOLARSHIPS (UNCHANGED BUT VERIFIED)
12. fee_structures
fee_structures

id
program_id
semester_id
category_id
total_amount
13. student_fees
student_fees

id
student_id
fee_structure_id
assigned_by
assigned_on
14. student_scholarship_applications
student_scholarship_applications

id
student_id
verification_status (PENDING / APPROVED / REJECTED)
verified_by
ATTENDANCE & LESSON PLANNING (REFERENTIAL)
15. attendance_records
attendance_records

id
student_id
subject_component_id
date
period
status (PRESENT / ABSENT)
16. lesson_plans
lesson_plans

id
subject_id
faculty_id
planned_content
actual_content
plan_date
GOVERNANCE & AUDIT
17. users / roles / permissions
(standard RBAC tables)

18. audit_logs
audit_logs

id
entity_type
entity_id
action
performed_by
old_value
new_value
created_at
ERD VALIDATION CHECKLIST
Requirement
Status
ATKT configurable
Complete
Component-wise failures
Complete
Promotion snapshot
Complete
Science vs Commerce
Complete
UG vs PG
Complete
NAAC reporting
Complete
Laravel friendly
Complete
No hard-coded rules
Complete
SCHEMA FREEZE POINT
After this:

No new tables unless legally required
No academic logic in controllers
All logic via services