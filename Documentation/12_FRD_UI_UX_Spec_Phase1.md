# 12. UI/UX Design Specification - Phase 1 (MVP)

## 1. Design System & Visual Identity

### 1.1 Color Palette (Indian Education Context)
| Role | Primary | Secondary | Accent | Background | Text |
|------|---------|-----------|--------|------------|------|
| **Admin** | Deep Blue `#1E3A8A` | Slate `#64748B` | Amber `#F59E0B` | White `#FFFFFF` | Charcoal `#1F2937` |
| **Faculty** | Teal `#0D9488` | Emerald `#10B981` | Orange `#F97316` | Off-White `#F8FAFC` | Dark Gray `#374151` |
| **Student** | Indigo `#4F46E5` | Purple `#7C3AED` | Pink `#EC4899` | Light Blue `#EFF6FF` | Navy `#1E293B` |
| **Parent** | Green `#059669` | Lime `#84CC16` | Cyan `#06B6D4` | Mint `#ECFDF5` | Forest `#064E3B` |
| **Alerts** | Error `#DC2626` | Warning `#D97706` | Success `#059669` | Info `#2563EB` | - |

### 1.2 Typography
- **Headings**: Inter Bold (H1: 32px, H2: 24px, H3: 20px)
- **Body**: Inter Regular (16px for mobile, 18px for desktop)
- **Small/Caption**: Inter Medium (14px)
- **Monospace**: JetBrains Mono (for code, IDs, roll numbers)

### 1.3 Spacing & Layout
- **Grid**: 8pt grid system
- **Container Max Width**: 1280px (desktop), 100% (mobile)
- **Card Padding**: 24px (desktop), 16px (mobile)
- **Border Radius**: 8px (cards), 4px (buttons), 12px (modals)

---

## 2. Navigation Architecture

### 2.1 Global Navigation Pattern
- **Desktop**: Left Sidebar Collapsible (240px expanded, 64px collapsed)
- **Mobile**: Bottom Tab Bar (5 max items) + Hamburger Menu for secondary
- **Breadcrumbs**: Required on all nested pages (Home > Module > Sub-module > Page)

### 2.2 Role-Based Navigation Menus

#### **Super Admin / Institute Owner**
1. Dashboard (Overview)
2. Admissions
3. Academics (Batch/Subject/Timetable)
4. Examinations
5. Finance (Fees + Expenses + Payroll)
6. Reports (NAAC/NEP/Custom)
7. User Management
8. Settings (Branding, Config)

#### **Principal / HOD**
1. Dashboard (Analytics)
2. Faculty Management
3. Timetable Approval
4. Examination Oversight
5. Student Progression (ATKT/Promotion)
6. NAAC Reports
7. Notices & Announcements

