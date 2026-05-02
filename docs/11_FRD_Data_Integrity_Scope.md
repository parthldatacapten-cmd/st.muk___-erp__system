# 11_FRD_Data_Integrity_Scope.md

## Functional Requirements Document: Data Integrity & Scope Management

**Version:** 1.0  
**Date:** 2024-01-15  
**Status:** Approved  
**Author:** Product Management Team  
**Priority:** CRITICAL  

---

## 1. Executive Summary

This document addresses critical data integrity challenges in student lifecycle management and examination systems, while strictly defining product scope boundaries to prevent feature creep. These requirements are essential for maintaining NAAC compliance, financial accuracy, and development focus.

### Key Objectives:
1. **Student Transfer Workflow**: Safe migration between streams/batches without data loss
2. **Exam Recalculation Engine**: Dynamic re-scoring when questions are modified/removed
3. **Scope Boundaries**: Clear definition of what the system will NOT support

---

## 2. Student Transfer Workflow ("Stream Switcher")

### 2.1 Problem Statement

When a student transfers mid-year (e.g., 11th Science → 11th Commerce):
- ❌ **Current Risk**: Changing `batch_id` overwrites historical data
- ❌ **Attendance Loss**: Past Science attendance disappears from NAAC reports
- ❌ **Fee Imbalance**: Ledger shows incorrect totals after stream change
- ❌ **Academic Record Corruption**: Old marksheets become inaccessible

### 2.2 Solution Architecture

#### 2.2.1 Transfer Workflow States

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   ACTIVE        │────▶│  TRANSITION      │────▶│   ACTIVE        │
│   (Science)     │     │  (Pending)       │     │   (Commerce)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
       │                        │                        │
       ▼                        ▼                        ▼
  Data Frozen            Validation              New Batch Active
  Archived               Checks                  Credit Note Generated
```

#### 2.2.2 Database Schema Changes

```sql
-- Student Batch History Table (Immutable)
CREATE TABLE student_batch_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id),
    batch_id UUID NOT NULL REFERENCES batches(id),
    stream_code VARCHAR(20) NOT NULL, -- 'SCIENCE', 'COMMERCE', 'ARTS'
    enrollment_date DATE NOT NULL,
    exit_date DATE, -- NULL if current
    exit_reason VARCHAR(100), -- 'TRANSFER', 'DROPOUT', 'COMPLETED'
    transfer_to_batch_id UUID REFERENCES batches(id),
    archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent updates after exit_date is set
    CONSTRAINT chk_exit_date CHECK (exit_date IS NULL OR exit_date >= enrollment_date)
);

-- Create index for fast historical queries
CREATE INDEX idx_student_batch_history_student ON student_batch_history(student_id);
CREATE INDEX idx_student_batch_history_batch ON student_batch_history(batch_id);

-- Financial Transaction with Transfer Reference
ALTER TABLE fee_transactions ADD COLUMN transfer_reference_id UUID;
ALTER TABLE fee_transactions ADD COLUMN is_credit_note BOOLEAN DEFAULT FALSE;
```

#### 2.2.3 Transfer Process Steps

**Step 1: Initiate Transfer Request**
- Admin selects student → "Transfer to Another Stream"
- System displays:
  - Current batch details
  - Attendance summary (cannot be changed)
  - Fee ledger balance
  - Pending dues
  - Academic records (marks, grades)

**Step 2: Validation Checks**
```python
def validate_transfer_request(student_id, new_batch_id):
    errors = []
    
    # Check pending fees
    pending_fees = get_pending_fees(student_id)
    if pending_fees > 0:
        errors.append(f"Cannot transfer with ₹{pending_fees} pending fees")
    
    # Check ongoing exams
    ongoing_exams = get_ongoing_exams_for_student(student_id)
    if ongoing_exams:
        errors.append(f"Cannot transfer during active exams: {ongoing_exams}")
    
    # Check attendance minimum (if required by policy)
    attendance_pct = calculate_attendance_percentage(student_id)
    if attendance_pct < 75:
        warnings.append(f"Attendance below 75%: {attendance_pct}%")
    
    return errors, warnings
