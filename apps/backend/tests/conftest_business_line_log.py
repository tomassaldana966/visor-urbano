"""
Configuration and fixtures for Business Line Log tests
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.business_line_log import BusinessLineLog
from app.models.user import UserModel
from app.models.user_roles import UserRoleModel
from app.schemas.business_line_log import BusinessLineLogCreate


@pytest.fixture
async def sample_business_line_log_data():
    """Sample data for creating business line logs"""
    return {
        "action": "Test business action",
        "previous": "Test previous state",
        "log_type": 1,
        "procedure_id": 123,
        "post_request": '{"test": "data"}'
    }


@pytest.fixture
async def admin_user_token(db_session: AsyncSession, create_test_user):
    """Create an admin user and return their token"""
    admin_role = UserRoleModel(
        name="Admin",
        description="Administrator role"
    )
    db_session.add(admin_role)
    await db_session.commit()
    await db_session.refresh(admin_role)
    
    admin_user = await create_test_user(
        email="admin@test.com",
        name="Admin",
        paternal_last_name="User",
        role_id=admin_role.id
    )
    
    # In a real implementation, you would generate a proper JWT token
    # For testing purposes, we'll return a mock token
    return f"admin_token_user_{admin_user.id}"


@pytest.fixture 
async def director_user_token(db_session: AsyncSession, create_test_user):
    """Create a director user and return their token"""
    director_role = UserRoleModel(
        name="Director",
        description="Director role"
    )
    db_session.add(director_role)
    await db_session.commit()
    await db_session.refresh(director_role)
    
    director_user = await create_test_user(
        email="director@test.com", 
        name="Director",
        paternal_last_name="User",
        role_id=director_role.id
    )
    
    return f"director_token_user_{director_user.id}"


@pytest.fixture
async def regular_user_token(db_session: AsyncSession, create_test_user):
    """Create a regular user and return their token"""
    regular_role = UserRoleModel(
        name="Regular",
        description="Regular user role"
    )
    db_session.add(regular_role)
    await db_session.commit()
    await db_session.refresh(regular_role)
    
    regular_user = await create_test_user(
        email="regular@test.com",
        name="Regular", 
        paternal_last_name="User",
        role_id=regular_role.id
    )
    
    return f"regular_token_user_{regular_user.id}"


@pytest.fixture
async def create_test_user(db_session: AsyncSession):
    """Factory fixture for creating test users"""
    async def _create_user(
        email: str,
        name: str = "Test",
        paternal_last_name: str = "User",
        cellphone: str = "1234567890",
        password: str = "test_password",
        role_id: int = None
    ) -> UserModel:
        user = UserModel(
            name=name,
            paternal_last_name=paternal_last_name,
            email=email,
            cellphone=cellphone,
            password=password,
            role_id=role_id
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user
    
    return _create_user


@pytest.fixture
async def sample_business_line_logs(db_session: AsyncSession, create_test_user):
    """Create sample business line logs for testing"""
    # Create a test user if none exists
    test_user = await create_test_user(
        email="logs_test@example.com",
        name="Logs",
        paternal_last_name="Test"
    )
    
    logs = []
    base_time = datetime.now() - timedelta(days=7)
    
    for i in range(10):
        log = BusinessLineLog(
            action=f"Test action {i}",
            previous=f"Previous state {i}" if i % 2 == 0 else None,
            user_id=test_user.id,
            log_type=(i % 3) + 1,  # Log types 1, 2, 3
            procedure_id=100 + i if i % 3 == 0 else None,
            host="test.local",
            user_ip=f"192.168.1.{100 + i}",
            role_id=1,
            user_agent="Test User Agent",
            post_request=f'{{"test_data": {i}}}',
            created_at=base_time + timedelta(hours=i),
            updated_at=base_time + timedelta(hours=i)
        )
        db_session.add(log)
        logs.append(log)
    
    await db_session.commit()
    
    # Refresh all logs to get their IDs
    for log in logs:
        await db_session.refresh(log)
    
    return logs


@pytest.fixture
async def business_line_log_factory(db_session: AsyncSession):
    """Factory for creating business line logs with custom parameters"""
    async def _create_log(
        action: str = "Test action",
        previous: str = None,
        user_id: int = None,
        log_type: int = 1,
        procedure_id: int = None,
        host: str = "test.local",
        user_ip: str = "127.0.0.1",
        role_id: int = 1,
        user_agent: str = "Test Agent",
        post_request: str = '{"test": true}'
    ) -> BusinessLineLog:
        
        # Create a test user if user_id not provided
        if user_id is None:
            test_user = UserModel(
                name="Factory",
                paternal_last_name="User",
                email=f"factory_{datetime.now().timestamp()}@test.com",
                cellphone="9999999999",
                password="test_pass"
            )
            db_session.add(test_user)
            await db_session.commit()
            await db_session.refresh(test_user)
            user_id = test_user.id
        
        log = BusinessLineLog(
            action=action,
            previous=previous,
            user_id=user_id,
            log_type=log_type,
            procedure_id=procedure_id,
            host=host,
            user_ip=user_ip,
            role_id=role_id,
            user_agent=user_agent,
            post_request=post_request
        )
        
        db_session.add(log)
        await db_session.commit()
        await db_session.refresh(log)
        
        return log
    
    return _create_log


@pytest.fixture
async def cleanup_business_line_logs(db_session: AsyncSession):
    """Clean up test business line logs after tests"""
    yield
    
    # Clean up test logs (those created by tests)
    result = await db_session.execute(
        select(BusinessLineLog).where(
            BusinessLineLog.action.like("Test%")
        )
    )
    test_logs = result.scalars().all()
    
    for log in test_logs:
        await db_session.delete(log)
    
    await db_session.commit()


@pytest.fixture
async def mock_client_request():
    """Mock request object for testing client info extraction"""
    class MockClient:
        def __init__(self, host="127.0.0.1"):
            self.host = host
    
    class MockHeaders:
        def __init__(self):
            self._headers = {
                "host": "test.local",
                "user-agent": "Test User Agent"
            }
        
        def get(self, key, default=""):
            return self._headers.get(key.lower(), default)
    
    class MockRequest:
        def __init__(self):
            self.client = MockClient()
            self.headers = MockHeaders()
            self.query_params = {"test": "param"}
    
    return MockRequest()


# Utility functions for tests
@pytest.fixture
def log_types_mapping():
    """Mapping of log types for testing"""
    return {
        1: "Autenticación",
        2: "Licencias Comerciales", 
        3: "Aperturas Provisionales",
        4: "Trámites",
        5: "Sistema",
        6: "Reportes",
        7: "Usuarios",
        8: "Configuración"
    }


@pytest.fixture
def sample_actions():
    """Sample actions for testing"""
    return [
        "Usuario inició sesión",
        "Usuario cerró sesión",
        "Creó nueva licencia comercial",
        "Modificó licencia comercial",
        "Aprobó solicitud",
        "Rechazó solicitud",
        "Generó reporte",
        "Exportó datos"
    ]


@pytest.fixture
def date_ranges():
    """Date ranges for testing filters"""
    now = datetime.now()
    return {
        "today": now.date(),
        "yesterday": (now - timedelta(days=1)).date(),
        "last_week": (now - timedelta(days=7)).date(),
        "last_month": (now - timedelta(days=30)).date()
    }


# Performance testing fixtures
@pytest.fixture
async def large_dataset_logs(db_session: AsyncSession, create_test_user):
    """Create a large dataset for performance testing"""
    test_user = await create_test_user(
        email="perf_test@example.com",
        name="Performance",
        paternal_last_name="Test"
    )
    
    logs = []
    base_time = datetime.now() - timedelta(days=365)  # 1 year of data
    
    # Create 1000 logs for performance testing
    for i in range(1000):
        log = BusinessLineLog(
            action=f"Performance test action {i}",
            previous=f"Previous {i}" if i % 10 == 0 else None,
            user_id=test_user.id,
            log_type=(i % 8) + 1,  # All log types
            procedure_id=1000 + i if i % 5 == 0 else None,
            host="perf.test.local",
            user_ip=f"10.0.{(i//255)+1}.{i%255+1}",
            role_id=(i % 3) + 1,
            user_agent="Performance Test Agent",
            post_request=f'{{"perf_test": {i}, "batch": {i//100}}}',
            created_at=base_time + timedelta(hours=i//10, minutes=i%60),
            updated_at=base_time + timedelta(hours=i//10, minutes=i%60)
        )
        logs.append(log)
        
        # Batch insert for better performance
        if len(logs) == 100:
            db_session.add_all(logs)
            await db_session.commit()
            logs = []
    
    # Insert remaining logs
    if logs:
        db_session.add_all(logs)
        await db_session.commit()
    
    return 1000  # Return count of created logs
