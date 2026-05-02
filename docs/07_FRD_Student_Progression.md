# Functional Requirements Document (FRD) - Student Progression & Results

## Document Information

| Attribute | Details |
|-----------|---------|
| **Document ID** | FRD-EDU-007 |
| **Version** | 1.0 |
| **Date** | December 2024 |
| **Prepared By** | Product Management Team |
| **Approved By** | CTO, Academic Head |
| **Status** | Draft |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Module Overview](#2-module-overview)
3. [Pass/Fail Logic Engine](#3-passfail-logic-engine)
4. [ATKT (Allow To Keep Terms) System](#4-atkt-allow-to-keep-terms-system)
5. [Promotion & Detention Rules](#5-promotion--detention-rules)
6. [Grade Point Calculation](#6-grade-point-calculation)
7. [Result Processing Workflow](#7-result-processing-workflow)
8. [Revaluation & Backlog Management](#8-revaluation--backlog-management)
9. [Certificate Generation](#9-certificate-generation)
10. [Reporting & Analytics](#10-reporting--analytics)

---

## 1. Introduction

### 1.1 Purpose

This document defines the complete student progression system including pass/fail determination, ATKT rules, promotion criteria, grade calculations, and result processing workflows for Indian educational institutions.

### 1.2 Scope

Covers:
- Pass/Fail logic for schools (CBSE, ICSE, State Boards)
- ATKT rules for colleges (Engineering, Medical, Arts, Commerce)
- Credit-based systems (CBCS, NEP 2020)
- Grade point calculations (GPA, CGPA, SGPA)
- Revaluation and backlog management
- Certificate generation (Marksheets, Provisional, Degree)

### 1.3 Regulatory Compliance

- **AICTE**: Model Curriculum regulations
- **UGC**: CBCS guidelines
- **University Acts**: Individual university ordinances
- **State Education Boards**: Secondary/Higher Secondary rules
- **NEP 2020**: Multiple entry/exit provisions

---

## 2. Module Overview

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Result Processing Engine                  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Pass/Fail    │  │   ATKT       │  │  Promotion   │       │
│  │   Logic      │  │   Engine     │  │   Rules      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   GPA/CGPA   │  │  Backlog     │  │ Certificate  │       │
│  │ Calculator   │  │  Manager     │  │  Generator   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────────────┐    ┌────────────────┐   ┌────────────────┐
│ School Board  │    │ Undergraduate  │   │ Postgraduate   │
│ (Class 10/12) │    │ (Semester)     │   │ (Credit-based) │
└───────────────┘    └────────────────┘   └────────────────┘
```

### 2.2 User Roles

| Role | Permissions |
|------|-------------|
| Exam Controller | Configure rules, approve results, modify grades |
| Faculty | Enter marks, view student progress, suggest promotions |
| HOD | Approve department results, view analytics |
| Admin | Generate certificates, access all reports |
| Student | View results, download marksheets, apply for revaluation |
| Parent | View child's results, attendance, progress |

---

## 3. Pass/Fail Logic Engine

### 3.1 School Board Pass Criteria (Class 10 & 12)

#### FR-RESULT-001: CBSE/State Board Pass Logic

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-RESULT-001 |
| **Feature** | School Pass/Fail Determination |
| **User Story** | As an exam controller, I want to configure pass criteria so that students are evaluated according to board regulations |

**Pass Criteria Configuration:**

**Option A: Subject-wise Pass (Traditional)**
```
For each subject:
- Theory: Minimum 33% of theory marks
- Practical: Minimum 33% of practical marks
- Overall: Minimum 33% of total marks

Student PASSES if:
- ALL subjects meet pass criteria

Student FAILS if:
- ANY subject fails to meet criteria
```

**Option B: Aggregate Pass (Modern)**
```
Student PASSES if:
- Aggregate percentage >= 33%
- AND minimum 25% in each subject (relaxed)

Student FAILS if:
- Aggregate < 33% OR
- Any subject < 25%
```

**Option C: Best of Five Rule (CBSE)**
```
If student fails in 1-2 subjects:
- Consider best 5 subjects including:
  * Language 1 (mandatory)
  * Language 2 (mandatory)
  * Best 3 from remaining subjects
- Calculate aggregate from best 5
- If aggregate >= 33%, declare PASS with "Additional Subject" notation
```

**Functional Flow:**

1. **Configure Pass Rules:**
   - Admin navigates to Examination → Pass Criteria
   - Selects academic year and class
   - Chooses pass rule type (Subject-wise/Aggregate/Best-of-Five)
   - Sets minimum percentages for:
     - Theory component
     - Practical component
     - Internal assessment
     - Overall subject
     - Aggregate (if applicable)
   - Saves configuration

2. **Automatic Pass/Fail Calculation:**
   ```
   FOR each student IN class:
       FOR each subject:
           theory_pct = (theory_obtained / theory_total) * 100
           practical_pct = (practical_obtained / practical_total) * 100
           internal_pct = (internal_obtained / internal_total) * 100
           total_pct = (total_obtained / total_max) * 100
           
           IF rule_type == "Subject-wise":
               IF theory_pct < theory_min OR 
                  practical_pct < practical_min OR
                  total_pct < overall_min:
                   subject_status = "FAIL"
               ELSE:
                   subject_status = "PASS"
           
           Store subject_status
       
       Calculate aggregate_percentage
       
       IF all_subjects_pass:
           final_result = "PASS"
           division = calculate_division(aggregate_percentage)
       ELSE IF failed_subjects_count <= max_fail_allowance:
           final_result = "ESSENTIAL REPEAT"
           failed_subjects_list = get_failed_subjects()
       ELSE:
           final_result = "FAIL"
   
   Update result database
   Generate result cards
   ```

3. **Division/Grade Assignment:**

**CBSE Class 10/12 Grading:**
| Percentage Range | Grade | Grade Points | Division |
|-----------------|-------|--------------|----------|
| 91-100% | A1 | 10.0 | Distinction |
| 81-90% | A2 | 9.0 | First Class |
| 71-80% | B1 | 8.0 | First Class |
| 61-70% | B2 | 7.0 | Second Class |
| 51-60% | C1 | 6.0 | Second Class |
| 41-50% | C2 | 5.0 | Pass |
| 33-40% | D | 4.0 | Pass |
| < 33% | E | 0.0 | Fail |

**State Board Divisions:**
| Percentage Range | Division |
|-----------------|----------|
| >= 75% | Distinction |
| 60-74% | First Class |
| 50-59% | Second Class |
| 40-49% | Pass Class |
| 33-39% | Pass (Supplementary) |
| < 33% | Fail |

**Output:**
- Individual result card with subject-wise marks
- Division/grade certificate
- Marksheet with grade points
- Consolidated statement of marks

---

### 3.2 College Semester Pass Logic

#### FR-RESULT-002: Engineering/College Pass Criteria

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-RESULT-002 |
| **Feature** | Semester Pass/Fail with Headway Rules |

**Pass Criteria for Engineering (AICTE Model):**

```
For each course (subject):
- Theory: Minimum 40% of theory marks (out of 70/80/100)
- Sessional/Internal: Minimum 40% of internal marks (out of 30/20)
- Overall: Minimum 40% of total marks

Student PASSES course if:
- (Theory + Sessional) >= 40% of total
- AND Theory >= 40% of theory max (headway rule)

Student FAILS course if:
- Total < 40% OR
- Theory < 40% of theory max (even if total >= 40%)
```

**Headway Rule Explanation:**
```
Example: Course with 70 Theory + 30 Sessional = 100 Total

Case 1:
- Theory: 25/70 (35.7%) ❌
- Sessional: 28/30 (93.3%) ✓
- Total: 53/100 (53%) ✓
- RESULT: FAIL (Theory headway not met)

Case 2:
- Theory: 30/70 (42.8%) ✓
- Sessional: 15/30 (50%) ✓
- Total: 45/100 (45%) ✓
- RESULT: PASS (All criteria met)
```

**Functional Flow:**

1. **Course Result Entry:**
   - Faculty enters marks for each student
   - System validates:
     - Theory marks <= theory maximum
     - Sessional marks <= sessional maximum
     - Total = Theory + Sessional
   - System auto-calculates pass/fail per course

2. **Semester Result Compilation:**
   ```
   FOR each student IN semester:
       passed_courses = []
       failed_courses = []
       
       FOR each course:
           IF course.passed:
               passed_courses.add(course)
               credits_earned += course.credits
           ELSE:
               failed_courses.add(course)
               credits_lost += course.credits
       
       total_credits = sum(all_course_credits)
       earned_credits = sum(passed_course_credits)
       
       IF failed_courses.count == 0:
           semester_status = "PASS"
           sgpa = calculate_sgpa(passed_courses)
       ELSE IF failed_courses.count <= atkt_limit:
           semester_status = "PASS WITH ATKT"
           sgpa = calculate_sgpa(passed_courses) // Only passed courses
           atkt_courses = failed_courses
       ELSE:
           semester_status = "FAIL"
           sgpa = 0
           must_repeat_semester = true
   
   Generate semester marksheet
   ```

---

## 4. ATKT (Allow To Keep Terms) System

### 4.1 ATKT Configuration

#### FR-RESULT-003: ATKT Rules Engine

| Attribute | Description |
|-----------|-------------|
| **ID** | FR-RESULT-003 |
| **Feature** | Allow To Keep Terms Configuration |
| **Applicability** | Engineering, Degree Colleges, Professional Courses |

**ATKT Rule Types:**

**Type A: Course-based ATKT (Most Common)**
```
Allowed if:
- Failed courses <= N (typically 2-4 courses)
- AND failed courses belong to current semester only

Not allowed if:
- Failed courses > N
- OR backlog from previous semester exists
```

**Type B: Credit-based ATKT**
```
Allowed if:
- Failed credits <= X% of total semester credits (typically 25-30%)
- Example: If semester has 24 credits, ATKT allowed for max 6 failed credits
```

**Type C: SGPA-based ATKT**
```
Allowed if:
- SGPA >= Y (typically 4.0-5.0 out of 10)
- Even with failed courses
```

**Configuration Interface:**

1. **Admin Setup:**
   - Navigate to Academics → ATKT Rules
   - Select program (B.Tech, BCA, MBA, etc.)
   - Configure:
     ```
     - Maximum failed courses allowed: [2] [3] [4] [Custom]
     - Maximum failed credits allowed: [___] or [% of total]
     - Minimum SGPA required: [___] / 10
     - Backlog limit from previous semesters: [0] [1] [2]
     - Is ATKT applicable for final semester? [Yes/No]
     - Grace marks policy: [Enabled/Disabled]
     ```

2. **Program-specific Rules:**
   ```
   B.Tech (Mumbai University Pattern):
   - Max 4 courses with backlogs allowed
   - No restriction on previous backlogs
   - Final semester: No ATKT (must clear all)
   
   B.Tech (GTU Pattern):
   - Max 3 backlogs allowed
   - If backlogs > 3, must repeat semester
   - Final year: Special ATKT rules apply
   
   BCA/MBA (CBCS):
   - Credit-based: Max 25% credits can be backlogs
   - Must maintain SGPA >= 5.0
   ```

### 4.2 ATKT Processing Workflow

#### FR-RESULT-004: ATKT Application Logic

**Functional Flow:**

```
FOR each student with failed courses:
    // Step 1: Check eligibility
    failed_count = count(failed_courses)
    failed_credits = sum(failed_courses.credits)
    total_credits = semester.total_credits
    backlog_from_prev = count(backlog_courses_from_previous_semesters)
    
    // Step 2: Apply rules
    eligible_for_atkt = true
    rejection_reason = ""
    
    IF failed_count > max_allowed_courses:
        eligible_for_atkt = false
        rejection_reason = "Exceeded maximum failed courses limit"
    
    IF failed_credits > (total_credits * atkt_credit_percentage / 100):
        eligible_for_atkt = false
        rejection_reason = "Failed credits exceed allowable limit"
    
    IF sgpa < min_sgpa_required:
        eligible_for_atkt = false
        rejection_reason = "SGPA below minimum threshold"
    
    IF backlog_from_prev > max_previous_backlogs:
        eligible_for_atkt = false
        rejection_reason = "Too many backlogs from previous semesters"
    
    IF is_final_semester AND NOT atkt_in_final_allowed:
        eligible_for_atkt = false
        rejection_reason = "ATKT not permitted in final semester"
    
    // Step 3: Apply decision
    IF eligible_for_atkt:
        student.semester_status = "PASS WITH ATKT"
        student.atkt_courses = failed_courses
        student.next_semester_eligible = true
        student.must_clear_atkt_in = next_exam_cycle
        
        // Generate ATKT challan (fee for re-exam)
        generate_atkt_fee_challan(student, failed_courses)
        
        // Notify student
        send_notification(student, "ATKT Applied", 
            "You are promoted with ${failed_count} backlogs. " +
            "Please clear these in the next examination.")
    ELSE:
        student.semester_status = "FAIL"
        student.must_repeat_semester = true
        student.next_semester_eligible = false
        
        send_notification(student, "Semester Failed",
            "You must repeat Semester ${semester_number}. " +
            "Reason: ${rejection_reason}")
```

### 4.3 ATKT Examination Cycle

#### FR-RESULT-005: Backlog Exam Management

**Exam Cycle Configuration:**

1. **Exam Frequency:**
   - Option A: Every semester (along with regular exams)
   - Option B: Twice a year (May-June, Nov-Dec)
   - Option C: Once a year (Summer break)

2. **Backlog Course Mapping:**
   ```
   When new syllabus is introduced:
   - System maps old course codes to new equivalents
   - Students with old backlogs can appear for new course
   - OR separate exam conducted for old syllabus (for 2 years)
   ```

3. **Automatic Registration:**
   ```
   Before each backlog exam cycle:
   - Identify all students with active backlogs
   - Auto-register them for relevant courses
   - Generate fee challan
   - Send admit cards
   - Create exam timetable (separate from regular)
   ```

---

## 5. Promotion & Detention Rules

### 5.1 School Promotion (Class to Class)

#### FR-RESULT-006: School Promotion Criteria

**No-Detention Policy (RTE Act - Classes 1-8):**
```
FOR classes 1 to 8:
    // As per Right to Education Act
    ALL students are automatically promoted
    NO student can be held back
    
    System actions:
    - Auto-promote all students to next class
    - Generate continuous comprehensive evaluation (CCE) report
    - Flag students needing remedial support
```

**Detention Allowed (Classes 9-12):**
```
FOR classes 9 to 12:
    Promotion criteria:
    - Pass in ALL subjects OR
    - Pass in at least N subjects (state-specific)
    
    Detention if:
    - Failed in more than M subjects
    - Attendance < 75% (in some boards)
    
    Example (Maharashtra State Board):
    - Class 9: Pass in 4 out of 5 subjects
    - Class 10: Must pass all subjects (no ATKT)
    - Class 11: Pass in 4 out of 5 subjects
    - Class 12: Must pass all subjects
```

### 5.2 College Promotion (Semester to Semester)

#### FR-RESULT-007: College Promotion Logic

**Engineering Promotion Matrix:**

```
Semester 1 → Semester 2:
- Pass in minimum 3 courses OR
- SGPA >= 4.0
- OR ATKT applied (max 4 backlogs)

Semester 2 → Semester 3:
- Clear Semester 1 OR
- Max 4 backlogs from Sem 1+2 combined
- SGPA >= 4.5

Year 2 → Year 3 (Semester 4 → 5):
- Max 6 backlogs from Sem 1-4
- OR earned credits >= 60% of total

Year 3 → Year 4 (Semester 6 → 7):
- Max 8 backlogs from Sem 1-6
- OR earned credits >= 70% of total

Final Semester (Semester 8):
- MUST clear all backlogs before appearing
- NO ATKT in final semester
- All courses must be passed for degree eligibility
```

**Functional Flow:**

```
FUNCTION check_promotion_eligibility(student, current_semester):
    total_backlogs = count_all_backlogs(student, up_to=current_semester)
    earned_credits = sum_earned_credits(student)
    total_credits_till_now = sum_total_credits(up_to=current_semester)
    sgpa_current = calculate_sgpa(current_semester)
    
    promotion_rules = get_promotion_rules(program=student.program, 
                                          year=current_semester.year)
    
    // Check multiple criteria
    meets_backlog_limit = total_backlogs <= promotion_rules.max_backlogs
    meets_credit_requirement = earned_credits >= (total_credits_till_now * 0.60)
    meets_sgpa_requirement = sgpa_current >= promotion_rules.min_sgpa
    
    IF meets_backlog_limit OR meets_credit_requirement:
        return PROMOTION_ELIGIBLE
    ELSE:
        return DETENTION_REQUIRED
```

### 5.3 NEP 2020 Multiple Entry/Exit

#### FR-RESULT-008: NEP Flexible Progression

**Multiple Exit Points:**

```
Undergraduate Program (4 years):

Exit after Year 1:
- Earned credits >= 44 (out of 176)
- Award: UNDERGRADUATE CERTIFICATE
- Can re-enter within 3 years

Exit after Year 2:
- Earned credits >= 88
- Award: UNDERGRADUATE DIPLOMA
- Can re-enter within 3 years

Exit after Year 3:
- Earned credits >= 132
- Award: BACHELOR'S DEGREE
- Can re-enter for Honors within 2 years

Complete Year 4:
- Earned credits >= 176
- Award: BACHELOR'S DEGREE WITH HONORS/SPECIALIZATION
```

**Academic Bank of Credits (ABC) Integration:**

```
When student exits:
1. Transfer credits to ABC ID
2. Generate digital certificate with credit details
3. Credits remain valid for 7 years

When student re-enters:
1. Fetch credits from ABC via API
2. Map to new institution's curriculum
3. Grant lateral entry to appropriate semester
4. Remaining credits to be earned
```

---

## 6. Grade Point Calculation

### 6.1 GPA/SGPA/CGPA Engine

#### FR-RESULT-009: Credit-Based Grading

**Grade Point Tables:**

**10-Point Scale (Most Common):**
| Marks Range | Grade | Grade Points | Performance |
|------------|-------|--------------|-------------|
| 90-100 | O | 10.0 | Outstanding |
| 80-89 | A+ | 9.0 | Excellent |
| 70-79 | A | 8.0 | Very Good |
| 60-69 | B+ | 7.0 | Good |
| 55-59 | B | 6.0 | Above Average |
| 50-54 | C | 5.0 | Average |
| 45-49 | P | 4.0 | Pass |
| 40-44 | D | 3.0 | Deficient but Pass |
| 0-39 | F | 0.0 | Fail |
| Absent | AB | 0.0 | Absent |

**4-Point Scale (Some Universities):**
| Marks Range | Grade | Grade Points |
|------------|-------|--------------|
| 80-100 | A | 4.0 |
| 70-79 | B | 3.0 |
| 60-69 | C | 2.0 |
| 50-59 | D | 1.0 |
| 0-49 | F | 0.0 |

**Calculation Algorithm:**

```
FUNCTION calculate_sgpa(semester):
    total_credit_points = 0
    total_credits = 0
    
    FOR each course IN semester:
        IF course.grade != 'F' AND course.grade != 'AB':
            grade_points = get_grade_points(course.grade)
            credit_points = grade_points * course.credits
            total_credit_points += credit_points
            total_credits += course.credits
    
    IF total_credits == 0:
        return 0.0
    
    sgpa = total_credit_points / total_credits
    return round(sgpa, 2)

FUNCTION calculate_cgpa(student):
    total_credit_points = 0
    total_credits = 0
    
    FOR each semester IN student.semesters_completed:
        FOR each course IN semester:
            IF course.grade != 'F':
                grade_points = get_grade_points(course.grade)
                credit_points = grade_points * course.credits
                total_credit_points += credit_points
                total_credits += course.credits
    
    IF total_credits == 0:
        return 0.0
    
    cgpa = total_credit_points / total_credits
    return round(cgpa, 2)
```

**Example Calculation:**

```
Semester 1 Results:
| Course | Credits | Marks | Grade | Grade Points | Credit Points |
|--------|---------|-------|-------|--------------|---------------|
| Math-I | 4 | 85 | A+ | 9.0 | 36.0 |
| Physics | 4 | 78 | A | 8.0 | 32.0 |
| Chemistry | 4 | 92 | O | 10.0 | 40.0 |
| Programming | 4 | 88 | A+ | 9.0 | 36.0 |
| English | 2 | 75 | A | 8.0 | 16.0 |
| Workshop | 2 | 95 | O | 10.0 | 20.0 |
| TOTAL | 20 | - | - | - | 180.0 |

SGPA = 180.0 / 20 = 9.00
```

### 6.2 Percentage to Grade Conversion

#### FR-RESULT-010: Custom Grading Schemes

**Institution-defined Grading:**

1. **Create Custom Scheme:**
   - Navigate to Academics → Grading Schemes
   - Click "New Grading Scheme"
   - Define:
     ```
     Scheme Name: "Engineering 2024 Pattern"
     Scale: 10-point / 4-point / Custom
     Passing Grade: P / D / C (configurable)
     
     Grade Definitions:
     - Grade: O | Min Marks: 90 | Max Marks: 100 | Points: 10
     - Grade: A+ | Min Marks: 80 | Max Marks: 89 | Points: 9
     - Grade: A | Min Marks: 70 | Max Marks: 79 | Points: 8
     ...
     ```

2. **Apply to Programs:**
   - Assign grading scheme to specific programs
   - Different schemes for UG/PG/Diploma
   - Version control for scheme changes

---

## 7. Result Processing Workflow

### 7.1 End-to-End Result Lifecycle

#### FR-RESULT-011: Result Processing Pipeline

**Phase 1: Mark Entry (2-3 weeks before result)**

```
1. Exam Controller announces "Mark Entry Open"
2. Faculty receive notification
3. Faculty login → Exam → Mark Entry
4. Select course and batch
5. Enter marks for each student:
   - Theory marks (validated against max)
   - Practical marks (if applicable)
   - Internal/Sessional marks
6. System auto-calculates totals
7. Faculty submits → Status: "Pending HOD Approval"
8. HOD reviews and approves → Status: "Ready for Processing"
```

**Phase 2: Result Validation (1 week)**

```
1. Exam Controller runs validation checks:
   - All courses marked? Y/N
   - Any marks exceeding maximum? Flag
   - Sudden spikes/drops in performance? Review
   - Comparison with previous year trends? Analyze

2. System generates exception report:
   - Courses with 100% pass rate (verify)
   - Courses with < 30% pass rate (verify)
   - Individual students with unusual patterns

3. Exam Controller reviews exceptions
4. Corrections sent back to faculty if needed
```

**Phase 3: Result Approval (2-3 days)**

```
1. Exam Controller clicks "Process Results"
2. System runs pass/fail logic for all students
3. Generates draft results
4. Principal/Dean reviews sample results
5. Approves final results
6. System locks results (no further changes)
7. Publishes to student portal
```

**Phase 4: Result Publication**

```
1. Results go live on student portal
2. SMS/Email notifications sent
3. Digital marksheets generated
4. Physical marksheets printed (optional)
5. University portal upload (if affiliated)
```

### 7.2 Result Modification & Correction

#### FR-RESULT-012: Post-Publication Changes

**Allowed Modifications:**

| Scenario | Who Can Change | Approval Required | Time Limit |
|----------|---------------|-------------------|------------|
| Data entry error | Faculty | HOD + Exam Controller | 7 days |
| Totalling mistake | Exam Cell | Exam Controller | 15 days |
| Grade change after revaluation | Exam Cell | University | 30 days |
| Wrong course mapping | Admin | Academic Council | Anytime |

**Audit Trail:**

```
Every modification logged:
- Original value
- New value
- Changed by (user ID)
- Date/time
- Reason for change
- Approval reference number
```

---

## 8. Revaluation & Backlog Management

### 8.1 Revaluation Process

#### FR-RESULT-013: Revaluation Workflow

**Revaluation Types:**

1. **Total Revaluation:** Complete re-checking of answer sheet
2. **Partial Revaluation:** Specific questions only
3. **Photocopy:** Get Xerox of evaluated answer sheet
4. **Challenge Evaluation:** Re-evaluation by different examiner

**Functional Flow:**

```
1. Student applies for revaluation:
   - Login to student portal
   - Navigate to Results → Revaluation
   - Select semester and course
   - Choose revaluation type
   - Pay fee online (₹300-1000 per course)
   - Submit application

2. System processes application:
   - Validates eligibility (within 15 days of result)
   - Confirms payment
   - Generates acknowledgment
   - Notifies exam cell

3. Exam cell action:
   - Retrieves original answer sheet
   - Sends to senior examiner
   - Examiner re-evaluates
   - New marks entered

4. Result update:
   IF new_marks > old_marks:
       UPDATE to new_marks
       REFUND 50% fee to student
       Issue revised marksheet
   ELSE IF new_marks < old_marks:
       RETAIN old_marks (benefit of doubt)
       NO refund
   ELSE:
       No change
       NO refund

5. Notification to student:
   - SMS/Email with revised status
   - Download revised marksheet
```

### 8.2 Backlog Tracking

#### FR-RESULT-014: Active Backlog Management

**Backlog Dashboard:**

```
Student View:
┌─────────────────────────────────────────────┐
│ My Active Backlogs                          │
├─────────────────────────────────────────────┤
│ Semester | Course Code | Course Name | Status│
├─────────────────────────────────────────────┤
│ Sem 2    | MA201       | Engg Math-II| Due  │
│ Sem 3    | CS301       | Data Struct | Due  │
│ Sem 3    | CS302       | DBMS        | Due  │
├─────────────────────────────────────────────┤
│ Total: 3 backlogs                           │
│ Next exam: May 2025                         │
│ Fee payable: ₹1500                          │
└─────────────────────────────────────────────┘
```

**Auto-Clearance Rules:**

```
When student appears for backlog exam:
- If PASS: Remove from active backlogs
- If FAIL: Keep active, allow next attempt
- After N attempts (typically 4-5):
  - Flag for academic counseling
  - May require repeating semester
```

---

## 9. Certificate Generation

### 9.1 Digital Certificate Engine

#### FR-RESULT-015: Automated Certificate Creation

**Certificate Types:**

1. **Provisional Certificate:** Issued immediately after passing
2. **Degree Certificate:** Original degree convocation
3. **Marksheet:** Semester-wise or consolidated
4. **Migration Certificate:** For transferring to other universities
5. **Character Certificate:** Conduct verification
6. **Transfer Certificate:** Leaving certificate

**Digital Signature Integration:**

```
Certificates include:
- QR code for verification
- Digital signature of authorities
- Unique certificate ID
- Blockchain hash (optional)
- Security features (watermarks, hologram data)
```

**Generation Workflow:**

```
1. Trigger event:
   - Student passes final semester
   - All dues cleared
   - Library books returned
   - Hostel vacated (if applicable)

2. System checks clearance:
   FOR each clearance_item:
       IF not_cleared:
           BLOCK certificate generation
           Notify student to clear dues

3. Generate certificate:
   - Fetch student data
   - Populate certificate template
   - Add QR code with verification URL
   - Apply digital signatures
   - Generate PDF
   - Store in secure repository

4. Delivery options:
   - Download from portal
   - Email delivery
   - Physical copy by post
   - Collect in person
```

### 9.2 Verification System

#### FR-RESULT-016: Certificate Authentication

**QR Code Verification:**

```
When QR scanned:
1. Redirects to: verify.educore.in/{certificate_id}
2. Displays:
   - Certificate details
   - Holder name
   - Program, year, grades
   - Validity status (Valid/Revoked)
   - Issuing authority
3. Option to download verified copy
```

**API for Third-party Verification:**

```
Employer/University can verify via API:
POST /api/v1/verify-certificate
{
  "certificate_id": "UNIV2024ENG12345",
  "dob": "2002-05-15"
}

Response:
{
  "valid": true,
  "name": "Rahul Sharma",
  "degree": "B.Tech Computer Science",
  "year": 2024,
  "cgpa": 8.45,
  "status": "Original"
}
```

---

## 10. Reporting & Analytics

### 10.1 Standard Reports

#### FR-RESULT-017: Pre-built Report Templates

**Academic Reports:**

| Report Name | Frequency | Audience | Key Metrics |
|-------------|-----------|----------|-------------|
| Semester Result Analysis | Per semester | HOD, Principal | Pass %, avg marks, toppers |
| Course-wise Performance | Per semester | Faculty, HOD | Difficulty index, question quality |
| Student Progress Report | On-demand | Student, Parent | Trend across semesters |
| Backlog Analysis | Monthly | Academic Dean | Backlog count, clearance rate |
| Division Distribution | Per semester | Management | % in each division |
| Year-on-Year Comparison | Annual | Management | Improvement trends |

**Regulatory Reports:**

| Report Name | Submission To | Frequency | Format |
|-------------|---------------|-----------|--------|
| University Returns | Affiliating University | Per semester | Prescribed format |
| AICTE MIS | AICTE | Annual | Online portal |
| NAAC SSR Data | NAAC | Every 5 years | Detailed Excel |
| State DPE Report | State Education Dept | Annual | Online |

### 10.2 Advanced Analytics

#### FR-RESULT-018: Predictive Analytics

**At-Risk Student Identification:**

```
ML Model predicts students likely to fail:
Input features:
- Attendance percentage
- Internal assessment scores
- Assignment submission rate
- Previous semester SGPA
- Library usage
- LMS engagement

Output:
- Risk score (0-100)
- Risk category: Low/Medium/High
- Recommended interventions
```

**Early Warning System:**

```
IF student.risk_score > 70:
    ALERT academic counselor
    NOTIFY student and parents
    SCHEDULE counseling session
    CREATE improvement plan
    MONITOR weekly progress
```

---

## Appendices

### Appendix A: Sample Pass/Fail Configurations

**CBSE Class 10:**
```json
{
  "board": "CBSE",
  "class": "10",
  "pass_rule": "subject_wise",
  "min_theory_pct": 33,
  "min_practical_pct": 33,
  "min_overall_pct": 33,
  "best_of_five": true,
  "grace_marks": {
    "enabled": true,
    "max_per_subject": 5,
    "total_max": 10
  }
}
```

**B.Tech Semester:**
```json
{
  "program": "B.Tech",
  "pass_rule": "headway",
  "min_theory_pct": 40,
  "min_sessional_pct": 40,
  "min_overall_pct": 40,
  "atkt": {
    "max_courses": 4,
    "applicable_in_final": false
  }
}
```

### Appendix B: Glossary

| Term | Definition |
|------|------------|
| ATKT | Allow To Keep Terms - Promotion with backlogs |
| SGPA | Semester Grade Point Average |
| CGPA | Cumulative Grade Point Average |
| Headway Rule | Minimum marks required in theory component |
| Backlog | Failed course that needs to be cleared |
| Revaluation | Re-checking of evaluated answer sheets |
| CBCS | Choice Based Credit System |
| ABC | Academic Bank of Credits |

---

**Document End**
