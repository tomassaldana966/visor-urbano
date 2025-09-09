import sys
from pathlib import Path

# Add project paths
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
app_dir = backend_dir / "app"
sys.path.insert(0, str(app_dir))

import pytest
import pytest_asyncio
import httpx
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from unittest.mock import Mock, AsyncMock, MagicMock
import base64
import json
from datetime import datetime, timedelta

# Import FastAPI app and dependencies
from app.main import app
from config.settings import get_db
from config.security import get_current_user
from app.models.requirements import Requirement
from app.models.requirements_query import RequirementsQuery
from app.models.procedures import Procedure
from app.models.municipality import Municipality
from app.models.user import UserModel
from app.schemas.requirements import (
    RequirementResponse,
    RequirementCreate,
    RequirementValidationUpdate,
    FolioValidationResponse,
)


@pytest.fixture
def mock_user():
    """Mock authenticated user with municipality."""
    user = Mock()
    user.id = 1
    user.municipality_id = 1
    user.role_id = 1
    user.email = "test@example.com"
    return user


@pytest.fixture
def mock_user_no_municipality():
    """Mock authenticated user without municipality."""
    user = Mock()
    user.id = 1
    user.municipality_id = None
    user.role_id = 1
    user.email = "test@example.com"
    return user


@pytest.fixture
def mock_admin_user():
    """Mock admin user."""
    user = Mock()
    user.id = 2
    user.municipality_id = 1
    user.role_id = 2
    user.email = "admin@example.com"
    return user