```

**Step 3: Calculate Fee Adjustment**
```python
def calculate_fee_adjustment(student_id, old_batch, new_batch):
    # Get paid fees for current academic year
    paid_fees = get_paid_fees(student_id, academic_year)
    
    # Calculate pro-rata fees for old batch (days enrolled / total days)
    days_in_old_batch = (transfer_date - old_batch.start_date).days
    total_days_in_year = (old_batch.end_date - old_batch.start_date).days
    pro_rata_old = (days_in_old_batch / total_days_in_year) * old_batch.total_fee
    
    # Calculate pro-rata fees for new batch
    days_in_new_batch = (new_batch.end_date - transfer_date).days
    pro_rata_new = (days_in_new_batch / total_days_in_year) * new_batch.total_fee
    
    # Calculate difference
    if pro_rata_old > pro_rata_new:
        # Institute owes student - Generate Credit Note
        credit_amount = pro_rata_old - pro_rata_new
        return {
            'type': 'CREDIT_NOTE',
            'amount': credit_amount,
            'description': f"Stream transfer: {old_batch.name} → {new_batch.name}"
        }
    else:
        # Student owes institute - Generate Additional Invoice
        due_amount = pro_rata_new - pro_rata_old
        return {
            'type': 'ADDITIONAL_INVOICE',
            'amount': due_amount,
            'description': f"Stream transfer: {old_batch.name} → {new_batch.name}"
        }
```

**Step 4: Execute Transfer (Atomic Transaction)**
```python
@transaction.atomic
def execute_student_transfer(student_id, new_batch_id, reason):
    # 1. Archive current batch record
    current_record = StudentBatchHistory.objects.filter(
        student_id=student_id, 
        exit_date__isnull=True
    ).first()
    
    current_record.exit_date = timezone.now().date()
    current_record.exit_reason = 'TRANSFER'
    current_record.transfer_to_batch_id = new_batch_id
    current_record.archived = True
    current_record.save()
    
    # 2. Create new batch record
    new_record = StudentBatchHistory.objects.create(
        student_id=student_id,
        batch_id=new_batch_id,
        stream_code=get_batch_stream(new_batch_id),
        enrollment_date=timezone.now().date()
    )
    
    # 3. Update student's current batch reference
    student.current_batch_id = new_batch_id
    student.save()
    
    # 4. Generate financial adjustment
    adjustment = calculate_fee_adjustment(student_id, current_record.batch_id, new_batch_id)
    
    if adjustment['type'] == 'CREDIT_NOTE':
        create_credit_note(
            student_id=student_id,
            amount=adjustment['amount'],
            description=adjustment['description'],
            transfer_reference_id=current_record.id
        )
    else:
        create_invoice(
            student_id=student_id,
            amount=adjustment['amount'],
            description=adjustment['description'],
            transfer_reference_id=current_record.id
        )
    
    # 5. Log audit trail
    AuditLog.objects.create(
        action='STUDENT_TRANSFER',
        user_id=current_user.id,
        details={
            'student_id': student_id,
            'from_batch': current_record.batch_id,
            'to_batch': new_batch_id,
            'financial_adjustment': adjustment
        }
    )
    
    return new_record
```

**Step 5: Post-Transfer Actions**
- ✅ Historical attendance remains accessible in NAAC reports under old batch
- ✅ Fee ledger shows credit note/invoice with clear transfer reference
- ✅ Academic records (marks, grades) remain linked to student (not batch)
- ✅ New timetable assignments begin immediately
- ✅ Automatic notifications to student, parents, and new batch teacher

#### 2.2.4 UI Mockup: Transfer Wizard

```
┌─────────────────────────────────────────────────────────────────┐
│  STUDENT TRANSFER WIZARD                                    ✕   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Student: Rajesh Kumar (ID: STU2024001)                         │
│  Current: 11th Science - Division A                             │
│                                                                 │
│  ────────────────────────────────────────────────────────────   │
│                                                                 │
│  STEP 1: Select New Stream                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Target Batch: [11th Commerce - Division B ▼]            │   │
│  │ Transfer Date: [2024-09-15 📅]                          │   │
│  │ Reason: [Student requested stream change ▼]             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ────────────────────────────────────────────────────────────   │
│                                                                 │
│  STEP 2: Review Impact                                          │
│                                                                 │
│  📊 Attendance Summary (Science):                               │
│     Present: 142 days | Absent: 8 days | Total: 94.7%          │
│     ⚠️ This data will be ARCHIVED and remain in NAAC reports   │
│                                                                 │
│  💰 Fee Ledger:                                                 │
│     Paid: ₹45,000 | Pending: ₹0                                │
│     Science Fee (pro-rata): ₹38,500                            │
│     Commerce Fee (pro-rata): ₹42,000                           │
│     ➕ Additional Payment Required: ₹3,500                     │
│                                                                 │
│  📚 Academic Records:                                           │
│     ✓ All marks and grades will be preserved                   │
│     ✓ Accessible from student profile permanently              │
│                                                                 │
│  ────────────────────────────────────────────────────────────   │
│                                                                 │
│  ☑ I understand that historical data will be archived           │
│  ☑ I approve the financial adjustment of ₹3,500                 │
│                                                                 │
│  [CANCEL]                              [REVIEW & CONFIRM ▶]     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.2.5 Reporting Impact

