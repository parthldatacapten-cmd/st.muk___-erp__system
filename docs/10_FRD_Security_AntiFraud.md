# Functional Requirements Document: Security & Anti-Fraud Features

## Document Control

| Version | Date | Author | Changes | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | December 2024 | Product Team | Initial Release | CTO/CEO |

---

## 1. Executive Summary

### 1.1 Purpose

This document defines comprehensive security and anti-fraud mechanisms to address critical vulnerabilities in educational ERP systems, specifically tailored for Indian institutions where cash transactions, proxy attendance, and grade manipulation are common concerns.

### 1.2 Problem Statements Addressed

1. **"Pass the Phone" Attendance Hack**: Students logging in as friends to mark proxy attendance via QR codes
2. **Faculty "Fake GPS" Exploit**: Teachers using mock location apps to punch in from home
3. **Cash Drawer Disputes**: Receptionists collecting cash, creating receipts, then deleting records to pocket money
4. **Combined Class & Absent Teacher Chaos**: Rigid timetables failing when teachers combine batches or call in sick
5. **Grace Marks & Moderation**: Purely mathematical ATKT engines failing borderline students who deserve grace marks

### 1.3 Scope

This FRD covers:
- Device binding and OTP verification workflows
- Random selfie challenges with liveness detection
- Mock location detection for Android/iOS
- Wi-Fi IP whitelisting for staff attendance
- Immutable financial ledger architecture
- End-of-Day cash settlement reports
- Multi-batch session scheduling
- Proxy/substitute teacher management
- Three-phase result processing with grace marks
- Complete audit trail systems

---

## 2. Feature Specifications

### 2.1 Student Proxy Prevention System

#### 2.1.1 1-Device-Per-Account Rule

**User Story**: As a system administrator, I want each student account bound to a single device so that proxy attendance via device sharing is prevented.

**Functional Requirements**:

| ID | Requirement | Priority |
|----|-------------|----------|
| DEV-01 | System shall capture and store device ID (Android ID / iOS IdentifierForVendor) on first login | P0 |
| DEV-02 | System shall block login attempts from unrecognized devices without OTP verification | P0 |
| DEV-03 | System shall send 6-digit SMS OTP to registered mobile number for device change requests | P0 |
| DEV-04 | System shall allow maximum 2 device changes per semester (configurable by institution) | P0 |
| DEV-05 | System shall display device change history with timestamps and IP addresses to admins | P1 |
| DEV-06 | System shall auto-logout from old device when new device is successfully bound | P0 |

**Data Schema**:
```json
{
  "user_id": "STU2024001",
  "device_id": "android_8f3a9b2c1d4e",
  "device_type": "Android",
  "device_model": "Samsung Galaxy M31",
  "os_version": "Android 13",
  "app_version": "2.1.0",
  "registered_at": "2024-01-15T10:30:00Z",
  "last_active": "2024-01-20T14:22:00Z",
  "change_count": 1,
  "max_changes_allowed": 2,
  "otp_verified": true,
  "ip_address": "103.21.58.142",
  "change_history": [
    {
      "previous_device_id": "android_1a2b3c4d5e",
      "changed_at": "2024-01-15T10:30:00Z",
      "otp_sent_to": "+91-9876543210",
      "ip_address": "103.21.58.142"
    }
  ]
}
```

**Workflow**:
1. Student logs in on new device
2. System detects unrecognized device ID
3. System sends SMS OTP to registered mobile
4. Student enters OTP within 5 minutes
5. System validates OTP and binds new device
6. System increments change_count
7. If change_count > max_changes_allowed, blocks with error: "Maximum device changes exceeded. Contact admin."
8. System logs out from previous device
9. Audit log entry created

**Edge Cases**:
- Student loses phone: Admin can reset device binding after identity verification
- Dual-SIM phones: OTP sent to primary registered number only
- No network connectivity: Offline mode not allowed for device binding

#### 2.1.2 Random Selfie Challenge

**User Story**: As a system, I want to randomly request live selfies during QR attendance scanning so that impersonation is detected and prevented.

**Functional Requirements**:

