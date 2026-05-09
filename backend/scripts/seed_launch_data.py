"""
SEED LAUNCH DATA SCRIPT
Populates Library, Chat, Audit, and Theme modules with realistic demo data.
Run this AFTER migrations to ensure the system looks "live" for demos.
"""

import sys
import os
from datetime import datetime, timedelta
import random
import uuid

# Add parent path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import get_db, engine
from app.modules.library.models import Author, Publisher, Book, BookIssue, LibraryFineConfig
from app.modules.chat.models import ChatMessage, Notification
from app.modules.audit.models import AuditLog
from app.modules.theme.models import InstitutionTheme
from app.modules.student.models import Student
from app.core.models import User, Institution

def seed_authors(db: Session, institution_id: str):
    print("📚 Seeding Authors...")
    authors_data = [
        ("R.K. Narayan", "Famous Indian author known for Malgudi Days"),
        ("Chetan Bhagat", "Bestselling author of 5 Point Someone"),
        ("Dr. A.P.J. Abdul Kalam", "Former President and scientist"),
        ("Ruskin Bond", "British-Indian author of children's books"),
        ("Sudha Murty", "Philanthropist and author"),
    ]
    
    authors = []
    for name, bio in authors_data:
        author = Author(
            id=f"auth_{uuid.uuid4().hex[:8]}",
            name=name,
            bio=bio,
            institution_id=institution_id
        )
        db.add(author)
        authors.append(author)
    
    db.commit()
    return authors

def seed_publishers(db: Session, institution_id: str):
    print("🏢 Seeding Publishers...")
    publishers_data = [
        ("Penguin Random House India", "New Delhi"),
        ("HarperCollins India", "Noida"),
        ("Rupa Publications", "Kolkata"),
        ("Westland Books", "Bangalore"),
    ]
    
    publishers = []
    for name, address in publishers_data:
        pub = Publisher(
            id=f"pub_{uuid.uuid4().hex[:8]}",
            name=name,
            address=address,
            institution_id=institution_id
        )
        db.add(pub)
        publishers.append(pub)
    
    db.commit()
    return publishers

def seed_books(db: Session, institution_id: str, authors: list, publishers: list):
    print("📖 Seeding Books...")
    books_data = [
        ("Swami and Friends", "Fiction", "A1-01", 10, 250.00),
        ("5 Point Someone", "Fiction", "A1-02", 8, 199.00),
        ("Wings of Fire", "Biography", "B1-01", 12, 350.00),
        ("The Blue Umbrella", "Children", "C1-01", 15, 150.00),
        ("Gently Falls the Bakula", "Fiction", "A1-03", 6, 225.00),
        ("Ignited Minds", "Self-Help", "D1-01", 20, 299.00),
        ("The God of Small Things", "Fiction", "A1-04", 5, 399.00),
        ("Malgudi Days", "Short Stories", "A1-05", 10, 275.00),
        ("Life of Pi", "Adventure", "B1-02", 7, 349.00),
        ("Revolution 2020", "Romance", "A1-06", 9, 189.00),
    ]
    
    books = []
    for i, (title, category, rack, copies, price) in enumerate(books_data):
        book = Book(
            id=f"book_{uuid.uuid4().hex[:8]}",
            title=title,
            isbn=f"978-81-{random.randint(10000, 99999)}-{random.randint(0, 9)}",
            author_id=random.choice(authors).id,
            publisher_id=random.choice(publishers).id,
            category=category,
            rack_number=rack,
            total_copies=copies,
            available_copies=random.randint(1, copies),
            price=price,
            purchase_date=datetime.now() - timedelta(days=random.randint(30, 365)),
            status="AVAILABLE",
            institution_id=institution_id
        )
        db.add(book)
        books.append(book)
    
    db.commit()
    return books

def seed_book_issues(db: Session, institution_id: str, books: list):
    print("📝 Seeding Book Issues...")
    
    # Get some demo students
    students = db.query(Student).filter(Student.institution_id == institution_id).limit(10).all()
    if not students:
        print("⚠️ No students found. Run student seed first.")
        return
    
    # Get a demo librarian/user
    librarian = db.query(User).filter(User.institution_id == institution_id, User.role == "ADMIN").first()
    if not librarian:
        print("⚠️ No admin user found.")
        return
    
    issues_count = 0
    for book in books[:5]:  # Issue first 5 books
        if book.available_copies > 0:
            student = random.choice(students)
            issue_date = datetime.now() - timedelta(days=random.randint(1, 20))
            due_date = issue_date + timedelta(days=14)
            
            # Some books are overdue
            is_overdue = issue_date < datetime.now() - timedelta(days=14)
            return_date = None
            fine = 0.0
            status = "ISSUED"
            
            if is_overdue and random.random() > 0.5:
                # Already returned with fine
                return_date = datetime.now() - timedelta(days=2)
                days_overdue = (return_date - due_date).days
                fine = min(days_overdue * 5.0, 500.0)
                status = "RETURNED"
                book.available_copies += 1
            
            issue = BookIssue(
                id=f"issue_{uuid.uuid4().hex[:8]}",
                book_id=book.id,
                student_id=student.id,
                issue_date=issue_date,
                due_date=due_date,
                return_date=return_date,
                fine_amount=fine,
                status=status,
                issued_by=librarian.id,
                institution_id=institution_id
            )
            db.add(issue)
            issues_count += 1
    
    db.commit()
    print(f"✅ Created {issues_count} book issue records")

