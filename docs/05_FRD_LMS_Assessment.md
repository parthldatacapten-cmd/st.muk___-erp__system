# Functional Requirements Document: LMS & Advanced Assessment Engine

**Document ID:** FRD-LMS-001  
**Version:** 1.0  
**Date:** May 2024  
**Product:** EduCore ERP (Multi-Tenant Indian Education Platform)  
**Priority:** CRITICAL (Phase 1 - Coaching Center Focus)  

---

## 1. Executive Summary

This document details the functional requirements for the **Learning Management System (LMS)** and **Advanced Assessment Engine**, specifically designed to support coaching centers preparing students for competitive exams (JEE, NEET, CUET) while remaining flexible enough for schools and colleges.

### Key Innovations
- **NTA-Style CBT Interface:** Exact replica of JEE/NEET computer-based test interface.
- **Drip Content Delivery:** Scheduled unlocking of study material.
- **Advanced Anti-Piracy:** Dynamic watermarking and concurrent login restrictions.
- **Hybrid Attendance:** NFC and QR-based attendance systems.

---

## 2. Learning Management System (LMS) Module

### 2.1 Resource Library
**Description:** Centralized vault for teachers to upload and manage study materials.

**Functional Requirements:**
- **FR-LMS-01:** System shall allow teachers to upload PDFs, PPTs, DOCX, and image files up to 50MB per file.
- **FR-LMS-02:** System shall organize resources by Board ➔ Class ➔ Subject ➔ Chapter ➔ Topic.
- **FR-LMS-03:** System shall provide a preview mode for PDFs and images without downloading.
- **FR-LMS-04:** System shall allow admins to set access permissions (e.g., "Visible only after fee payment").
- **FR-LMS-05:** System shall support bulk upload via ZIP files with auto-extraction to correct folders.

### 2.2 Video Lecture Platform
**Description:** Hosting and streaming of recorded video classes.

**Functional Requirements:**
- **FR-LMS-06:** System shall support video uploads up to 2GB with automatic transcoding to 360p, 480p, 720p, and 1080p.
- **FR-LMS-07:** Player shall implement **Adaptive Bitrate Streaming (HLS)**, automatically adjusting quality based on student's internet speed.
- **FR-LMS-08:** Player shall include playback speed controls (0.5x, 1.0x, 1.5x, 2.0x).
- **FR-LMS-09:** System shall track video watch progress (e.g., "45% completed") and resume from last position.
- **FR-LMS-10:** System shall prevent downloading of video files directly (streaming only).

### 2.3 Drip Content System
**Description:** Time-based release of study material to prevent binge-watching and ensure structured learning.

**Functional Requirements:**
- **FR-LMS-11:** Admin shall be able to set "Unlock Dates" for specific chapters or batches.
- **FR-LMS-12:** System shall automatically unlock content at 12:00 AM IST on the scheduled date.
- **FR-LMS-13:** System shall support dependency rules (e.g., "Chapter 2 unlocks only if Chapter 1 quiz score > 50%").
- **FR-LMS-14:** Students shall see a "Locked" icon with an expected unlock date for future content.

### 2.4 Live Classes Integration
**Description:** Seamless integration with third-party meeting tools and native WebRTC.

**Functional Requirements:**
- **FR-LMS-15:** System shall integrate with **Zoom API** to auto-generate meeting links and push notifications to students.
- **FR-LMS-16:** System shall integrate with **Google Meet** via calendar invites.
- **FR-LMS-17:** System shall offer a **Native WebRTC** option for low-latency streaming within the app (no external link required).
- **FR-LMS-18:** Live class recordings shall be automatically saved to the Resource Library post-session.
- **FR-LMS-19:** System shall support "Waiting Room" functionality for live classes.

### 2.5 Doubt Resolution Forum
**Description:** Interactive Q&A platform for students and teachers.