@pytest.fixture
def sample_requirement():
    """Sample requirement data."""
    return Requirement(
        id=1,
        municipality_id=1,
        field_id=1,
        requirement_code="REQ001",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_requirements_query():
    """Sample requirements query data."""
    return RequirementsQuery(
        id=1,
        folio="TEST-FOLIO-001",
        municipality_id=1,
        municipality_name="Test Municipality",
        street="Test Street 123",
        neighborhood="Test Neighborhood",
        scian_code="123456",
        scian_name="Test Business",
        property_area=100.0,
        activity_area=50.0,
        applicant_name="Test Applicant",
        applicant_character="Owner",
        person_type="Physical",
        status=1,
        user_id=0,
        alcohol_sales=False,
        created_at=datetime.now()
    )


@pytest.fixture
def sample_municipality():
    """Sample municipality data."""
    return Municipality(
        id=1,
        name="Test Municipality",
        issue_license=True
    )


class TestHelper:
    """Helper class for test setup and dependency management."""
    
    @staticmethod
    def setup_dependencies(current_user=None, db_session=None):
        """Set up FastAPI dependency overrides for testing."""
        
        if current_user:
            async def override_get_current_user():
                return current_user
            app.dependency_overrides[get_current_user] = override_get_current_user
        
        if db_session:
            async def override_get_db():
                yield db_session
            app.dependency_overrides[get_db] = override_get_db
    
    @staticmethod
    def cleanup_dependencies():
        """Clean up FastAPI dependency overrides."""
        app.dependency_overrides.clear()


class TestRequirementsList:
    """Tests for GET /requirements/ endpoint."""

    @pytest.mark.asyncio
    async def test_list_requirements_success(self, mock_user, sample_requirement):
        """Test successful requirements listing."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Mock query result
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [sample_requirement]
        mock_session.execute.return_value = mock_result
        
        # Define dependency overrides
        async def override_get_current_user():
            return mock_user
            
        async def override_get_db():
            yield mock_session
        
        # Apply dependency overrides
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get("/v1/requirements/")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 1
        finally:
            # Clean up dependency overrides
            app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_list_requirements_no_municipality(self, mock_user_no_municipality):
        """Test requirements listing with user having no municipality."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Define dependency overrides
        async def override_get_current_user():
            return mock_user_no_municipality
            
        async def override_get_db():
            yield mock_session
        
        # Apply dependency overrides
        app.dependency_overrides[get_current_user] = override_get_current_user
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get("/v1/requirements/")
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert "User has no municipality assigned" in response.json()["detail"]
        finally:
            # Clean up dependency overrides
            app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_list_requirements_pagination(self, mock_user, sample_requirement):
        """Test requirements listing with pagination."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Mock query result
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [sample_requirement]
        mock_session.execute.return_value = mock_result
        
        # Setup dependencies
        TestHelper.setup_dependencies(current_user=mock_user, db_session=mock_session)
        
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get("/v1/requirements/?skip=10&limit=5")
            
            assert response.status_code == status.HTTP_200_OK
        finally:
            TestHelper.cleanup_dependencies()


class TestGetRequirement:
    """Tests for GET /requirements/{requirement_id} endpoint."""

    @pytest.mark.asyncio
    async def test_get_requirement_success(self, sample_requirement):
        """Test successful requirement retrieval."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Mock query result
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = sample_requirement
        mock_session.execute.return_value = mock_result
        
        # Setup dependencies
        TestHelper.setup_dependencies(db_session=mock_session)
        
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get("/v1/requirements/1")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["id"] == 1
        finally:
            TestHelper.cleanup_dependencies()

    @pytest.mark.asyncio
    async def test_get_requirement_not_found(self):
        """Test requirement not found."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Mock query result
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_session.execute.return_value = mock_result
        
        # Setup dependencies
        TestHelper.setup_dependencies(db_session=mock_session)
        
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get("/v1/requirements/999")
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert "Requirement not found" in response.json()["detail"]
        finally:
            TestHelper.cleanup_dependencies()


class TestActivateRequirement:
    """Tests for POST /requirements/activate endpoint."""

    @pytest.mark.asyncio
    async def test_activate_requirement_success(self, mock_user, sample_requirement):
        """Test successful requirement activation."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Configure specific methods as non-async
        mock_session.add = Mock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()
        
        # Setup dependencies
        TestHelper.setup_dependencies(current_user=mock_user, db_session=mock_session)
        
        try:
            requirement_data = {
                "municipality_id": 1,
                "field_id": 1,
                "requirement_code": "REQ001"
            }
            
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.post("/v1/requirements/activate", json=requirement_data)
            
            assert response.status_code == status.HTTP_202_ACCEPTED
            data = response.json()
            assert "Requirement activated successfully" in data["message"]
        finally:
            TestHelper.cleanup_dependencies()

    @pytest.mark.asyncio
    async def test_activate_requirement_no_municipality(self, mock_user_no_municipality):
        """Test requirement activation with user having no municipality."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Setup dependencies
        TestHelper.setup_dependencies(current_user=mock_user_no_municipality, db_session=mock_session)
        
        try:
            requirement_data = {
                "municipality_id": 1,
                "field_id": 1,
                "requirement_code": "REQ001"
            }
            
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.post("/v1/requirements/activate", json=requirement_data)
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
        finally:
            TestHelper.cleanup_dependencies()


class TestDeactivateRequirement:
    """Tests for DELETE /requirements/{requirement_id}/deactivate endpoint."""

    @pytest.mark.asyncio
    async def test_deactivate_requirement_success(self, sample_requirement):
        """Test successful requirement deactivation."""
        # Mock database session
        mock_session = AsyncMock()
        
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = sample_requirement
        mock_session.execute.return_value = mock_result
        
        # Configure specific methods as non-async for db operations
        mock_session.delete = AsyncMock()
        mock_session.commit = AsyncMock()
        
        # Setup dependencies
        TestHelper.setup_dependencies(db_session=mock_session)
        
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.delete("/v1/requirements/1/deactivate")
            
            assert response.status_code == status.HTTP_202_ACCEPTED
            data = response.json()
            assert "Requirement deactivated successfully" in data["message"]
        finally:
            TestHelper.cleanup_dependencies()

    @pytest.mark.asyncio
    async def test_deactivate_requirement_not_found(self):
        """Test requirement deactivation when requirement not found."""
        # Mock database session
        mock_session = AsyncMock()
        
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_session.execute.return_value = mock_result
        
        # Setup dependencies
        TestHelper.setup_dependencies(db_session=mock_session)
        
        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.delete("/v1/requirements/999/deactivate")
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
        finally:
            TestHelper.cleanup_dependencies()


class TestValidateFolioRequirements:
    """Tests for GET /requirements/validate/folio/{encoded_folio} endpoint."""

    @pytest.mark.asyncio
    async def test_validate_folio_success(self, mock_user, sample_requirements_query, sample_municipality):
        """Test successful folio validation."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Mock requirements queries result
        mock_req_result = Mock()
        mock_req_result.scalars.return_value.all.return_value = [sample_requirements_query]
        
        # Mock municipality result
        mock_muni_result = Mock()
        mock_muni_result.scalars.return_value.first.return_value = sample_municipality
        
        mock_session.execute.side_effect = [mock_req_result, mock_muni_result]
        
        # Setup dependencies
        TestHelper.setup_dependencies(current_user=mock_user, db_session=mock_session)
        
        try:
            # Encode folio
            test_folio = "TEST-FOLIO-001"
            encoded_folio = base64.b64encode(test_folio.encode()).decode()
            
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get(f"/v1/requirements/validate/folio/{encoded_folio}")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]["folio"] == test_folio
        finally:
            TestHelper.cleanup_dependencies()

    @pytest.mark.asyncio
    async def test_validate_folio_invalid_encoding(self, mock_user):
        """Test folio validation with invalid base64 encoding."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Setup dependencies
        TestHelper.setup_dependencies(current_user=mock_user, db_session=mock_session)
        
        try:
            invalid_folio = "invalid-base64!"
            
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get(f"/v1/requirements/validate/folio/{invalid_folio}")
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert "Invalid folio encoding" in response.json()["detail"]
        finally:
            TestHelper.cleanup_dependencies()

    @pytest.mark.asyncio
    async def test_validate_folio_not_found(self, mock_user):
        """Test folio validation when folio not found."""
        # Mock database session
        mock_session = AsyncMock()
        
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result
        
        # Setup dependencies
        TestHelper.setup_dependencies(current_user=mock_user, db_session=mock_session)
        
        try:
            test_folio = "NONEXISTENT-FOLIO"
            encoded_folio = base64.b64encode(test_folio.encode()).decode()
            
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get(f"/v1/requirements/validate/folio/{encoded_folio}")
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert "procedure folio does not exist" in response.json()["detail"]
        finally:
            TestHelper.cleanup_dependencies()

    @pytest.mark.asyncio
    async def test_validate_folio_municipality_not_online(self, mock_user, sample_requirements_query):
        """Test folio validation when municipality doesn't allow online procedures."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Mock requirements queries result
        mock_req_result = Mock()
        mock_req_result.scalars.return_value.all.return_value = [sample_requirements_query]
        
        # Mock municipality result (not allowing online procedures)
        offline_municipality = Municipality(
            id=1,
            name="Offline Municipality",
            issue_license=False
        )
        mock_muni_result = Mock()
        mock_muni_result.scalars.return_value.first.return_value = offline_municipality
        
        mock_session.execute.side_effect = [mock_req_result, mock_muni_result]
        
        # Setup dependencies
        TestHelper.setup_dependencies(current_user=mock_user, db_session=mock_session)
        
        try:
            test_folio = "TEST-FOLIO-001"
            encoded_folio = base64.b64encode(test_folio.encode()).decode()
            
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.get(f"/v1/requirements/validate/folio/{encoded_folio}")
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert "not available for online procedures" in response.json()["detail"]
        finally:
            TestHelper.cleanup_dependencies()