**NAAC Compliance Reports:**
- Historical attendance included in "Student Progression" metrics
- Transfer students counted in both batches for enrollment statistics
- Credit notes tracked in "Financial Management" criteria

**Financial Reports:**
- Credit notes appear in "Revenue Adjustments" report
- Transfer-related transactions tagged for easy filtering
- End-of-year reconciliation includes transfer adjustments

---

## 3. Exam Recalculation Engine ("Bonus Marks Crisis")

### 3.1 Problem Statement

When teachers upload exams with errors:
- ❌ **Scenario**: Question #5 has wrong answer key or is ambiguous
- ❌ **Impact**: 500 students scored incorrectly
- ❌ **Manual Fix Nightmare**: Re-calculating ranks manually takes days
- ❌ **Risk**: Human error in manual recalculation causes disputes

### 3.2 Solution: Automated Recalculation Trigger

#### 3.2.1 Database Design for Recalculation

```sql
-- Question Bank with Version Control
CREATE TABLE exam_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_id UUID NOT NULL REFERENCES exams(id),
    question_number INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(20) NOT NULL, -- 'MCQ', 'NUMERICAL', 'SUBJECTIVE'
    correct_answer JSONB, -- Flexible format for different types
    marks_allocated DECIMAL(5,2) NOT NULL,
    negative_marks DECIMAL(5,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'ACTIVE', -- 'ACTIVE', 'CHALLENGED', 'DELETED', 'BONUS'
    challenged_by_count INTEGER DEFAULT 0,
    reviewed_by UUID REFERENCES faculty(id),
    review_notes TEXT,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Student Responses (Immutable - Append Only)
CREATE TABLE student_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    exam_id UUID NOT NULL REFERENCES exams(id),
    student_id UUID NOT NULL REFERENCES students(id),
    question_id UUID NOT NULL REFERENCES exam_questions(id),
    selected_answer JSONB, -- Student's response
    is_correct BOOLEAN, -- Calculated at time of submission
    marks_awarded DECIMAL(5,2), -- Calculated at time of submission
    response_time_seconds INTEGER,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Cannot update, only insert new version if needed
    CONSTRAINT unique_student_question UNIQUE(student_id, question_id, exam_id)
);

-- Exam Results Cache (Materialized View for Performance)
CREATE MATERIALIZED VIEW exam_results_cache AS
SELECT 
    exam_id,
    student_id,
    COUNT(*) as total_questions,
    SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct_count,
    SUM(marks_awarded) as total_marks,
    RANK() OVER (PARTITION BY exam_id ORDER BY SUM(marks_awarded) DESC) as all_india_rank
FROM student_responses
GROUP BY exam_id, student_id;

-- Index for fast recalculations
CREATE INDEX idx_responses_exam ON student_responses(exam_id);
CREATE INDEX idx_responses_question ON student_responses(question_id);
```

#### 3.2.2 Recalculation Trigger Logic

