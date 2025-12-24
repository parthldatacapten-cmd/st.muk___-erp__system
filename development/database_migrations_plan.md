# Database Migrations Plan

## Overview
This document outlines the database migration strategy for the PVGS system. Migrations are organized by priority and dependency to ensure proper database structure implementation.

## Migration Execution Order

### Phase 1: Foundation Tables (Priority: HIGH)
**Run these first - core system foundation**

```sql
-- 001_create_users_table.php
-- 002_create_roles_and_permissions_tables.php (spatie/laravel-permission)
-- 003_create_audit_logs_table.php
-- 004_create_academic_years_table.php
-- 005_create_programs_table.php
-- 006_create_subjects_table.php
```

### Phase 2: User Management (Priority: HIGH)
**Essential user-related tables**

```sql
-- 007_create_students_table.php
-- 008_create_faculty_table.php
-- 009_create_staff_table.php
-- 010_create_user_roles_table.php (pivot for user-role relationships)
```

### Phase 3: Academic Structure (Priority: HIGH)
**Core academic functionality**

```sql
-- 011_create_program_subjects_table.php (pivot)
-- 012_create_semesters_table.php
-- 013_create_batches_table.php
-- 014_create_student_enrollments_table.php
-- 015_create_faculty_assignments_table.php
```

### Phase 4: Attendance System (Priority: HIGH)
**Daily operations tracking**

```sql
-- 016_create_attendance_sessions_table.php
-- 017_create_student_attendance_table.php
-- 018_create_faculty_attendance_table.php
-- 019_create_attendance_reports_table.php
```

### Phase 5: Financial System (Priority: MEDIUM)
**Fee and payment management**

```sql
-- 020_create_fee_categories_table.php
-- 021_create_fee_structures_table.php
-- 022_create_installment_plans_table.php
-- 023_create_student_fees_table.php
-- 024_create_payments_table.php
-- 025_create_payment_transactions_table.php
```

### Phase 6: Examination System (Priority: MEDIUM)
**Assessment and results**

```sql
-- 026_create_exam_types_table.php
-- 027_create_exams_table.php
-- 028_create_exam_schedules_table.php
-- 029_create_student_marks_table.php
-- 030_create_grades_table.php
-- 031_create_results_table.php
-- 032_create_atkt_records_table.php
```

### Phase 7: Advanced Features (Priority: LOW)
**Reporting and analytics**

```sql
-- 033_create_naac_reports_table.php
-- 034_create_lesson_plans_table.php
-- 035_create_syllabus_table.php
-- 036_create_notifications_table.php
-- 037_create_documents_table.php
-- 038_create_system_settings_table.php
```

## Detailed Table Specifications

### 1. Users Table (Foundation)
```php
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email')->unique();
    $table->string('phone')->nullable();
    $table->string('password');
    $table->enum('user_type', ['student', 'faculty', 'staff', 'admin']);
    $table->boolean('is_active')->default(true);
    $table->timestamp('email_verified_at')->nullable();
    $table->rememberToken();
    $table->timestamps();
});
```

### 2. Students Table (Core)
```php
Schema::create('students', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->string('student_id')->unique();
    $table->string('first_name');
    $table->string('last_name');
    $table->date('date_of_birth');
    $table->enum('gender', ['male', 'female', 'other']);
    $table->text('address');
    $table->string('phone');
    $table->string('emergency_contact');
    $table->foreignId('program_id')->constrained();
    $table->foreignId('batch_id')->constrained();
    $table->enum('status', ['active', 'inactive', 'graduated', 'transferred'])->default('active');
    $table->json('documents')->nullable(); // Store document paths
    $table->timestamps();
});
```

### 3. Programs Table (Academic Structure)
```php
Schema::create('programs', function (Blueprint $table) {
    $table->id();
    $table->string('program_code')->unique();
    $table->string('program_name');
    $table->text('description');
    $table->integer('duration_years');
    $table->integer('total_semesters');
    $table->decimal('total_fees', 10, 2);
    $table->boolean('is_active')->default(true);
    $table->timestamps();
});
```

### 4. Subjects Table (Academic Structure)
```php
Schema::create('subjects', function (Blueprint $table) {
    $table->id();
    $table->string('subject_code')->unique();
    $table->string('subject_name');
    $table->text('description');
    $table->integer('credits');
    $table->enum('type', ['theory', 'practical', 'both']);
    $table->integer('theory_marks')->default(0);
    $table->integer('practical_marks')->default(0);
    $table->boolean('is_active')->default(true);
    $table->timestamps();
});
```

### 5. Fee Structures Table (Financial)
```php
Schema::create('fee_structures', function (Blueprint $table) {
    $table->id();
    $table->foreignId('program_id')->constrained();
    $table->foreignId('fee_category_id')->constrained();
    $table->decimal('amount', 10, 2);
    $table->enum('frequency', ['one_time', 'annual', 'semester', 'monthly']);
    $table->boolean('is_mandatory')->default(true);
    $table->boolean('is_active')->default(true);
    $table->timestamps();
});
```

