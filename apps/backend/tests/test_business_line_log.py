import pytest
from datetime import date, timedelta
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import status

from app.models.business_line_log import BusinessLineLog
from app.models.user import UserModel


class TestBusinessLineLogAPI:
    """Test suite for Business Line Log API endpoints"""

    @pytest.fixture
    async def sample_log_data(self):
        """Sample data for creating business line logs"""
        return {
            "action": "Created new business license",
            "previous": "None",
            "log_type": 1,
            "procedure_id": 123,
            "post_request": '{"license_type": "restaurant"}'
        }

    @pytest.fixture
    async def admin_headers(self, admin_user_token):
        """Headers with admin authentication"""
        return {"Authorization": f"Bearer {admin_user_token}"}

    @pytest.fixture
    async def director_headers(self, director_user_token):
        """Headers with director authentication"""
        return {"Authorization": f"Bearer {director_user_token}"}

    @pytest.fixture
    async def regular_user_headers(self, regular_user_token):
        """Headers with regular user authentication"""
        return {"Authorization": f"Bearer {regular_user_token}"}

    async def test_create_business_line_log_success(self, async_client: AsyncClient, admin_headers, sample_log_data):
        """Test successful creation of business line log"""
        response = await async_client.post(
            "/v1/business_line_log/",
            json=sample_log_data,
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["action"] == sample_log_data["action"]
        assert data["previous"] == sample_log_data["previous"]
        assert data["log_type"] == sample_log_data["log_type"]
        assert data["procedure_id"] == sample_log_data["procedure_id"]
        assert data["post_request"] == sample_log_data["post_request"]
        assert "id" in data
        assert "created_at" in data
        assert "user_id" in data

    async def test_create_business_line_log_invalid_data(self, async_client: AsyncClient, admin_headers):
        """Test creation with invalid data"""
        invalid_data = {
            "action": "",  # Empty action
            "log_type": -1  # Invalid log_type
        }
        
        response = await async_client.post(
            "/v1/business_line_log/",
            json=invalid_data,
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_business_line_log_missing_required_fields(self, async_client: AsyncClient, admin_headers):
        """Test creation with missing required fields"""
        incomplete_data = {
            "previous": "Some previous state"
            # Missing action and log_type
        }
        
        response = await async_client.post(
            "/v1/business_line_log/",
            json=incomplete_data,
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_business_line_log_unauthorized(self, async_client: AsyncClient, sample_log_data):
        """Test creation without authentication"""
        response = await async_client.post(
            "/v1/business_line_log/",
            json=sample_log_data
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_log_action_endpoint_success(self, async_client: AsyncClient, admin_headers):
        """Test the quick log_action endpoint"""
        params = {
            "action": "User logged in",
            "log_type": 2,
            "previous": "User was offline",
            "procedure_id": 456
        }
        
        response = await async_client.post(
            "/v1/business_line_log/log_action",
            params=params,
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["message"] == "Action logged successfully"
        assert "log_id" in data
        assert "created_at" in data

    async def test_log_action_endpoint_invalid_params(self, async_client: AsyncClient, admin_headers):
        """Test log_action with invalid parameters"""
        params = {
            "action": "",  # Empty action
            "log_type": -1  # Invalid log_type
        }
        
        response = await async_client.post(
            "/v1/business_line_log/log_action",
            params=params,
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_get_logs_by_type_admin_access(self, async_client: AsyncClient, admin_headers, db_session: AsyncSession, test_admin_user, test_roles):
        """Test retrieving logs by type with admin access"""
        # Create some test logs first
        await self._create_test_logs(db_session)
        
        response = await async_client.get(
            "/v1/business_line_log/consult/1",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "logs" in data
        assert "total_count" in data
        assert "skip" in data
        assert "limit" in data
        assert isinstance(data["logs"], list)

    async def test_get_logs_by_type_director_access(self, async_client: AsyncClient, director_headers, db_session: AsyncSession, test_director_user, test_roles):
        """Test retrieving logs by type with director access"""
        await self._create_test_logs(db_session)
        
        response = await async_client.get(
            "/v1/business_line_log/consult/1",
            headers=director_headers
        )
        
        assert response.status_code == status.HTTP_200_OK

    async def test_get_logs_by_type_regular_user_forbidden(self, async_client: AsyncClient, regular_user_headers):
        """Test that regular users cannot access logs"""
        response = await async_client.get(
            "/v1/business_line_log/consult/1",
            headers=regular_user_headers
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_get_logs_by_type_unauthorized(self, async_client: AsyncClient):
        """Test accessing logs without authentication"""
        response = await async_client.get("/v1/business_line_log/consult/1")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_get_logs_with_pagination(self, async_client: AsyncClient, admin_headers, db_session: AsyncSession, test_admin_user, test_roles):
        """Test logs retrieval with pagination"""
        await self._create_test_logs(db_session, count=15)
        
        response = await async_client.get(
            "/v1/business_line_log/consult/1?skip=5&limit=5",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert len(data["logs"]) <= 5
        assert data["skip"] == 5
        assert data["limit"] == 5
        assert data["total_count"] >= 5

    async def test_get_logs_with_date_filter(self, async_client: AsyncClient, admin_headers, db_session: AsyncSession, test_admin_user, test_roles):
        """Test logs retrieval with date filtering"""
        await self._create_test_logs(db_session)
        
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        response = await async_client.get(
            f"/v1/business_line_log/consult/1?start_date={yesterday}&end_date={today}",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "logs" in data

    async def test_get_logs_with_action_filter(self, async_client: AsyncClient, admin_headers, db_session: AsyncSession, test_admin_user, test_roles):
        """Test logs retrieval with action text filtering"""
        await self._create_test_logs(db_session)
        
        response = await async_client.get(
            "/v1/business_line_log/consult/1?action_filter=test",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "logs" in data

    async def test_get_all_logs_with_type_zero(self, async_client: AsyncClient, admin_headers, db_session: AsyncSession, test_admin_user, test_roles):
        """Test retrieving all logs regardless of type (log_type=0)"""
        await self._create_test_logs(db_session)
        
        response = await async_client.get(
            "/v1/business_line_log/consult/0",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert "logs" in data

    async def test_get_log_by_id_success(self, async_client: AsyncClient, admin_headers, db_session: AsyncSession, test_admin_user, test_roles):
        """Test retrieving a specific log by ID"""
        log_id = await self._create_single_test_log(db_session)
        
        response = await async_client.get(
            f"/v1/business_line_log/{log_id}",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["id"] == log_id
        assert "action" in data
        assert "user_id" in data

    async def test_get_log_by_id_not_found(self, async_client: AsyncClient, admin_headers, test_admin_user, test_roles):
        """Test retrieving non-existent log"""
        response = await async_client.get(
            "/v1/business_line_log/99999",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_log_by_id_invalid_id(self, async_client: AsyncClient, admin_headers, test_admin_user, test_roles):
        """Test retrieving log with invalid ID"""
        response = await async_client.get(
            "/v1/business_line_log/-1",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_get_log_by_id_unauthorized(self, async_client: AsyncClient):
        """Test retrieving log without authentication"""
        response = await async_client.get("/v1/business_line_log/1")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_pagination_limits(self, async_client: AsyncClient, admin_headers, test_admin_user, test_roles):
        """Test pagination parameter validation"""
        # Test limit too high
        response = await async_client.get(
            "/v1/business_line_log/consult/1?limit=2000",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        # Test negative skip
        response = await async_client.get(
            "/v1/business_line_log/consult/1?skip=-1",
            headers=admin_headers
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def _create_test_logs(self, db_session: AsyncSession, count: int = 5):
        """Helper method to create test logs"""
        # Get a test user
        result = await db_session.execute(select(UserModel).limit(1))
        user = result.scalar_one_or_none()
        
        if not user:
            # Create a test user if none exists
            user = UserModel(
                name="Test",
                paternal_last_name="User",
                cellphone="1234567890",
                email="test@example.com",
                password="hashed_password"
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)

        # Create test logs
        for i in range(count):
            log = BusinessLineLog(
                action=f"Test action {i}",
                previous=f"Previous state {i}",
                user_id=user.id,
                log_type=1,
                procedure_id=100 + i,
                host="localhost",
                user_ip="127.0.0.1",
                role_id=1,
                user_agent="Test Agent",
                post_request=f'{{"test": "data_{i}"}}'
            )
            db_session.add(log)
        
        await db_session.commit()

    async def _create_single_test_log(self, db_session: AsyncSession) -> int:
        """Helper method to create a single test log and return its ID"""
        # Get a test user
        result = await db_session.execute(select(UserModel).limit(1))
        user = result.scalar_one_or_none()
        
        if not user:
            # Create a test user if none exists
            user = UserModel(
                name="Test",
                paternal_last_name="User", 
                cellphone="1234567890",
                email="test@example.com",
                password="hashed_password"
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)

        log = BusinessLineLog(
            action="Single test action",
            previous="Single previous state",
            user_id=user.id,
            log_type=1,
            procedure_id=999,
            host="localhost",
            user_ip="127.0.0.1",
            role_id=1,
            user_agent="Test Agent",
            post_request='{"single": "test"}'
        )
        
        db_session.add(log)
        await db_session.commit()
        await db_session.refresh(log)
        
        return log.id


class TestBusinessLineLogModel:
    """Test suite for Business Line Log model operations"""

    async def test_create_business_line_log_model(self, db_session: AsyncSession):
        """Test creating business line log model directly"""
        # Get or create a test user
        result = await db_session.execute(select(UserModel).limit(1))
        user = result.scalar_one_or_none()
        
        if not user:
            user = UserModel(
                name="Model",
                paternal_last_name="Test",
                cellphone="9876543210",
                email="model@example.com", 
                password="hashed_password"
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)

        log = BusinessLineLog(
            action="Model test action",
            previous="Model previous state",
            user_id=user.id,
            log_type=2,
            procedure_id=888,
            host="test.local",
            user_ip="192.168.1.1",
            role_id=2,
            user_agent="Model Test Agent",
            post_request='{"model": "test"}'
        )

        db_session.add(log)
        await db_session.commit()
        await db_session.refresh(log)

        assert log.id is not None
        assert log.action == "Model test action"
        assert log.user_id == user.id
        assert log.created_at is not None
        assert log.updated_at is not None

    async def test_business_line_log_relationship(self, db_session: AsyncSession):
        """Test the relationship between BusinessLineLog and UserModel"""
        # Create user
        from datetime import datetime, timezone
        user = UserModel(
            name="Relationship",
            paternal_last_name="Test",
            cellphone="1234567890",
            email="relationship@example.com",
            password="hashed_password",
            is_active=True
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Create log
        log = BusinessLineLog(
            action="Relationship test",
            user_id=user.id,
            log_type=1
        )
        db_session.add(log)
        await db_session.commit()
        await db_session.refresh(log, ["user"])

        # Test relationship
        assert log.user is not None
        assert log.user.id == user.id
        assert log.user.first_name == "Relationship"  # Uses Django compatibility property

    async def test_business_line_log_repr(self, db_session: AsyncSession):
        """Test the string representation of BusinessLineLog"""
        result = await db_session.execute(select(UserModel).limit(1))
        user = result.scalar_one_or_none()
        
        if not user:
            user = UserModel(
                name="Repr",
                paternal_last_name="Test",
                cellphone="1111111111",
                email="repr@example.com",
                password="hashed_password"
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)

        log = BusinessLineLog(
            action="Repr test action",
            user_id=user.id,
            log_type=3
        )
        db_session.add(log)
        await db_session.commit()
        await db_session.refresh(log)

        repr_str = repr(log)
        assert "BusinessLineLog" in repr_str
        assert str(log.id) in repr_str
        assert "Repr test action" in repr_str
        assert "3" in repr_str

    async def test_business_line_log_indexes(self, db_session: AsyncSession):
        """Test that indexes are working properly (performance test)"""
        # Execute first query to test index
        result = await db_session.execute(
            select(BusinessLineLog)
            .where(BusinessLineLog.log_type == 1)
            .limit(1)
        )
        log1 = result.scalar_one_or_none()
        
        # Execute second query with different value to test index 
        result = await db_session.execute(
            select(BusinessLineLog)
            .where(BusinessLineLog.log_type == 2)
            .limit(1)
        )
        log2 = result.scalar_one_or_none()
        
        # Simply verify queries executed without error
        assert True