```python
class ExamRecalculationEngine:
    """
    Automatically recalculates all student scores when question parameters change.
    """
    
    @transaction.atomic
    def update_question(self, question_id, updates, admin_user):
        """
        Update a question and trigger mass recalculation.
        
        Args:
            question_id: UUID of the question
            updates: Dict with fields to update (correct_answer, marks_allocated, status)
            admin_user: User making the change
        """
        old_question = ExamQuestion.objects.select_for_update().get(id=question_id)
        
        # Validate changes
        if 'status' in updates and updates['status'] == 'DELETED':
            # Question being removed - marks will be redistributed
            pass
        
        # Update question
        for key, value in updates.items():
            setattr(old_question, key, value)
        old_question.version += 1
        old_question.save()
        
        # Log the change
        AuditLog.objects.create(
            action='QUESTION_MODIFIED',
            user_id=admin_user.id,
            exam_id=old_question.exam_id,
            details={
                'question_id': question_id,
                'old_values': serialize_question(old_question),
                'new_values': updates
            }
        )
        
        # Trigger recalculation
        self.recalculate_exam_scores(old_question.exam_id, question_id)
        
        return old_question
    
    def recalculate_exam_scores(self, exam_id, modified_question_id=None):
        """
        Recalculate scores for all students in an exam.
        
        Args:
            exam_id: UUID of the exam
            modified_question_id: Optional - if None, recalculate all questions
        """
        exam = Exam.objects.get(id=exam_id)
        
        # Get all questions for this exam
        questions = ExamQuestion.objects.filter(exam_id=exam_id, status__in=['ACTIVE', 'BONUS'])
        
        # Build marking scheme
        marking_scheme = {}
        for q in questions:
            marking_scheme[q.id] = {
                'correct_answer': q.correct_answer,
                'marks': q.marks_allocated if q.status == 'ACTIVE' else 0,
                'negative_marks': q.negative_marks if q.status == 'ACTIVE' else 0,
                'is_bonus': q.status == 'BONUS'
            }
        
        # Get all student responses for this exam
        responses = StudentResponse.objects.filter(exam_id=exam_id).select_related('student')
        
        # Group by student
        student_responses = defaultdict(list)
        for response in responses:
            student_responses[response.student_id].append(response)
        
        # Recalculate for each student
        results_to_update = []
        for student_id, resp_list in student_responses.items():
            total_marks = 0
            correct_count = 0
            
            for resp in resp_list:
                q_scheme = marking_scheme.get(resp.question_id)
                if not q_scheme:
                    continue
                
                # Check if answer is correct
                is_correct = self.evaluate_answer(resp.selected_answer, q_scheme['correct_answer'])
                
                # Calculate marks
                if q_scheme['is_bonus']:
                    # Bonus question - everyone gets full marks
                    marks_awarded = q_scheme['marks']
                    is_correct = True
                elif is_correct:
                    marks_awarded = q_scheme['marks']
                    correct_count += 1
                else:
                    marks_awarded = -q_scheme['negative_marks']
                
                total_marks += marks_awarded
                
                # Update response record (append new calculation)
                resp.marks_awarded = marks_awarded
                resp.is_correct = is_correct
                results_to_update.append(resp)
            
            # Store new total for ranking
            student_results[student_id] = total_marks
        
        # Bulk update all responses
        StudentResponse.objects.bulk_update(results_to_update, ['marks_awarded', 'is_correct'])
        
        # Recalculate rankings
        self.recalculate_rankings(exam_id, student_results)
        
        # Refresh materialized view
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY exam_results_cache")
        
        # Notify stakeholders
        self.notify_recalculation_complete(exam_id, len(student_results))
    
    def recalculate_rankings(self, exam_id, student_results):
        """
        Recalculate All-India Ranks based on new scores.
        """
        # Sort students by marks (descending)
        sorted_students = sorted(
            student_results.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Assign ranks (handling ties)
        current_rank = 1
        previous_marks = None
        rank_data = []
        
        for idx, (student_id, marks) in enumerate(sorted_students):
            if marks != previous_marks:
                current_rank = idx + 1
            
            rank_data.append({
                'exam_id': exam_id,
                'student_id': student_id,
                'rank': current_rank,
                'percentile': self.calculate_percentile(idx, len(sorted_students))
            })
            
            previous_marks = marks
        
        # Bulk update ranks
        ExamResult.objects.bulk_update_or_create(rank_data)
    
    def evaluate_answer(self, student_answer, correct_answer):
        """
        Evaluate if student answer matches correct answer.
        Supports MCQ, Numerical, and Multi-correct formats.
        """
        # Implementation depends on question type
        # Returns True/False
        pass
```

