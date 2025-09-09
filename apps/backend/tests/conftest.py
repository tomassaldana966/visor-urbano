"""
Test configuration for dependency tests.
This file sets up the Python path and common test fixtures.
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Add the app directory to the Python path as well
app_dir = backend_dir / "app"
sys.path.insert(0, str(app_dir))

# Set environment variables for testing
os.environ["APP_ENV"] = "testing"
os.environ["DATABASE_HOST"] = "localhost"
os.environ["DATABASE_PORT"] = "5432"
os.environ["DATABASE_NAME"] = "test_visor"
os.environ["DATABASE_USERNAME"] = "test_user"
os.environ["DATABASE_PASSWORD"] = "test_pass"

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean, Text, Float, BigInteger, ForeignKey
from config.security import get_password_hash, create_access_token
from datetime import timedelta


# Create minimal table definitions without geographic dependencies
test_metadata = MetaData()

# Define only the essential tables needed for testing (without PostGIS dependencies)
users_table = Table(
    'users',
    test_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(150), unique=True, nullable=False),
    Column('email', String(255), unique=True, nullable=False),
    Column('password_hash', String(128), nullable=False),
    Column('is_active', Boolean, nullable=False, default=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

password_recovery_table = Table(
    'password_recovery',
    test_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('token', String(255), nullable=False),
    Column('created_at', DateTime, nullable=True),
    Column('expires_at', DateTime, nullable=True),
    Column('used_at', DateTime, nullable=True),
    Column('is_used', Boolean, nullable=False, default=False),
)

procedures_table = Table(
    'procedures',
    test_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('folio', String(255), nullable=True),
    Column('current_step', Integer, nullable=True),
    Column('user_signature', String(255), nullable=True),
    Column('user_id', Integer, nullable=True),
    Column('window_user_id', Integer, nullable=True),
    Column('entry_role', Integer, nullable=True),
    Column('documents_submission_date', DateTime, nullable=True),
    Column('procedure_start_date', DateTime, nullable=True),
    Column('window_seen_date', DateTime, nullable=True),
    Column('license_delivered_date', DateTime, nullable=True),
    Column('has_signature', Integer, nullable=True),
    Column('no_signature_date', DateTime, nullable=True),
    Column('official_applicant_name', String(255), nullable=True),
    Column('responsibility_letter', String(255), nullable=True),
    Column('sent_to_reviewers', Integer, nullable=True),
    Column('sent_to_reviewers_date', DateTime, nullable=True),
    Column('license_pdf', String(255), nullable=True),
    Column('payment_order', String(255), nullable=True),
    Column('status', Integer, nullable=False),
    Column('step_one', Integer, nullable=True),
    Column('step_two', Integer, nullable=True),
    Column('step_three', Integer, nullable=True),
    Column('step_four', Integer, nullable=True),
    Column('director_approval', Integer, nullable=True, default=0),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
    Column('window_license_generated', Integer, nullable=True, default=0),
    Column('procedure_type', String(255), nullable=True),
    Column('license_status', String(255), nullable=True),
    Column('reason', String(255), nullable=True),
    Column('renewed_folio', String(255), nullable=True),
    Column('requirements_query_id', Integer, nullable=True),
    Column('municipality_id', Integer, nullable=True),
    Column('business_license_type_id', Integer, nullable=True),
)

# Additional tables that might be referenced
business_signatures_table = Table(
    'business_signatures',
    test_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('signature_data', Text, nullable=True),
    Column('created_at', DateTime, nullable=True),
)

municipalities_table = Table(
    'municipalities',
    test_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(250), nullable=False),
    Column('image', String(250), nullable=True),
    Column('director', String(250), nullable=True),
    Column('director_signature', String(250), nullable=True),
    Column('process_sheet', Integer, nullable=True, default=1),
    Column('solving_days', Integer, nullable=True),
    Column('issue_license', Integer, nullable=True, default=0),
    Column('address', String(255), nullable=True),
    Column('phone', String(255), nullable=True),
    Column('email', String(255), nullable=True),
    Column('website', String(255), nullable=True),
    Column('responsible_area', String(250), nullable=True),
    Column('allow_online_procedures', Boolean, default=False, nullable=True),
    Column('allow_window_reviewer_licenses', Boolean, default=False, nullable=True),
    Column('low_impact_license_cost', String(255), nullable=True),
    Column('license_additional_text', Text, nullable=True),
    Column('theme_color', String(7), nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
    Column('deleted_at', DateTime, nullable=True),
    Column('window_license_generation', Integer, nullable=True, default=0),
    Column('license_restrictions', Text, nullable=True, default=''),
    Column('license_price', String(255), nullable=True),
    Column('initial_folio', Integer, nullable=True),
    Column('has_zoning', Boolean, default=False, nullable=True)
)

procedure_registrations_table = Table(
    'procedure_registrations',
    test_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('folio', String(255), unique=True, nullable=False),
    Column('status', String(50), nullable=False, default='active'),
    Column('title', String(500), nullable=True),
    Column('description', Text, nullable=True),
    Column('user_id', Integer, nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

business_license_types_table = Table(
    'business_license_types',
    test_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('description', Text, nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

auth_user_table = Table(
    'auth_user',
    test_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(150), unique=True, nullable=False),
    Column('email', String(255), unique=True, nullable=False),
    Column('password', String(128), nullable=False),
    Column('is_active', Boolean, nullable=False, default=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

requirements_querys_table = Table(
    'requirements_querys',
    test_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
    Column('description', Text, nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

user_roles_table = Table(
    'user_roles',
    test_metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('name', String(20), nullable=False),
    Column('description', String(200), nullable=True),
    Column('municipality_id', Integer, ForeignKey('municipalities.id'), nullable=True),
    Column('deleted_at', DateTime, nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI application."""
    from app.main import app
    return TestClient(app)


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create a test database engine using SQLite in memory."""
    # Use SQLite in memory for testing with test models (no PostGIS dependencies)
    from tests.models_no_postgis import Base as TestBase
    database_url = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(database_url, echo=False)
    # Create tables using test Base metadata (without PostGIS dependencies)
    async with engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.create_all)
    yield engine
    # Clean up
    await engine.dispose()


@pytest.fixture(scope="session")
def test_models():
    """Provide access to test models."""
    from tests.models_no_postgis import User, PasswordRecovery, BusinessLineLog, Municipality
    return {
        'User': User,
        'PasswordRecovery': PasswordRecovery,
        'BusinessLineLog': BusinessLineLog,
        'Municipality': Municipality
    }


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine):
    """Create a database session for testing."""
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()  # Rollback any changes made during the test


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session):
    """Create an async HTTP client for testing."""
    from app.main import app
    from config.settings import get_session, get_db
    import httpx
    
    # Override both database dependencies
    async def override_get_session():
        yield db_session
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_db] = override_get_db
    
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def sample_procedures(db_session):
    """Create sample procedure data for testing."""
    # Insert test data directly using SQL
    await db_session.execute(
        procedures_table.insert().values([
            {
                'id': 1,
                'folio': 'PROC-001',
                'status': 1,
                'current_step': 1,
                'procedure_type': 'new',
                'user_id': 1,
                'window_user_id': 1,
                'entry_role': 1,
                'step_one': 1,
                'step_two': 0,
                'step_three': 0,
                'step_four': 0,
                'director_approval': 0,
                'window_license_generated': 0
            },
            {
                'id': 2,
                'folio': 'PROC-002',
                'status': 2,
                'current_step': 2,
                'procedure_type': 'renewal',
                'user_id': 2,
                'window_user_id': 2,
                'entry_role': 2,
                'step_one': 1,
                'step_two': 1,
                'step_three': 0,
                'step_four': 0,
                'director_approval': 0,
                'window_license_generated': 0
            },
            {
                'id': 3,
                'folio': 'PROC-003',
                'status': 3,
                'current_step': 3,
                'procedure_type': 'new',
                'user_id': 3,
                'window_user_id': 3,
                'entry_role': 3,
                'step_one': 1,
                'step_two': 1,
                'step_three': 1,
                'step_four': 0,
                'director_approval': 1,
                'window_license_generated': 0
            }
        ])
    )
    
    await db_session.commit()
    return {
        'procedures': [
            {'id': 1, 'folio': 'PROC-001', 'status': 1},
            {'id': 2, 'folio': 'PROC-002', 'status': 2},
            {'id': 3, 'folio': 'PROC-003', 'status': 3}
        ]
    }


@pytest_asyncio.fixture(scope="function")
async def test_admin_user(db_session, test_models):
    """Create an admin test user."""
    User = test_models['User']
    user = User(
        name="Admin",
        paternal_last_name="User",
        email="admin@test.com",
        password=get_password_hash("adminpass123"),
        cellphone="1234567890",
        is_active=True,
        municipality_id=1,
        role_id=1  # Admin role
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_director_user(db_session, test_models):
    """Create a director test user."""
    User = test_models['User']
    user = User(
        name="Director",
        paternal_last_name="User",
        email="director@test.com",
        password=get_password_hash("directorpass123"),
        cellphone="1234567891",
        is_active=True,
        municipality_id=1,
        role_id=2  # Director role
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_regular_user(db_session, test_models):
    """Create a regular test user."""
    User = test_models['User']
    user = User(
        name="Regular",
        paternal_last_name="User",
        email="regular@test.com",
        password=get_password_hash("regularpass123"),
        cellphone="1234567892",
        is_active=True,
        municipality_id=1,
        role_id=3  # Regular user role
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")  
async def test_roles(db_session):
    """Create test roles in the database."""
    from tests.models_no_postgis import UserRole
    
    # Create admin role
    admin_role = UserRole(
        id=1,
        name="admin",
        description="Administrator role",
        municipality_id=1
    )
    db_session.add(admin_role)
    
    # Create director role  
    director_role = UserRole(
        id=2,
        name="director", 
        description="Director role",
        municipality_id=1
    )
    db_session.add(director_role)
    
    # Create regular user role
    user_role = UserRole(
        id=3,
        name="user",
        description="Regular user role", 
        municipality_id=1
    )
    db_session.add(user_role)
    
    await db_session.commit()
    return {"admin": admin_role, "director": director_role, "user": user_role}


@pytest.fixture(scope="function")
def admin_user_token(test_admin_user):
    """Generate JWT token for admin user."""
    access_token_expires = timedelta(minutes=30)
    token_data = {
        "sub": test_admin_user.email,
        "user_id": str(test_admin_user.id),
        "municipality_id": test_admin_user.municipality_id,
        "role_id": test_admin_user.role_id
    }
    return create_access_token(data=token_data, expires_delta=access_token_expires)


@pytest.fixture(scope="function")
def director_user_token(test_director_user):
    """Generate JWT token for director user."""
    access_token_expires = timedelta(minutes=30)
    token_data = {
        "sub": test_director_user.email,
        "user_id": str(test_director_user.id),
        "municipality_id": test_director_user.municipality_id,
        "role_id": test_director_user.role_id
    }
    return create_access_token(data=token_data, expires_delta=access_token_expires)


@pytest.fixture(scope="function")
def regular_user_token(test_regular_user):
    """Generate JWT token for regular user."""
    access_token_expires = timedelta(minutes=30)
    token_data = {
        "sub": test_regular_user.email,
        "user_id": str(test_regular_user.id),
        "municipality_id": test_regular_user.municipality_id,
        "role_id": test_regular_user.role_id
    }
    return create_access_token(data=token_data, expires_delta=access_token_expires)