| ID | Requirement | Priority |
|----|-------------|----------|
| SELF-01 | System shall trigger selfie prompt randomly for 10-20% of all QR attendance scans | P0 |
| SELF-02 | System shall provide 10-second countdown timer for selfie capture | P0 |
| SELF-03 | System shall use front camera only for selfie capture | P0 |
| SELF-04 | System shall perform AI-based liveness detection (blink detection, head movement) | P0 |
| SELF-05 | System shall embed timestamp, geo-coordinates, and device ID in selfie metadata | P0 |
| SELF-06 | System shall store selfie in secure cloud storage with 90-day retention | P1 |
| SELF-07 | System shall flag suspicious patterns (same face for different students) for admin review | P1 |
| SELF-08 | System shall allow admins to view selfie audit trail with filters | P1 |

**Technical Implementation**:
- Liveness Detection SDK: AWS Rekognition / Azure Face API / On-device ML model
- Storage: Encrypted S3 bucket with lifecycle policy (90 days → Glacier)
- Privacy: Selfies automatically deleted after 90 days unless flagged for investigation

**UI/UX Flow**:
1. Student scans QR code
2. System determines if selfie challenge triggered (random 15% probability)
3. If triggered: Show full-screen camera view with countdown timer
4. Student positions face in oval frame
5. System captures 3 frames over 2 seconds for liveness check
6. AI validates: Eyes blinked? Head moved slightly? Real person vs. photo?
7. Success: Attendance marked + confirmation screen
8. Failure: Error message "Liveness check failed. Try again." + manual attendance request option

**Success Metrics**:
- False Rejection Rate (FRR): < 2%
- False Acceptance Rate (FAR): < 0.1%
- Average capture time: < 5 seconds

---

### 2.2 Faculty Fake GPS Prevention

#### 2.2.1 Mock Location Detection

**User Story**: As an institution admin, I want the app to detect and block attendance marking when mock locations are enabled so that faculty cannot fake their GPS location.

**Functional Requirements**:

| ID | Requirement | Priority |
|----|-------------|----------|
| MOCK-01 | Android app shall detect if "Developer Options" is enabled | P0 |
| MOCK-02 | Android app shall detect if "Allow Mock Locations" setting is ON | P0 |
| MOCK-03 | iOS app shall detect jailbroken devices | P0 |
| MOCK-04 | App shall block attendance punch-in with clear error message if mock location detected | P0 |
| MOCK-05 | App shall provide instructions to disable mock locations | P1 |
| MOCK-06 | System shall log all mock location detection events for admin review | P1 |

**Android Implementation** (Kotlin):
```kotlin
fun isMockLocationEnabled(context: Context): Boolean {
    val locationManager = context.getSystemService(Context.LOCATION_SERVICE) as LocationManager
    
    // Check ALLOW_MOCK_LOCATION setting
    val isMockSettingOn = Settings.Secure.getInt(
        context.contentResolver,
        Settings.Secure.ALLOW_MOCK_LOCATION,
        0
    ) != 0
    
    // Check if Developer Options is enabled (API 25+)
    val isDeveloperOptionsOn = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN_MR1) {
        Settings.Global.getInt(
            context.contentResolver,
            Settings.Global.DEVELOPMENT_SETTINGS_ENABLED,
            0
        ) != 0
    } else {
        false
    }
    
    // Heuristic: Check for mock location provider
    val isMockProvider = locationManager.allProviders.contains(LocationManager.GPS_PROVIDER) &&
        locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) &&
        // Additional checks for suspicious location patterns
        isLocationSuspicious()
    
    return isMockSettingOn || isDeveloperOptionsOn || isMockProvider
}

fun isLocationSuspicious(): Boolean {
    // Check for instantaneous large distance jumps
    // Check for perfectly straight movement patterns
    // Check for static coordinates over extended periods
    // Implementation depends on historical location data analysis
}
```

**Error Messages**:
- "Mock Location Detected: Please disable 'Allow Mock Locations' in Developer Options to mark attendance."
- "Developer Mode Active: Attendance marking is disabled when Developer Options are enabled."
- "Jailbreak Detected: For security reasons, attendance cannot be marked on jailbroken devices."

#### 2.2.2 Wi-Fi IP Whitelist (Fallback)

**User Story**: As an admin, I want to restrict staff attendance to institute Wi-Fi networks only so that remote fake punch-ins are prevented even if GPS is spoofed.

**Functional Requirements**:

| ID | Requirement | Priority |
|----|-------------|----------|
| WIFI-01 | Admin shall configure allowed Wi-Fi SSIDs for each campus/institution | P0 |
| WIFI-02 | System shall validate current Wi-Fi SSID against whitelist before allowing attendance | P0 |
| WIFI-03 | System shall optionally validate IP address range (e.g., 192.168.1.x) | P1 |
| WIFI-04 | System shall support multiple Wi-Fi networks for multi-campus institutions | P0 |
| WIFI-05 | App shall show clear error if not connected to approved Wi-Fi | P0 |
| WIFI-06 | System shall use Wi-Fi validation as primary OR fallback to GPS geo-fencing | P0 |

**Configuration UI**:
```
Campus: Main Building
Allowed Wi-Fi Networks:
  1. SSID: "Mukesh_College_Staff" 
     IP Range: 192.168.10.1 - 192.168.10.254
     Subnet: 255.255.255.0
     
  2. SSID: "Mukesh_College_Guest"
     IP Range: 192.168.20.1 - 192.168.20.254
     Subnet: 255.255.255.0
     
[Add Network] [Remove] [Test Connection]
```

**Validation Logic**:
```javascript
async function validateWifiAttendance(currentSSID, currentIP, allowedNetworks) {
    const match = allowedNetworks.find(net => {
        const ssidMatch = net.ssid === currentSSID;
        const ipMatch = isIPInRange(currentIP, net.ipRangeStart, net.ipRangeEnd);
        return ssidMatch && (net.requireIP ? ipMatch : true);
    });
    
    if (!match) {
        throw new Error(`Attendance allowed only on institute Wi-Fi. Connected to: ${currentSSID}`);
    }
    
    return true;
}
```

---

### 2.3 Financial Integrity & Immutability

#### 2.3.1 Immutable Ledger Architecture

**User Story**: As a cashier, I cannot delete any financial transaction so that fraud is prevented and complete audit trails are maintained.

**Functional Requirements**:

| ID | Requirement | Priority |
|----|-------------|----------|
| IMM-01 | Database shall REVOKE DELETE privilege on financial_transactions table for ALL roles including Super Admin | P0 |
| IMM-02 | UI shall not display any "Delete" button for financial transactions | P0 |
| IMM-03 | System shall allow "Reverse" operation only with mandatory reason field (min 20 characters) | P0 |
| IMM-04 | Reversed transactions shall remain visible with "REVERSED" watermark/strikethrough | P0 |
| IMM-05 | System shall maintain original transaction amount, date, and creator information permanently | P0 |
| IMM-06 | Receipt numbers shall be sequential, auto-incrementing with no gaps allowed | P0 |
| IMM-07 | System shall prevent modification of receipt number, amount, or date after creation | P0 |
| IMM-08 | Audit log shall record: action, performed_by, timestamp, IP, reason (for reversals) | P0 |

**Database Schema**:
```sql
-- Main transactions table (immutable)
CREATE TABLE financial_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    receipt_number VARCHAR(20) UNIQUE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL, -- 'FEE_PAYMENT', 'REFUND', 'EXPENSE', etc.
    amount DECIMAL(10,2) NOT NULL,
    payment_mode VARCHAR(50) NOT NULL, -- 'CASH', 'UPI', 'CARD', 'CHEQUE'
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE', -- 'ACTIVE', 'REVERSED'
    
    -- Immutable fields
    student_id UUID REFERENCES students(id),
    fee_category_id UUID REFERENCES fee_categories(id),
    academic_year VARCHAR(9) NOT NULL,
    
    -- Audit fields (never modified)
    created_by VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_ip INET NOT NULL,
    
    -- Reversal fields (nullable until reversed)
    reversed_by VARCHAR(50),
    reversed_at TIMESTAMP WITH TIME ZONE,
    reversed_ip INET,
    reversal_reason TEXT,
    
    -- Constraint: No updates to critical fields
    CONSTRAINT immutable_fields CHECK (
        (status = 'ACTIVE' AND reversed_by IS NULL AND reversed_at IS NULL AND reversal_reason IS NULL)
        OR
        (status = 'REVERSED' AND reversed_by IS NOT NULL AND reversed_at IS NOT NULL AND reversal_reason IS NOT NULL)
    )
);

-- Append-only audit log
CREATE TABLE transaction_audit_log (
    log_id BIGSERIAL PRIMARY KEY,
    transaction_id UUID NOT NULL REFERENCES financial_transactions(id),
    action VARCHAR(20) NOT NULL CHECK (action IN ('CREATE', 'REVERSE')),
    performed_by VARCHAR(50) NOT NULL,
    performed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    performed_ip INET NOT NULL,
    details JSONB NOT NULL, -- Contains reason for reversals, old/new values if any
    user_agent TEXT,
    
    -- Constraint: Only INSERT allowed, no UPDATE/DELETE
    CONSTRAINT audit_immutable CHECK (TRUE) -- Application-level enforcement
);

-- Database-level permissions
REVOKE DELETE ON financial_transactions FROM PUBLIC;
REVOKE DELETE ON financial_transactions FROM admin_role;
REVOKE DELETE ON financial_transactions FROM super_admin;
REVOKE UPDATE ON financial_transactions FROM PUBLIC;
-- Only specific fields can be updated via stored procedure with audit

GRANT INSERT ON transaction_audit_log TO app_role;
REVOKE UPDATE, DELETE ON transaction_audit_log FROM PUBLIC;
REVOKE UPDATE, DELETE ON transaction_audit_log FROM admin_role;
```