#### 3.2.3 UI Workflow: Question Challenge & Recalculation

```
┌─────────────────────────────────────────────────────────────────┐
│  EXAM QUESTION MANAGEMENT                                    ✕   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Exam: JEE Mock Test #5 (500 Students)                          │
│  Status: COMPLETED | Results: PUBLISHED                         │
│                                                                 │
│  ────────────────────────────────────────────────────────────   │
│                                                                 │
│  Question #5: [Chemistry - Organic Reactions]                   │
│  Marks: +4 | Negative: -1                                       │
│                                                                 │
│  ⚠️ 47 students have challenged this question                   │
│                                                                 │
│  Current Status: [ACTIVE ▼]                                     │
│                                                                 │
│  Actions:                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ ○ Keep as is (No changes)                               │   │
│  │ ○ Mark as BONUS (All students get +4)                   │   │
│  │ ○ Update Correct Answer                                 │   │
│  │    Current: [A]  New: [B ▼]                             │   │
│  │ ○ Delete Question (Remove from scoring)                 │   │
│  │    → Marks will be redistributed                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Impact Preview:                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ If marked as BONUS:                                     │   │
│  │ • 500 students will receive +4 marks                    │   │
│  │ • Top rank score: 184 → 188                             │   │
│  │ • Estimated recalculation time: ~3 seconds              │   │
│  │                                                         │   │
│  │ If deleted:                                             │   │
│  │ • Total marks: 200 → 196                                │   │
│  │ • All scores recalculated out of 196                    │   │
│  │ • Rankings will change                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Reason for change:                                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Question had ambiguous wording in option C...           │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ☑ I understand this will recalculate scores for 500 students   │
│  ☑ I approve the automatic rank reassignment                    │
│                                                                 │
│  [CANCEL]                         [PREVIEW CHANGES] [CONFIRM]   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.2.4 Performance Optimization

**For Large Exams (10,000+ Students):**
```python
# Use background job queue for massive recalculations
from celery import Celery

@app.task(bind=True, max_retries=3)
def recalculate_exam_async(self, exam_id, question_id):
    try:
        engine = ExamRecalculationEngine()
        engine.recalculate_exam_scores(exam_id, question_id)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

**Database Optimization:**
- Partition `student_responses` table by `exam_id`
- Use parallel query execution for large recalculations
- Cache frequently accessed ranking data in Redis

---

## 4. Scope Boundaries - What We DON'T Build

### 4.1 Philosophy: "Do One Thing Exceptionally Well"

In the Indian B2B education market, clients will request features that seem simple but are actually complex ecosystems. We must **strictly say NO** to avoid becoming a bloated, unfocused product.

### 4.2 Explicitly Out of Scope

#### ❌ 1. Transport Tracking (School Buses)

**Why We Say No:**
- Requires GPS hardware integration (different vendors, different APIs)
- Real-time location tracking needs WebSocket infrastructure
- Parent expectations: Live map, ETA predictions, route optimization
- Liability issues: What if bus is late? What if GPS fails?
- Market has specialized players: Trakmatics, GPSGuru, BusOn

**Our Alternative:**
- Provide CSV export of student addresses
- Recommend partners: "We integrate with Trakmatics for transport tracking"
- Focus on core: Student data, not vehicle telemetry

#### ❌ 2. Library Management

**Why We Say No:**
- ISBN API integrations (costly, rate-limited)
- Barcode/RFID scanner hardware support
- Book reservation workflows, fine calculations
- Physical inventory management (lost books, damage tracking)
- Different user behavior: Librarians vs Teachers

**Our Alternative:**
- Simple field in student profile: "Library Dues: ₹XXX"
- Manual entry by librarian (no automation)
- Recommend: Koha, LibSys for dedicated library management

#### ❌ 3. Hostel Management

**Why We Say No:**
- Room/bed allocation algorithms (complex constraints)
- Mess fee calculations (daily meal tracking)
- Out-pass/in-pass approval workflows
- Visitor management
- Inventory management (linen, furniture)
- Completely different operational workflow