#### **Faculty / Teacher**
1. Dashboard (Today's Schedule)
2. My Classes (Attendance Marking)
3. LMS (Upload Notes/Videos)
4. Assignments (Create/Grade)
5. Tests (Create/Monitor/Grade)
6. Student Performance Analytics
7. Leave Application
8. Payslips

#### **Student**
1. Dashboard (Upcoming Classes/Tests)
2. My Schedule (Timetable)
3. Learning Material (Notes/Videos)
4. Assignments (Submit/View Grades)
5. Test Results & Analytics
6. Fee Status & Payment
7. Attendance History
8. Profile

#### **Parent**
1. Dashboard (Child Overview)
2. Child's Attendance
3. Test Results & Report Cards
4. Fee Payment & Receipts
5. Notices from School
6. PTM Booking
7. Contact Teachers

---

## 3. Screen Inventory - Phase 1 MVP (~52 Screens)

### 3.1 Authentication Module (6 Screens)
| # | Screen Name | Purpose | Key Elements |
|---|-------------|---------|--------------|
| A1 | Login | Multi-role login | Role selector, Email/Phone, Password, OTP option, Forgot Password |
| A2 | Registration (Institution) | New college/school signup | Institute name, Logo upload, Address, Contact, Admin details |
| A3 | Student Self-Registration | Admission form | Personal info, Parent details, Documents upload, Course selection |
| A4 | OTP Verification | 2FA / Device binding | OTP input, Resend timer, Device name display |
| A5 | Password Reset | Recovery flow | Email/Phone input, OTP, New password, Confirm password |
| A6 | First-Time Setup Wizard | Institution onboarding | Logo, Theme color, Academic year setup, Board selection, Admin creation |

### 3.2 Admin Dashboard Module (8 Screens)
| # | Screen Name | Purpose | Key Elements |
|---|-------------|---------|--------------|
| D1 | Super Admin Dashboard | KPI overview | Total students, Fee collection today, Attendance %, Pending approvals, Quick actions |
| D2 | Admission Management | View/approve applications | Filter by status, Bulk approve/reject, Document preview, Fee structure assignment |
| D3 | Batch/Class Management | Create/edit batches | Batch name, Stream (Science/Commerce), Capacity, Assigned HOD, Subjects mapping |
| D4 | Subject & Syllabus Mapping | Link subjects to batches | Subject list, Chapter breakdown, Target completion date, Teacher assignment |
| D5 | Timetable Generator | Drag-drop scheduling | Calendar view, Conflict warnings, Auto-generate button, Print/Export PDF |
| D6 | Faculty Management | Staff directory & HR | Add teacher, Qualification, Salary config, Leave balance, Performance metrics |
| D7 | Fee Structure Builder | Define fee plans | Installment dates, Amount per installment, Late fee rules, Scholarship discounts |
| D8 | Defaulter List | Track pending fees | Student list, Outstanding amount, Days overdue, Send SMS/WhatsApp button |

### 3.3 Finance & Accounts Module (7 Screens)
| # | Screen Name | Purpose | Key Elements |
|---|-------------|---------|--------------|
| F1 | Fee Collection Counter | Cash/Card/UPI payment | Student search (QR/ID), Fee breakdown, Payment mode selection, Receipt print |
| F2 | Payment Receipt View | GST-compliant receipt | Institute logo, Student details, Fee breakdown, QR code, Digital signature |
| F3 | Expense Entry | Record institute expenses | Category (Salary/Infrastructure/etc.), Amount, Vendor, Bill upload, Approval status |
| F4 | Expense Approval Workflow | Principal approves expenses | Pending list, Approve/Reject buttons, Comments, Budget vs Actual chart |
| F5 | Payroll Dashboard | Salary processing | Faculty list, Basic pay, Allowances, Deductions (PF/TDS), Net pay, Process button |
| F6 | Salary Slip View | Downloadable payslip | Month/year, Earnings breakdown, Deductions breakdown, Net pay, Download PDF |
| F7 | EOD Cash Settlement | End-of-day report | Opening balance, Total cash collected, Reversals, Closing balance, Cashier sign-off |

### 3.4 Attendance Module (5 Screens)
| # | Screen Name | Purpose | Key Elements |
|---|-------------|---------|--------------|
| AT1 | Generate Dynamic QR | Teacher displays QR | Full-screen QR (refreshes every 30s), Session info, Batch name, Timer countdown |
| AT2 | Student Scan Interface | Mobile scan screen | Camera viewfinder, Geo-location indicator, Selfie prompt (random), Success confirmation |
| AT3 | NFC Tap Interface | Mobile-to-mobile tap | "Tap to mark attendance" button, Peer device detection, Confirmation animation |
| AT4 | Attendance Dashboard | Real-time monitoring | Present/Absent count, List of absent students, Mark manual attendance, Export CSV |
| AT5 | Proxy Detection Alerts | Security notifications | Suspicious patterns list, Device change alerts, Mock location flags, Action buttons |

### 3.5 LMS Module (8 Screens)
| # | Screen Name | Purpose | Key Elements |
|---|-------------|---------|--------------|
| L1 | Resource Library | Browse notes/videos | Folder tree, Search bar, File type filter, Upload button, Watermark toggle |
| L2 | Video Player | Watch recorded lectures | Adaptive quality selector, Playback speed, Captions, Bookmark, Note-taking panel |
| L3 | Live Class Launcher | Start Zoom/Meet/WebRTC | Meeting link generation, Recording toggle, Attendance auto-mark, Chat moderation |
| L4 | Assignment Creation | Teacher creates homework | Title, Description, Attachment upload, Due date, Max marks, Rubric builder |
| L5 | Assignment Submission | Student uploads work | File upload (PDF/Image), Text editor, Submit button, Late submission warning |
| L6 | Grading Interface | Teacher grades submissions | Side-by-side view (submission + rubric), Marks input, Remarks, Annotate PDF |
| L7 | Doubt Forum | Q&A board | Post question (text+image), Upvote, Teacher reply, Mark as resolved, Threaded comments |
| L8 | Drip Content Scheduler | Release schedule | Chapter list, Unlock date picker, Prerequisite chains, Preview student view |

### 3.6 Assessment & Exams Module (9 Screens)
| # | Screen Name | Purpose | Key Elements |
|---|-------------|---------|--------------|
| EX1 | Question Bank Manager | Store/categorize questions | Subject/topic/difficulty filters, LaTeX editor, Image upload, Bulk import CSV |
| EX2 | Test Creator | Build mock tests | Select questions, Set marking scheme (+4/-1), Time limit, Shuffle options, NTA preview |
| EX3 | CBT Exam Interface (Student) | Take test | Question palette (color-coded), Timer, Flag for review, Next/Previous, Submit |
| EX4 | Subjective Answer Upload | Upload handwritten sheets | Camera capture, Multi-page scan, Preview, Submit before deadline |
| EX5 | Digital Annotation Tool | Grade subjective answers | Pen/highlighter tools, Text comments, Marks per question, Total calculation |
| EX6 | Result Processing Dashboard | Draft → Moderation → Publish | Raw scores list, Grace marks interface, Bulk moderation rules, Publish button |
| EX7 | Leaderboard & Analytics | Rank visualization | All-India Rank, Percentile, Spider chart (topic-wise accuracy), Time spent analysis |
| EX8 | Exam Recalculation Log | Audit trail for changes | Question change history, Affected students count, Old vs New scores, Trigger timestamp |
| EX9 | Hall Ticket Generator | Print admit cards | Student photo, Roll number, Exam center, Date/time, Barcode/QR, Print PDF |

### 3.7 Student Progression Module (5 Screens)
| # | Screen Name | Purpose | Key Elements |
|---|-------------|---------|--------------|
| SP1 | ATKT Dashboard | Track backlogs | Student list, Failed subjects count, Eligible for next sem?, Promotion status |
| SP2 | GPA/SGPA/CGPA Calculator | Automatic computation | Credit table, Grade points, Formula display, Historical trend graph |
| SP3 | Transfer Workflow Wizard | Stream change (Science→Commerce) | Impact preview, Fee adjustment calc, Credit note generation, Archive old data |
| SP4 | Promotion/Detention List | Year-end decisions | Auto-calculated eligibility, Principal override button, Reason field, Bulk action |
| SP5 | Certificate Generator | Issue mark sheets | Template selector, Data merge, QR verification code, Bulk print, Digital signature |

### 3.8 Compliance & Reports Module (4 Screens)
| # | Screen Name | Purpose | Key Elements |
|---|-------------|---------|--------------|
| CR1 | NAAC SSR Dashboard | Criteria I-VII overview | Completion % per criterion, DVV matrix upload, Evidence links, Submit button |
| CR2 | NEP Credit Tracker | Multiple Entry/Exit | Credits earned, Exit point eligibility (Certificate/Diploma/Degree), Course mapping |
| CR3 | ABC Integration Status | Academic Bank of Credits | Sync status, Credit transfer requests, Partner institution list, API logs |
| CR4 | Custom Report Export | Fixed reports + CSV | Report type selector (Attendance/Fee/Result), Date range, Export CSV/PDF button |

---

## 4. Key User Flows (Step-by-Step)

### Flow 1: Student Marks Attendance via QR
```
1. Teacher opens "Generate Dynamic QR" screen → Clicks "Start Session"
2. System generates QR (valid 30s) with embedded session_id + timestamp
3. Students open app → Tap "Scan Attendance" → Camera opens
4. App detects geo-location (within 100m of institute) → Validates
5. Student scans QR → App sends {student_id, session_id, location, timestamp, device_id}
6. Backend validates: 
   - Is student enrolled in this batch?
   - Is QR still valid?
   - Is location within geo-fence?
   - Has student already marked attendance?
7. If valid → Mark present + Show success animation
8. If random selfie trigger (15% chance) → Open camera → Capture → AI liveness check → Confirm
9. Teacher dashboard updates in real-time (Present count increments)
```

### Flow 2: Fee Payment with Immutable Ledger
```
1. Receptionist searches student by ID/QR
2. System shows pending installments with due dates
3. Receptionist selects installment → Chooses payment mode (Cash/UPI/Card)
4. If Cash → Enter amount received → System calculates change (if any)
5. Click "Generate Receipt" → Preview GST-compliant receipt
6. Confirm → Transaction saved to `fee_transactions` table (INSERT only, NO DELETE)
7. Receipt PDF generated with unique sequential number + QR code
8. SMS sent to parent with payment confirmation
9. End of Day: Cashier runs "EOD Settlement" → Counts physical cash → Matches with system total
10. Discrepancy? → Must enter reason → Supervisor approval required
```

### Flow 3: Exam Recalculation After Question Deletion
```
1. Admin notices wrong question in "Test XYZ" → Opens "Question Bank"
2. Finds question → Clicks "Edit" → Marks as "INVALID/BONUS" OR deletes
3. System triggers background job: `recalculate_exam_scores(test_id)`
4. Job iterates through all student attempts:
   - If marked BONUS: Add full marks to everyone
   - If deleted: Remove from total marks, recalculate percentage
5. Updates materialized view `exam_leaderboard_view`
6. Notifies affected students: "Your score has been revised"
7. Logs entry in `exam_recalculation_log`: {test_id, changed_by, timestamp, affected_count, old_avg, new_avg}
8. Leaderboard automatically refreshes with new ranks
```

---

## 5. Component Library Specifications

### 5.1 Core Components (Atomic Design)
| Component | Variants | Props | Usage |
|-----------|----------|-------|-------|
| **Button** | Primary, Secondary, Danger, Ghost | size(sm/md/lg), loading, disabled, icon | All CTAs |
| **Input** | Text, Number, Date, File | label, placeholder, error, required, mask | Forms |
| **Card** | Default, Hoverable, Collapsible | title, subtitle, actions, padding | Containers |
| **Table** | Sortable, Paginated, Selectable | columns, data, onRowClick, bulkActions | Data lists |
| **Modal** | Confirmation, Form, Alert | title, content, footer, onClose | Overlays |
| **Badge** | Success, Warning, Error, Info | variant, children | Status indicators |
| **Avatar** | Circle, Square, Group | src, alt, size, fallback | User profiles |
| **Calendar** | Month, Week, Day, Agenda | events, onDateClick, viewMode | Scheduling |

### 5.2 Complex Components
| Component | Description | Dependencies |
|-----------|-------------|--------------|
| **QR Scanner** | Camera feed + QR detection | react-qr-reader, expo-camera |
| **Signature Pad** | Canvas for digital signatures | react-signature-canvas |
| **Rich Text Editor** | WYSIWYG for assignments/notices | TipTap or Quill |
| **Chart Suite** | Line, Bar, Pie, Spider charts | Recharts or Chart.js |
| **Drag-Drop Calendar** | Timetable scheduling | react-big-calendar + dnd-kit |
| **File Uploader** | Multi-file with progress | react-dropzone |
| **Data Grid** | Advanced table with filters | AG Grid or TanStack Table |

---

## 6. Responsive Design Rules

### 6.1 Breakpoints
```css
/* Mobile First Approach */
--bp-mobile: 320px;    /* Minimum */
--bp-tablet: 768px;    /* Tablet portrait */
--bp-desktop: 1024px;  /* Laptop */
--bp-large: 1440px;    /* Desktop large */
```

### 6.2 Adaptive Layout Patterns
| Element | Mobile (<768px) | Tablet (768-1024px) | Desktop (>1024px) |
|---------|-----------------|---------------------|-------------------|
| **Navigation** | Bottom tab bar (5 items) + Hamburger | Left sidebar (collapsed) | Left sidebar (expanded) |
| **Dashboard Cards** | 1 column | 2 columns | 4 columns |
| **Tables** | Horizontal scroll + Card view on tap | Horizontal scroll | Full width with sticky header |
| **Forms** | Single column | 2 columns | 2-3 columns based on complexity |
| **Modals** | Full screen | 80% width | 500px max-width centered |
| **Charts** | Stacked vertical | Side-by-side horizontal | Interactive tooltips |

### 6.3 Touch Targets
- **Minimum Button Size**: 44x44px (iOS guideline)
- **Icon Buttons**: 48x48px touch area with 24px icon
- **Form Inputs**: 48px height minimum
- **Table Row Height**: 56px for easy tapping

---

## 7. Accessibility Standards (WCAG 2.1 AA)

### 7.1 Color Contrast
- **Normal Text**: Minimum 4.5:1 ratio
- **Large Text**: Minimum 3:1 ratio
- **UI Components**: Minimum 3:1 ratio against adjacent colors

### 7.2 Keyboard Navigation
- All interactive elements must be focusable (Tab key)
- Visible focus indicators (2px outline)
- Skip to main content link on every page
- Modal traps focus until closed

### 7.3 Screen Reader Support
- All images have alt text
- Form inputs have associated labels
- ARIA landmarks for regions (banner, navigation, main, contentinfo)
- Dynamic content changes announced (live regions)

### 7.4 Language Support
- **Default**: English
- **Phase 2**: Hindi, Marathi, Tamil (i18n ready structure)
- Date formats: DD/MM/YYYY (Indian standard)
- Currency: ₹ INR with comma separators (₹1,23,456)

---

## 8. Prototype Links (To Be Created in Figma)

### 8.1 Figma File Structure
```
📁 EduCore ERP - Phase 1
├── 🎨 Design System
│   ├── Colors
│   ├── Typography
│   ├── Components (Atoms, Molecules, Organisms)
│   └── Icons (24x24, 16x16 sets)
├── 👤 Admin Flows
│   ├── Dashboard
│   ├── Admissions
│   ├── Finance
│   └── Reports
├── 👨‍🏫 Faculty Flows
│   ├── Attendance Marking
│   ├── LMS Upload
│   └── Grading
├── 👨‍🎓 Student Flows
│   ├── View Schedule
│   ├── Submit Assignment
│   └── Check Results
├── 👪 Parent Flows
│   ├── Child Overview
│   └── Fee Payment
└── 📱 Mobile Screens (All roles)
```

### 8.2 Prototype Priority Order
1. **Authentication Flow** (Login → Dashboard)
2. **QR Attendance Flow** (Teacher generates → Student scans)
3. **Fee Payment Flow** (Search → Pay → Receipt)
4. **Exam Creation Flow** (Question bank → Test → Publish)
5. **Result Moderation Flow** (Draft → Grace marks → Publish)

---

## 9. Handoff to Development Team

### 9.1 Deliverables Checklist
- [ ] Figma file with all 52 screens
- [ ] Interactive prototypes for 5 key flows
- [ ] Design system published as Storybook
- [ ] Asset export (SVG icons, illustrations)
- [ ] Redlines for spacing/padding
- [ ] Animation specs (timing, easing curves)

### 9.2 Developer Tools Integration
- **Storybook**: Component documentation
- **Zeplin/Figma Dev Mode**: CSS snippets, asset download
- **Lighthouse**: Accessibility auditing
- **Chromatic**: Visual regression testing

### 9.3 Version Control for Design
- Figma version history for major iterations
- Branch naming: `feature/screen-name` (mirrors Git)
- Weekly design-dev sync meetings

---

## 10. Success Metrics for UI/UX

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Task Completion Rate** | >90% | User testing sessions |
| **Time-on-Task** | <2 min for attendance | Analytics tracking |
| **Error Rate** | <5% | Form validation failures |
| **SUS Score** | >80 (Excellent) | Post-launch survey |
| **Mobile Adoption** | >75% of students | App analytics |
| **Accessibility Score** | >95 (Lighthouse) | Automated audits |

---

## Appendix A: Screen Mockup Descriptions (Text-Based Wireframes)

### Screen D1: Super Admin Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  [Logo] EduCore ERP              [User Avatar] ▼           │
├─────────────┬───────────────────────────────────────────────┤
│ 📊 Dashboard│  Welcome back, Admin!                         │
│ 📝 Admissions│                                               │
│ 📚 Academics│  ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│ 📝 Exams    │  │ Total   │ │ Fees    │ │ Attend- │         │
│ 💰 Finance  │  │Students │ │ Today   │ │ ance %  │         │
│ 📈 Reports  │  │ 1,245   │ │ ₹85,400 │ │ 94.2%   │         │
│ 👥 Users    │  │ +12     │ │ +8%     │ │ -2.1%   │         │
│ ⚙️ Settings │  └─────────┘ └─────────┘ └─────────┘         │
│             │                                               │
│             │  📅 Today's Schedule                          │
│             │  ┌───────────────────────────────────────┐   │
│             │  │ 09:00 - B.Sc Physics - Prof. Sharma   │   │
│             │  │ 10:30 - B.Com Math  - Prof. Patel     │   │
│             │  │ 14:00 - M.Sc Chem   - Prof. Kumar     │   │
│             │  └───────────────────────────────────────┘   │
│             │                                               │
│             │  ⚠️ Pending Approvals (3)                     │
│             │  • Fee reversal request - Roll 2024-001      │
│             │  • Leave application - Prof. Singh            │
│             │  • New batch creation - MBA 2025              │
│             │                                               │
│             │  [View All]                                   │
└─────────────┴───────────────────────────────────────────────┘
```

### Screen AT1: Generate Dynamic QR (Teacher)
```
┌─────────────────────────────────────────────────────────────┐
│  ← Back          Mark Attendance                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Batch: B.Sc Computer Science (Sem 3)                      │
│  Subject: Data Structures                                   │
│  Date: 15 Oct 2024                                          │
│  Time: 10:00 AM - 11:30 AM                                 │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │              ████  ██  ████  ██                    │   │
│  │              █  █  ██  █  █  ██                    │   │
│  │              ████  ██  ████  ██   (QR Code)        │   │
│  │              █  █      █  █                        │   │
│  │              ████      ████                        │   │
│  │                                                     │   │
│  │         Valid for: 00:23 seconds                   │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  👥 Students Present: 42/60                                │
│                                                             │
│  [Refresh QR]     [End Session]     [Export to CSV]        │
│                                                             │
│  ℹ️ Tips: Ensure projector is bright. QR refreshes         │
│     every 30 seconds to prevent screenshots.                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Screen EX3: CBT Exam Interface (NTA Style)
```
┌─────────────────────────────────────────────────────────────┐
│  JEE Mock Test - Physics          ⏱ 02:45:33    [Submit]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Question 17 of 75                              [+4, -1]   │
│                                                             │
│  A particle moves in a circular path of radius R with      │
│  constant speed v. The magnitude of average acceleration   │
│  over half a revolution is:                                │
│                                                             │
│  ○ (A) v²/R                                                │
│  ● (B) 2v²/πR   ← Selected                                 │
│  ○ (C) v²/2R                                               │
│  ○ (D) Zero                                                │
│                                                             │
│  [Mark for Review]  [Clear Response]  [Save & Next →]     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Question Palette:                                          │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐               │
│  │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │10 │ ...           │
│  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤               │
│  │🟢 │🟢 │🔴 │🟡 │⚪ │🟢 │🔴 │⚪ │🟡 │🟢 │                 │
│  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘               │
│  🟢 Answered  🔴 Marked for Review  ⚪ Not Visited         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Document Status**: ✅ Complete  
**Next Step**: Create Figma prototypes based on these specifications  
**Approval Required**: Before development begins, UI/UX lead must sign off on wireframes