**Reversal Workflow**:
1. User clicks "Reverse Transaction" button
2. Modal opens with mandatory fields:
   - Reason (textarea, min 20 chars, required)
   - Reversal amount (defaults to full amount, can be partial)
   - Attach supporting document (optional: scanned letter, complaint, etc.)
3. User submits reversal request
4. System validates: Reason length ≥ 20 characters
5. If amount > ₹50,000 or cumulative daily reversals > threshold, require manager approval
6. Manager receives notification, reviews, approves/rejects
7. Upon approval:
   - Original transaction status changed to 'REVERSED'
   - New reversing transaction created (negative amount)
   - Both entries linked
   - Audit log updated
8. Receipt printed with "CANCELLED" watermark

**Audit Report Fields**:
- Transaction ID
- Receipt Number
- Original Amount
- Current Status (Active/Reversed)
- Created By / Date / IP
- Reversed By / Date / IP (if applicable)
- Reversal Reason
- Time Gap (creation to reversal)

#### 2.3.2 End-of-Day (EOD) Cash Settlement

**User Story**: As a receptionist/cashier, I must generate and submit an EOD cash settlement report daily so that discrepancies between physical cash and system records are caught immediately.

**Functional Requirements**:

| ID | Requirement | Priority |
|----|-------------|----------|
| EOD-01 | System shall generate EOD report automatically at configurable time (default: 6:00 PM) | P0 |
| EOD-02 | Report shall show: Opening Balance, Total Cash Collected, Total Reversals, Expected Closing Balance | P0 |
| EOD-03 | Cashier shall enter "Actual Physical Cash Count" manually | P0 |
| EOD-04 | System shall calculate variance (Expected - Actual) and highlight if > ₹100 | P0 |
| EOD-05 | Cashier shall digitally sign report (typed name + employee ID) | P0 |
| EOD-06 | Admin/Manager shall approve report within 24 hours | P0 |
| EOD-07 | System shall lock report after approval; no modifications allowed | P0 |
| EOD-08 | Variance > ₹500 shall trigger email alert to Finance Head | P1 |

**EOD Report Format**:
```
═══════════════════════════════════════════════════════
         END-OF-DAY CASH SETTLEMENT REPORT
═══════════════════════════════════════════════════════
Date: 20-Jan-2024
Cashier: Priya Sharma (EMP001)
Counter: Main Reception

OPENING BALANCE:           ₹ 15,450.00

CASH COLLECTED TODAY:
  - Fee Payments:          ₹ 1,25,300.00
  - Form Sales:            ₹    2,500.00
  - Other Income:          ₹    1,200.00
  -------------------------
  Total Collected:         ₹ 1,29,000.00

REVERSALS/REFUNDS:
  - Receipt #INV-2024-0156 ₹   -5,000.00 (Wrong entry)
  - Receipt #INV-2024-0189 ₹   -2,500.00 (Student left)
  -------------------------
  Total Reversals:         ₹   -7,500.00

EXPECTED CLOSING BALANCE:  ₹ 1,36,950.00
(Ops: 15,450 + 129,000 - 7,500)

ACTUAL PHYSICAL COUNT:     ₹ 1,36,850.00
(Entered by Cashier)

VARIANCE:                  ₹     -100.00 ⚠️
(Minor discrepancy - within tolerance)

CASHIER DECLARATION:
"I hereby confirm that the above physical cash count is accurate 
to the best of my knowledge."

Digital Signature: Priya Sharma
Employee ID: EMP001
Timestamp: 20-Jan-2024 18:15:32

───────────────────────────────────────────────────────
MANAGER APPROVAL:
[ ] Verified and Approved
[ ] Rejected (Reason: ________________)

Approved By: ________________
Date: ________________
═══════════════════════════════════════════════════════
```

