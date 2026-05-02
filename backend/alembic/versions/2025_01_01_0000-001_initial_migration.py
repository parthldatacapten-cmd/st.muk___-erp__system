"""Initial migration - Create institutions and users tables."""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial tables for institutions and users."""
    
    # Create institutions table
    op.create_table(
        'institutions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False, unique=True),
        sa.Column('logo_url', sa.String(length=500), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('type', sa.Enum('SCHOOL', 'COLLEGE', 'COACHING', 'UNIVERSITY', name='institutiontype'), nullable=False),
        sa.Column('board', sa.String(length=100), nullable=True),  # CBSE, ICSE, State, etc.
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        
        # Theme & Branding
        sa.Column('theme_primary_color', sa.String(length=7), nullable=True, default='#1e40af'),
        sa.Column('theme_secondary_color', sa.String(length=7), nullable=True, default='#64748b'),
        sa.Column('theme_logo_light', sa.String(length=500), nullable=True),
        sa.Column('theme_logo_dark', sa.String(length=500), nullable=True),
        sa.Column('theme_favicon', sa.String(length=500), nullable=True),
        
        # Feature Flags
        sa.Column('feature_nfc_attendance', sa.Boolean(), nullable=False, default=False),
        sa.Column('feature_qr_attendance', sa.Boolean(), nullable=False, default=False),
        sa.Column('feature_lms', sa.Boolean(), nullable=False, default=False),
        sa.Column('feature_assessment', sa.Boolean(), nullable=False, default=False),
        sa.Column('feature_naac_reports', sa.Boolean(), nullable=False, default=False),
        
        # Metadata
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index on code for fast lookups
    op.create_index('ix_institutions_code', 'institutions', ['code'])
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('institution_id', sa.Integer(), sa.ForeignKey('institutions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('role', sa.Enum('SUPER_ADMIN', 'INSTITUTION_ADMIN', 'PRINCIPAL', 'FACULTY', 'STUDENT', 'PARENT', 'ACCOUNTANT', name='userrole'), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'ACTIVE', 'SUSPENDED', 'REJECTED', name='userstatus'), nullable=False, default='PENDING'),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.Column('approved_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        
        # Anti-fraud: Device binding
        sa.Column('registered_device_id', sa.String(length=255), nullable=True),
        sa.Column('device_bind_count', sa.Integer(), nullable=False, default=0),
        sa.Column('last_device_change_at', sa.DateTime(timezone=True), nullable=True),
        
        # Metadata
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for fast lookups
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_institution_id', 'users', ['institution_id'])
    op.create_index('ix_users_role', 'users', ['role'])
    op.create_index('ix_users_status', 'users', ['status'])
    
    # Create unique constraint on email + institution_id
    op.create_unique_constraint('uq_users_email_institution', 'users', ['email', 'institution_id'])


def downgrade() -> None:
    """Drop tables in reverse order."""
    op.drop_constraint('uq_users_email_institution', 'users', type_='unique')
    op.drop_index('ix_users_status', table_name='users')
    op.drop_index('ix_users_role', table_name='users')
    op.drop_index('ix_users_institution_id', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_institutions_code', table_name='institutions')
    op.drop_table('institutions')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS userstatus')
    op.execute('DROP TYPE IF EXISTS userrole')
    op.execute('DROP TYPE IF EXISTS institutiontype')