**Our Alternative:**
- Single field: "Hostel Resident: Yes/No"
- Hostel fee added to main fee structure (lump sum)
- No room tracking, no mess menus, no visitor logs

#### ❌ 4. Custom Report Builders

**Why We Say No:**
- Building a mini-Tableau takes 6+ months
- Users want drag-and-drop but don't know SQL
- Performance nightmares with complex joins
- Support burden: "Why doesn't my report work?"
- Security risks: Users accidentally expose sensitive data

**Our Alternative:**
- **Fixed Report Suite**: 50+ pre-built reports (NAAC, AICTE, internal)
- **Filter Options**: Date range, batch, stream, gender filters on each report
- **Raw CSV Export**: "Download raw data" button for power users
- **Scheduled Reports**: Email PDF/CSV every Monday at 9 AM

### 4.3 How to Handle Client Requests

**Script for Sales Team:**

> *"That's a great requirement! However, we've made a strategic decision to focus 100% on delivering the best academic management, examination, and compliance platform. For [Transport/Library/Hostel], we recommend our certified partners who specialize in that area. We can provide you with a data export that integrates seamlessly with their systems."*

**Product Rule:**
> *"If a feature requires hardware integration, real-time tracking, or a completely different user persona, it's OUT OF SCOPE."*

### 4.4 Scope Creep Decision Matrix

| Feature Request | Core to Academics? | Requires Hardware? | Different User Persona? | Decision |
|-----------------|-------------------|-------------------|------------------------|----------|
| NFC Attendance | ✅ YES | ❌ NO (uses phone) | ❌ Same (students) | ✅ BUILD |
| QR Code Attendance | ✅ YES | ❌ NO | ❌ Same | ✅ BUILD |
| Bus GPS Tracking | ❌ NO | ✅ YES | ✅ YES (drivers) | ❌ NO |
| Library Barcodes | ❌ NO | ✅ YES | ✅ YES (librarians) | ❌ NO |
| Hostel Bed Allocation | ❌ NO | ❌ NO | ✅ YES (wardens) | ❌ NO |
| NAAC Reports | ✅ YES | ❌ NO | ❌ Same | ✅ BUILD |
| Custom Report Builder | ⚠️ MAYBE | ❌ NO | ❌ Same | ❌ NO (use CSV export) |
| Video Lectures | ✅ YES | ❌ NO | ❌ Same | ✅ BUILD |
| Live Classes | ✅ YES | ❌ NO | ❌ Same | ✅ BUILD |
| Fee Payment Gateway | ✅ YES | ❌ NO | ❌ Same | ✅ BUILD |

---

## 5. User Stories

### US-1: Student Stream Transfer
**As an** Admin  
**I want to** transfer a student from one stream to another with automated archival and fee adjustment  
**So that** historical data is preserved for compliance and financial ledgers remain balanced  

**Acceptance Criteria:**
- [ ] Transfer wizard shows attendance summary before confirmation
- [ ] Historical batch record is archived (not deleted)
- [ ] Credit note or invoice generated automatically
- [ ] NAAC reports include archived attendance data
- [ ] Student receives notification of transfer completion
- [ ] Audit log captures all transfer details

**Story Points:** 13

---

### US-2: Question Recalculation
**As an** Exam Controller  
**I want to** modify a question and automatically recalculate all student scores  
**So that** I can fix errors without manual re-scoring of hundreds of papers  

**Acceptance Criteria:**
- [ ] Updating question triggers background recalculation job
- [ ] All student scores updated within 30 seconds (for 500 students)
- [ ] Rankings recalculated automatically
- [ ] Materialized view refreshed
- [ ] Notification sent to all affected students
- [ ] Audit log captures who made the change and why

**Story Points:** 21

---

### US-3: Bonus Marks Application
**As a** Principal  
**I want to** mark a question as "BONUS" so all students receive full marks  
**So that** I can compensate for a flawed question without deleting it  

**Acceptance Criteria:**
- [ ] Question status can be changed to "BONUS"
- [ ] All students automatically receive full marks for that question
- [ ] Recalculation happens instantly
- [ ] Report shows which questions were marked as bonus

**Story Points:** 8

---