def seed_chat_messages(db: Session, institution_id: str):
    print("💬 Seeding Chat Messages...")
    
    users = db.query(User).filter(User.institution_id == institution_id).all()
    if len(users) < 2:
        print("⚠️ Need at least 2 users for chat")
        return
    
    messages = [
        ("Fee payment deadline extended?", "GENERAL"),
        ("Can I get extra time for library book return?", "GENERAL"),
        ("Exam schedule has been updated", "EXAM"),
        ("Your child was absent today", "ATTENDANCE"),
        ("Please submit project report by Friday", "GENERAL"),
    ]
    
    count = 0
    for msg_text, msg_type in messages:
        sender = random.choice(users)
        receiver = random.choice([u for u in users if u.id != sender.id])
        
        msg = ChatMessage(
            id=f"msg_{uuid.uuid4().hex[:8]}",
            sender_id=sender.id,
            receiver_id=receiver.id,
            message=msg_text,
            is_read=random.choice([True, False]),
            institution_id=institution_id
        )
        db.add(msg)
        
        # Also create notification
        notif = Notification(
            id=f"notif_{uuid.uuid4().hex[:8]}",
            user_id=receiver.id,
            title=f"New Message from {sender.full_name}",
            message=msg_text,
            type=msg_type,
            channel="IN_APP",
            is_sent=True,
            is_read=False,
            institution_id=institution_id
        )
        db.add(notif)
        count += 1
    
    db.commit()
    print(f"✅ Created {count} chat messages and notifications")

def seed_audit_logs(db: Session, institution_id: str):
    print("🛡️ Seeding Audit Logs (God Mode)...")
    
    users = db.query(User).filter(User.institution_id == institution_id).all()
    if not users:
        return
    
    actions = [
        ("CREATE", "STUDENT", "New admission processed"),
        ("UPDATE", "FEE", "Fee structure modified"),
        ("DELETE", "USER", "Inactive user removed"),
        ("LOGIN", "USER", "Successful login"),
        ("UPDATE", "ATTENDANCE", "Bulk attendance marked"),
        ("CREATE", "EXAM", "Question paper uploaded"),
        ("REVERSE", "FEE", "Transaction reversed - wrong entry"),
    ]
    
    logs = []
    for action, entity, desc in actions:
        user = random.choice(users)
        log = AuditLog(
            id=f"audit_{uuid.uuid4().hex[:8]}",
            user_id=user.id,
            action=action,
            entity_type=entity,
            entity_id=f"ent_{uuid.uuid4().hex[:8]}",
            old_values={"status": "pending"} if action == "UPDATE" else None,
            new_values={"status": "approved"} if action == "UPDATE" else {"result": "success"},
            ip_address=f"192.168.1.{random.randint(1, 254)}",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            timestamp=datetime.now() - timedelta(hours=random.randint(1, 72)),
            institution_id=institution_id
        )
        logs.append(log)
        db.add(log)
    
    db.commit()
    print(f"✅ Created {len(logs)} audit trail entries")

def seed_theme(db: Session, institution_id: str):
    print("🎨 Seeding Default Theme...")
    
    theme = InstitutionTheme(
        id=f"theme_{uuid.uuid4().hex[:8]}",
        institution_id=institution_id,
        primary_color="#2563EB",  # Professional Blue
        secondary_color="#7C3AED",  # Purple accent
        logo_url="/logos/demo-school-logo.png",
        favicon_url="/favicons/demo.ico",
        font_family="Inter",
        layout_mode="SIDEBAR",
        is_active=True
    )
    db.add(theme)
    db.commit()
    print("✅ Theme configured")

def main():
    print("🚀 Starting Launch Data Seeding...")
    
    db = Session(bind=engine)
    
    try:
        # Get demo institution
        institution = db.query(Institution).filter(Institution.name == "EduCore Demo School").first()
        if not institution:
            print("❌ Demo institution not found. Run base seed first!")
            return
        
        inst_id = institution.id
        print(f"🏫 Found Institution: {institution.name}")
        
        # Seed all modules
        authors = seed_authors(db, inst_id)
        publishers = seed_publishers(db, inst_id)
        books = seed_books(db, inst_id, authors, publishers)
        seed_book_issues(db, inst_id, books)
        seed_chat_messages(db, inst_id)
        seed_audit_logs(db, inst_id)
        seed_theme(db, inst_id)
        
        print("\n✅ LAUNCH SEEDING COMPLETE!")
        print("System is now ready for demo with:")
        print("  - 5 Authors, 4 Publishers, 10 Books")
        print("  - Active Book Issues (some overdue)")
        print("  - Chat Messages & Notifications")
        print("  - Audit Trail Logs")
        print("  - Custom Theme Settings")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