---

### 2.4 Timetable Flexibility Engine

#### 2.4.1 Multi-Batch Session Support

**User Story**: As a coordinator, I want to schedule a single lecture for multiple batches combined so that seminars, labs, or guest lectures can be managed efficiently.

**Functional Requirements**:

| ID | Requirement | Priority |
|----|-------------|----------|
| MULTI-01 | System shall allow selecting multiple batches for a single lecture session | P0 |
| MULTI-02 | System shall validate room capacity ≥ sum of all selected batch strengths | P0 |
| MULTI-03 | Attendance marked once shall apply to all linked batches | P0 |
| MULTI-04 | Each batch's syllabus tracker shall update independently based on their curriculum mapping | P0 |
| MULTI-05 | Teachers shall see combined student list with batch identifiers | P1 |
| MULTI-06 | Reports shall allow filtering by individual batch or combined view | P1 |

**Data Model**:
```json
{
  "session_id": "LEC-2024-0156",
  "subject_id": "CS301",
  "teacher_id": "FAC042",
  "batch_ids": ["CS-A-2024", "CS-B-2024"],
  "room_id": "SEMINAR-HALL-1",
  "scheduled_time": "2024-01-22T10:00:00Z",
  "duration_minutes": 90,
  "session_type": "COMBINED_LECTURE",
  "total_students": 120,
  "room_capacity": 150,
  "attendance_status": "MARKED",
  "syllabus_topics_covered": ["Introduction to Machine Learning", "Supervised vs Unsupervised"]
}
```

#### 2.4.2 Proxy/Substitute Teacher Module

**User Story**: As an admin, I want to quickly assign a substitute teacher for absent faculty so that classes continue without disruption and attendance can be marked properly.

**Functional Requirements**:

| ID | Requirement | Priority |
|----|-------------|----------|
| SUB-01 | Admin shall select absent teacher and date/time slots for substitution | P0 |
| SUB-02 | System shall suggest available teachers based on free slots in their timetable | P0 |
| SUB-03 | Admin shall assign substitute teacher with one click | P0 |
| SUB-04 | Substitute teacher shall receive push notification + SMS with class details | P0 |
| SUB-05 | Substitute shall have temporary permission to mark attendance for assigned batches | P0 |
| SUB-06 | Permission shall be valid only for specified date/time slots | P0 |
| SUB-07 | Original teacher's dashboard shall show "Covered by [Substitute Name]" | P1 |
| SUB-08 | Attendance reports shall indicate "Marked by Substitute" flag | P1 |
| SUB-09 | Recurring substitutions shall be supported (e.g., "Every Monday for 4 weeks") | P1 |

**Substitution Request Form**:
```
┌─────────────────────────────────────────────────────┐
│              SUBSTITUTE TEACHER ASSIGNMENT          │
├─────────────────────────────────────────────────────┤
│ Absent Teacher: Mr. Rajesh Sharma (FAC023)          │
│ Date: 22-Jan-2024                                   │
│                                                     │
│ Classes to Cover:                                   │
│ ☐ 10:00-11:00 | CS-A | Room 301 | Data Structures  │
│ ☐ 11:00-12:00 | CS-B | Room 302 | Algorithms       │
│ ☐ 14:00-15:00 | CS-C | Lab-2  | DBMS Lab           │
│                                                     │
│ Suggested Substitutes (based on availability):      │
│ 1. Ms. Anita Desai (FAC015) - Free all slots ⭐    │
│ 2. Mr. Vikram Patel (FAC031) - Free 10-12 only     │
│ 3. Mrs. Sunita Rao (FAC008) - Free 14-15 only      │
│                                                     │
│ Select Substitute: [Ms. Anita Desai ▼]             │
│                                                     │
│ Duration:                                           │
│ ○ One-time (22-Jan-2024 only)                      │
│ ○ Recurring: Every [Monday] for [4] weeks          │
│                                                     │
│ Message to Substitute (optional):                   │
│ [Please cover DS lecture for CS-A. Syllabus: Trees]│
│                                                     │
│ [Assign Substitute]  [Cancel]                       │
└─────────────────────────────────────────────────────┘
```

---

### 2.5 Grace Marks & Moderation Workflow

#### 2.5.1 Three-Phase Result Processing

