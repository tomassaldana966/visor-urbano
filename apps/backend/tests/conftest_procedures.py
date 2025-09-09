"""
Isolated test configuration for procedures tests only.
This avoids loading geographic models that cause PostGIS/SQLite conflicts.
"""
import sys
import os
from pathlib import Path
from datetime import datetime

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
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean, Text, BigInteger, ForeignKey


# Create minimal table definitions without geographic dependencies
metadata = MetaData()

# Define only the procedures table structure needed for testing
procedures_table = Table(
    'procedures',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('folio', String(255), unique=True, nullable=False),
    Column('status', String(50), nullable=False, default='active'),
    Column('title', String(500), nullable=True),
    Column('description', Text, nullable=True),
    Column('category', String(100), nullable=True),
    Column('priority', String(20), nullable=True),
    Column('assigned_to', String(255), nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

# Add historical procedures table for testing copy-historical endpoint
historical_procedures_table = Table(
    'historical_procedures',
    metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
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
    Column('window_license_generated', Integer, default=0),
    Column('procedure_type', String(255), nullable=True),
    Column('license_status', String(255), nullable=True),
    Column('reason', String(255), nullable=True),
    Column('renewed_folio', String(255), nullable=True),
    Column('requirements_query_id', Integer, nullable=True)
)

# Dependencies tables that procedures might reference
dependencies_table = Table(
    'dependencies',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('procedure_id', Integer, nullable=False),
    Column('name', String(255), nullable=False),
    Column('description', Text, nullable=True),
    Column('status', String(50), nullable=False, default='pending'),
)

attachments_table = Table(
    'attachments',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('procedure_id', Integer, nullable=False),
    Column('filename', String(255), nullable=False),
    Column('file_type', String(50), nullable=True),
    Column('file_size', Integer, nullable=True),
    Column('file_path', String(500), nullable=True),
    Column('uploaded_at', DateTime, nullable=True),
)


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI application."""
    # Only import the specific router we need
    from fastapi import FastAPI
    from app.routers.procedures import router as procedures_router
    
    # Create a minimal app with just the procedures router
    app = FastAPI()
    app.include_router(procedures_router, prefix="/v1/procedures", tags=["procedures"])
    
    return TestClient(app)


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create a test database engine using SQLite in memory."""
    from sqlalchemy.ext.asyncio import create_async_engine
    
    # Use SQLite in memory for testing
    database_url = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(database_url, echo=False)
    
    # Create only the tables we need for procedures testing
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    
    yield engine
    
    # Clean up
    await engine.dispose()


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
    from fastapi import FastAPI
    from app.routers.procedures import router as procedures_router
    import httpx
    
    # Create a minimal app with just the procedures router
    app = FastAPI()
    app.include_router(procedures_router, prefix="/v1/procedures", tags=["procedures"])
    
    # Override database dependencies with our test session
    async def override_get_session():
        yield db_session
    
    async def override_get_db():
        yield db_session
    
    # Import the actual dependency functions
    try:
        from config.settings import get_session, get_db
        app.dependency_overrides[get_session] = override_get_session
        app.dependency_overrides[get_db] = override_get_db
    except ImportError:
        # If config.settings doesn't exist, try alternative imports
        pass
    
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
                'status': 'active',
                'title': 'Test Procedure 1',
                'description': 'Description for procedure 1',
                'category': 'urban_planning',
                'priority': 'high',
                'assigned_to': 'user1@example.com'
            },
            {
                'id': 2,
                'folio': 'PROC-002',
                'status': 'pending',
                'title': 'Test Procedure 2',
                'description': 'Description for procedure 2',
                'category': 'permits',
                'priority': 'medium',
                'assigned_to': 'user2@example.com'
            },
            {
                'id': 3,
                'folio': 'PROC-003',
                'status': 'completed',
                'title': 'Test Procedure 3',
                'description': 'Description for procedure 3',
                'category': 'inspection',
                'priority': 'low',
                'assigned_to': 'user3@example.com'
            }
        ])
    )
    
    # Insert some historical procedures
    await db_session.execute(
        historical_procedures_table.insert().values([
            {
                'id': 1,
                'folio': 'HIST-001',
                'status': 1,  # Completed
                'procedure_type': 'urban_planning',
                'official_applicant_name': 'Historical User 1',
                'created_at': datetime.now()
            },
            {
                'id': 2,
                'folio': 'HIST-002',
                'status': 1,  # Completed
                'procedure_type': 'permits',
                'official_applicant_name': 'Historical User 2',
                'created_at': datetime.now()
            }
        ])
    )
    
    # Insert some dependencies
    await db_session.execute(
        dependencies_table.insert().values([
            {
                'procedure_id': 1,
                'name': 'Document Review',
                'description': 'Review submitted documents',
                'status': 'completed'
            },
            {
                'procedure_id': 1,
                'name': 'Site Inspection',
                'description': 'Conduct on-site inspection',
                'status': 'pending'
            }
        ])
    )
    
    # Insert some attachments
    await db_session.execute(
        attachments_table.insert().values([
            {
                'procedure_id': 1,
                'filename': 'document1.pdf',
                'file_type': 'application/pdf',
                'file_size': 1024000,
                'file_path': '/uploads/document1.pdf'
            }
        ])
    )
    
    await db_session.commit()
    return {
        'procedures': [
            {'id': 1, 'folio': 'PROC-001', 'status': 'active'},
            {'id': 2, 'folio': 'PROC-002', 'status': 'pending'},
            {'id': 3, 'folio': 'PROC-003', 'status': 'completed'}
        ]
    }
