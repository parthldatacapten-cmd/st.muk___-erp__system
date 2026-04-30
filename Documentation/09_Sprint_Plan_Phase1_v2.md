# Sprint Planning Document: Phase 1 (Sprints 1-8)

**Document ID:** SPRINT-PLAN-001  
**Version:** 2.0 (Updated with LMS, Assessment & Smart Attendance)  
**Date:** May 2024  
**Product:** EduCore ERP - Multi-Tenant Indian Education Platform  

---

## 1. Sprint Overview

| Sprint | Duration | Focus Area | Key Deliverables |
|--------|----------|------------|------------------|
| **Sprint 1** | Weeks 1-2 | Foundation & Setup | Multi-tenancy architecture, Institution branding, User auth |
| **Sprint 2** | Weeks 3-4 | Admission & Fees | Digital admission forms, Fee structures, Payment gateway |
| **Sprint 3** | Weeks 5-6 | Smart Attendance | NFC attendance, QR Code scanning, Geo-fencing |
| **Sprint 4** | Weeks 7-8 | LMS Core | Resource library, Video upload/transcoding, Drip content |
| **Sprint 5** | Weeks 9-10 | Live Classes & Doubts | Zoom/Meet integration, Doubt forum, Assignments |
| **Sprint 6** | Weeks 11-12 | Assessment Engine | Question bank, NTA CBT interface, Test creation |
| **Sprint 7** | Weeks 13-14 | Results & Analytics | Auto-grading, Leaderboards, Performance charts |
| **Sprint 8** | Weeks 15-16 | Security & Polish | Watermarking, Concurrent login, Load testing, Bug fixes |

---

## 2. Detailed Sprint Breakdown

### **Sprint 1: Foundation & Multi-Tenancy (Weeks 1-2)**

**Goal:** Establish scalable architecture supporting multiple institutions with custom branding.

#### User Stories:
1. **US-1.1:** As an Admin, I want to register my institution so that I can configure branding (logo, colors, name).
   - *Tasks:* DB schema for tenants, Logo upload API, Theme customization endpoint.
   - *Points:* 5

2. **US-1.2:** As a User, I want to log in via email/password or OTP so that I can access the system securely.
   - *Tasks:* JWT authentication, OTP service integration (Firebase/Twilio), Role-based middleware.
   - *Points:* 8

3. **US-1.3:** As a Super Admin, I want to create roles (Principal, Teacher, Student, Parent) with permissions so that data access is controlled.
   - *Tasks:* RBAC schema, Permission matrix UI, Middleware for API protection.
   - *Points:* 5

4. **US-1.4:** As a Developer, I want CI/CD pipelines set up so that deployments are automated.
   - *Tasks:* GitHub Actions setup, Docker containerization, Staging environment config.
   - *Points:* 3

**Sprint Goal Completion Criteria:**
- ✅ New institution can onboard and customize branding in <10 minutes.
- ✅ Login works with both password and OTP.
- ✅ 4 distinct roles created with isolated dashboards.

---

### **Sprint 2: Admission & Fee Management (Weeks 3-4)**

**Goal:** Enable digital admissions and fee collection with payment gateway integration.

#### User Stories:
1. **US-2.1:** As an Admin, I want to create customizable admission forms so that I can collect student data.
   - *Tasks:* Form builder UI, Dynamic field validation, Document upload (Aadhar, marksheets).
   - *Points:* 8

2. **US-2.2:** As a Parent, I want to fill admission form online and pay application fee so that I don't need to visit campus.
   - *Tasks:* Public form endpoint, Razorpay/PayU integration, Receipt generation.
   - *Points:* 13

3. **US-2.3:** As an Admin, I want to define fee structures (installments, scholarships) so that billing is flexible.
   - *Tasks:* Fee schema (one-time, recurring, installment), Scholarship/discount logic.
   - *Points:* 8

4. **US-2.4:** As an Accountant, I want to generate GST-compliant receipts automatically so that accounting is simplified.
   - *Tasks:* PDF receipt template, GST calculation logic, Email/SMS delivery.
   - *Points:* 5

5. **US-2.5:** As an Admin, I want to track defaulters and send reminders so that fee collection improves.
   - *Tasks:* Defaulter list query, SMS/WhatsApp API integration (MSG91/Interakt).
   - *Points:* 5

