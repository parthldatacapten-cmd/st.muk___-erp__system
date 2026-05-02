# Functional Requirements Document (FRD) - User Management, Finance & Scheduling

## Document Information

| Attribute | Details |
|-----------|---------|
| **Document ID** | FRD-EDU-008 |
| **Version** | 1.0 |
| **Date** | December 2024 |
| **Prepared By** | Product Management Team |
| **Approved By** | CTO, CFO, Operations Head |
| **Status** | Draft |

---

## Table of Contents

1. [Module 1: User Management & Student Approval](#1-module-1-user-management--student-approval)
2. [Module 2: Fee Management & Accounts](#2-module-2-fee-management--accounts)
3. [Module 3: Expense Management](#3-module-3-expense-management)
4. [Module 4: Faculty Payroll & Salary](#4-module-4-faculty-payroll--salary)
5. [Module 5: Lecture Scheduling & Timetable](#5-module-5-lecture-scheduling--timetable)
6. [Module 6: Universal Attendance System](#6-module-6-universal-attendance-system)
7. [Integration & Reporting](#7-integration--reporting)

---

# 1. Module 1: User Management & Student Approval

## 1.1 Overview

**Module ID**: USER-001  
**Priority**: P0 (Critical)  
**Description**: Complete user lifecycle management from registration to approval, including role-based access control, multi-level approval workflows, and student admission processing.

---

## 1.2 User Registration & Onboarding

### FR-USER-001: Multi-Channel User Registration

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-USER-001 |
| **Feature** | User Registration from Multiple Sources |
| **User Story** | As a prospective student/parent, I want to register through multiple channels so that I can choose the most convenient method |

**Registration Channels:**

**Channel A: Online Self-Registration (Web/Mobile)**
```
1. User visits institution portal
2. Clicks "Register" or "Apply Now"
3. Selects user type:
   - Prospective Student
   - Parent/Guardian
   - Staff/Faculty (by invitation only)
   
4. Fills basic information:
   - Full Name
   - Date of Birth
   - Gender
   - Email Address (verified via OTP)
   - Mobile Number (verified via OTP)
   - Aadhaar Number (optional, validated)
   - Password (min 8 chars, special chars, numbers)

5. Uploads profile photo (auto-crop tool)
6. Accepts terms & conditions
7. Submits registration
8. System generates unique User ID
9. Sends welcome email/SMS with login credentials
```

**Channel B: Bulk Import by Admin**
```
1. Admin navigates to Users → Bulk Import
2. Downloads Excel template
3. Fills user data in template:
   | Name | Email | Mobile | DOB | Role | Department | 
   
4. Uploads completed Excel file
5. System validates:
   - Duplicate emails/mobile numbers
   - Valid email format
   - Valid mobile number format (10 digits)
   - Required fields completeness
   
6. Shows preview with errors highlighted
7. Admin corrects errors and re-uploads
8. Confirms import
9. System creates users and sends credentials via email/SMS
```

**Channel C: API Integration (Third-party)**
```
For coaching chains or school networks:
- Sync users from central CRM
- Real-time user creation via REST API
- Webhook notifications for new registrations
```

**Validation Rules:**
- Email must be unique across system
- Mobile number must be unique (can be shared for parent-student relationship)
- Aadhaar validation: 12 digits with checksum verification
- Password strength meter displayed during creation
- CAPTCHA for self-registration to prevent bots

---

### FR-USER-002: Student Admission Approval Workflow

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-USER-002 |
| **Feature** | Multi-Level Student Approval System |
| **User Story** | As an admission officer, I want to process student applications through configurable approval stages so that we maintain quality and compliance |

**Approval Workflow Configuration:**

**Step 1: Define Workflow Stages**
```
Admin configures approval pipeline:

Example 1: Engineering College
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Application │ -> │ Document    │ -> │ Entrance    │ -> │ Final       │
│ Submitted   │    │ Verification│    │ Score Check │    │ Admission   │
│             │    │             │    │             │    │ Offer       │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     ↓                   ↓                   ↓                   ↓
  Auto                 Admission          Academic           Principal
  Acknowledgment       Officer            Coordinator        Approval

Example 2: School (Class 11)
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Form        │ -> │ Marks       │ -> │ Seat        │ -> │ Fee         │
│ Submission  │    │ Verification│    │ Allocation  │    │ Payment     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Step 2: Configure Approval Rules**

**Auto-Approval Rules:**
```
IF applicant.class_10_percentage >= 90
AND applicant.category == "General"
AND all_documents_uploaded == true
THEN auto_approve_stage_2
ELSE manual_review_required
```

**Conditional Routing:**
```
IF applicant.stream_preference == "Science"
THEN route_to = "Science_HOD"
ELSE IF applicant.stream_preference == "Commerce"
THEN route_to = "Commerce_HOD"
ELSE route_to = "Arts_HOD"
```

**SLA Configuration:**
```
Each stage has time limit:
- Document Verification: 48 hours
- Academic Review: 72 hours
- Principal Approval: 24 hours

IF sla_breached:
  - Escalate to higher authority
  - Send reminder notification
  - Log breach for performance tracking
```

**Functional Flow:**

```
1. Student submits application with documents
2. System assigns application number (e.g., ADM-2024-001234)
3. System sends acknowledgment SMS/Email
4. Application appears in "Pending Verification" queue

5. Admission Officer reviews:
   - Views uploaded documents (marksheets, caste certificate, etc.)
   - Verifies authenticity
   - Cross-checks with board results (if API available)
   - Marks as "Verified" or "Rejected with reason"

6. If verified → moves to next stage
   If rejected → student notified with reason, can re-submit

7. Academic Coordinator reviews:
   - Checks eligibility criteria
   - Validates entrance exam scores
   - Applies reservation rules (SC/ST/OBC/EWS)
   - Calculates merit score

8. Merit list generated automatically:
   ```
   Merit Score = 
     (Class 10 % * 0.40) + 
     (Entrance Score * 0.50) + 
     (Extra-curricular * 0.10) + 
     (Reservation bonus if applicable)
   ```

9. Seat allocation based on:
   - Merit rank
   - Stream preference
   - Category reservation
   - Seat availability

10. Provisional offer letter generated
11. Student accepts offer and pays admission fee
12. Final enrollment confirmed
13. Student account activated with full access
```

**Approval Dashboard:**

```
┌────────────────────────────────────────────────────────────┐
│ Admission Approval Dashboard                               │
├────────────────────────────────────────────────────────────┤
│ Summary:                                                   │
│ - Total Applications: 1,245                                │
│ - Pending My Action: 23                                    │
│ - Approved Today: 45                                       │
│ - Rejected Today: 3                                        │
│ - SLA Breaches: 2                                          │
├────────────────────────────────────────────────────────────┤
│ Pending Queue (Sorted by submission date):                 │
│ ┌──────────┬─────────────┬──────────┬─────────┬─────────┐ │
│ │ App No   │ Student     │ Stage    │ Since   │ Action  │ │
│ ├──────────┼─────────────┼──────────┼─────────┼─────────┤ │
│ │ 001234   │ Rahul S.    │ Doc Verify│ 2 days │ [Review]│ │
│ │ 001235   │ Priya M.    │ Merit Calc│ 1 day  │ [Review]│ │
│ │ 001236   │ Amit K.     │ HOD Approval│ 4hrs │ [Review]│ │
│ └──────────┴─────────────┴──────────┴─────────┴─────────┘ │
└────────────────────────────────────────────────────────────┘
```

**Notifications:**

| Event | Recipient | Channel | Template |
|-------|-----------|---------|----------|
| Application submitted | Student | SMS + Email | "Your application ADM-XXX received" |
| Moved to next stage | Student | Email | "Application progressed to Stage Y" |
| Action required | Approver | Email + In-app | "X applications pending your review" |
| Approved | Student | SMS + Email | "Congratulations! Your admission approved" |
| Rejected | Student | Email | "Application status update - Action required" |
| SLA breach | Supervisor | Email | "Urgent: X applications breached SLA" |
| Fee payment due | Student | SMS + WhatsApp | "Pay admission fee to confirm seat" |

---

## 1.3 Role-Based Access Control (RBAC)

### FR-USER-003: Granular Permission Management

**Permission Matrix Structure:**

```
Permissions organized by module:
┌─────────────────────────────────────────────────────────────┐
│ Module: Student Management                                  │
├─────────────────────────────────────────────────────────────┤
│ Permission Code | Description              | Type           │
│ STU_VIEW        | View student list        | Read           │
│ STU_CREATE      | Add new student          | Create         │
│ STU_EDIT        | Modify student details   | Update         │
│ STU_DELETE      | Remove student           | Delete         │
│ STU_EXPORT      | Export to Excel          | Export         │
│ STU_PRINT       | Print reports            | Print          │
│ STU_APPROVE     | Approve admissions       | Approve        │
│ STU_TRANSFER    | Transfer to other class  | Special        │
└─────────────────────────────────────────────────────────────┘
```

**Role Templates:**

**1. Super Admin (System Owner)**
```
- All permissions across all modules
- Can create institution admins
- Access to system configuration
- Audit log viewer
- Cannot be deleted
```

**2. Institution Admin (Principal/Manager)**
```
- Full access within their institution
- Manage staff and roles
- Approve financial transactions
- View all reports
- Configure academic structure
```

**3. Admission Officer**
```
Student Module: VIEW, CREATE, EDIT, EXPORT
Admission Module: VIEW, CREATE, EDIT, APPROVE
Fee Module: VIEW (fee structure only)
Reports: Admission reports only
```

**4. Faculty/Teacher**
```
Student Module: VIEW (assigned classes only)
Attendance Module: VIEW, CREATE (for own classes)
Marks Module: VIEW, CREATE, EDIT (own subjects)
LMS Module: FULL (own courses)
Timetable Module: VIEW (own schedule)
NO access to: Fees, Admissions, HR, Admin settings
```

**5. Accountant**
```
Fee Module: FULL (collect fees, generate receipts)
Expense Module: VIEW, CREATE (record expenses)
Payroll Module: VIEW, CREATE (enter salary data)
Reports: Financial reports only
NO access to: Academics, Student records (except fee dues)
```

**6. Student**
```
View own: Attendance, Marks, Timetable, Fee dues
Download: Marksheets, Receipts, Study material
Submit: Assignments, Leave applications
NO access to: Other students' data, Admin functions
```

**7. Parent**
```
View child's: Attendance, Marks, Fee dues, Notices
Communicate with: Teachers, Administration
Pay fees: Online payment access
NO access to: Academic content, Other children's data (unless multiple children)
```

**Field-Level Security:**

```
Example: Accountant role viewing student record
Visible fields:
✓ Name, Photo, Class, Roll Number
✓ Fee payment history, Outstanding amount
✗ Parent contact details (masked: XXXXX12345)
✗ Academic performance
✗ Attendance details
✗ Caste category (unless relevant for fee concession)
```

---

## 1.4 User Lifecycle Management

### FR-USER-004: Status Transitions & Workflows

**Student Lifecycle:**

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Prospect     │ -> │ Applicant    │ -> │ Enrolled     │
│ (Inquiry)    │    │ (Applied)    │    │ (Active)     │
└──────────────┘    └──────────────┘    └──────────────┘
                           ↓                    ↓
                    ┌──────────────┐    ┌──────────────┐
                    │ Rejected     │    │ Alumni       │
                    │ (Closed)     │    │ (Graduated)  │
                    └──────────────┘    └──────────────┘
                                              ↓
                                       ┌──────────────┐
                                       │ Inactive     │
                                       │ (Left/Dropout)│
                                       └──────────────┘
```

**Status Change Triggers:**

| From Status | To Status | Trigger Event | Auto/Manual |
|-------------|-----------|---------------|-------------|
| Prospect | Applicant | Submit application | Auto |
| Applicant | Enrolled | Pay admission fee + Approval | Auto |
| Applicant | Rejected | Rejection by approver OR timeout | Manual |
| Enrolled | Active | Attend first class | Auto |
| Enrolled | Inactive | Fee default > 60 days OR leave request | Manual |
| Active | Alumni | Complete final semester | Auto |
| Active | Inactive | Take gap year/semester | Manual |

**Bulk Status Updates:**

```
Scenario: Start of Academic Year
1. Admin selects: "Promote Students"
2. System shows promotion rules:
   - Current class: Class 10
   - Target class: Class 11
   - Promotion criteria: Pass in all subjects
   
3. System identifies eligible students:
   ✓ Passed students: 245
   ✗ Failed students: 12
   ⚠ ATKT eligible: 8
   
4. Admin reviews and confirms
5. System updates:
   - Promoted students → Class 11 (new section allocation)
   - Failed students → Retain in Class 10 (flag for counseling)
   - ATKT students → Class 11 with backlog tag
   
6. Notifications sent to all stakeholders
```

---

# 2. Module 2: Fee Management & Accounts

## 2.1 Overview

**Module ID**: FEE-001  
**Priority**: P0 (Critical)  
**Description**: Comprehensive fee collection, receipt generation, installment tracking, refund processing, and financial reporting integrated with payment gateways.

---

## 2.2 Fee Structure Configuration

### FR-FEE-001: Flexible Fee Plan Builder

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-FEE-001 |
| **Feature** | Multi-dimensional Fee Structure Creation |
| **User Story** | As an accountant, I want to define complex fee structures so that we can handle different programs, categories, and payment plans |

**Fee Components:**

```
Fee Head Types:
1. Tuition Fee (recurring, monthly/quarterly/semester)
2. Admission Fee (one-time)
3. Development Fee (annual)
4. Laboratory Fee (course-specific)
5. Library Fee (annual/semester)
6. Sports Fee (annual)
7. Examination Fee (per exam)
8. Transport Fee (optional, route-based)
9. Hostel Fee (optional, room-type based)
10. Mess Fee (optional, monthly)
11. Medical Insurance (annual)
12. Alumni Fee (one-time, final year)
13. Late Fee (auto-calculated on delay)
14. Re-examination Fee (per course)
```

**Fee Structure Matrix:**

```
Example: B.Tech Computer Science

┌─────────────────────────────────────────────────────────────┐
│ Fee Component      | General | OBC    | SC/ST  | EWS     │
├─────────────────────────────────────────────────────────────┤
│ Tuition (sem)      | ₹50,000 | ₹25,000| ₹0     | ₹25,000 │
│ Development (yr)   | ₹10,000 | ₹10,000| ₹5,000 | ₹10,000 │
│ Lab Fee (sem)      | ₹5,000  | ₹5,000 | ₹5,000 | ₹5,000  │
│ Library (sem)      | ₹2,000  | ₹2,000 | ₹2,000 | ₹2,000  │
│ Exam Fee (sem)     | ₹1,500  | ₹1,500 | ₹0     | ₹1,500  │
│ Insurance (yr)     | ₹500    | ₹500   | ₹500   | ₹500    │
├─────────────────────────────────────────────────────────────┤
│ TOTAL (Semester 1) | ₹69,000 | ₹44,000| ₹7,000 | ₹44,000 │
│ (Excluding hostel) |         |        |        |         │
└─────────────────────────────────────────────────────────────┘

Scholarship Adjustments:
- Merit Scholarship: 100% tuition waiver for top 10 rankers
- Sports Quota: 50% tuition waiver
- Staff Children: 25% all fees
```

**Configuration Interface:**

```
1. Navigate to Accounts → Fee Structure → Create New
2. Select Program: B.Tech Computer Science
3. Select Academic Year: 2024-25
4. Add Fee Heads:
   - Click "Add Component"
   - Select head type from dropdown
   - Enter base amount
   - Set frequency (One-time/Monthly/Quarterly/Semester/Annual)
   - Define applicability (All students/Specific categories)
   
5. Configure Category-wise Variations:
   - Click "Add Category Rule"
   - Select category (OBC/SC/ST/EWS/General)
   - Apply discount percentage or fixed amount
   - OR enter custom amounts per component
   
6. Set Payment Plans:
   Option A: Full Payment (5% discount)
   Option B: Two Installments (No discount)
   Option C: Monthly EMIs (2% additional charge)
   
7. Configure Late Fee Rules:
   - Grace period: 7 days
   - After grace: ₹100 per day
   - Maximum late fee: ₹5,000
   
8. Save and Publish
```

---

## 2.3 Fee Collection & Payment Processing

### FR-FEE-002: Multi-Channel Fee Collection

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-FEE-002 |
| **Feature** | Fee Collection Across Multiple Channels |
| **User Story** | As a parent, I want to pay fees through my preferred method so that it's convenient for me |

**Payment Channels:**

**Channel 1: Online Payment Gateway**
```
Integrated Gateways:
- Razorpay (UPI, Cards, NetBanking, Wallets)
- PayU (Credit cards, EMI)
- CC Avenue (Multi-currency for NRI)
- PhonePe/Paytm (UPI)
- BharatQR

Payment Flow:
1. Student/Parent logs into portal
2. Navigates to "Pay Fees"
3. System shows outstanding amount with breakdown
4. User selects payment method
5. Redirected to payment gateway
6. Completes payment authentication
7. Callback to EduCore with payment status
8. Auto-generates receipt
9. Updates ledger in real-time
10. Sends confirmation SMS/Email with receipt PDF
```

**Channel 2: Counter Payment (Cash/Card at Office)**
```
Accountant workflow:
1. Student/Parent visits accounts office
2. Accountant searches student by ID/name
3. System displays fee dues
4. Parent selects payment mode:
   - Cash (with denomination entry)
   - Card (swipe machine integration)
   - Cheque/DD (details entry)
   - UPI QR scan (dynamic QR generation)
   
5. Accountant enters amount received
6. System validates against due amount
7. If partial payment:
   - Records partial payment
   - Shows remaining balance
   - Generates interim receipt
   
8. If full payment:
   - Clears all dues
   - Generates final receipt
   - Removes defaulter tag
   
9. Prints receipt (thermal/A4)
10. Sends digital copy via SMS/Email
```

**Channel 3: Bank Transfer (NEFT/RTGS)**
```
1. Institution provides bank details on portal
2. Parent initiates transfer from their bank
3. Enters transaction reference in portal
4. System marks as "Pending Verification"
5. Accountant matches with bank statement
6. Verifies and approves
7. Receipt generated
```

**Channel 4: Bulk Payment (Corporate Sponsorship)**
```
For companies sponsoring employees' children:
1. Company uploads list of beneficiaries
2. System calculates total amount
3. Single invoice generated for company
4. Company makes bulk payment
5. Individual receipts generated for each student
6. Linked to respective student accounts
```

**Receipt Generation:**

```
GST-Compliant Receipt Format:

╔══════════════════════════════════════════════════════╗
║                  TAX INVOICE                         ║
║                                                      ║
║  Institution Name & Address                          ║
║  GSTIN: 27ABCDE1234F1Z5                              ║
║                                                      ║
║  Receipt No: RCPT-2024-001234                        ║
║  Date: 15-Aug-2024                                   ║
║                                                      ║
║  Received from: Mr. Rajesh Sharma                    ║
║  Student: Priya Sharma (Roll: CS2024001)             ║
║  Class: B.Tech CSE Semester 3                        ║
║                                                      ║
║  Payment Details:                                    ║
║  ┌────────────────────┬──────────┬────────┬────────┐ ║
║  │ Fee Head           │ Amount   │ GST %  │ GST Amt│ ║
║  ├────────────────────┼──────────┼────────┼────────┤ ║
║  │ Tuition Fee        │ 50,000   │ 0%     │ 0      │ ║
║  │ Development Fee    │ 10,000   │ 18%    │ 1,800  │ ║
║  │ Lab Fee            │ 5,000    │ 18%    │ 900    │ ║
║  ├────────────────────┼──────────┼────────┼────────┤ ║
║  │ Subtotal           │ 65,000   │        │ 2,700  │ ║
║  │ CGST (9%)          │          │        │ 1,350  │ ║
║  │ SGST (9%)          │          │        │ 1,350  │ ║
║  ├────────────────────┼──────────┼────────┼────────┤ ║
║  │ GRAND TOTAL        │          │        │ 67,700 │ ║
║  └────────────────────┴──────────┴────────┴────────┘ ║
║                                                      ║
║  Payment Mode: UPI                                   ║
║  Transaction ID: 123456789012                        ║
║                                                      ║
║  [QR Code for Verification]                          ║
║  Verify at: https://verify.educore.in/RCPT-2024-... ║
║                                                      ║
║  Authorized Signatory                                ║
║  [Digital Signature]                                 ║
╚══════════════════════════════════════════════════════╝
```

---

## 2.4 Installment Management & Defaulter Tracking

### FR-FEE-003: Installment Plans & Reminders

**Installment Configuration:**

```
Example: Semester Fee ₹60,000 in 3 Installments

Installment 1 (40%):
- Due Date: 1st June 2024
- Amount: ₹24,000
- Grace Period: 7 days
- Late Fee after grace: ₹100/day

Installment 2 (35%):
- Due Date: 1st August 2024
- Amount: ₹21,000
- Grace Period: 7 days

Installment 3 (25%):
- Due Date: 1st October 2024
- Amount: ₹15,000
- Grace Period: 7 days

Early Payment Discount:
- Pay all at once before 1st June: 5% discount (₹3,000 off)
```

**Automated Reminder System:**

```
Reminder Schedule:

7 days before due date:
  SMS: "Dear Parent, Fee installment of ₹24,000 due on 1-Jun. 
        Pay early & save ₹3,000. Login: [link]"

1 day before due date:
  SMS + WhatsApp: "Reminder: Fee due tomorrow. Avoid late fee. 
                   Pay now: [UPI link]"

On due date (9 AM):
  Email + SMS: "Today is the due date for fee payment. 
                Pay before midnight to avoid late fee."

1 day after due date:
  SMS: "Late fee of ₹100/day applicable from today. 
        Clear dues immediately."

7 days after due date:
  Phone call task created for accounts staff
  Email to parent with late fee calculation

15 days after due date:
  Warning letter generated
  Mark as "High Risk Defaulter"
  Restrict exam form submission

30 days after due date:
  Show-cause notice
  Block attendance viewing
  Escalate to principal

60 days after due date:
  Discontinue student (status change to Inactive)
  Legal notice initiated
```

**Defaulter Dashboard:**

```
┌─────────────────────────────────────────────────────────────┐
│ Fee Defaulter Dashboard                                     │
├─────────────────────────────────────────────────────────────┤
│ Summary:                                                    │
│ - Total Defaulters: 234                                     │
│ - Amount Outstanding: ₹1.45 Crore                           │
│ - > 30 Days: 45 students                                    │
│ - > 60 Days: 12 students                                    │
├─────────────────────────────────────────────────────────────┤
│ Defaulter List (Sortable by Days Overdue):                  │
│ ┌────────┬──────────┬─────────┬──────────┬────────┬──────┐ │
│ │ Roll   │ Name     │ Due Amt │ Days Due │ Contact│Action│ │
│ ├────────┼──────────┼─────────┼──────────┼────────┼──────┤ │
│ │ CS201  │ Amit K.  │ ₹24,000 │ 45       │ [Call] │[Send]│ │
│ │ CS202  │ Neha P.  │ ₹60,000 │ 62       │ [Call] │[Notice]││
│ │ ME101  │ Rohan S. │ ₹15,000 │ 12       │ [Call] │[Send]│ │
│ └────────┴──────────┴─────────┴──────────┴────────┴──────┘ │
│                                                             │
│ Quick Actions:                                              │
│ [Send Bulk SMS] [Generate Letters] [Export to Excel]       │
└─────────────────────────────────────────────────────────────┘
```

---

## 2.5 Refund Processing

### FR-FEE-004: Refund Management

**Refund Scenarios:**

| Scenario | Refund % | Processing Time | Approval Required |
|----------|----------|-----------------|-------------------|
| Admission cancelled before classes start | 100% (minus ₹1000 admin fee) | 7 days | Accountant |
| Withdrawal within 15 days of classes | 80% of tuition fee | 15 days | Principal |
| Withdrawal within 30 days | 50% of tuition fee | 30 days | Principal + CFO |
| Withdrawal after 30 days | 0% | N/A | N/A |
| Duplicate payment | 100% | 3 days | Accountant |
| Scholarship applied post-payment | Differential amount | 7 days | Accountant |

**Refund Workflow:**

```
1. Student/Parent submits refund request:
   - Login to portal
   - Navigate to "Request Refund"
   - Select reason from dropdown
   - Upload supporting documents (if required)
   - Enter bank account details for refund
   - Submit request

2. System validates:
   - Eligibility based on dates
   - Calculation of refundable amount
   - Bank account verification (penny drop)

3. Approval workflow:
   - Route to appropriate approver based on amount
   - Approver reviews and approves/rejects
   - If rejected, reason communicated

4. Payment processing:
   - NEFT/IMPS initiation
   - UTR number recorded
   - Receipt generated

5. Notification:
   - SMS/Email with refund status
   - Refund receipt downloadable
```

---

# 3. Module 3: Expense Management

## 3.1 Overview

**Module ID**: EXP-001  
**Priority**: P1 (High)  
**Description**: Track institutional expenses, manage purchase requisitions, vendor payments, and budget monitoring.

---

## 3.2 Expense Categories & Budgeting

### FR-EXP-001: Expense Classification

**Expense Heads:**

```
1. Salary & Benefits
   - Teaching Staff Salary
   - Non-Teaching Staff Salary
   - Guest Lecturer Payments
   - Provident Fund Contributions
   - Gratuity

2. Infrastructure & Maintenance
   - Building Maintenance
   - Electrical & Plumbing
   - HVAC Services
   - Pest Control
   - Housekeeping Supplies

3. Academic Expenses
   - Laboratory Consumables
   - Library Books & Journals
   - Stationery & Printing
   - Software Licenses
   - Research Grants

4. Utilities
   - Electricity
   - Water
   - Internet & Telephone
   - Gas

5. Administrative
   - Office Supplies
   - Travel & Conveyance
   - Marketing & Advertising
   - Professional Fees (Audit, Legal)
   - Insurance Premiums

6. Events & Activities
   - Sports Events
   - Cultural Programs
   - Seminars & Conferences
   - Industrial Visits

7. Capital Expenditure
   - Equipment Purchase
   - Furniture
   - Vehicles
   - Construction
```

**Budget Allocation:**

```
Annual Budget Planning:

1. Department heads submit budget requests (April)
2. Finance team consolidates
3. Management reviews and approves
4. System allocates budgets per department per head

Example Budget:
┌────────────────────┬─────────────┬─────────────┬──────────┐
│ Department         │ Head        │ Allocated   │ Utilized │
├────────────────────┼─────────────┼─────────────┼──────────┤
│ Computer Engg      │ Lab Supplies│ ₹5,00,000   │ ₹2,34,000│
│ Mechanical Engg    │ Equipment   │ ₹10,00,000  │ ₹8,75,000│
│ Library            │ Books       │ ₹3,00,000   │ ₹1,20,000│
│ Admin              │ Travel      │ ₹2,00,000   │ ₹1,85,000│
└────────────────────┴─────────────┴─────────────┴──────────┘

Alerts:
- 75% budget utilized → Yellow alert to HOD
- 90% budget utilized → Red alert, requires CFO approval for new expenses
- 100% budget exhausted → Block further expenses in that head
```

---

## 3.3 Purchase Requisition & Approval

### FR-EXP-002: Purchase Workflow

**Purchase Request Flow:**

```
1. Staff raises purchase requisition:
   - Item description
   - Quantity
   - Estimated cost
   - Vendor suggestion (optional)
   - Justification
   - Required by date

2. HOD reviews and approves

3. Finance checks budget availability:
   IF budget_available:
      proceed
   ELSE:
      reject OR escalate for budget enhancement

4. Principal/CFO approval (based on amount):
   - < ₹10,000: Auto-approved
   - ₹10,000 - ₹50,000: Principal approval
   - ₹50,000 - ₹2,00,000: CFO approval
   - > ₹2,00,000: Management committee approval

5. Purchase order generated and sent to vendor

6. Goods received:
   - Store keeper verifies quantity & quality
   - GRN (Goods Received Note) generated

7. Invoice processing:
   - Vendor invoice matched with PO and GRN
   - Three-way match validation
   - Payment scheduled as per credit terms

8. Payment released via cheque/NEFT
```

---

# 4. Module 4: Faculty Payroll & Salary

## 4.1 Overview

**Module ID**: PAY-001  
**Priority**: P1 (High)  
**Description**: Automated salary calculation, payslip generation, tax deductions, loan management, and statutory compliance.

---

## 4.2 Salary Structure Configuration

### FR-PAY-001: Flexible Salary Components

**Salary Components:**

```
Earnings:
1. Basic Salary (40-50% of CTC)
2. Dearness Allowance (DA) - % of Basic
3. House Rent Allowance (HRA) - % of Basic
4. Transport Allowance (fixed)
5. Medical Allowance (fixed)
6. Special Allowance (balancing component)
7. Conveyance Allowance
8. Phone/Internet Reimbursement
9. Book Grant (annual)
10. Research Allowance (for PhD faculty)

Deductions:
1. Provident Fund (12% of Basic)
2. Professional Tax (state-specific, max ₹2,500/year)
3. Income Tax (TDS as per IT Act)
4. National Pension Scheme (NPS) - optional
5. Loan EMI (if any)
6. Advance Salary recovery
7. Leave without pay adjustment
8. Penalty (late coming, absence)

Reimbursements (Tax-exempt up to limits):
1. Fuel reimbursement (bills required)
2. Newspaper allowance
3. Children education allowance (₹100/month/child, max 2)
4. Hostel subsidy (₹300/month/child)
```

**Salary Configuration Example:**

```
Faculty: Dr. Rajesh Kumar
Designation: Associate Professor
Experience: 12 years

CTC: ₹12,00,000 per annum

Monthly Breakdown:
┌─────────────────────────────┬─────────────┬─────────────┐
│ Component                   │ Monthly     │ Annual      │
├─────────────────────────────┼─────────────┼─────────────┤
│ BASIC SALARY                │ ₹40,000     │ ₹4,80,000   │
│ Dearness Allowance (10%)    │ ₹4,000      │ ₹48,000     │
│ HRA (40% of Basic)          │ ₹16,000     │ ₹1,92,000   │
│ Transport Allowance         │ ₹3,600      │ ₹43,200     │
│ Medical Allowance           │ ₹1,250      │ ₹15,000     │
│ Special Allowance           │ ₹10,150     │ ₹1,21,800   │
│ Book Grant (monthly prov.)  │ ₹2,000      │ ₹24,000     │
├─────────────────────────────┼─────────────┼─────────────┤
│ GROSS EARNINGS              │ ₹77,000     │ ₹9,24,000   │
├─────────────────────────────┼─────────────┼─────────────┤
│ LESS DEDUCTIONS:            │             │             │
│ Provident Fund (12%)        │ ₹4,800      │ ₹57,600     │
│ Professional Tax            │ ₹200        │ ₹2,400      │
│ TDS (estimated)             │ ₹3,500      │ ₹42,000     │
│ NPS (employee contribution) │ ₹4,000      │ ₹48,000     │
├─────────────────────────────┼─────────────┼─────────────┤
│ TOTAL DEDUCTIONS            │ ₹12,500     │ ₹1,50,000   │
├─────────────────────────────┼─────────────┼─────────────┤
│ NET SALARY (in hand)        │ ₹64,500     │ ₹7,74,000   │
└─────────────────────────────┴─────────────┴─────────────┘

Employer Contribution (not deducted from salary):
- PF Employer: ₹4,800/month
- ESI (if applicable): ₹900/month
- Total Employer Cost: ₹12,00,000 + ₹68,400 = ₹12,68,400
```

---

## 4.3 Payroll Processing

### FR-PAY-002: Automated Salary Calculation

**Monthly Payroll Cycle:**

```
Day 1-25: Data Collection
- Attendance data synced (late arrivals, leaves, absences)
- Leave without pay entries
- Overtime hours (if applicable)
- Bonus/commission entries
- Loan EMI updates
- New joinings and resignations

Day 26: Payroll Lock
- Freeze all input data
- Generate preliminary payroll report
- HR reviews for anomalies

Day 27: Validation
- Compare with previous month (variance analysis)
- Check for outliers (>20% variation flagged)
- Verify statutory limits (PF ceiling, PT slabs)

Day 28: Approval
- CFO reviews and approves
- Digital signature applied

Day 29: Disbursement
- Bank transfer file generated (SBI/HDFC format)
- Uploaded to corporate banking
- Salary credited to employee accounts

Day 30: Payslip Distribution
- Payslips emailed to all employees
- Available on employee portal
- SMS notification sent
```

**Payslip Format:**

```
╔══════════════════════════════════════════════════════╗
║                    PAYSLIP                           ║
║                   August 2024                        ║
║                                                      ║
║  Employee: Dr. Rajesh Kumar                          ║
║  ID: EMP-CS-042                                      ║
║  Designation: Associate Professor                    ║
║  Department: Computer Engineering                    ║
║  Bank A/c: XXXXXXXXXXXX1234                          ║
║  PAN: ABCDE1234F                                     ║
║                                                      ║
║  EARNINGS               │ Amount  │ DEDUCTIONS│Amount│
║  ──────────────────────┼─────────┼───────────┼──────│
║  Basic Salary          │ 40,000  │ PF        │ 4,800│
║  DA (10%)              │  4,000  │ PT        │   200│
║  HRA (40%)             │ 16,000  │ TDS       │ 3,500│
║  Transport Allowance   │  3,600  │ NPS       │ 4,000│
║  Medical Allowance     │  1,250  │           │      │
║  Special Allowance     │ 10,150  │           │      │
║  Book Grant            │  2,000  │           │      │
║  ──────────────────────┼─────────┼───────────┼──────│
║  Gross Earnings        │ 77,000  │ Total Ded │12,500│
║  ──────────────────────┴─────────┴───────────┴──────│
║                                                      ║
║  NET SALARY          : ₹64,500                       ║
║  (Rupees Sixty Four Thousand Five Hundred Only)     ║
║                                                      ║
║  Payment Date: 29-Aug-2024                           ║
║  UTR No: SBIN0123456789                              ║
║                                                      ║
║  [Download PDF] [Print]                              ║
╚══════════════════════════════════════════════════════╝
```

---

## 4.4 Statutory Compliance

### FR-PAY-003: Compliance Reports

**Monthly Filings:**

| Form | Purpose | Due Date | Authority |
|------|---------|----------|-----------|
| ECR (PF) | Provident Fund Return | 15th of next month | EPFO |
| TDS Return (Form 24Q) | Quarterly TDS | 7th of next month | Income Tax |
| Professional Tax | Monthly PT | 15th of next month | State Govt |
| ESI Return | Employee State Insurance | 15th of next month | ESIC |

**Auto-Generation Features:**

```
System generates:
1. PF ECR file (Excel format for EPFO portal upload)
2. TDS challan (Form 281)
3. Form 16 (annual, for employees)
4. Form 24Q (quarterly TDS return)
5. Investment declaration compilation
6. Tax computation statements
```

---

# 5. Module 5: Lecture Scheduling & Timetable

## 5.1 Overview

**Module ID**: TIME-001  
**Priority**: P1 (High)  
**Description**: Conflict-free timetable generation, resource allocation, room scheduling, and calendar management for all users.

---

## 5.2 Constraint-Based Timetable Generation

### FR-TIME-001: Genetic Algorithm Scheduler

**Hard Constraints (Must Not Violate):**

```
1. Faculty Conflict:
   - Same teacher cannot teach two classes simultaneously
   
2. Room Conflict:
   - Same room cannot host two classes simultaneously
   
3. Student Conflict:
   - Same batch cannot have two subjects at same time
   
4. Capacity Constraint:
   - Class size <= Room capacity
   
5. Availability Constraint:
   - Teacher unavailable times (leave, other commitments)
   - Room unavailable times (maintenance, events)
   
6. Duration Match:
   - Class duration must fit in allocated slot
```

**Soft Constraints (Try to Optimize):**

```
1. Teacher Preference:
   - Preferred time slots (morning/evening)
   - Consecutive classes minimized
   - Gap between classes of same subject
   
2. Workload Distribution:
   - Even distribution across week
   - Max teaching hours per day <= 6
   - Minimum gap for preparation
   
3. Room Optimization:
   - Minimize room changes for teachers
   - Prefer nearest lab for theory+practical combo
   
4. Student Convenience:
   - No free periods in middle of day
   - Heavy subjects in morning slots
   - Physical education not after lunch
```

**Algorithm Flow:**

```
FUNCTION generate_timetable(semester, constraints):
    // Step 1: Initialize population
    population = create_random_timetables(100)
    
    // Step 2: Evaluate fitness
    FOR each timetable IN population:
        fitness = calculate_fitness(timetable, constraints)
        // Fitness = (hard_constraints_met * 1000) + soft_constraints_score
    
    // Step 3: Genetic evolution
    FOR generation IN 1..1000:
        // Selection
        parents = select_best_timetables(population, 50)
        
        // Crossover
        children = crossover(parents)
        
        // Mutation
        mutated = apply_mutation(children, rate=0.1)
        
        // Evaluate new generation
        population = mutated + best_of_previous
        
        // Check convergence
        IF best_fitness > threshold:
            BREAK
    
    // Step 4: Return best solution
    RETURN get_best_timetable(population)
```

---

## 5.3 Interactive Timetable Editor

### FR-TIME-002: Drag-and-Drop Scheduler

**UI Features:**

```
1. Calendar View:
   - Weekly view (Mon-Sat)
   - Time slots (8 AM - 6 PM, 1-hour intervals)
   - Color-coded by subject/faculty
   
2. Drag-and-Drop:
   - Drag subject from palette to time slot
   - Move existing classes to different slots
   - Swap two classes
   
3. Real-time Conflict Detection:
   - Red highlight if conflict detected
   - Tooltip showing conflict details
   - Suggestions for alternative slots
   
4. Bulk Operations:
   - Copy timetable from previous semester
   - Apply pattern to multiple batches
   - Clone faculty schedule
```

**Conflict Resolution Assistant:**

```
When conflict detected:

┌─────────────────────────────────────────────────────────┐
│ ⚠️ CONFLICT DETECTED                                    │
├─────────────────────────────────────────────────────────┤
│ Issue: Dr. Sharma already assigned to "Data Structures" │
│        in Room 301 at 10 AM on Monday                   │
│                                                         │
│ You're trying to schedule: "DBMS" with same teacher     │
│                                                         │
│ Suggested Solutions:                                    │
│ 1. Move DBMS to 11 AM (Room 301 available)             │
│ 2. Move DBMS to Tuesday 10 AM (Teacher available)      │
│ 3. Assign different teacher for DBMS (List available)  │
│ 4. Use Room 302 (same time, needs projector)           │
├─────────────────────────────────────────────────────────┤
│ [Auto-fix] [Manual Override] [Cancel]                   │
└─────────────────────────────────────────────────────────┘
```

---

## 5.4 Universal Calendar System

### FR-TIME-003: Integrated Calendar for All Users

**Calendar Views:**

```
Institution Calendar:
- Academic year start/end
- Holidays (national, state, local)
- Festival breaks
- Examination periods
- Result declaration dates
- Convocation day

Department Calendar:
- Department events
- Guest lectures
- Workshops
- Industry visits
- Project deadlines

Faculty Calendar:
- Teaching schedule
- Office hours
- Leave marked
- Conference/training
- Meeting schedules

Student Calendar:
- Class timetable
- Exam schedule
- Assignment due dates
- Event participation
- Personal events (synced from Google/Outlook)
```

**Calendar Integration:**

```
Sync Options:
1. iCal Feed:
   - Subscribe URL provided
   - Auto-updates in Google Calendar, Outlook, Apple Calendar
   
2. Google Calendar API:
   - One-click sync to personal Google account
   - Two-way sync (personal events visible in app)
   
3. Export Formats:
   - PDF (printable monthly view)
   - Excel (for data analysis)
   - CSV (for import to other systems)
```

**Event Scheduling:**

```
Schedule Extra Class/Event:

1. Organizer selects:
   - Event type (Guest Lecture/Workshop/Extra Class)
   - Required resources (room, projector, lab equipment)
   - Preferred date/time
   - Target audience (specific batch/all students)
   
2. System checks availability:
   - Room free? ✓/✗
   - Faculty available? ✓/✗
   - Batch free? ✓/✗
   - Equipment available? ✓/✗
   
3. If conflicts:
   - Suggests alternative slots
   - Shows waitlist option
   
4. Once confirmed:
   - Calendar updated for all participants
   - Room booking locked
   - Notifications sent
   - Attendance sheet pre-generated
```

---

# 6. Module 6: Universal Attendance System

## 6.1 Overview

**Module ID**: ATT-001  
**Priority**: P0 (Critical)  
**Description**: Multi-modal attendance tracking (NFC, QR, Biometric, Manual) for students and faculty with automated alerts and reporting.

---

## 6.2 NFC-Based Attendance

### FR-ATT-001: Mobile NFC Tap System

**Technology Stack:**
```
- NFC Type 4 Tags (NTAG213/215)
- Android NFC (API level 14+)
- iOS Core NFC (iPhone 7+)
- AES-128 encryption for tag data
```

**Implementation Flow:**

```
Setup Phase:
1. Institution purchases NFC tags/stickers (₹20-50 each)
2. Admin registers each tag in system:
   - Tag UID scanned
   - Assigned to student/faculty
   - Linked to user profile
   
3. Users install EduCore mobile app
4. App requests NFC permission
5. Test tap performed to verify

Daily Usage - Student Side:
1. Student arrives at campus
2. Opens EduCore app (or unlock phone if background read enabled)
3. Taps phone on NFC reader at entrance
   OR taps NFC sticker on fellow student's phone (peer-to-peer)
   
4. App reads tag, encrypts data:
   {
     user_id: "CS2024001",
     timestamp: "2024-08-15T09:15:32+05:30",
     location: "Main Gate",
     device_id: "abc123xyz",
     signature: "encrypted_hash"
   }
   
5. Sends to server via WiFi/4G
6. Server validates:
   - User exists and is active
   - Within allowed time window (e.g., 8 AM - 10 AM for morning)
   - Location matches expected checkpoint
   - Not a duplicate tap (within 5 minutes)
   
7. Marks attendance
8. Push notification: "Attendance marked at 9:15 AM ✓"

Faculty Side - Classroom NFC:
1. Faculty arrives at classroom
2. Places phone on desk (NFC reader mode)
3. Students tap their phones on faculty's phone as they enter
4. Real-time attendance list displayed on faculty app
5. Faculty can manually mark absentees after class starts
```

**Security Measures:**

```
1. Anti-spoofing:
   - Device fingerprinting
   - GPS location verification
   - Time-window enforcement
   - One-tap-per-person-per-session
   
2. Encryption:
   - Tag data encrypted with AES-128
   - TLS 1.3 for data transmission
   - Server-side signature verification
   
3. Offline Mode:
   - App stores taps locally if no internet
   - Syncs when connectivity restored
   - Timestamp preserved
```

---

## 6.3 QR Code Attendance

### FR-ATT-002: Projector QR Scan System

**Use Case:**
Perfect for classrooms with projectors, lecture halls, and large venues.

**Workflow:**

```
1. Faculty starts class:
   - Opens EduCore Faculty app
   - Selects "Mark Attendance"
   - Chooses class and subject
   
2. System generates dynamic QR code:
   - Displayed on projector/screen
   - Contains encrypted session data:
     {
       faculty_id: "EMP042",
       class_id: "CS301-A",
       subject: "Data Structures",
       timestamp: "2024-08-15T10:00:00+05:30",
       session_token: "random_256_bit_value",
       expires_at: "2024-08-15T10:05:00+05:30"
     }
   - QR refreshes every 30 seconds (prevents screenshot sharing)
   
3. Students scan QR:
   - Open EduCore Student app
   - Tap "Scan QR" button
   - Camera scans projector QR
   - App decrypts and validates session
   
4. Geo-fencing validation:
   - App checks device GPS
   - Must be within 50 meters of classroom
   - Prevents remote marking by friends
   
5. Attendance submission:
   - Student app sends:
     {
       student_id: "CS2024001",
       session_token: "...",
       gps_location: "18.5204° N, 73.8567° E",
       device_id: "xyz789"
     }
   - Server validates and marks present
   
6. Real-time dashboard:
   - Faculty sees attendance count updating live
   - List of present/absent students
   - Can close attendance after 10 minutes
   
7. Proxy prevention:
   - Each QR valid for one scan per student
   - Screenshot QR won't work (expires in 30 sec)
   - GPS mismatch rejected
   - Device ID logged for audit
```

**QR Code Display:**

```
┌─────────────────────────────────────────────────────────┐
│  📊 Data Structures - CS301-A                           │
│  Faculty: Dr. Sharma                                    │
│                                                         │
│           Scan QR to mark attendance                    │
│                                                         │
│              ████████████████████                      │
│              ██                ██                      │
│              ██  ▓▓▓▓  ▓▓  ▓▓▓▓ ██                      │
│              ██  ▓▓  ▓▓▓▓▓▓  ▓▓ ██                      │
│              ██  ▓▓▓▓▓▓  ▓▓▓▓  ██                      │
│              ██                ██                      │
│              ████████████████████                      │
│                                                         │
│  ⏱️  Refreshes in: 23 seconds                           │
│  📍 Must be in classroom (GPS enabled)                  │
│                                                         │
│  Present: 42/60                                         │
│  [Close Attendance] [Extend Time]                       │
└─────────────────────────────────────────────────────────┘
```

---

## 6.4 Biometric Integration

### FR-ATT-003: Fingerprint/Face Recognition

**Supported Devices:**
- Morpho/Safran biometric scanners
- Hikvision face recognition terminals
- Zkteco fingerprint devices
- Any device with SDK support

**Integration Architecture:**

```
Biometric Device → Local Agent (Windows Service) → EduCore Cloud API

OR

Biometric Device → Direct API (if network-enabled) → EduCore Cloud
```

**Enrollment Process:**

```
1. Student/Faculty goes to admin office
2. Admin opens biometric enrollment module
3. Captures:
   - Fingerprint (right thumb + left thumb)
   - Face photo (multiple angles)
   - Iris scan (optional, high-security institutions)
   
4. Biometric template created and stored
5. Linked to user profile
6. Test verification performed
```

**Daily Attendance:**

```
Morning Entry:
1. User places finger on scanner / looks at camera
2. Device matches biometric template
3. Sends user ID + timestamp to server
4. Server marks attendance
5. Display shows: "Welcome, Rahul Sharma - Class CS301-A"

Exit Tracking (Optional):
- Second punch at end of day
- Calculate total hours on campus
- Flag early departures
```

---

## 6.5 Manual Attendance & Corrections

### FR-ATT-004: Fallback & Override System

**Manual Marking by Faculty:**

```
1. Faculty opens class roster in app/web
2. List of students displayed with checkboxes
3. Default: All marked present
4. Faculty unchecks absentees
5. Adds remarks if needed (e.g., "Late by 15 min")
6. Submits attendance
7. Students notified of status
```

**Attendance Correction Workflow:**

```
Scenario: Student was marked absent but was present

1. Student raises correction request:
   - App → Attendance → Request Correction
   - Select date and class
   - Provide reason
   - Optional: Upload proof (photo, witness)
   
2. Faculty receives notification
3. Reviews request
4. Approves or rejects with reason
5. If approved:
   - Attendance updated
   - Audit log created
   - Notification sent
   
6. If rejected:
   - Student can escalate to HOD
   - HOD makes final decision
```

---

## 6.6 Attendance Analytics & Alerts

### FR-ATT-005: Smart Notifications

**Automated Alerts:**

| Trigger | Recipient | Message |
|---------|-----------|---------|
| Student absent | Parent (SMS) | "Your child [Name] is absent today. Contact school if this is unexpected." |
| Attendance < 75% | Student + Parent | "Warning: Your attendance is 72%. Minimum 75% required for exam eligibility." |
| Faculty absent | HOD + Admin | "Dr. Sharma is absent today. Classes need substitute arrangement." |
| Early departure | Parent | "Your child left campus at 2 PM (before regular 4 PM dismissal)." |
| Continuous absent (3 days) | Counselor | "Student [Name] absent for 3 consecutive days. Follow-up required." |

**Attendance Reports:**

```
Monthly Attendance Report - Class CS301-A

┌──────────┬─────────────┬───────┬────────┬────────┬─────────┐
│ Roll No  │ Name        │ Total │ Present│ Absent │ %       │
├──────────┼─────────────┼───────┼────────┼────────┼─────────┤
│ CS202401 │ Amit Kumar  │ 22    │ 20     │ 2      │ 90.9%   │
│ CS202402 │ Priya Singh │ 22    │ 16     │ 6      │ 72.7% ⚠️│
│ CS202403 │ Rahul Das   │ 22    │ 22     │ 0      │ 100%    │
└──────────┴─────────────┴───────┴────────┴────────┴─────────┘

Class Average: 87.3%
Lowest: Priya Singh (72.7%) - Needs intervention
Highest: Rahul Das (100%)
```

---

# 7. Integration & Reporting

## 7.1 Cross-Module Integrations

```
┌─────────────────────────────────────────────────────────────┐
│                     Integration Matrix                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Mgmt ←→ Fee Mgmt:                                    │
│  - Student status affects fee collection (Inactive = block) │
│  - Fee default triggers user status change                  │
│                                                             │
│  Attendance ←→ Payroll:                                    │
│  - Faculty attendance affects salary calculation            │
│  - Late arrivals trigger penalty deduction                  │
│                                                             │
│  Timetable ←→ Attendance:                                  │
│  - Attendance marked only for scheduled classes             │
│  - Substitute arrangements tracked                          │
│                                                             │
│  Fee Mgmt ←→ Results:                                      │
│  - Fee clearance required for result download               │
│  - Defaulter list blocks exam registration                  │
│                                                             │
│  User Mgmt ←→ Payroll:                                     │
│  - Employee onboarding creates payroll record               │
│  - Exit process triggers full & final settlement            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 7.2 Executive Dashboards

### FR-RPT-001: Role-Based Dashboards

**Principal Dashboard:**

```
┌─────────────────────────────────────────────────────────────┐
│  Good Morning, Dr. Deshmukh                                 │
│  PVG College of Engineering                                 │
├─────────────────────────────────────────────────────────────┤
│  QUICK STATS                                                │
│  ┌────────────┬────────────┬────────────┬────────────┐     │
│  │ 👥 Students│ 👨‍🏫 Faculty │ 📚 Classes │ 💰 Collections│     │
│  │   2,450    │    185     │    42      │  ₹12.5 Cr   │     │
│  │   +3.2%    │    +5      │   Today    │  (85% of target)│   │
│  └────────────┴────────────┴────────────┴────────────┘     │
├─────────────────────────────────────────────────────────────┤
│  ALERTS (5)                                                 │
│  ⚠️ 45 students with attendance < 75%                       │
│  ⚠️ ₹2.3 Cr fee pending (>30 days)                          │
│  ⚠️ 3 faculty on leave today                                │
│  ⚠️ NAAC report submission due in 15 days                   │
│  ℹ️ Board visit scheduled for 25 Aug                        │
├─────────────────────────────────────────────────────────────┤
│  RECENT ACTIVITY                                            │
│  • 234 fees collected today (₹8.5 Lakhs)                    │
│  • 1,842 attendance marked (92% of classes)                 │
│  • 12 new admission approvals pending                       │
│  • 5 expense requests awaiting approval                     │
└─────────────────────────────────────────────────────────────┘
```

**CFO Dashboard:**

```
┌─────────────────────────────────────────────────────────────┐
│  Financial Overview - August 2024                           │
├─────────────────────────────────────────────────────────────┤
│  COLLECTION SUMMARY                                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Target: ₹15.0 Cr | Collected: ₹12.5 Cr (83%)         │   │
│  │ ████████████████████████████░░░░░░░░░░░░░░░░░░░░░░   │   │
│  │ Outstanding: ₹2.5 Cr | Overdue: ₹1.2 Cr              │   │
│  └──────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│  EXPENSE TRACKING                                           │
│  Budget Utilization: 62% (₹8.4 Cr of ₹13.5 Cr)             │
│  Top Expense Heads:                                         │
│  • Salary: ₹6.2 Cr                                          │
│  • Infrastructure: ₹1.1 Cr                                  │
│  • Utilities: ₹0.6 Cr                                       │
├─────────────────────────────────────────────────────────────┤
│  PAYROLL STATUS                                             │
│  August Salary: Processed ✓                                 │
│  Disbursed: 29-Aug | Total: ₹6.8 Cr                         │
│  Next Payroll: 29-Sep (25 days remaining)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 7.3 Regulatory Reports

### FR-RPT-002: Compliance Reporting

**Auto-Generated Reports:**

| Report | Frequency | Recipient | Format |
|--------|-----------|-----------|--------|
| AISHE Return | Annual | Ministry of Education | Online Portal |
| AICTE MIS | Annual | AICTE | Excel + Online |
| University Affiliation Return | Annual | Affiliating University | Prescribed Format |
| Fee Collection Report | Monthly | Management | PDF + Excel |
| TDS Returns | Quarterly | Income Tax Dept | Online (Form 24Q) |
| PF ECR | Monthly | EPFO | Excel (ECR File) |
| Attendance Summary | Monthly | Parents | PDF (via Email) |

---

**Document End**
