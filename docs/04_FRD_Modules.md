# Functional Requirements Document (FRD) - EduCore ERP Modules

## Document Information

| Attribute | Details |
|-----------|---------|
| **Document ID** | FRD-EDU-001 |
| **Version** | 1.0 |
| **Date** | December 2024 |
| **Prepared By** | Product Management Team |
| **Approved By** | CTO, Head of Engineering |
| **Status** | Draft |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Module 1: Institution Setup & Configuration](#2-module-1-institution-setup--configuration)
3. [Module 2: Admission Management](#3-module-2-admission-management)
4. [Module 3: Student Information System](#4-module-3-student-information-system)
5. [Module 4: Fee Management](#5-module-4-fee-management)
6. [Module 5: Attendance Management](#6-module-5-attendance-management)
7. [Module 6: Examination & Assessment](#7-module-6-examination--assessment)
8. [Integration Requirements](#8-integration-requirements)
9. [Reporting Requirements](#9-reporting-requirements)
10. [Appendices](#10-appendices)

---

## 1. Introduction

### 1.1 Purpose

This Functional Requirements Document (FRD) provides detailed functional specifications for the EduCore ERP system. It serves as a guide for developers, testers, and stakeholders to understand the specific behaviors, inputs, outputs, and user interactions for each module.

### 1.2 Scope

This document covers 6 core modules for MVP (Phase 1):
- Institution Setup & Configuration
- Admission Management
- Student Information System
- Fee Management
- Attendance Management
- Examination & Assessment

### 1.3 Definitions & Acronyms

| Term | Definition |
|------|------------|
| FRD | Functional Requirements Document |
| UI | User Interface |
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| RBAC | Role-Based Access Control |
| CBCS | Choice Based Credit System |
| ATKT | Allow To Keep Terms |
| CGPA | Cumulative Grade Point Average |

---

## 2. Module 1: Institution Setup & Configuration

### 2.1 Overview

**Module ID**: INST-001  
**Priority**: P0 (Critical)  
**Description**: Enables institutions to configure their academic structure, branding, roles, and workflows without code.

### 2.2 Functional Requirements

#### FR-INST-001: White-Label Branding Configuration

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-INST-001 |
| **Feature** | Institution Branding Setup |
| **User Story** | As an admin, I want to upload my institution's logo and set brand colors so that the ERP reflects our identity |
| **Preconditions** | User is logged in as Super Admin |
| **Trigger** | Navigate to Settings → Branding |

**Functional Flow**:
1. System displays current branding settings (default theme)
2. User uploads logo (PNG/JPG/SVG, max 5MB)
3. System validates file type and size
4. System generates favicon from logo automatically
5. User selects primary color (color picker)
6. User selects secondary color (color picker)
7. User previews changes in real-time
8. User clicks "Save"
9. System applies branding across all modules
10. System clears cache and refreshes UI

**Input Fields**:
- Logo file (required)
- Favicon file (optional, auto-generated if not provided)
- Primary color hex code (required)
- Secondary color hex code (required)
- Institution name (required)
- Tagline (optional)

**Validation Rules**:
- Logo: Only PNG, JPG, SVG formats allowed
- Logo size: Maximum 5MB
- Colors: Valid hex codes only (#RRGGBB format)
- Institution name: 3-100 characters, alphanumeric + spaces

**Output**:
- Updated UI with new branding
- Confirmation message: "Branding updated successfully"
- Email notification to all admins about branding change

**Error Scenarios**:
- Invalid file format → Display error: "Only PNG, JPG, SVG files allowed"
- File too large → Display error: "File size exceeds 5MB limit"
- Invalid color code → Display error: "Please enter valid hex color code"

---

#### FR-INST-002: Academic Structure Builder

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-INST-002 |
| **Feature** | Define Classes, Streams, Subjects |
| **User Story** | As an admin, I want to define my institution's academic structure so that I can organize students and courses properly |
| **Preconditions** | Institution setup completed |
| **Trigger** | Navigate to Academics → Structure Builder |

**Functional Flow**:

**Step 1: Add Class/Standard/Semester**
1. User clicks "Add New Class"
2. System displays form:
   - Class name (e.g., "Class 10", "Semester 1", "FY B.Tech")
   - Class code (unique identifier, e.g., "C10", "S01", "FYBT")
   - Academic level (dropdown: Pre-Primary, Primary, Middle, Secondary, Higher Secondary, Undergraduate, Postgraduate, Diploma, Doctoral)
   - Duration in years (numeric)
   - Is active? (checkbox)
3. User fills form and saves
4. System validates uniqueness of class code
5. System creates class record

**Step 2: Add Streams/Branches** (for Class 11+, Undergraduate, etc.)
1. User selects a class
2. User clicks "Add Stream"
3. System displays form:
   - Stream name (e.g., "Science", "Commerce", "Computer Engineering")
   - Stream code (unique)
   - Eligibility criteria (text field, e.g., "Passed Class 10 with 60%")
   - Seats capacity (numeric)
4. User saves stream
5. System associates stream with selected class

**Step 3: Add Subjects**
1. User selects class and stream
2. User clicks "Add Subject"
3. System displays form:
   - Subject name (e.g., "Physics", "Data Structures")
   - Subject code (unique, e.g., "PHY101", "CS201")
   - Subject type (dropdown: Theory, Practical, Tutorial, Lab, Project, Seminar)
   - Credits (numeric, e.g., 3, 4)
   - LTP pattern (Lecture-Tutorial-Practical, e.g., "3-1-2")
   - Total marks (numeric, e.g., 100)
   - Theory marks (numeric)
   - Practical marks (numeric)
   - Internal assessment marks (numeric)
   - Is compulsory? (checkbox)
   - Prerequisite subjects (multi-select from subject list)
4. User saves subject
5. System validates credit and mark distribution

**Step 4: Bulk Import**
1. User clicks "Import from Excel"
2. System displays template download link
3. User downloads template, fills data, uploads file
4. System validates data
5. System shows preview with errors (if any)
6. User confirms import
7. System imports records and displays summary

**Input Validation**:
- Class code: Unique, 2-10 characters, alphanumeric
- Stream code: Unique within class, 2-10 characters
- Subject code: Unique within stream, 3-10 characters
- Credits: Positive number, max 10 per subject
- Marks: Theory + Practical + Internal = Total marks
- LTP: Format "X-Y-Z" where X,Y,Z are non-negative integers

**Output**:
- Hierarchical academic structure tree view
- Export to Excel/PDF option
- Subject catalog with codes and credits

---

#### FR-INST-003: Role & Permission Manager

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-INST-003 |
| **Feature** | Define Roles and Permissions |
| **User Story** | As an admin, I want to create custom roles with specific permissions so that users access only what they need |
| **Preconditions** | User is Super Admin |
| **Trigger** | Navigate to Settings → Roles & Permissions |

**Functional Requirements**:

**FR-INST-003.1: Pre-defined Roles**
System provides these default roles:
- Super Admin (full access, cannot be deleted)
- Institution Admin
- Academic Coordinator
- Teacher/Faculty
- Accountant
- Admission Officer
- Exam Controller
- Librarian
- Hostel Warden
- Transport In-charge
- Student
- Parent
- Guest (read-only)

**FR-INST-003.2: Custom Role Creation**
1. User clicks "Create New Role"
2. System displays form:
   - Role name (required, unique)
   - Role description (optional)
   - Base role to copy from (dropdown)
3. User fills form and proceeds to permission matrix

**FR-INST-003.3: Permission Matrix**
System displays matrix with:
- **Rows**: All system modules and sub-modules
- **Columns**: Permission types (View, Create, Edit, Delete, Export, Print, Approve)
- **Cells**: Checkboxes to grant/revoke permissions

Example:
```
| Module          | View | Create | Edit | Delete | Export | Print | Approve |
|-----------------|------|--------|------|--------|--------|-------|---------|
| Student Master  | ☑    | ☑      | ☐    | ☐      | ☑      | ☑     | ☐       |
| Fee Collection  | ☑    | ☑      | ☑    | ☐      | ☑      | ☑     | ☐       |
| Result Entry    | ☑    | ☑      | ☑    | ☐      | ☐      | ☐     | ☐       |
| Reports         | ☑    | ☐      | ☐    | ☐      | ☑      | ☑     | ☐       |
```

**FR-INST-003.4: Data Access Restrictions**
1. User defines data scope for role:
   - All institution data
   - Only assigned department/class
   - Only self-created records
2. User sets field-level restrictions:
   - Hide salary information
   - Hide contact numbers
   - Mask Aadhaar numbers
3. User saves role

**Validation**:
- Role name must be unique
- At least one permission must be granted
- Cannot delete Super Admin role
- Cannot remove all permissions from a role

**Output**:
- Role list with permission summary
- User assignment interface
- Audit log of role changes

---

#### FR-INST-004: Workflow Designer

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-INST-004 |
| **Feature** | Drag-Drop Approval Workflow Builder |
| **User Story** | As an admin, I want to design approval workflows without coding so that I can automate processes like leave approvals and fee concessions |
| **Preconditions** | User is Super Admin |
| **Trigger** | Navigate to Settings → Workflows |

**Functional Flow**:

**Step 1: Select Process Type**
1. System displays list of configurable processes:
   - Leave Approval (Student/Staff)
   - Fee Concession
   - Certificate Request
   - Purchase Requisition
   - Room Booking
   - Custom Process
2. User selects process or creates custom

**Step 2: Design Workflow**
1. System opens visual workflow designer (canvas)
2. User drags nodes from toolbar:
   - **Start Node**: Trigger event (e.g., "Leave Request Submitted")
   - **Approval Node**: Assign approver (role/person)
   - **Condition Node**: If-else branching
   - **Action Node**: Auto-actions (send email, update status)
   - **End Node**: Workflow completion
3. User connects nodes with arrows
4. User configures each node:

**Approval Node Configuration**:
- Approver type: Role / Specific person / Dynamic (based on requester's department)
- Approval type: Sequential / Parallel
- SLA: Time limit for approval (e.g., 48 hours)
- Escalation: Auto-escalate to higher authority if SLA breached
- Delegation: Allow approver to delegate to substitute

**Condition Node Configuration**:
- Condition builder (drag-drop):
  ```
  IF [Leave Days] > 5
  THEN Route to [Principal]
  ELSE Route to [HOD]
  ```
- Multiple conditions with AND/OR operators

**Step 3: Test Workflow**
1. User clicks "Test Workflow"
2. System simulates workflow with sample data
3. System displays step-by-step execution path
4. User validates and publishes

**Step 4: Publish & Monitor**
1. User clicks "Publish"
2. System activates workflow
3. System displays dashboard:
   - Active workflows count
   - Pending approvals
   - Average approval time
   - SLA compliance percentage

**Output**:
- Visual workflow diagram
- Workflow execution logs
- Pending approvals dashboard
- SLA breach alerts

---

## 3. Module 2: Admission Management

### 3.1 Overview

**Module ID**: ADM-001  
**Priority**: P0 (Critical)  
**Description**: Manage end-to-end admission process from inquiry to enrollment.

### 3.2 Functional Requirements

#### FR-ADM-001: Online Application Form Builder

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-ADM-001 |
| **Feature** | Customizable Online Admission Forms |
| **User Story** | As an admission coordinator, I want to create custom application forms for different programs so that I can collect relevant information from applicants |

**Functional Flow**:

**Step 1: Create New Form**
1. User navigates to Admissions → Form Builder
2. User clicks "Create New Form"
3. System displays form properties:
   - Form name (e.g., "B.Tech Admission 2025")
   - Program/Course (dropdown from academic structure)
   - Academic year (dropdown)
   - Application fee amount (numeric)
   - Start date and end date (date pickers)
   - Is active? (checkbox)
4. User saves form

**Step 2: Add Form Sections**
1. User clicks "Add Section"
2. System creates section container
3. User names section (e.g., "Personal Details", "Academic Qualifications", "Family Information", "Upload Documents")
4. User reorders sections via drag-drop

**Step 3: Add Form Fields**
For each section, user adds fields:

**Field Types Available**:
- Single-line text
- Multi-line text (textarea)
- Number
- Email
- Phone
- Date
- Dropdown (single select)
- Radio buttons (single select)
- Checkboxes (multi-select)
- File upload
- Signature pad
- Aadhaar number (with validation)
- Photo upload (with crop tool)

**Field Properties**:
- Field label (required)
- Field code (auto-generated, editable)
- Placeholder text
- Help text (tooltip)
- Is required? (checkbox)
- Default value
- Validation rules:
  - Min/max length
  - Min/max value (for numbers)
  - Regex pattern (custom validation)
  - Allowed file types (for uploads)
  - Max file size
- Conditional display rules:
  ```
  Show this field ONLY IF [Category] equals "OBC"
  ```

**Example Form Configuration**:
```
Section: Personal Details
├─ Applicant Name (Text, Required)
├─ Date of Birth (Date, Required, Must be >= 5 years ago)
├─ Gender (Radio: Male/Female/Other, Required)
├─ Aadhaar Number (Aadhaar field, Required, Validated)
├─ Category (Dropdown: General/OBC/SC/ST/EWS, Required)
└─ If Category != "General":
   └─ Caste Certificate Number (Text, Required)

Section: Academic Qualifications
├─ Class 10 Board (Dropdown, Required)
├─ Class 10 Year (Number, Required, Range: 2018-2024)
├─ Class 10 Percentage (Number, Required, 0-100)
├─ Class 12 Board (Dropdown, Required)
├─ Class 12 Year (Number, Required)
├─ Class 12 Percentage (Number, Required)
└─ Entrance Exam Score (Number, Optional)

Section: Upload Documents
├─ Passport Photo (File Upload, Required, JPG/PNG, Max 200KB)
├─ Signature (Signature Pad or File Upload, Required)
├─ Class 10 Marksheet (File Upload, Required, PDF, Max 2MB)
├─ Class 12 Marksheet (File Upload, Required, PDF, Max 2MB)
└─ Caste Certificate (File Upload, Conditional, PDF, Max 2MB)
```

**Step 4: Preview & Publish**
1. User clicks "Preview"
2. System displays form as applicant will see
3. User tests form submission
4. User clicks "Publish"
5. System generates public URL for form
6. System enables online payment for application fee

**Output**:
- Public application form URL
- QR code for form sharing
- Application tracking number format configuration
- Auto-confirmation email template

---

#### FR-ADM-002: Application Processing Dashboard

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-ADM-002 |
| **Feature** | Application Tracking & Processing |
| **User Story** | As an admission officer, I want to view and process applications in a dashboard so that I can efficiently manage admissions |

**Functional Flow**:

**Dashboard View**:
1. System displays kanban board or table view with columns:
   - Submitted
   - Under Scrutiny
   - Shortlisted
   - Rejected
   - Offered
   - Accepted (Admitted)
   - Waitlisted

2. Each application card shows:
   - Application number
   - Applicant name
   - Program applied
   - Submission date
   - Application fee status (Paid/Pending)
   - Entrance score (if applicable)
   - Category (General/OBC/SC/ST/EWS)

3. Filters available:
   - Program-wise
   - Category-wise
   - Date range
   - Payment status
   - Search by name/application number

**Application Detail View**:
1. User clicks on application
2. System displays:
   - All form responses
   - Uploaded documents (view/download)
   - Payment receipt
   - Communication history (emails/SMS sent)
   - Internal notes (visible only to staff)
   - Action buttons

**Processing Actions**:

**FR-ADM-002.1: Scrutiny & Verification**
1. User opens application
2. User verifies documents against uploaded copies
3. User marks verification status for each document:
   - Verified ✓
   - Mismatch ⚠
   - Missing ✗
4. User adds remarks (if mismatch/missing)
5. User submits verification
6. System updates application status

**FR-ADM-002.2: Merit List Generation**
1. User selects program and category
2. User clicks "Generate Merit List"
3. System calculates merit score based on configured criteria:
   ```
   Example Criteria:
   - Class 12 Percentage: 70% weightage
   - Entrance Exam Score: 30% weightage
   
   Merit Score = (12th_Percentage * 0.7) + (Entrance_Score * 0.3)
   ```
4. System displays ranked list with tie-breaking rules:
   - Higher marks in relevant subjects
   - Older applicant (age preference)
   - Alphabetical order (last resort)
5. User reviews and publishes merit list
6. System notifies shortlisted candidates via SMS/Email

**FR-ADM-002.3: Offer Letter Generation**
1. User selects shortlisted applicants (bulk or individual)
2. User clicks "Generate Offer Letters"
3. System populates offer letter template with:
   - Applicant name
   - Program name
   - Seat category
   - Fee structure
   - Last date to accept
   - Reporting instructions
4. System sends offer letter via email
5. System updates application status to "Offered"
6. System starts countdown for acceptance deadline

**FR-ADM-002.4: Acceptance & Admission Confirmation**
1. Applicant logs in to portal
2. Applicant views offer letter
3. Applicant clicks "Accept Offer"
4. System prompts for acceptance fee payment (if applicable)
5. Upon payment, system:
   - Generates unique student ID
   - Converts application to student record
   - Sends welcome email with login credentials
   - Updates status to "Admitted"
6. System adds student to respective class roster

**Output**:
- Daily admission summary report
- Category-wise seat availability dashboard
- Revenue collected (application fees + acceptance fees)
- Conversion funnel analytics (Applied → Shortlisted → Admitted)

---

## 4. Module 3: Student Information System

### 4.1 Overview

**Module ID**: SIS-001  
**Priority**: P0 (Critical)  
**Description**: Comprehensive student database and lifecycle management.

### 4.2 Functional Requirements

#### FR-SIS-001: Student Master Database

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-SIS-001 |
| **Feature** | Complete Student Profile Management |
| **User Story** | As an admin, I want to maintain comprehensive student profiles so that I have all student information in one place |

**Functional Flow**:

**Student Profile Tabs**:

**Tab 1: Basic Information**
- Student ID (auto-generated, read-only)
- Admission Number (editable)
- First Name (required)
- Middle Name (optional)
- Last Name (required)
- Name as per Aadhaar (required)
- Gender (dropdown: Male/Female/Other/Prefer not to say)
- Date of Birth (date picker, required)
- Place of Birth (text)
- Blood Group (dropdown)
- Religion (dropdown, optional)
- Caste/Category (dropdown: General/OBC/SC/ST/EWS/Other)
- Sub-caste (text, conditional)
- Physically Disabled? (Yes/No)
  - If Yes: Disability type, percentage, certificate upload
- Nationality (default: Indian)
- Aadhaar Number (12 digits, validated)
- PAN Number (optional, for tax purposes)

**Tab 2: Contact Information**
- Permanent Address:
  - Address line 1
  - Address line 2
  - City (required)
  - District (required)
  - State (dropdown, required)
  - PIN code (6 digits, validated)
  - Country (default: India)
- Local/Correspondence Address (checkbox: Same as permanent)
- Student Mobile Number (10 digits, validated)
- Student Email (email format, optional for school, required for college)
- Preferred language for communication (dropdown)

**Tab 3: Family/Guardian Information**
- Father Details:
  - First Name, Last Name (required)
  - Occupation (dropdown)
  - Organization/Company (text)
  - Designation (text)
  - Monthly Income (numeric, ranges: <2L, 2-5L, 5-10L, 10-20L, >20L)
  - Mobile Number (required)
  - Email (optional)
  - Aadhaar Number (optional)
- Mother Details: (same fields as father)
- Guardian Details (if parents unavailable): (same fields + relationship type)
- Siblings Information:
  - Name, Age, Studying in same institution? (Yes/No, Class if yes)
  - Alumni of this institution? (Yes/No, passing year if yes)

**Tab 4: Previous Academic Records**
- Qualification 1 (Class 10/Equivalent):
  - Board/University (dropdown)
  - School/College Name (text)
  - Year of Passing (number)
  - Roll Number (text)
  - Total Marks (number)
  - Obtained Marks (number)
  - Percentage/CGPA (auto-calculated)
  - Marksheet upload (PDF, required)
  - TC (Transfer Certificate) upload (PDF, required)
- Qualification 2 (Class 12/Graduation): (same fields)
- Entrance Exams Appeared:
  - Exam name (JEE Main, NEET, CET, etc.)
  - Roll Number
  - Score/Rank
  - Scorecard upload

**Tab 5: Current Enrollment**
- Enrolled Program/Class (dropdown from academic structure)
- Stream/Branch (dropdown, based on program)
- Section/Division (dropdown)
- Roll Number (auto/manual)
- Enrollment Date (date picker)
- Current Semester/Year (dropdown)
- Admission Type (dropdown: Freshman, Lateral Entry, Transfer, Re-admission)
- Seat Category (General/OBC/SC/ST/EWS/NRI)
- Admission Quota (Merit/Management/Sports/Alumni)
- Scholarship Availed? (Yes/No, details if yes)
- Hostel Required? (Yes/No)
- Transport Required? (Yes/No, route selection if yes)

**Tab 6: Documents Repository**
- System displays grid of required documents:
  | Document | Status | Upload Date | View | Replace |
  |----------|--------|-------------|------|---------|
  | Passport Photo | ✓ Uploaded | 15-Jun-2024 | [View] | [Replace] |
  | Aadhaar Card | ✓ Uploaded | 15-Jun-2024 | [View] | [Replace] |
  | Class 10 Marksheet | ✓ Uploaded | 15-Jun-2024 | [View] | [Replace] |
  | Class 12 Marksheet | ✓ Uploaded | 15-Jun-2024 | [View] | [Replace] |
  | Caste Certificate | ⚠ Expires Soon | 20-Jun-2024 | [View] | [Replace] |
  | Income Certificate | ✗ Missing | - | - | [Upload] |
  | Medical Fitness Cert | ✗ Missing | - | - | [Upload] |

- Document expiry tracking (for certificates with validity)
- Automated reminders for expiring documents (30 days before expiry)

**Tab 7: Timeline & Activity Log**
- Chronological feed of all student activities:
  - "15-Jun-2024: Admission confirmed"
  - "20-Jun-2024: Fee paid for Semester 1"
  - "01-Jul-2024: Attendance below 75% alert sent"
  - "15-Aug-2024: Internal test 1 marks entered"
  - "01-Sep-2024: Library book overdue fine imposed"
- Filterable by activity type
- Exportable to PDF

**Actions**:
- Edit profile (with audit trail)
- Promote to next class/semester
- Transfer to different stream/branch
- Generate TC (Transfer Certificate)
- Generate Bonafide Certificate
- Export complete profile to PDF
- Merge duplicate records (admin only)

---

## 5. Module 4: Fee Management

### 5.1 Overview

**Module ID**: FEE-001  
**Priority**: P0 (Critical)  
**Description**: Comprehensive fee collection, tracking, and financial reporting.

### 5.2 Functional Requirements

#### FR-FEE-001: Fee Structure Definition

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-FEE-001 |
| **Feature** | Flexible Fee Structure Configuration |
| **User Story** | As an accountant, I want to define fee structures for different programs so that I can accurately bill students |

**Functional Flow**:

**Step 1: Create Fee Component Master**
1. User navigates to Fees → Components
2. User clicks "Add Component"
3. System displays form:
   - Component name (Tuition Fee, Development Fee, Exam Fee, Library Fee, Sports Fee, Lab Fee, Hostel Fee, Mess Fee, Transport Fee, etc.)
   - Component code (unique, e.g., TUITION, DEV, EXAM)
   - Component type (dropdown: Recurring, One-time, Optional, Refundable Deposit)
   - Applicable GST % (dropdown: 0%, 5%, 12%, 18%, 28%)
   - Is refundable? (checkbox)
4. User saves component

**Step 2: Create Fee Structure**
1. User navigates to Fees → Fee Structures
2. User clicks "Create New Fee Structure"
3. System displays form:
   - Structure name (e.g., "B.Tech CSE 2024 Batch")
   - Program/Class (dropdown)
   - Stream/Branch (dropdown)
   - Academic Year (dropdown)
   - Applicable for (dropdown: All Students, Day Scholars Only, Hostellers Only, Transport Users Only)
   - Effective date (date picker)
4. User saves and proceeds to add components

**Step 3: Add Fee Components**
1. User clicks "Add Component"
2. System displays component selector
3. User selects component from master
4. User enters amount (numeric)
5. User sets frequency (dropdown: One-time, Monthly, Quarterly, Half-Yearly, Annual, Per Semester)
6. User sets due date rule:
   - Fixed date (e.g., 10th of every month)
   - Relative date (e.g., Within 15 days of semester start)
7. User sets late fee rule:
   - Late fee type (Fixed amount / Percentage / Per day)
   - Late fee amount (e.g., ₹500 or 2% or ₹50/day)
   - Grace period (days, e.g., 7 days)
8. User repeats for all components

**Example Fee Structure**:
```
Fee Structure: B.Tech Computer Science (2024-28 Batch)
Applicable For: All Students

| Component        | Amount    | Frequency    | Due Date        | Late Fee Rule          |
|------------------|-----------|--------------|-----------------|------------------------|
| Tuition Fee      | ₹80,000   | Per Semester | 31-Jul, 31-Dec  | ₹100/day after 7 days  |
| Development Fee  | ₹20,000   | One-time     | At Admission    | No late fee            |
| Exam Fee         | ₹5,000    | Per Semester | 30-Sep, 28-Feb  | ₹500 flat              |
| Library Fee      | ₹2,000    | Annual       | 31-Jul          | ₹20/day                |
| Sports Fee       | ₹1,000    | Annual       | 31-Jul          | No late fee            |
| Lab Fee          | ₹3,000    | Per Semester | 31-Jul, 31-Dec  | ₹500 flat              |
| Hostel Fee       | ₹40,000   | Per Semester | 31-Jul, 31-Dec  | ₹100/day               |
| Mess Fee         | ₹18,000   | Per Semester | 31-Jul, 31-Dec  | ₹50/day                |
| Caution Money    | ₹5,000    | Refundable   | At Admission    | N/A                    |
|                  |           |              |                 |                        |
| TOTAL (Day Scholar w/o Hostel)    | ₹1,11,000/semester         |
| TOTAL (Hosteller)                 | ₹1,69,000/semester         |
```

**Step 4: Installment Plans**
1. User clicks "Add Installment Plan"
2. System displays installment builder:
   - Plan name (e.g., "Quarterly Plan", "Monthly Plan")
   - Number of installments (numeric)
   - Installment breakdown:
     ```
     Installment 1: 40% due on 31-Jul
     Installment 2: 30% due on 31-Oct
     Installment 3: 30% due on 31-Jan
     ```
3. User assigns plan to fee structure
4. System allows students to choose plan during fee payment

**Step 5: Concession & Scholarship Rules**
1. User navigates to Fees → Concessions
2. User clicks "Create Concession Rule"
3. System displays rule builder:
   - Rule name (e.g., "Sports Quota Concession", "Staff Ward Discount")
   - Eligibility criteria:
     ```
     IF [Category] equals "Sports Quota"
     AND [Enrollment Year] >= 2024
     THEN Apply Concession
     ```
   - Concession type:
     - Percentage discount on tuition fee (e.g., 50%)
     - Fixed amount discount (e.g., ₹25,000)
     - Waive specific components (e.g., waive Sports Fee)
   - Approval required? (Yes/No)
   - Approver role (dropdown, if approval required)
   - Validity (academic year range)
4. User saves rule
5. System auto-applies concession to eligible students

**Output**:
- Fee structure catalog
- Student-wise fee ledger
- Due date calendar
- Expected revenue projection report

---

*(Continued in next part due to length...)*