**Sprint Goal Completion Criteria:**
- ✅ End-to-end admission flow tested with 10 dummy students.
- ✅ Payment gateway successful + failed transaction handling.
- ✅ Fee receipts downloadable with institution logo.

---

### **Sprint 3: Smart Attendance (NFC & QR) (Weeks 5-6)**

**Goal:** Implement next-gen attendance systems eliminating hardware dependency.

#### User Stories:
1. **US-3.1:** As a Teacher, I want to mark attendance via NFC tap so that it's fast and contactless.
   - *Tasks:* Android HCE implementation, NFC payload encryption, Tap detection logic.
   - *Points:* 13

2. **US-3.2:** As a Teacher, I want to display a dynamic QR code on projector so that students can scan from seats.
   - *Tasks:* QR generation API (TOTP-based), Real-time refresh (10s), Teacher dashboard widget.
   - *Points:* 8

3. **US-3.3:** As a Student, I want to scan QR and have my GPS validated so that proxy attendance is prevented.
   - *Tasks:* Mobile app QR scanner, GPS coordinate capture, Geo-fence validation logic.
   - *Points:* 8

4. **US-3.4:** As an Admin, I want to see real-time attendance count so that I know class strength instantly.
   - *Tasks:* WebSocket for live updates, Dashboard counter component, Absent alert trigger.
   - *Points:* 5

5. **US-3.5:** As a System, I want to detect expired QR codes so that late scans are rejected.
   - *Tasks:* TOTP validation, Timestamp comparison, Rejection response handler.
   - *Points:* 3

**Sprint Goal Completion Criteria:**
- ✅ NFC tap marks attendance in <2 seconds.
- ✅ QR code expires after 2 minutes; late scans rejected.
- ✅ Geo-fencing prevents attendance from outside classroom (tested with mock locations).

---

### **Sprint 4: LMS Core - Resources & Video (Weeks 7-8)**

**Goal:** Build centralized learning repository with video streaming capabilities.

#### User Stories:
1. **US-4.1:** As a Teacher, I want to upload PDFs/PPTs organized by chapter so that students can access notes.
   - *Tasks:* File upload API (50MB limit), Folder structure (Board→Class→Subject→Chapter), Preview renderer.
   - *Points:* 8

2. **US-4.2:** As a Teacher, I want to upload videos that are auto-transcoded so that students with slow internet can watch.
   - *Tasks:* Video upload (2GB), FFmpeg transcoding pipeline (360p/480p/720p/1080p), HLS stream generation.
   - *Points:* 13

3. **US-4.3:** As a Student, I want video quality to adjust automatically based on my internet speed so that playback is smooth.
   - *Tasks:* HLS player integration, Bandwidth detection, Adaptive bitrate switching.
   - *Points:* 8

4. **US-4.4:** As an Admin, I want to schedule content release (drip) so that students follow a structured pace.
   - *Tasks:* Unlock date field per chapter, Cron job for daily unlock check, "Locked" UI state.
   - *Points:* 5

5. **US-4.5:** As a Student, I want to resume video from where I left off so that I don't waste time seeking.
   - *Tasks:* Progress tracking API, Local storage of last timestamp, Auto-seek on load.
   - *Points:* 3

**Sprint Goal Completion Criteria:**
- ✅ Video uploads process within 5 minutes for 1GB file.
- ✅ Adaptive streaming works on 3G/4G/WiFi networks.
- ✅ Drip content unlocks exactly at 12:00 AM IST.

---

### **Sprint 5: Live Classes & Doubt Forum (Weeks 9-10)**

**Goal:** Enable synchronous learning and asynchronous doubt resolution.

#### User Stories:
1. **US-5.1:** As a Teacher, I want to schedule a Zoom class from the app so that links are auto-shared.
   - *Tasks:* Zoom API integration, Meeting creation endpoint, Auto-email/SMS to students.
   - *Points:* 8

2. **US-5.2:** As a Teacher, I want to start a native WebRTC class so that students join without external links.
   - *Tasks:* WebRTC signaling server, Video room creation, Participant management.
   - *Points:* 13

3. **US-5.3:** As a Student, I want to post doubts with images/equations so that teachers understand my problem.
   - *Tasks:* Rich text editor, Image upload, LaTeX rendering (MathJax), Tagging system.
   - *Points:* 8

4. **US-5.4:** As a Teacher, I want to reply to doubts with annotated images so that explanations are clear.
   - *Tasks:* Image annotation tool (draw/text), Reply threading, Notification system.
   - *Points:* 5