**User Story**: As a principal, I want to review draft results and add grace marks to borderline students before publishing final results so that deserving students are not failed due to narrow margins.

**Functional Requirements**:

| ID | Requirement | Priority |
|----|-------------|----------|
| GRACE-01 | System shall implement three distinct phases: Raw → Draft/Moderation → Published | P0 |
| GRACE-02 | Phase 1 (Raw): Auto-calculate marks from OMR/answer keys + manual grading by teachers | P0 |
| GRACE-03 | Phase 2 (Draft): Results hidden from students; accessible only to Principal/HOD | P0 |
| GRACE-04 | Principal/HOD shall add grace marks (+1 to +5 per subject, configurable cap) | P0 |
| GRACE-05 | Bulk moderation rules shall be supported (e.g., "Pass all students with 32-34 marks") | P0 |
| GRACE-06 | Every grace mark addition shall require mandatory justification (min 10 chars) | P0 |
| GRACE-07 | Phase 3 (Published): Final results locked, visible to students/parents | P0 |
| GRACE-08 | Moderation audit report shall show original marks, grace added, final marks, approver | P0 |
| GRACE-09 | Institution shall configure: max grace marks, eligible subjects, attendance criteria | P1 |

**Phase Transition Rules**:
```
PHASE 1 (RAW RESULTS)
  ↓ [Principal clicks "Move to Moderation"]
PHASE 2 (DRAFT/MODERATION)
  - Students cannot view results
  - Teachers cannot modify marks
  - Only Principal/HOD can add grace marks
  - Audit trail active
  ↓ [Principal clicks "Publish Results"]
  - Confirmation modal: "Results will be published and cannot be changed. Continue?"
  - Requires digital signature (Principal password)
PHASE 3 (PUBLISHED)
  - Results visible to students/parents
  - All mark fields locked (read-only)
  - Re-evaluation workflow separate process
```

**Grace Marks Interface**:
```
┌─────────────────────────────────────────────────────────────────┐
│                    MODERATION DASHBOARD                         │
│ Exam: Semester III - Dec 2023 | Batch: CS-A                     │
├─────────────────────────────────────────────────────────────────┤
│ Students Eligible for Grace Marks: 23                           │
│ (Scored between 30-34 in any subject, Attendance > 75%)         │
│                                                                 │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Student: Rohit Kumar (STU2021-CS-045)                       │ │
│ │ Attendance: 82% ✓                                           │ │
│ │                                                             │ │
│ │ Subject: Data Structures (CS301)                            │ │
│ │ Original Marks: 33/70 (Failed, Pass Mark: 35)               │ │
│ │ Grace Marks Allowed: +1 to +5                               │ │
│ │                                                             │ │
│ │ Add Grace Marks: [+2 ▼]                                     │ │
│ │ New Total: 35/70 (PASS) ✓                                   │ │
│ │                                                             │ │
│ │ Justification (Required):                                   │ │
│ │ [Borderline case. Good internal assessment performance.]    │ │
│ │                                                             │ │
│ │ [Apply Grace] [Skip]                                        │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│ BULK ACTION:                                                    │
│ [Apply +2 grace to all students with 33 marks]                 │
│ [Apply +1 grace to all students with 34 marks]                 │
│                                                                 │
│ Progress: 15/23 reviewed | 8 pending                           │
│                                                                 │
│ [Save & Continue] [Move to Publish Phase]                      │
└─────────────────────────────────────────────────────────────────┘
```

**Moderation Audit Report**:
```
═══════════════════════════════════════════════════════════
              MODERATION AUDIT REPORT
═══════════════════════════════════════════════════════════
Exam: Semester III - Dec 2023
Batch: CS-A
Generated: 15-Jan-2024 14:30:00

Stu_ID    Name           Subject      Orig  Grace  Final  Approved_By
─────────────────────────────────────────────────────────────────────
STU045    Rohit Kumar    CS301        33    +2     35     Dr. Patil
STU067    Sneha Reddy    CS302        34    +1     35     Dr. Patil
STU089    Amit Shah      CS304        32    +3     35     Dr. Patil
STU102    Pooja Singh    CS301        33    +2     35     Dr. Patil
...

Summary:
- Total Students Moderated: 23
- Total Grace Marks Awarded: 48
- Subjects Most Moderated: CS301 (Data Structures) - 12 students
- Average Grace per Student: +2.1

Approved By: Dr. Suresh Patil (Principal)
Digital Signature: [Verified]
Timestamp: 15-Jan-2024 14:28:45
═══════════════════════════════════════════════════════════
```

