import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock
import uuid

from app.main import app
from tests.models_for_testing import UserTestModel, PasswordRecoveryTestModel
from config.security import get_password_hash, verify_password
from config.settings import get_session


class TestPasswordReset:
    """Test cases for password reset functionality"""

    @pytest_asyncio.fixture
    async def test_user(self, db_session: AsyncSession):
        """Create a test user for password reset tests"""
        user = UserTestModel(
            name="Test",
            paternal_last_name="User",
            maternal_last_name="Example",
            cellphone="1234567890",
            email="test@example.com",
            password=get_password_hash("old_password123"),
            is_active=True
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    @pytest_asyncio.fixture
    async def valid_token(self, db_session: AsyncSession, test_user):
        """Create a valid password recovery token"""
        token = str(uuid.uuid4())
        recovery = PasswordRecoveryTestModel(
            email=test_user.email,
            token=token,
            expiration_date=PasswordRecoveryTestModel.get_expiration_time(24),
            used=0
        )
        db_session.add(recovery)
        await db_session.commit()
        return recovery

    @pytest_asyncio.fixture
    async def expired_token(self, db_session: AsyncSession, test_user):
        """Create an expired password recovery token"""
        token = str(uuid.uuid4())
        recovery = PasswordRecoveryTestModel(
            email=test_user.email,
            token=token,
            expiration_date=(datetime.now(timezone.utc) - timedelta(hours=1)).replace(tzinfo=None),  # Expired
            used=0
        )
        db_session.add(recovery)
        await db_session.commit()
        return recovery

    @pytest_asyncio.fixture
    async def used_token(self, db_session: AsyncSession, test_user):
        """Create a used password recovery token"""
        token = str(uuid.uuid4())
        recovery = PasswordRecoveryTestModel(
            email=test_user.email,
            token=token,
            expiration_date=PasswordRecoveryTestModel.get_expiration_time(24),
            used=1  # Already used
        )
        db_session.add(recovery)
        await db_session.commit()
        return recovery

    async def test_request_password_reset_valid_email(self, async_client: AsyncClient, test_user):
        """Test password reset request with valid email"""
        with patch('app.routers.password.send_email') as mock_send_email:
            response = await async_client.post(
                "/v1/password/reset-password-request",
                json={"email": test_user.email}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "Check your inbox" in data["detail"]
            mock_send_email.assert_called_once()

    async def test_request_password_reset_invalid_email(self, async_client: AsyncClient):
        """Test password reset request with non-existent email"""
        response = await async_client.post(
            "/v1/password/reset-password-request",
            json={"email": "nonexistent@example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "If this email exists" in data["detail"]

    async def test_request_password_reset_rate_limiting(self, async_client: AsyncClient, test_user, db_session: AsyncSession):
        """Test rate limiting for password reset requests"""
        # Create a recent token
        recent_token = PasswordRecoveryTestModel(
            email=test_user.email,
            token=str(uuid.uuid4()),
            expiration_date=PasswordRecoveryTestModel.get_expiration_time(24),
            used=0,
            created_at=(datetime.now(timezone.utc) - timedelta(minutes=2)).replace(tzinfo=None)  # 2 minutes ago
        )
        db_session.add(recent_token)
        await db_session.commit()

        with patch('app.routers.password.send_email'):
            response = await async_client.post(
                "/v1/password/reset-password-request",
                json={"email": test_user.email}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert "wait 5 minutes" in data["detail"]

    @patch('app.routers.password.send_email')
    async def test_request_password_reset_email_failure(self, mock_send_email, async_client: AsyncClient, test_user, db_session: AsyncSession):
        """Test password reset request when email sending fails"""
        mock_send_email.side_effect = Exception("Email service unavailable")
        
        response = await async_client.post(
            "/v1/password/reset-password-request",
            json={"email": test_user.email}
        )
        
        assert response.status_code == 500
        
        # Verify token was cleaned up
        stmt = select(PasswordRecoveryTestModel).where(PasswordRecoveryTestModel.email == test_user.email)
        result = await db_session.execute(stmt)
        tokens = result.scalars().all()
        assert len(tokens) == 0

    async def test_reset_password_with_valid_token(self, async_client: AsyncClient, test_user, valid_token, db_session: AsyncSession):
        """Test password reset with valid token"""
        new_password = "new_password123"
        
        response = await async_client.post(
            "/v1/password/change-password",
            json={
                "email": test_user.email,
                "password": new_password,
                "token": valid_token.token
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "successfully updated" in data["detail"]
        
        # Verify password was changed
        await db_session.refresh(test_user)
        assert verify_password(new_password, test_user.password)
        
        # Verify token was cleaned up
        stmt = select(PasswordRecoveryTestModel).where(PasswordRecoveryTestModel.email == test_user.email)
        result = await db_session.execute(stmt)
        tokens = result.scalars().all()
        assert len(tokens) == 0

    async def test_reset_password_with_invalid_token(self, async_client: AsyncClient, test_user):
        """Test password reset with invalid token"""
        response = await async_client.post(
            "/v1/password/change-password",
            json={
                "email": test_user.email,
                "password": "new_password123",
                "token": "invalid_token"
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Invalid or expired token" in data["detail"]

    async def test_reset_password_with_expired_token(self, async_client: AsyncClient, test_user, expired_token, db_session: AsyncSession):
        """Test password reset with expired token"""
        response = await async_client.post(
            "/v1/password/change-password",
            json={
                "email": test_user.email,
                "password": "new_password123",
                "token": expired_token.token
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Invalid or expired token" in data["detail"]
        
        # Verify expired token was cleaned up
        stmt = select(PasswordRecoveryTestModel).where(PasswordRecoveryTestModel.id == expired_token.id)
        result = await db_session.execute(stmt)
        token = result.scalars().first()
        assert token is None

    async def test_reset_password_with_used_token(self, async_client: AsyncClient, test_user, used_token, db_session: AsyncSession):
        """Test password reset with already used token"""
        response = await async_client.post(
            "/v1/password/change-password",
            json={
                "email": test_user.email,
                "password": "new_password123",
                "token": used_token.token
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Invalid or expired token" in data["detail"]

    async def test_reset_password_nonexistent_user(self, async_client: AsyncClient, db_session: AsyncSession):
        """Test password reset for non-existent user with valid token format"""
        # Create a token for non-existent user
        token = str(uuid.uuid4())
        recovery = PasswordRecoveryTestModel(
            email="nonexistent@example.com",
            token=token,
            expiration_date=PasswordRecoveryTestModel.get_expiration_time(24),
            used=0
        )
        db_session.add(recovery)
        await db_session.commit()
        
        response = await async_client.post(
            "/v1/password/change-password",
            json={
                "email": "nonexistent@example.com",
                "password": "new_password123",
                "token": token
            }
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "User not found" in data["detail"]
        
        # Verify orphaned token was cleaned up
        stmt = select(PasswordRecoveryTestModel).where(PasswordRecoveryTestModel.email == "nonexistent@example.com")
        result = await db_session.execute(stmt)
        tokens = result.scalars().all()
        assert len(tokens) == 0


class TestAuthenticatedPasswordChange:
    """Test cases for authenticated password change"""

    @pytest_asyncio.fixture
    async def authenticated_user(self, db_session: AsyncSession):
        """Create an authenticated test user"""
        user = UserTestModel(
            name="Auth",
            paternal_last_name="User",
            maternal_last_name="Example",
            cellphone="1234567890",
            email="auth@example.com",
            password=get_password_hash("current_password123"),
            is_active=True
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user

    async def test_change_password_success(self, async_client: AsyncClient, authenticated_user, db_session: AsyncSession):
        """Test successful password change for authenticated user"""
        from app.main import app
        from config.security import get_current_user
        
        # Override the dependency
        async def mock_get_current_user():
            return authenticated_user
        
        app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            response = await async_client.post(
                "/v1/password/change-authenticated",
                json={
                    "current_password": "current_password123",
                    "new_password": "new_password123"
                }
            )
            
            assert response.status_code == 202
            data = response.json()
            assert "successfully" in data["detail"]
            
            # Verify password was changed
            await db_session.refresh(authenticated_user)
            assert verify_password("new_password123", authenticated_user.password)
            assert not verify_password("current_password123", authenticated_user.password)
        finally:
            # Clean up the override
            app.dependency_overrides.clear()

    async def test_change_password_wrong_current_password(self, async_client: AsyncClient, authenticated_user):
        """Test password change with wrong current password"""
        from app.main import app
        from config.security import get_current_user
        
        # Override the dependency
        async def mock_get_current_user():
            return authenticated_user
        
        app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            response = await async_client.post(
                "/v1/password/change-authenticated",
                json={
                    "current_password": "wrong_password",
                    "new_password": "new_password123"
                }
            )
            
            assert response.status_code == 422
            data = response.json()
            assert "Current password is incorrect" in data["detail"]
        finally:
            # Clean up the override
            app.dependency_overrides.clear()


class TestPasswordRecoveryModel:
    """Test cases for PasswordRecovery model methods"""

    def test_is_expired_false(self):
        """Test is_expired method returns False for valid token"""
        recovery = PasswordRecoveryTestModel(
            email="test@example.com",
            token="test_token",
            expiration_date=(datetime.now(timezone.utc) + timedelta(hours=1)).replace(tzinfo=None),
            used=0
        )
        assert not recovery.is_expired()

    def test_is_expired_true(self):
        """Test is_expired method returns True for expired token"""
        recovery = PasswordRecoveryTestModel(
            email="test@example.com",
            token="test_token",
            expiration_date=(datetime.now(timezone.utc) - timedelta(hours=1)).replace(tzinfo=None),
            used=0
        )
        assert recovery.is_expired()

    def test_is_valid_true(self):
        """Test is_valid method returns True for valid token"""
        recovery = PasswordRecoveryTestModel(
            email="test@example.com",
            token="test_token",
            expiration_date=(datetime.now(timezone.utc) + timedelta(hours=1)).replace(tzinfo=None),
            used=0
        )
        assert recovery.is_valid()

    def test_is_valid_false_expired(self):
        """Test is_valid method returns False for expired token"""
        recovery = PasswordRecoveryTestModel(
            email="test@example.com",
            token="test_token",
            expiration_date=(datetime.now(timezone.utc) - timedelta(hours=1)).replace(tzinfo=None),
            used=0
        )
        assert not recovery.is_valid()

    def test_is_valid_false_used(self):
        """Test is_valid method returns False for used token"""
        recovery = PasswordRecoveryTestModel(
            email="test@example.com",
            token="test_token",
            expiration_date=(datetime.now(timezone.utc) + timedelta(hours=1)).replace(tzinfo=None),
            used=1
        )
        assert not recovery.is_valid()

    def test_get_expiration_time_default(self):
        """Test get_expiration_time with default hours"""
        expiration = PasswordRecoveryTestModel.get_expiration_time()
        expected = (datetime.now(timezone.utc) + timedelta(hours=24)).replace(tzinfo=None)
        # Allow 1 second difference for test execution time
        assert abs((expiration - expected).total_seconds()) < 1

    def test_get_expiration_time_custom(self):
        """Test get_expiration_time with custom hours"""
        expiration = PasswordRecoveryTestModel.get_expiration_time(12)
        expected = (datetime.now(timezone.utc) + timedelta(hours=12)).replace(tzinfo=None)
        # Allow 1 second difference for test execution time
        assert abs((expiration - expected).total_seconds()) < 1


class TestPasswordValidation:
    """Test cases for password validation and schemas"""

    async def test_password_reset_request_invalid_email(self, async_client: AsyncClient):
        """Test password reset request with invalid email format"""
        response = await async_client.post(
            "/v1/password/reset-password-request",
            json={"email": "invalid-email"}
        )
        
        assert response.status_code == 422

    async def test_password_reset_short_password(self, async_client: AsyncClient):
        """Test password reset with password that's too short"""
        response = await async_client.post(
            "/v1/password/change-password",
            json={
                "email": "test@example.com",
                "password": "short",
                "token": "test_token"
            }
        )
        
        assert response.status_code == 422

    async def test_authenticated_password_change_short_password(self, async_client: AsyncClient):
        """Test authenticated password change with short password"""
        from app.main import app
        from config.security import get_current_user
        
        # Create a mock user for authentication
        mock_user = UserTestModel(
            id=1,
            name="Test",
            paternal_last_name="User", 
            maternal_last_name="Example",
            cellphone="1234567890",
            email="test@example.com",
            password=get_password_hash("current_password123"),
            is_active=True
        )
        
        # Override the dependency
        async def mock_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_current_user] = mock_get_current_user
        
        try:
            response = await async_client.post(
                "/v1/password/change-authenticated",
                json={
                    "current_password": "current_password123",
                    "new_password": "short"
                }
            )
        
            assert response.status_code == 422
        finally:
            # Clean up the override
            app.dependency_overrides.clear()
