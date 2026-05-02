"""Seed script to create Super Admin and Demo Institution."""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from app.db.base_class import Base
from app.models.institution import Institution
from app.models.user import User, UserRole, UserStatus, InstitutionType

# Configuration
DATABASE_URL = "postgresql+asyncpg://eduserp:eduserp_secure_pass@localhost:5432/educore_db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    """Create Super Admin and Demo Institution."""
    
    # Create engine and session
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Create tables (if not exists)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session() as session:
        # Check if Super Admin already exists
        super_admin = await session.execute(
            User.__table__.select().where(User.role == UserRole.SUPER_ADMIN)
        )
        
        if super_admin.first():
            print("✅ Super Admin already exists. Skipping...")
            return
        
        print("🌱 Creating Super Admin account...")
        
        # Create Super Admin
        hashed_password = pwd_context.hash("SuperAdmin@123!")
        
        new_super_admin = User(
            email="superadmin@educore.system",
            password_hash=hashed_password,
            first_name="System",
            last_name="Administrator",
            phone="+91-9876543210",
            role=UserRole.SUPER_ADMIN,
            status=UserStatus.ACTIVE,
            institution_id=None  # Super admin is system-wide
        )
        
        session.add(new_super_admin)
        await session.flush()  # Get the ID
        
        print(f"✅ Super Admin created: {new_super_admin.email}")
        
        # Create Demo Institution
        print("🏫 Creating Demo Institution...")
        
        demo_institution = Institution(
            name="EduCore Demo School",
            code="DEMO-SCHOOL-001",
            address="123 Education Street, Knowledge City, India - 400001",
            phone="+91-22-12345678",
            email="info@demoschool.edu.in",
            website="https://demoschool.edu.in",
            type=InstitutionType.SCHOOL,
            board="CBSE",
            theme_primary_color="#1e40af",
            theme_secondary_color="#64748b",
            feature_nfc_attendance=True,
            feature_qr_attendance=True,
            feature_lms=True,
            feature_assessment=True,
            feature_naac_reports=True
        )
        
        session.add(demo_institution)
        await session.flush()
        
        print(f"✅ Demo Institution created: {demo_institution.name} ({demo_institution.code})")
        
        # Create Institution Admin for Demo School
        print("👤 Creating Institution Admin for Demo School...")
        
        inst_admin = User(
            email="admin@demoschool.edu.in",
            password_hash=pwd_context.hash("InstAdmin@123!"),
            first_name="Demo",
            last_name="Administrator",
            phone="+91-9876543211",
            role=UserRole.INSTITUTION_ADMIN,
            status=UserStatus.ACTIVE,
            institution_id=demo_institution.id,
            approved_by=new_super_admin.id
        )
        
        session.add(inst_admin)
        await session.commit()
        
        print(f"✅ Institution Admin created: {inst_admin.email}")
        
        print("\n" + "="*60)
        print("🎉 SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 LOGIN CREDENTIALS:")
        print("-"*60)
        print(f"Super Admin:")
        print(f"  Email: superadmin@educore.system")
        print(f"  Password: SuperAdmin@123!")
        print(f"\nInstitution Admin (Demo School):")
        print(f"  Email: admin@demoschool.edu.in")
        print(f"  Password: InstAdmin@123!")
        print("="*60)


if __name__ == "__main__":
    try:
        asyncio.run(seed_database())
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        sys.exit(1)