---

## 3. Technical Implementation Guidelines

### 3.1 Device Binding Service

```python
class DeviceBindingService:
    def __init__(self):
        self.max_changes_per_semester = 2
    
    def bind_device(self, user_id: str, device_id: str, otp: str) -> bool:
        # Verify OTP
        if not self.verify_otp(user_id, otp):
            raise OTPVerificationError("Invalid OTP")
        
        # Check change count
        change_count = self.get_change_count(user_id)
        if change_count >= self.max_changes_per_semester:
            raise MaxChangesExceededError("Maximum device changes exceeded")
        
        # Bind new device
        old_device = self.get_current_device(user_id)
        self.update_device_binding(user_id, device_id)
        self.increment_change_count(user_id)
        self.logout_other_sessions(user_id, exclude_device=device_id)
        self.log_audit_event(user_id, 'DEVICE_CHANGE', old_device, device_id)
        
        return True
```

### 3.2 Immutable Transaction Service

```python
class FinancialTransactionService:
    def create_transaction(self, data: dict) -> Transaction:
        # Generate sequential receipt number
        receipt_no = self.generate_sequential_receipt_number()
        
        # Create transaction (INSERT only)
        transaction = Transaction(
            receipt_number=receipt_no,
            **data,
            status='ACTIVE'
        )
        db.session.add(transaction)
        db.session.commit()
        
        # Create audit log
        self.create_audit_log(
            transaction_id=transaction.id,
            action='CREATE',
            details=data
        )
        
        return transaction
    
    def reverse_transaction(self, transaction_id: str, reason: str, user: str) -> Transaction:
        if len(reason) < 20:
            raise ValidationError("Reversal reason must be at least 20 characters")
        
        transaction = Transaction.query.get(transaction_id)
        if transaction.status == 'REVERSED':
            raise AlreadyReversedError("Transaction already reversed")
        
        # Update transaction (status change only)
        transaction.status = 'REVERSED'
        transaction.reversed_by = user
        transaction.reversed_at = datetime.utcnow()
        transaction.reversal_reason = reason
        
        # Create reversing transaction (negative amount)
        reverse_txn = Transaction(
            receipt_number=self.generate_sequential_receipt_number(),
            amount=-transaction.amount,
            status='ACTIVE',
            related_transaction_id=transaction.id,
            created_by=user,
            reversal_reference=transaction.receipt_number
        )
        db.session.add(reverse_txn)
        
        # Audit log
        self.create_audit_log(
            transaction_id=transaction.id,
            action='REVERSE',
            performed_by=user,
            details={'reason': reason, 'reverse_txn_id': reverse_txn.id}
        )
        
        db.session.commit()
        return transaction
```

---

## 4. User Stories Summary

| ID | User Story | Acceptance Criteria | Story Points |
|----|------------|---------------------|--------------|
| SEC-01 | As a student, I must verify my device via OTP when changing phones | OTP sent, device bound, change count incremented | 5 |
| SEC-02 | As a system, I must randomly request a selfie during QR attendance | 10-20% trigger rate, liveness check passed | 8 |
| SEC-03 | As a teacher, I cannot mark attendance if Mock Locations are enabled | App detects mock location, shows error, blocks action | 5 |
| SEC-04 | As an admin, I want staff attendance only on institute Wi-Fi | SSID whitelist, IP validation, fallback to GPS | 5 |
| SEC-05 | As a cashier, I cannot delete any financial transaction | Delete button disabled, DB REVOKE DELETE, only Reverse option | 8 |
| SEC-06 | As a principal, I want to add grace marks in draft stage | Draft phase exists, grace interface, audit trail | 8 |
| SEC-07 | As a coordinator, I want to assign substitute teachers | One-click substitution, temporary permissions, notifications | 5 |
| SEC-08 | As a receptionist, I must generate EOD cash settlement report | Opening/closing balance, digital signature, discrepancy alerts | 5 |
| SEC-09 | As an admin, I want multi-batch scheduling for combined classes | Multiple batches per session, room capacity check, unified attendance | 5 |
| SEC-10 | As a student, I want my attendance selfie to be private and auto-deleted | 90-day retention, encrypted storage, auto-deletion | 3 |

**Total Story Points**: 57

---

## 5. Risk Mitigation Matrix