**Functional Requirements:**
- **FR-LMS-20:** Students shall be able to post questions with text, images (for math/physics diagrams), and LaTeX equations.
- **FR-LMS-21:** System shall tag questions by Subject and Topic automatically using AI keywords.
- **FR-LMS-22:** Teachers shall be able to reply with text, annotated images, or short video clips.
- **FR-LMS-23:** System shall upvote useful answers; top-voted answers appear first.
- **FR-LMS-24:** "Resolved" status can only be marked by the question asker or assigned teacher.
- **FR-LMS-25:** Private doubts: Option for students to mark a doubt as "Private" (visible only to them and teachers).

### 2.6 Assignments & Homework
**Description:** Digital submission and grading workflow.

**Functional Requirements:**
- **FR-LMS-26:** Teachers shall create assignments with due dates, instructions, and attached reference files.
- **FR-LMS-27:** Students shall submit assignments as PDF, images, or text input.
- **FR-LMS-28:** Late submissions shall be flagged automatically; configurable penalty rules (e.g., -10% marks per day).
- **FR-LMS-29:** Teachers shall grade submissions with rubrics, comments, and annotated markups on PDFs.
- **FR-LMS-30:** Graded assignments shall be instantly visible to students with feedback.

---

## 3. Advanced Assessment & Mock Test Engine

### 3.1 Question Bank Vault
**Description:** Massive repository of questions with advanced categorization.

**Functional Requirements:**
- **FR-ASSESS-01:** System shall store unlimited questions categorized by: Subject, Topic, Sub-Topic, Difficulty (Easy/Medium/Hard), and Exam Type (JEE/NEET/Board).
- **FR-ASSESS-02:** Editor shall support **LaTeX** for mathematical equations and chemical formulas.
- **FR-ASSESS-03:** System shall support multiple question types: Single Correct MCQ, Multiple Correct MCQ, Integer Type, Numerical Value, Match the Column, and Subjective.
- **FR-ASSESS-04:** Teachers shall upload images/diagrams for questions (e.g., geometry, physics circuits).
- **FR-ASSESS-05:** Bulk import via Excel/CSV with specific templates for question migration.

### 3.2 NTA-Style CBT Interface (Computer Based Test)
**Description:** Exact replica of the National Testing Agency interface used in JEE/NEET to familiarize students.

**Functional Requirements:**
- **FR-ASSESS-06:** Interface shall display a **Question Palette** on the right with color codes:
  - Green: Answered
  - Red: Not Answered
  - Yellow: Marked for Review
  - Purple: Answered & Marked for Review
  - White: Not Visited
- **FR-ASSESS-07:** Timer shall be displayed prominently at the top-right, synchronized with server time.
- **FR-ASSESS-08:** "Save & Next" button must be mandatory to move forward; direct jumping allowed but requires save confirmation.
- **FR-ASSESS-09:** Section-wise timing support (e.g., Physics 60 mins, Chemistry 60 mins) with auto-lock after time expires.
- **FR-ASSESS-10:** Full-screen mode enforcement to prevent tab switching (with warning logs).

### 3.3 Custom Marking Schemes
**Description:** Flexible scoring logic for various exam patterns.

**Functional Requirements:**
- **FR-ASSESS-11:** Admin shall configure marking schemes per test:
  - Correct: +4
  - Incorrect: -1
  - Unattempted: 0
  - Partial Marks: Configurable for "Multiple Correct" types (e.g., +2 if 2 out of 3 correct options selected).
- **FR-ASSESS-12:** System shall support negative marking toggles (On/Off per section).
- **FR-ASSESS-13:** Normalization support for multiple shifts (using percentile method).

### 3.4 Subjective Exam Support
**Description:** Digital handling of descriptive answer sheets.