### US-4: Raw Data Export
**As a** Data Analyst  
**I want to** download raw CSV data for any module  
**So that** I can create custom reports in Excel/Power BI  

**Acceptance Criteria:**
- [ ] Every list view has "Export CSV" button
- [ ] CSV includes all columns visible in the table
- [ ] Large exports (>10,000 rows) are processed asynchronously
- [ ] Email notification when export is ready
- [ ] Download link expires after 24 hours

**Story Points:** 5

---

### US-5: Partner Integration Documentation
**As a** Sales Engineer  
**I want to** provide clients with partner recommendations for out-of-scope features  
**So that** they can still get complete solutions without us building everything  

**Acceptance Criteria:**
- [ ] Help documentation lists recommended partners for Transport, Library, Hostel
- [ ] CSV export formats documented for partner integration
- [ ] Sales team trained on "how to say no" scripts

**Story Points:** 3

---

## 6. Technical Implementation Checklist

### 6.1 Transfer Workflow
- [ ] Create `student_batch_history` table
- [ ] Implement transfer wizard UI
- [ ] Build fee adjustment calculator
- [ ] Add credit note generation
- [ ] Update NAAC report queries to include archived data
- [ ] Write unit tests for edge cases (mid-exam transfer, etc.)

### 6.2 Recalculation Engine
- [ ] Add version control to `exam_questions` table
- [ ] Make `student_responses` immutable (append-only)
- [ ] Create materialized view for rankings
- [ ] Build background job for async recalculation
- [ ] Implement question challenge workflow
- [ ] Load test with 10,000 students

### 6.3 Scope Enforcement
- [ ] Remove any existing code for Transport/Library/Hostel
- [ ] Add "Export CSV" button to all list views
- [ ] Create partner recommendation page in help docs
- [ ] Train sales team on scope boundaries

---

## 7. Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Transfer breaks historical reports | Low | High | Comprehensive testing with NAAC report suite |
| Recalculation slows down system | Medium | High | Background jobs, database partitioning, load testing |
| Clients demand out-of-scope features | High | Medium | Clear documentation, partner network, sales training |
| Data corruption during transfer | Low | Critical | Atomic transactions, rollback mechanisms, backups |

---

## 8. Success Metrics

- **Transfer Workflow**: 100% of transfers preserve historical data (verified by NAAC reports)
- **Recalculation**: <30 seconds for 500 students, <5 minutes for 10,000 students
- **Scope Adherence**: Zero development hours spent on out-of-scope features
- **Client Satisfaction**: <5% of clients request out-of-scope features after demo

---

## 9. Appendix: Sample SQL Queries

### Get Student's Complete Batch History
```sql
SELECT 
    sbh.enrollment_date,
    sbh.exit_date,
    b.name as batch_name,
    sbh.stream_code,
    COUNT(DISTINCT a.id) as total_attendance_days,
    SUM(CASE WHEN a.status = 'PRESENT' THEN 1 ELSE 0 END) as present_days
FROM student_batch_history sbh
JOIN batches b ON sbh.batch_id = b.id
LEFT JOIN attendance a ON a.student_id = sbh.student_id 
    AND a.date BETWEEN sbh.enrollment_date AND COALESCE(sbh.exit_date, CURRENT_DATE)
WHERE sbh.student_id = 'UUID_HERE'
GROUP BY sbh.enrollment_date, sbh.exit_date, b.name, sbh.stream_code
ORDER BY sbh.enrollment_date;
```

### Recalculate Exam Rankings (Manual Query)
```sql
WITH student_totals AS (
    SELECT 
        exam_id,
        student_id,
        SUM(marks_awarded) as total_marks
    FROM student_responses
    WHERE exam_id = 'UUID_HERE'
    GROUP BY exam_id, student_id
),
ranked_students AS (
    SELECT 
        student_id,
        total_marks,
        RANK() OVER (ORDER BY total_marks DESC) as all_india_rank,
        PERCENT_RANK() OVER (ORDER BY total_marks ASC) as percentile
    FROM student_totals
)
SELECT * FROM ranked_students
ORDER BY all_india_rank;
```

---

**Document Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | | | |
| Tech Lead | | | |
| QA Lead | | | |

---

**END OF DOCUMENT**
