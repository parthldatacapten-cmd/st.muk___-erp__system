FUNCTIONAL REQUIREMENTS DOCUMENT (FRD)
PVG's College of Science & Commerce System
FRD – MODULE 4: FEES & INSTALLMENTS
(Critical – Accounts Pain Area)

4.1 Purpose
To manage clear, enforceable, auditable fee collection with:

Installment control
Scholarship handling
Accurate reports
Zero ambiguity for accounts & management
4.2 Actors
Accounts Staff
Super Admin
Student
Principal (Observer)
4.3 Core Concepts
Fee Type
Examples:

Tuition Fee
Lab Fee
Exam Fee
Admission Fee
Fee Structure

Program + Academic Unit based
Can vary by:
Program
Year
Category (scholarship)
4.4 Installment Design (VERY IMPORTANT)
Rules
A fee structure can have:

One-time payment OR
Multiple installments
Installments have:

Sequence number (1, 2, 3…)
Amount
Due date
Grace period (optional)
Critical Rule
A later installment CANNOT be paid unless all previous installments are fully paid.
This directly fixes the old system failure.

4.5 Scholarship Handling (Design Decision)
Scholarships are NOT fee items.
They are:

Adjustments
Applied after eligibility verification
Reduce payable amount
Example:

Tuition Fee: 60,000
Scholarship: 20,000
Net Payable: 40,000
4.6 Student Fee Assignment
On admission:

Student auto-linked to:
Fee structure
Installment plan
Manual override allowed (with approval + audit)
4.7 Payment Flow
Online Payment

Gateway integration (Phase 1 optional)
Auto-allocation to current installment
Offline Payment

Cash / Bank / DD entry
Receipt generation
4.8 Fee Status Tracking
For each student:

Total fees
Paid amount
Due amount
Installment-wise status
4.9 Reports (MANDATORY)
Accounts reports:

Installment-wise payment list
Due students (by installment)
Scholarship-adjusted collections
Program-wise collections
Principal reports:

Collection summary
Outstanding dues
4.10 Validations & Audit
Installment order enforced
Amount mismatch blocked
All fee edits logged
No deletion of paid records