5. **US-5.5:** As a Student, I want to submit homework digitally with a deadline so that I don't lose physical copies.
   - *Tasks:* Assignment creation UI, Submission endpoint, Late flag logic, Grading interface.
   - *Points:* 8

**Sprint Goal Completion Criteria:**
- ✅ Zoom meeting links generated and pushed to 100 students in <30 seconds.
- ✅ WebRTC call supports 50 concurrent users with <500ms latency.
- ✅ LaTeX equations render correctly in doubt posts.

---

### **Sprint 6: Assessment Engine - Question Bank & CBT (Weeks 11-12)**

**Goal:** Build professional test-taking experience matching JEE/NEET standards.

#### User Stories:
1. **US-6.1:** As a Teacher, I want to create questions with LaTeX and images so that math/science problems are accurate.
   - *Tasks:* Question editor with LaTeX support, Image upload, Difficulty tagging.
   - *Points:* 8

2. **US-6.2:** As a Student, I want to take a test with NTA-style interface so that I'm familiar with actual exam UI.
   - *Tasks:* CBT frontend (question palette, color codes), Timer sync, Save & Next logic.
   - *Points:* 13

3. **US-6.3:** As an Admin, I want to configure marking schemes (+4/-1, partial marks) so that different exam patterns are supported.
   - *Tasks:* Marking scheme schema, Scoring engine, Partial mark logic for multi-correct.
   - *Points:* 8

4. **US-6.4:** As a Student, I want section-wise timers so that I practice time management per subject.
   - *Tasks:* Section timer component, Auto-lock on expiry, Warning alerts.
   - *Points:* 5

5. **US-6.5:** As a Teacher, I want to bulk import questions via Excel so that I don't enter manually.
   - *Tasks:* CSV/Excel parser, Validation rules, Error reporting, Bulk insert API.
   - *Points:* 5

**Sprint Goal Completion Criteria:**
- ✅ CBT interface passes visual comparison with actual JEE Main screenshot (95% similarity).
- ✅ 500 students can take test simultaneously with <200ms latency.
- ✅ Partial marking calculates correctly for multi-correct MCQs.

---

### **Sprint 7: Results, Leaderboards & Analytics (Weeks 13-14)**

**Goal:** Provide instant results and deep performance insights.

#### User Stories:
1. **US-7.1:** As a Student, I want to see my result immediately after submission so that I know my performance.
   - *Tasks:* Auto-grading engine, Score calculation, Rank generation (AIR/Institute).
   - *Points:* 8

2. **US-7.2:** As a Student, I want to see my rank on leaderboard so that I'm motivated to improve.
   - *Tasks:* Leaderboard query (Top 100), Privacy filter, Real-time ranking updates.
   - *Points:* 5

3. **US-7.3:** As a Student, I want to see spider charts of my strengths/weaknesses so that I know what to revise.
   - *Tasks:* Radar chart component (Chart.js), Topic-wise accuracy calculation, Weak topic identification.
   - *Points:* 8

4. **US-7.4:** As a Parent, I want to receive SMS with my child's rank so that I'm informed instantly.
   - *Tasks:* Result-triggered SMS webhook, Template customization, MSG91 integration.
   - *Points:* 3

5. **US-7.5:** As a Student, I want to compare my performance with toppers so that I understand gaps.
   - *Tasks:* Comparative analytics (time spent, accuracy), Top 10% benchmark data.
   - *Points:* 5

**Sprint Goal Completion Criteria:**
- ✅ Results generated within 5 seconds of test submission.
- ✅ Spider charts accurately reflect topic-wise performance.
- ✅ SMS delivered to parents within 10 seconds of result declaration.

---

### **Sprint 8: Security, Anti-Piracy & Polish (Weeks 15-16)**

**Goal:** Secure content and prepare for production launch.

#### User Stories:
1. **US-8.1:** As an Admin, I want dynamic watermarks on PDFs so that students don't share screenshots.
   - *Tasks:* PDF overlay renderer (Name+Phone+Timestamp), Random position algorithm, Canvas obfuscation.
   - *Points:* 8

2. **US-8.2:** As an Admin, I want to prevent concurrent logins so that accounts aren't shared.
   - *Tasks:* Session tracking (Redis), Auto-logout on new login, Device info logging.
   - *Points:* 5