class TestUpdateFolioRequirements:
    """Tests for PUT /requirements/validate/folio/{requirements_query_id} endpoint."""

    @pytest.mark.asyncio
    async def test_update_folio_create_procedure(self, mock_user, sample_requirements_query):
        """Test updating folio validation and creating new procedure."""
        # Let's take a direct approach by patching the actual function and testing its result
        # This avoids the issues with FastAPI dependencies and authentication
        
        # Import the actual function we want to test
        from app.routers.requirements import update_folio_requirements
        
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock requirements query result
        mock_req_result = Mock()
        mock_req_result.scalars.return_value.first.return_value = sample_requirements_query
        
        # Mock procedure result (no existing procedure)
        mock_proc_result = Mock()
        mock_proc_result.scalars.return_value.all.return_value = []
        
        # Set up return values for the db.execute calls
        mock_db.execute.side_effect = [mock_req_result, mock_proc_result]
        
        # Create mock implementations of the async methods
        def mock_add_impl(obj):
            # Set procedure properties for testing (this is synchronous, not async)
            obj.id = 1
            obj.folio = "TEST-FOLIO-001"
            return None
        
        async def mock_commit():
            return None
            
        async def mock_refresh(obj):
            return None
        
        # Configure the mock methods
        mock_db.add = Mock(side_effect=mock_add_impl)  # Synchronous Mock
        mock_db.commit = AsyncMock(side_effect=mock_commit)
        mock_db.refresh = AsyncMock(side_effect=mock_refresh)
        
        # Create validation data using the proper schema
        from app.schemas.requirements import RequirementValidationUpdate
        validation_data = RequirementValidationUpdate(user_id=mock_user.id)
        
        # Call the function directly, bypassing all the FastAPI machinery
        result = await update_folio_requirements(
            requirements_query_id=1,
            validation_data=validation_data,
            current_user=mock_user,
            db=mock_db
        )
        
        # Assert that the function returned the expected result
        assert "message" in result
        assert "Procedure created successfully" in result["message"]
        assert "procedure_id" in result
        assert "folio" in result
        
        # Verify the mock methods were called
        assert mock_db.add.call_count == 1
        assert mock_db.commit.call_count == 2  # Once for updating the query, once for the procedure
        assert mock_db.refresh.call_count == 1

    @pytest.mark.asyncio
    async def test_update_folio_existing_procedure_access_granted(self, mock_user, sample_requirements_query):
        """Test updating folio validation with existing procedure - access granted."""
        # Mock database session
        mock_session = AsyncMock()
        
        # Set user_id to match current user
        sample_requirements_query.user_id = mock_user.id
        
        # Mock requirements query result
        mock_req_result = Mock()
        mock_req_result.scalars.return_value.first.return_value = sample_requirements_query
        
        # Mock existing procedure with user_id matching the current user
        existing_procedure = Mock()
        existing_procedure.id = 1
        existing_procedure.folio = "TEST-FOLIO-001"
        existing_procedure.user_id = mock_user.id  # Set the user_id to match current user
        existing_procedure.window_user_id = None
        
        mock_proc_result = Mock()
        mock_proc_result.scalars.return_value.all.return_value = [existing_procedure]
        
        mock_session.execute.side_effect = [mock_req_result, mock_proc_result]
        
        # Setup dependencies
        TestHelper.setup_dependencies(current_user=mock_user, db_session=mock_session)
        
        try:
            validation_data = {"user_id": mock_user.id}
            
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.put("/v1/requirements/validate/folio/1", json=validation_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "Procedure access granted" in data["message"]
        finally:
            TestHelper.cleanup_dependencies()

    @pytest.mark.asyncio
    async def test_update_folio_existing_procedure_access_denied(self, mock_user, sample_requirements_query):
        """Test updating folio validation with existing procedure - access denied."""
        try:
            # Set user_id to different user (not 0, not current user)
            sample_requirements_query.user_id = 999
            
            # Mock requirements query result
            mock_req_result = Mock()
            mock_req_result.scalars.return_value.first.return_value = sample_requirements_query
            
            # Mock existing procedure with user_id different from mock_user.id
            existing_procedure = Mock()
            existing_procedure.id = 1
            existing_procedure.folio = "TEST-FOLIO-001"
            existing_procedure.user_id = 999  # Different from mock_user.id
            existing_procedure.window_user_id = None
            
            mock_proc_result = Mock()
            mock_proc_result.scalars.return_value.all.return_value = [existing_procedure]
            
            mock_session = AsyncMock()
            mock_session.execute.side_effect = [mock_req_result, mock_proc_result]
            
            TestHelper.setup_dependencies(current_user=mock_user, db_session=mock_session)
            
            validation_data = {"user_id": mock_user.id}
            
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.put("/v1/requirements/validate/folio/1", json=validation_data)
            
            assert response.status_code == status.HTTP_403_FORBIDDEN
            assert "Access denied to this procedure" in response.json()["detail"]
        finally:
            TestHelper.cleanup_dependencies()

    @pytest.mark.asyncio
    async def test_update_folio_admin_user_access(self, mock_admin_user, sample_requirements_query):
        """Test updating folio validation with admin user - should have access."""
        # Mock database session
        mock_session = AsyncMock()

        try:
            # Set user_id to different user
            sample_requirements_query.user_id = 999

            # Mock requirements query result
            mock_req_result = Mock()
            mock_req_result.scalars.return_value.first.return_value = sample_requirements_query

            # Mock existing procedure
            existing_procedure = Mock()
            existing_procedure.id = 1
            existing_procedure.folio = "TEST-FOLIO-001"
            mock_proc_result = Mock()
            mock_proc_result.scalars.return_value.all.return_value = [existing_procedure]

            mock_session.execute.side_effect = [mock_req_result, mock_proc_result]

            TestHelper.setup_dependencies(current_user=mock_admin_user, db_session=mock_session)

            validation_data = {"user_id": mock_admin_user.id}

            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.put("/v1/requirements/validate/folio/1", json=validation_data)

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "Procedure access granted" in data["message"]
        finally:
            TestHelper.cleanup_dependencies()

    @pytest.mark.asyncio
    async def test_update_folio_requirements_query_not_found(self, mock_user):
        """Test updating folio validation when requirements query not found."""
        try:
            # Mock requirements query result (not found)
            mock_result = Mock()
            mock_result.scalars.return_value.first.return_value = None
            
            mock_session = AsyncMock()
            mock_session.execute.return_value = mock_result
            
            TestHelper.setup_dependencies(mock_user, mock_session)
            
            validation_data = {"user_id": mock_user.id}
            
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.put("/v1/requirements/validate/folio/999", json=validation_data)
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            assert "Requirements query not found" in response.json()["detail"]
        finally:
            TestHelper.cleanup_dependencies()


if __name__ == "__main__":
    pytest.main([__file__])