### 6. Installment Plans Table (Financial)
```php
Schema::create('installment_plans', function (Blueprint $table) {
    $table->id();
    $table->foreignId('fee_structure_id')->constrained();
    $table->integer('installment_number');
    $table->decimal('amount', 10, 2);
    $table->date('due_date');
    $table->text('description');
    $table->boolean('is_active')->default(true);
    $table->timestamps();
});
```

### 7. Student Fees Table (Financial)
```php
Schema::create('student_fees', function (Blueprint $table) {
    $table->id();
    $table->foreignId('student_id')->constrained();
    $table->foreignId('fee_structure_id')->constrained();
    $table->decimal('total_amount', 10, 2);
    $table->decimal('paid_amount', 10, 2)->default(0);
    $table->decimal('pending_amount', 10, 2);
    $table->enum('status', ['pending', 'partial', 'paid', 'overdue'])->default('pending');
    $table->date('due_date');
    $table->timestamps();
});
```

### 8. Attendance Sessions Table (Attendance)
```php
Schema::create('attendance_sessions', function (Blueprint $table) {
    $table->id();
    $table->foreignId('subject_id')->constrained();
    $table->foreignId('faculty_id')->constrained('faculty');
    $table->foreignId('batch_id')->constrained();
    $table->date('attendance_date');
    $table->time('start_time');
    $table->time('end_time');
    $table->enum('session_type', ['theory', 'practical']);
    $table->text('topic')->nullable();
    $table->timestamps();
});
```

### 9. Student Attendance Table (Attendance)
```php
Schema::create('student_attendance', function (Blueprint $table) {
    $table->id();
    $table->foreignId('attendance_session_id')->constrained();
    $table->foreignId('student_id')->constrained();
    $table->enum('status', ['present', 'absent', 'late', 'excused'])->default('present');
    $table->text('remarks')->nullable();
    $table->timestamps();

    $table->unique(['attendance_session_id', 'student_id']);
});
```

### 10. Exams Table (Examination)
```php
Schema::create('exams', function (Blueprint $table) {
    $table->id();
    $table->foreignId('subject_id')->constrained();
    $table->foreignId('batch_id')->constrained();
    $table->string('exam_name');
    $table->enum('exam_type', ['internal', 'external', 'practical', 'viva']);
    $table->date('exam_date');
    $table->time('start_time');
    $table->integer('duration_minutes');
    $table->integer('total_marks');
    $table->integer('passing_marks');
    $table->text('instructions')->nullable();
    $table->timestamps();
});
```

### 11. Student Marks Table (Examination)
```php
Schema::create('student_marks', function (Blueprint $table) {
    $table->id();
    $table->foreignId('exam_id')->constrained();
    $table->foreignId('student_id')->constrained();
    $table->decimal('marks_obtained', 5, 2);
    $table->decimal('percentage', 5, 2);
    $table->enum('grade', ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F']);
    $table->text('remarks')->nullable();
    $table->timestamps();

    $table->unique(['exam_id', 'student_id']);
});
```

### 12. ATKT Records Table (Examination)
```php
Schema::create('atkt_records', function (Blueprint $table) {
    $table->id();
    $table->foreignId('student_id')->constrained();
    $table->foreignId('subject_id')->constrained();
    $table->foreignId('semester_id')->constrained();
    $table->enum('status', ['pending', 'cleared', 'failed_again'])->default('pending');
    $table->integer('attempt_number')->default(1);
    $table->date('exam_date')->nullable();
    $table->decimal('marks_obtained', 5, 2)->nullable();
    $table->timestamps();
});
```

## Migration Dependencies

### Must Run Before:
- **Users table**: Before all other tables (foreign key references)
- **Programs & Subjects**: Before student enrollments and faculty assignments
- **Academic Structure**: Before attendance and examination tables
- **Fee Structures**: Before student fees and payments

### Can Run In Parallel:
- **Audit logs**: Independent of other tables
- **Notifications**: Can be created after core tables
- **System settings**: Independent configuration

## Rollback Strategy

### Safe Rollbacks:
```bash
# Rollback specific migration
php artisan migrate:rollback --step=1

# Rollback to specific migration
php artisan migrate:rollback --path=database/migrations/2024_01_01_000010_create_students_table.php
```

### Data Preservation:
- **Soft deletes**: Implement for critical data
- **Backup before rollback**: Always backup database before rollback
- **Seeders**: Recreate test data after rollback

## Testing Migrations

### Migration Testing:
```bash
# Test migrations without affecting database
php artisan migrate --pretend

# Rollback and re-run
php artisan migrate:rollback && php artisan migrate

# Check migration status
php artisan migrate:status
```

### Data Integrity Checks:
- Foreign key constraints validation
- Data type consistency
- Index performance
- Relationship integrity

This migration plan ensures a structured database implementation with proper dependencies and rollback capabilities.