3. **US-8.3:** As a Student, I want invisible watermarks on videos so that piracy is traceable.
   - *Tasks:* Forensic watermarking library, User ID embedding, Extraction tool for admin.
   - *Points:* 8

4. **US-8.4:** As a QA Engineer, I want load testing completed so that system handles 5000 concurrent users.
   - *Tasks:* JMeter/Gatling scripts, Performance bottleneck identification, Database indexing optimization.
   - *Points:* 8

5. **US-8.5:** As a User, I want bug fixes and UI polish so that the app feels professional.
   - *Tasks:* Bug bash session, UI consistency audit, Error message improvements.
   - *Points:* 5

**Sprint Goal Completion Criteria:**
- ✅ Screenshots of PDFs clearly show user-specific watermarks.
- ✅ Sharing login results in immediate logout of first device (tested with 2 devices).
- ✅ System sustains 5000 concurrent users with <1% error rate.

---

## 3. Velocity Tracking

| Sprint | Planned Points | Committed Points | Actual Points | Status |
|--------|---------------|------------------|---------------|--------|
| 1 | 21 | 21 | TBD | In Progress |
| 2 | 39 | 39 | TBD | Planned |
| 3 | 37 | 37 | TBD | Planned |
| 4 | 37 | 37 | TBD | Planned |
| 5 | 42 | 42 | TBD | Planned |
| 6 | 39 | 39 | TBD | Planned |
| 7 | 29 | 29 | TBD | Planned |
| 8 | 34 | 34 | TBD | Planned |

**Total Story Points:** 278 points  
**Team Velocity Assumption:** 35 points/sprint (4 developers, 2 weeks)  
**Buffer:** 10% contingency included in estimates

---

## 4. Risk Management

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| NFC not working on iOS | High | Medium | Fallback to QR mode; iOS limited to scanner role only |
| Video transcoding too slow | Medium | High | Use cloud transcoding service (AWS MediaConvert) instead of self-hosted FFmpeg |
| Geo-fencing false positives | Medium | Medium | Increase GPS accuracy threshold to 50m; allow manual override by teacher |
| Payment gateway downtime | Low | High | Support multiple gateways (Razorpay + PayU); retry logic with failover |
| NTA interface patent issues | Low | High | Design UI similar but not identical; consult legal team |
| Watermark impacts UX | Medium | Low | Make watermark semi-transparent (opacity 15%); move every 10s |

---

## 5. Definition of Done (DoD)

For a user story to be considered complete:
1. ✅ Code reviewed and merged to main branch.
2. ✅ Unit tests written with >80% coverage.
3. ✅ Integration tests passed for critical paths.
4. ✅ UI/UX matches Figma designs.
5. ✅ Tested on Chrome, Firefox, Safari, and mobile browsers.
6. ✅ No critical/high severity bugs open.
7. ✅ Documentation updated (API docs, user manuals).
8. ✅ Deployed to staging environment and verified by Product Owner.

---

## 6. Tools & Technology Stack

- **Frontend:** React.js (Web), React Native (Mobile)
- **Backend:** Node.js (Express) / Python (FastAPI)
- **Database:** PostgreSQL (Relational), MongoDB (Question Bank, Logs)
- **Cache:** Redis (Sessions, Leaderboards)
- **Video:** AWS S3 + CloudFront (HLS streaming), FFmpeg (Transcoding)
- **Real-time:** Socket.io (WebSocket)
- **CI/CD:** GitHub Actions, Docker, Kubernetes
- **Testing:** Jest (Unit), Cypress (E2E), JMeter (Load)
- **Monitoring:** Prometheus + Grafana, Sentry (Error tracking)

---

## 7. Sprint Ceremonies

- **Sprint Planning:** Day 1 of each sprint (2 hours)
- **Daily Standup:** Every day at 10 AM IST (15 mins)
- **Sprint Review:** Last day of sprint (1 hour) - Demo to stakeholders
- **Sprint Retrospective:** After review (45 mins) - Continuous improvement
- **Backlog Refinement:** Mid-sprint (1 hour) - Prepare for next sprint

---

## 8. Success Metrics for Phase 1

1. **Adoption:** 20 coaching centers onboarded and actively using.
2. **Engagement:** >70% daily active users (students watching videos/taking tests).
3. **Performance:** <2 second page load time, <200ms API response time.
4. **Security:** Zero data breaches, zero successful piracy incidents.
5. **Revenue:** ₹10 Lakhs MRR achieved from subscription fees.
