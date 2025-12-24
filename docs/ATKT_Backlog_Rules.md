ATKT & BACKLOG RULES
PVG's College of Science & Commerce System
OFFICIAL DECISION
For ALL of the following:

ATKT allowed for UG → Configurable per program
ATKT allowed for PG → Configurable per program
Max backlogs → Configurable per program
Component-wise ATKT → Configurable per program
Promotion allowed with ATKT → Configurable per program
Science vs Commerce differences → Handled via program rules
No hard-coded academic rules anywhere

WHY THIS IS THE RIGHT CALL
Universities change rules
PG ≠ UG
Science ≠ Commerce
Animation ≠ Computer Science
NAAC requires historical accuracy
Prevents future rewrites
This is exactly why the old system failed.

FINAL ATKT CONFIGURATION MODEL
1. atkt_rules (Program-Level Configuration)
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
Supports:

Rule changes over time
NAAC historical reporting
University circular updates
2. exam_results (Component-Aware)
exam_results

id
student_id
program_id
semester_id
subject_id
component_type (THEORY / PRACTICAL / PROJECT)
marks_obtained
max_marks
pass_marks
result_status (PASS / FAIL)
exam_attempt (REGULAR / ATKT / REVAL)
3. student_backlogs (System-Derived, Not Manual)
student_backlogs

id
student_id
program_id
subject_id
component_type
semester_id
academic_year
backlog_status (ACTIVE / CLEARED)
cleared_exam_id
Staff cannot manually edit backlogs
System derives it from exam results

RESULT & PROMOTION LOGIC (SYSTEM)
Step 1 — Component Level
If component FAIL → backlog created

Step 2 — Subject Level
If any component FAIL → subject = ATKT

Step 3 — Program Rule Check
Count active backlogs
Fetch atkt_rules for program

Step 4 — Promotion Decision

Condition
Outcome
Backlogs ≤ limit & promotion_allowed = YES
PROMOTED WITH ATKT
Backlogs > limit
NOT PROMOTED
No backlogs
PASS
RESULT TEMPLATES (PROGRAM-SPECIFIC)
Each program defines:

Component display
ATKT labels
Promotion status
Backlog summary
Stored as:
result_templates

program_id
layout_config (JSON)
NAAC & REPORTING BENEFITS
With this design you can generate:

Pass % by program
Backlog clearance rate
Category-wise progression
Year-wise academic outcomes
All without manual Excel work.

STATUS CHECK
Area
Status
ATKT rules
Final
Configurability
Yes
ERD consistency
Maintained
Laravel suitability
Excellent
NAAC compliance
Strong