| Risk | Likelihood | Impact | Mitigation Strategy | Owner |
|------|------------|--------|---------------------|-------|
| Student proxy via device sharing | High | High | 1-Device rule + Selfie challenge + OTP | Product Manager |
| Teacher fake GPS attendance | Medium | High | Mock location detection + Wi-Fi IP whitelist | Tech Lead |
| Cash theft by deletion | Medium | Critical | Immutable ledger + EOD reports + Audit trail | Finance Head |
| Timetable conflicts during substitutions | High | Medium | Multi-batch support + Proxy module | Academic Coordinator |
| Unfair failures without grace marks | High | High | Moderation phase + Grace marks workflow | Principal |
| Privacy concerns with selfies | Medium | Medium | Auto-deletion, encryption, limited access | Compliance Officer |
| OTP delivery failures | Low | High | Fallback to email, manual override by admin | Tech Lead |
| Wi-Fi network downtime | Low | Medium | Fallback to GPS geo-fencing with strict radius | Tech Lead |

---

## 6. Testing Strategy

### 6.1 Test Scenarios

**Device Binding**:
- TC-DEV-01: First-time login binds device successfully
- TC-DEV-02: Login from new device triggers OTP
- TC-DEV-03: Incorrect OTP rejected
- TC-DEV-04: Third device change blocked (max 2 reached)
- TC-DEV-05: Old device logged out after new binding

**Selfie Challenge**:
- TC-SELF-01: Selfie triggered for ~15% of scans
- TC-SELF-02: Liveness detection passes for real person
- TC-SELF-03: Photo-of-photo attack rejected
- TC-SELF-04: Timeout after 10 seconds
- TC-SELF-05: Selfie stored with correct metadata

**Mock Location**:
- TC-MOCK-01: Attendance blocked when mock location enabled
- TC-MOCK-02: Error message displayed clearly
- TC-MOCK-03: Attendance works after disabling mock location

**Immutable Ledger**:
- TC-IMM-01: Delete button not visible in UI
- TC-IMM-02: Direct DB DELETE query fails (permission denied)
- TC-IMM-03: Reversal creates negative transaction
- TC-IMM-04: Audit log contains all required fields
- TC-IMM-05: Receipt numbers sequential with no gaps

**Grace Marks**:
- TC-GRACE-01: Draft phase hides results from students
- TC-GRACE-02: Grace marks applied within limits
- TC-GRACE-03: Bulk moderation applies to all eligible students
- TC-GRACE-04: Published results locked and read-only
- TC-GRACE-05: Audit report shows all changes

---

## 7. Deployment Checklist

- [ ] Device binding service deployed and tested
- [ ] SMS gateway integrated for OTP delivery
- [ ] Selfie liveness detection SDK integrated
- [ ] Mock location detection implemented for Android/iOS
- [ ] Wi-Fi SSID configuration UI built
- [ ] Database permissions set (REVOKE DELETE on transactions)
- [ ] EOD report template configured
- [ ] Multi-batch scheduling logic tested
- [ ] Substitute teacher notification system active
- [ ] Grace marks workflow implemented with three phases
- [ ] Audit log tables created and append-only enforced
- [ ] All user stories tested and accepted
- [ ] Penetration testing completed
- [ ] Privacy policy updated for selfie data handling

---

## 8. Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Proxy attendance reduction | > 90% | Compare pre/post implementation attendance anomalies |
| Fake GPS attempts blocked | 100% | Log analysis of mock location detection events |
| Cash discrepancies | < 0.1% of transactions | EOD report variance analysis |
| Grace marks processing time | < 2 hours per batch | Time tracking from raw to published |
| Audit compliance | 100% | Random audit sample checks |
| User satisfaction | > 4.5/5 | Post-implementation survey |

---

## Appendix A: Regulatory Compliance

- **DPDP Act 2023**: Selfie data classified as personal data; requires consent, limited retention, encryption
- **AICTE Guidelines**: ATKT and grace marks policies must align with university regulations
- **ISO 27001**: Financial immutability meets information security controls
- **GDPR**: Right to erasure does not apply to financial records (legal obligation exception)

## Appendix B: Glossary

- **ATKT**: Allowed To Keep Terms (conditional promotion despite failures)
- **EOD**: End of Day
- **FRR/FAR**: False Rejection/Acceptance Rate (biometric metrics)
- **OTP**: One-Time Password
- **RBAC**: Role-Based Access Control
