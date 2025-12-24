# PVGS Academic & Administrative System

This repository contains the complete documentation set for the PVGS (PVG's College of Science & Commerce) Academic & Administrative System, an ERP solution designed to manage academic, administrative, and compliance processes for the institution.

## Documentation Overview

The `docs/` folder contains professional documentation extracted from the comprehensive system specification:

- **[PRD_Product_Requirements_Document.md](docs/PRD_Product_Requirements_Document.md)** - Product Requirements Document outlining objectives, scope, stakeholders, and success metrics.
- **[FRD_Roles_Permissions.md](docs/FRD_Roles_Permissions.md)** - Functional Requirements for Roles & Permissions module (RBAC).
- **[FRD_Student_Admission_Profile.md](docs/FRD_Student_Admission_Profile.md)** - Functional Requirements for Student Admission & Profile management.
- **[FRD_Fees_Installments.md](docs/FRD_Fees_Installments.md)** - Functional Requirements for Fees & Installments (critical accounts module).
- **[FRD_Attendance.md](docs/FRD_Attendance.md)** - Functional Requirements for Attendance tracking (student & staff).
- **[FRD_Lesson_Planning.md](docs/FRD_Lesson_Planning.md)** - Functional Requirements for Lesson Planning.
- **[FRD_Examination_Results.md](docs/FRD_Examination_Results.md)** - Functional Requirements for Examination & Results.
- **[FRD_Reports_NAAC.md](docs/FRD_Reports_NAAC.md)** - Functional Requirements for Reports & NAAC compliance.
- **[ERD_Database_Schema.md](docs/ERD_Database_Schema.md)** - Database schema design with ATKT/backlog handling.
- **[Laravel_Module_Breakdown.md](docs/Laravel_Module_Breakdown.md)** - Laravel-based module architecture and folder structure.
- **[Phase_Planning.md](docs/Phase_Planning.md)** - Detailed phase-by-phase development checklist.
- **[ATKT_Backlog_Rules.md](docs/ATKT_Backlog_Rules.md)** - ATKT & Backlog rules configuration.
- **[API_Service_Layer_Planning.md](docs/API_Service_Layer_Planning.md)** - API endpoints and service layer design.
- **[Open_Data_Gaps_Next_Steps.md](docs/Open_Data_Gaps_Next_Steps.md)** - Open data gaps requiring confirmation.

## System Overview

The PVGS system is designed to replace an existing off-the-shelf solution that failed to meet the institution's needs. Key features include:

- **Academic Structure Management**: Flexible UG/PG programs with component-based subjects.
- **Role-Based Access Control**: Program-scoped visibility and assignment-based permissions.
- **Student Lifecycle Management**: From admission to results, with audit trails.
- **Fees & Installments**: Enforced installment order with scholarship adjustments.
- **Attendance Tracking**: Timetable-linked attendance with NAAC compliance.
- **Examination & Results**: Configurable templates without forced online exams.
- **NAAC Reporting**: Dynamic, exportable reports for compliance.

## Technology Stack

- **Backend**: Laravel (PHP)
- **Frontend**: Web-based (desktop-first)
- **Database**: Relational (MySQL/PostgreSQL)
- **Hosting**: Self-hosted on PVGS servers

## Development Phases

- **Phase 1**: Core system with all essential modules.
- **Phase 2**: Optimizations and advanced features.
- **Phase 3**: Enhancements (mobile, QR attendance, online exams).

## Contact

For questions or clarifications, refer to the documentation or contact the development team.