**Functional Requirements:**
- **FR-ASSESS-14:** Students shall upload photos/PDFs of handwritten answer sheets within a time window post-exam.
- **FR-ASSESS-15:** Teacher interface shall display uploaded images side-by-side with a scoring panel.
- **FR-ASSESS-16:** Teachers shall annotate directly on images (draw circles, underline, add text comments).
- **FR-ASSESS-17:** Question-wise breakup of marks for subjective answers.

### 3.5 Automated Results & Leaderboards
**Description:** Instant result processing and ranking.

**Functional Requirements:**
- **FR-ASSESS-18:** System shall generate results within 5 seconds of test submission for objective tests.
- **FR-ASSESS-19:** Metrics calculated: Total Score, Percentile, All-India Rank (AIR), Institute Rank, Subject-wise ranks.
- **FR-ASSESS-20:** Leaderboard shall display Top 100 students publicly (configurable privacy settings).
- **FR-ASSESS-21:** SMS/WhatsApp alerts to parents with rank and score immediately upon result declaration.

### 3.6 Performance Analytics
**Description:** Deep insights into student performance.

**Functional Requirements:**
- **FR-ASSESS-22:** **Spider/Radar Charts** showing strength across topics (e.g., High in Algebra, Low in Calculus).
- **FR-ASSESS-23:** Time analysis: Average time spent per question vs. toppers' average.
- **FR-ASSESS-24:** Accuracy trends: Graph showing accuracy % over last 10 tests.
- **FR-ASSESS-25:** "Weak Topics" recommendation engine suggesting specific chapters to revise.
- **FR-ASSESS-26:** Comparative analysis: Student's performance vs. Class Average vs. Top 10% Average.

---

## 4. Security & Anti-Piracy Features

### 4.1 Dynamic Watermarking
**FR-SEC-01:** All PDF notes viewed in-app shall have a dynamic overlay watermark containing:
- Student Name
- Mobile Number
- Timestamp
- IP Address
*(Watermark moves randomly every 10 seconds to prevent cropping)*

**FR-SEC-02:** Video player shall embed invisible forensic watermarks linking the stream to the user ID.

**FR-SEC-03:** Screenshots taken on mobile devices shall trigger a warning or blur the screen (OS permitting).

### 4.2 Concurrent Login Restriction
**FR-SEC-04:** System shall allow only **one active session** per student account.
**FR-SEC-05:** If a login occurs from a new device, the older session shall be terminated immediately with a notification: *"You logged in from another device."*
**FR-SEC-06:** Admin dashboard shall show active device details (Device Model, IP, Location, Last Active).

### 4.3 Data Protection
**FR-SEC-07:** Database encryption at rest (AES-256) for all student data and payment info.
**FR-SEC-08:** Automated daily incremental backups and weekly full backups to off-site storage.
**FR-SEC-09:** Role-Based Access Control (RBAC) ensuring teachers cannot access financial data or modify grades after submission deadline.

---

## 5. Technical Architecture Notes

- **Video Streaming:** Use HLS (HTTP Live Streaming) with CDN integration (Cloudflare/AWS CloudFront).
- **LaTeX Rendering:** MathJax or KaTeX libraries for client-side rendering.
- **Real-time Communication:** WebSocket for live doubt forums and chat.
- **Storage:** Object storage (AWS S3 / MinIO for self-hosted) for media files.
- **Database:** PostgreSQL for relational data; MongoDB for question banks and logs.

---

## 6. Acceptance Criteria

1. **Load Test:** System must support 5,000 concurrent users taking a mock test simultaneously without latency > 200ms.
2. **Video Playback:** Video must start within 2 seconds on 4G networks.
3. **Security:** Attempting to share a login must result in immediate logout of the first device.
4. **UI Fidelity:** NTA Interface must pass a visual comparison test against actual JEE Main interface with 95% similarity.
5. **Watermark:** Screenshots of PDFs must clearly show user-specific details.

---

## 7. Out of Scope (For Phase 1)
- AI-based auto-grading of subjective answers.
- VR/AR content delivery.
- Offline mode for video lectures (DRM complexity).
