"""
Comprehensive tests for business_types router endpoints.

This test suite covers:
1. POST /business_types/disable - Disable business type
2. POST /business_types/disable/status/{status} - Update disabled status
3. POST /business_types/disable/certificate/{status} - Update certificate status
4. DELETE /business_types/disable/{id} - Delete disabled configuration
5. GET /business_types/enabled - Get enabled business types
6. GET /business_types/disabled - Get disabled business types
7. GET /business_types/all - Get all business types

Tests include success cases, error scenarios, validation, and edge cases.
"""
import sys
from pathlib import Path

# Add project paths
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
app_dir = backend_dir / "app"
sys.path.insert(0, str(app_dir))

import pytest
import pytest_asyncio
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime

# Mock WeasyPrint before importing anything that might use it
sys.modules['weasyprint'] = Mock()

# Import router directly to avoid WeasyPrint dependency
try:
    sys.path.insert(0, str(app_dir / "routers"))
    from business_types import router
except ImportError:
    # If direct import fails due to WeasyPrint, create a mock router
    from fastapi import APIRouter
    router = APIRouter()
    # We'll mock the actual endpoint functions in the tests
from app.models.business_types import BusinessType
from app.models.business_type_config import BusinessTypeConfig
from app.schemas.business_types import BusinessTypeResponse, BusinessTypeDisable
from app.schemas.business_type_config import BusinessTypeImpactRequest
from config.settings import get_db
from config.security import get_current_user

# Create test app
app = FastAPI()
app.include_router(router, prefix="/v1/business_types")

# Mock data
MOCK_BUSINESS_TYPE_CONFIGS = [
    {
        "id": 1,
        "business_type_id": 1,
        "municipality_id": 1,
        "is_disabled": False,
        "has_certificate": True,
        "impact_level": None,
        "name": "Restaurant",
        "description": "Food service establishment",
        "code": "REST001",
        "related_words": "food, dining, restaurant"
    },
    {
        "id": 2,
        "business_type_id": 2,
        "municipality_id": 1,
        "is_disabled": False,
        "has_certificate": False,
        "impact_level": None,
        "name": "Retail Store",
        "description": "General retail establishment",
        "code": "RET001",
        "related_words": "store, retail, shop"
    },
    {
        "id": 3,
        "business_type_id": 3,
        "municipality_id": 1,
        "is_disabled": True,
        "has_certificate": True,
        "impact_level": None,
        "name": "Bar",
        "description": "Alcoholic beverage establishment",
        "code": "BAR001",
        "related_words": "bar, alcohol, drinks"
    }
]

MOCK_DISABLED_BUSINESS_TYPES = [
    {
        "id": 1,
        "business_type_id": 3,
        "reason": "License suspended",
        "disabled_by_user_id": 1,
        "municipality_id": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

class TestBusinessTypesEndpoints:
    """Tests for business types router endpoints."""

    @pytest.fixture
    def mock_user(self):
        """Create a mock user."""
        user = Mock()
        user.id = 1
        user.municipality_id = 1
        user.role_id = 1
        return user

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def mock_db_session(self):
        """Create mock database session."""
        return AsyncMock()
        
    @pytest.fixture
    def setup_db_patching(self):
        """Set up patching for SQLAlchemy interactions."""
        # We'll patch SQLAlchemy's select function to return a mockable object
        # that doesn't break when used in the router
        select_patch = patch('app.routers.business_types.select', 
                            return_value=Mock(
                                where=lambda *args: Mock(
                                    where=lambda *args: "mock_statement"
                                )
                            ))
        
        # Start the patch
        mock_select = select_patch.start()
        
        # Yield to allow test to run
        yield mock_select
        
        # Stop the patch after test completes
        select_patch.stop()

    @pytest.fixture
    def sample_business_types(self):
        """Create sample business type config objects."""
        business_types = []
        for data in MOCK_BUSINESS_TYPE_CONFIGS:
            business_type = Mock()
            # Set all attributes directly as properties, not specs
            for key, value in data.items():
                setattr(business_type, key, value)
            # Add business_type relationship mock
            business_type.business_type = Mock()
            business_type.business_type.name = data.get("name", "Mock Business Type")
            business_type.business_type.description = data.get("description", "Mock Description")
            business_type.business_type.code = data.get("code", "MOCK001")
            business_type.business_type.related_words = data.get("related_words", "mock, test")
            # Make sure these are actual strings and not mock objects
            business_type.code = data.get("code", "MOCK001")
            business_type.related_words = data.get("related_words", "mock, test")
            business_types.append(business_type)
        return business_types

    def test_get_enabled_business_types(self, client, mock_db_session, sample_business_types):
        """Test GET /business_types/enabled endpoint."""
        # Filter enabled business types (is_disabled = False)
        enabled_types = [bt for bt in sample_business_types if not bt.is_disabled]
        
        # Set up the response object with all required fields
        for bt in enabled_types:
            # Ensure business_type is properly mocked
            if not hasattr(bt, 'business_type'):
                bt.business_type = Mock()
                bt.business_type.name = bt.name
                bt.business_type.description = bt.description
                bt.business_type.code = bt.code
                bt.business_type.related_words = bt.related_words
            
            # Make sure all required fields are strings, not mock objects
            bt.code = str(bt.code) if bt.code else "TEST001"
            bt.related_words = str(bt.related_words) if bt.related_words else "test, keywords"
            bt.name = str(bt.name) if bt.name else "Test Business Type"
            bt.description = str(bt.description) if bt.description else "Test Description"
        
        # Mock database query
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = enabled_types
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/business_types/enabled?municipality_id=1")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 2  # Only enabled types (is_disabled=False)
            assert all(not item["is_disabled"] for item in data)
        finally:
            app.dependency_overrides.clear()

    def test_get_disabled_business_types(self, client, mock_db_session, sample_business_types):
        """Test GET /business_types/disabled endpoint."""
        # Filter disabled business types
        disabled_types = [bt for bt in sample_business_types if bt.is_disabled]
        
        # Set up the response object with all required fields
        for bt in disabled_types:
            # Ensure business_type is properly mocked
            if not hasattr(bt, 'business_type'):
                bt.business_type = Mock()
                bt.business_type.name = bt.name
                bt.business_type.description = bt.description
                bt.business_type.code = bt.code
                bt.business_type.related_words = bt.related_words
            
            # Make sure all required fields are strings, not mock objects
            bt.code = str(bt.code) if bt.code else "TEST001"
            bt.related_words = str(bt.related_words) if bt.related_words else "test, keywords"
            bt.name = str(bt.name) if bt.name else "Test Business Type"
            bt.description = str(bt.description) if bt.description else "Test Description"
        
        # Mock database query
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = disabled_types
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/business_types/disabled?municipality_id=1")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 1  # Only disabled types
            assert all(item["is_disabled"] for item in data)
        finally:
            app.dependency_overrides.clear()

    def test_get_all_business_types(self, client, mock_db_session, sample_business_types, mock_user):
        """Test GET /business_types/all endpoint."""
        # Set up the response object with all required fields
        for bt in sample_business_types:
            # Ensure business_type is properly mocked
            if not hasattr(bt, 'business_type'):
                bt.business_type = Mock()
                bt.business_type.name = bt.name
                bt.business_type.description = bt.description
                bt.business_type.code = bt.code
                bt.business_type.related_words = bt.related_words
            
            # Make sure all required fields are strings, not mock objects
            bt.code = str(bt.code) if bt.code else "TEST001"
            bt.related_words = str(bt.related_words) if bt.related_words else "test, keywords"
            bt.name = str(bt.name) if bt.name else "Test Business Type"
            bt.description = str(bt.description) if bt.description else "Test Description"
        
        # Mock database query
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = sample_business_types
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.get("/v1/business_types/all")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 3  # All business types
            assert data[0]["name"] == "Restaurant"
            assert data[2]["name"] == "Bar"
        finally:
            app.dependency_overrides.clear()

    def test_disable_business_type(self, client, mock_db_session, mock_user):
        """Test POST /business_types/disable endpoint."""
        disable_data = {
            "business_type_id": 1,
            "municipality_id": 1
        }
        
        # Create a comprehensive mock that will work with pydantic serialization
        mock_business_type = Mock()
        mock_business_type.name = "Test Business Type"
        mock_business_type.description = "Test Description"
        mock_business_type.code = "TEST001"
        mock_business_type.related_words = "test, business"
        
        # Create a mock config that behaves like the actual object after refresh
        final_mock_config = Mock()
        final_mock_config.id = 1
        final_mock_config.business_type_id = 1
        final_mock_config.municipality_id = 1
        final_mock_config.is_disabled = True
        final_mock_config.has_certificate = False
        final_mock_config.impact_level = None
        final_mock_config.name = "Test Business Type"
        final_mock_config.description = "Test Description"
        final_mock_config.code = "TEST001"
        final_mock_config.related_words = "test, business"
        final_mock_config.business_type = mock_business_type
        
        # Mock database operations
        created_obj = None
        
        def mock_add(obj):
            nonlocal created_obj
            created_obj = obj
            # Set properties to make it work with the endpoint
            obj.id = 1
        
        def mock_refresh(obj):
            # Replace the object's attributes with our final mock values
            obj.id = final_mock_config.id
            obj.business_type_id = final_mock_config.business_type_id
            obj.municipality_id = final_mock_config.municipality_id
            obj.is_disabled = final_mock_config.is_disabled
            obj.has_certificate = final_mock_config.has_certificate
            obj.impact_level = final_mock_config.impact_level
            obj.name = final_mock_config.name
            obj.description = final_mock_config.description
            obj.code = final_mock_config.code
            obj.related_words = final_mock_config.related_words
        
        mock_db_session.add = Mock(side_effect=mock_add)
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock(side_effect=mock_refresh)
        
        # Mock the query result (no existing record)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.post("/v1/business_types/disable", json=disable_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["business_type_id"] == 1
            assert data["is_disabled"] == True
            assert data["has_certificate"] == False
            assert data["name"] == "Test Business Type"
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
            mock_db_session.refresh.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_update_disabled_status(self, client, mock_db_session, mock_user):
        """Test POST /business_types/disable/status/{status} endpoint."""
        update_data = {
            "business_type_id": 1,
            "municipality_id": 1
        }
        
        # Mock existing disabled business type
        mock_disabled_type = Mock()
        mock_disabled_type.id = 1
        mock_disabled_type.business_type_id = 1
        mock_disabled_type.municipality_id = 1
        mock_disabled_type.is_disabled = True
        mock_disabled_type.has_certificate = False
        mock_disabled_type.impact_level = 1
        mock_disabled_type.name = "Test Business Type"
        mock_disabled_type.description = "Test Description"
        mock_disabled_type.code = "TEST001"
        mock_disabled_type.related_words = "test, business"
        
        # Mock business_type relationship with actual string values
        mock_disabled_type.business_type = Mock()
        mock_disabled_type.business_type.name = "Test Business Type"
        mock_disabled_type.business_type.description = "Test Description"
        mock_disabled_type.business_type.code = "TEST001"
        mock_disabled_type.business_type.related_words = "test, business"
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_disabled_type
        mock_db_session.execute.return_value = mock_result
        mock_db_session.commit = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            # Test enabling (status=1 should set is_disabled to True)
            response = client.post("/v1/business_types/disable/status/1", json=update_data)
            
            assert response.status_code == status.HTTP_200_OK
            assert mock_disabled_type.is_disabled == True  # Should be set to bool(1) = True
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_update_certificate_status(self, client, mock_db_session, mock_user):
        """Test POST /business_types/disable/certificate/{status} endpoint."""
        update_data = {
            "business_type_id": 1,
            "municipality_id": 1,
            "status": True
        }
        
        # Mock existing business type
        mock_business_type = Mock()
        mock_business_type.id = 1
        mock_business_type.business_type_id = 1
        mock_business_type.municipality_id = 1
        mock_business_type.is_disabled = False
        mock_business_type.has_certificate = False
        mock_business_type.impact_level = 1
        mock_business_type.name = "Test Business Type"
        mock_business_type.description = "Test Description"
        mock_business_type.code = "TEST001"
        mock_business_type.related_words = "test, business"
        
        # Mock business_type relationship with actual string values
        mock_business_type.business_type = Mock()
        mock_business_type.business_type.name = "Test Business Type"
        mock_business_type.business_type.description = "Test Description"
        mock_business_type.business_type.code = "TEST001"
        mock_business_type.business_type.related_words = "test, business"
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_business_type
        mock_db_session.execute.return_value = mock_result
        mock_db_session.commit = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            # Test with status=1 (should set has_certificate to True)
            response = client.post("/v1/business_types/disable/certificate/1", json=update_data)
            
            assert response.status_code == status.HTTP_200_OK
            assert mock_business_type.has_certificate == True  # Should be set to bool(1) = True
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_delete_disabled_configuration(self, client, mock_db_session, mock_user):
        """Test DELETE /business_types/disable/{id} endpoint."""
        # Mock database operations
        mock_db_session.execute = AsyncMock()
        mock_db_session.commit = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.delete("/v1/business_types/disable/1")
            
            assert response.status_code == status.HTTP_204_NO_CONTENT
            mock_db_session.execute.assert_called_once()
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_delete_disabled_configuration_not_found(self, client, mock_db_session, mock_user):
        """Test DELETE /business_types/disable/{id} with non-existent ID."""
        # Mock database operations
        mock_db_session.execute = AsyncMock()
        mock_db_session.commit = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.delete("/v1/business_types/disable/999")
            
            # The endpoint always returns 204 even if the record doesn't exist
            assert response.status_code == status.HTTP_204_NO_CONTENT
            mock_db_session.execute.assert_called_once()
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_disable_business_type_validation_error(self, client, mock_user):
        """Test POST /business_types/disable with invalid data."""
        invalid_data = {
            "business_type_id": "invalid",  # Should be integer
            "municipality_id": "also_invalid"  # Should be integer
        }
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.post("/v1/business_types/disable", json=invalid_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        finally:
            app.dependency_overrides.clear()

    def test_update_status_not_found(self, client, mock_db_session, mock_user):
        """Test POST /business_types/disable/status/{status} with non-existent configuration."""
        update_data = {
            "business_type_id": 999,
            "municipality_id": 1
        }

        # Create a final mock object that will be returned after creation
        final_mock_config = Mock()
        final_mock_config.id = 1
        final_mock_config.business_type_id = 999
        final_mock_config.municipality_id = 1
        final_mock_config.is_disabled = True  # status=1 sets to bool(1) = True
        final_mock_config.has_certificate = False
        final_mock_config.impact_level = 0
        final_mock_config.name = "Test Business Type"
        final_mock_config.description = "Test Description"
        final_mock_config.code = "TEST001"
        final_mock_config.related_words = "test, business"

        # Mock business_type relationship
        mock_business_type = Mock()
        mock_business_type.name = "Test Business Type"
        mock_business_type.description = "Test Description"
        mock_business_type.code = "TEST001"
        mock_business_type.related_words = "test, business"
        final_mock_config.business_type = mock_business_type

        # Track the created object
        created_obj = None

        def mock_add(obj):
            nonlocal created_obj
            created_obj = obj
            # Set basic properties
            obj.id = None  # Will be set by refresh
        
        def mock_refresh(obj):
            # Set all the final values on the object
            obj.id = final_mock_config.id
            obj.business_type_id = final_mock_config.business_type_id
            obj.municipality_id = final_mock_config.municipality_id
            obj.is_disabled = final_mock_config.is_disabled
            obj.has_certificate = final_mock_config.has_certificate
            obj.impact_level = final_mock_config.impact_level
            obj.name = final_mock_config.name
            obj.description = final_mock_config.description
            obj.code = final_mock_config.code
            obj.related_words = final_mock_config.related_words
        
        mock_db_session.add = Mock(side_effect=mock_add)
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock(side_effect=mock_refresh)
        
        # Mock database query - not found initially, then return our final config
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        
        # Second query result for loading business_type relationship
        mock_final_result = Mock()
        mock_final_result.scalar_one.return_value = final_mock_config
        
        mock_db_session.execute.side_effect = [mock_result, mock_final_result]
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            # Use patch to mock the BusinessTypeConfig constructor
            with patch('app.routers.business_types.BusinessTypeConfig', return_value=final_mock_config):
                response = client.post("/v1/business_types/disable/status/1", json=update_data)
            
            # The endpoint creates a new record if not found, so it should return 200
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["business_type_id"] == 999
            assert data["is_disabled"] == True
            assert data["has_certificate"] == False
            assert data["name"] == "Test Business Type"
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_update_certificate_not_found(self, client, mock_db_session, mock_user):
        """Test POST /business_types/disable/certificate/{status} with non-existent business type."""
        update_data = {
            "business_type_id": 999,
            "municipality_id": 1,
            "status": True
        }
        
        # Create a final mock object that will be returned after creation
        final_mock_config = Mock()
        final_mock_config.id = 1
        final_mock_config.business_type_id = 999
        final_mock_config.municipality_id = 1
        final_mock_config.is_disabled = False
        final_mock_config.has_certificate = True  # status=1 sets to bool(1) = True
        final_mock_config.impact_level = 0
        final_mock_config.name = "Test Business Type"
        final_mock_config.description = "Test Description"
        final_mock_config.code = "TEST001"
        final_mock_config.related_words = "test, business"
        
        # Mock business_type relationship
        mock_business_type = Mock()
        mock_business_type.name = "Test Business Type"
        mock_business_type.description = "Test Description"
        mock_business_type.code = "TEST001"
        mock_business_type.related_words = "test, business"
        final_mock_config.business_type = mock_business_type
        
        # Track the created object
        created_obj = None
        
        def mock_add(obj):
            nonlocal created_obj
            created_obj = obj
            # Set basic properties
            obj.id = None  # Will be set by refresh

        def mock_refresh(obj):
            # Set all the final values on the object
            obj.id = final_mock_config.id
            obj.business_type_id = final_mock_config.business_type_id
            obj.municipality_id = final_mock_config.municipality_id
            obj.is_disabled = final_mock_config.is_disabled
            obj.has_certificate = final_mock_config.has_certificate
            obj.impact_level = final_mock_config.impact_level
            obj.name = final_mock_config.name
            obj.description = final_mock_config.description
            obj.code = final_mock_config.code
            obj.related_words = final_mock_config.related_words
        
        mock_db_session.add = Mock(side_effect=mock_add)
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock(side_effect=mock_refresh)
        
        # Mock database query - not found initially, then return our final config
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        
        # Second query result for loading business_type relationship
        mock_final_result = Mock()
        mock_final_result.scalar_one.return_value = final_mock_config
        
        mock_db_session.execute.side_effect = [mock_result, mock_final_result]
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            # Use patch to mock the BusinessTypeConfig constructor
            with patch('app.routers.business_types.BusinessTypeConfig', return_value=final_mock_config):
                response = client.post("/v1/business_types/disable/certificate/1", json=update_data)
            
            # The endpoint creates a new record if not found, so it should return 200
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["business_type_id"] == 999
            assert data["is_disabled"] == False
            assert data["has_certificate"] == True
            assert data["name"] == "Test Business Type"
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.parametrize("status_value,expected_has_certificate", [
        (1, True),   # status=1 should set has_certificate to True (bool(1))
        (0, False),  # status=0 should set has_certificate to False (bool(0))
    ])
    def test_update_certificate_various_statuses(self, client, mock_db_session, mock_user, status_value, expected_has_certificate):
        """Test certificate status updates with various status values."""
        update_data = {
            "business_type_id": 1,
            "municipality_id": 1,
            "status": True
        }
        
        # Mock existing business type with all required fields for response validation
        mock_business_type = Mock()
        mock_business_type.id = 1
        mock_business_type.business_type_id = 1
        mock_business_type.municipality_id = 1
        mock_business_type.is_disabled = False
        mock_business_type.has_certificate = True  # Start with True
        mock_business_type.impact_level = 0
        mock_business_type.name = "Test Business Type"
        mock_business_type.description = "Test Description"
        mock_business_type.code = "TEST001"
        mock_business_type.related_words = "test, business"
        
        # Mock business_type relationship with actual string values
        mock_business_type.business_type = Mock()
        mock_business_type.business_type.name = "Test Business Type"
        mock_business_type.business_type.description = "Test Description"
        mock_business_type.business_type.code = "TEST001"
        mock_business_type.business_type.related_words = "test, business"
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = mock_business_type
        mock_db_session.execute.return_value = mock_result
        mock_db_session.commit = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.post(f"/v1/business_types/disable/certificate/{status_value}", json=update_data)
            
            assert response.status_code == status.HTTP_200_OK
            assert mock_business_type.has_certificate == expected_has_certificate
        finally:
            app.dependency_overrides.clear()

    def test_get_business_types_empty_list(self, client, mock_db_session, mock_user):
        """Test endpoints when no business types exist."""
        # Mock empty result
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.get("/v1/business_types/all")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 0
        finally:
            app.dependency_overrides.clear()

    def test_create_business_type_success(self, client, mock_db_session, mock_user):
        """Test POST /business_types/ endpoint with valid data."""
        create_data = {
            "name": "New Business Type",
            "description": "A new type of business",
            "is_active": True,
            "code": "NEW001",
            "related_words": "new, business, type"
        }
        
        # Mock the created business type instance
        mock_business_type = Mock()
        mock_business_type.id = 1
        mock_business_type.name = create_data["name"]
        mock_business_type.description = create_data["description"]
        mock_business_type.is_active = create_data["is_active"]
        mock_business_type.code = create_data["code"]
        mock_business_type.related_words = create_data["related_words"]
        
        # Mock database operations
        mock_db_session.add = Mock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock(side_effect=lambda x: setattr(x, 'id', 1))
        
        # Mock the query results (no existing business type with same name or code)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        def override_require_admin_or_director_role():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            with patch.object(BusinessType, '__new__', return_value=mock_business_type):
                response = client.post("/v1/business_types/", json=create_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["name"] == create_data["name"]
            assert data["description"] == create_data["description"]
            assert data["code"] == create_data["code"]
            assert data["related_words"] == create_data["related_words"]
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
            mock_db_session.refresh.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_create_business_type_duplicate_name(self, client, mock_db_session, mock_user):
        """Test POST /business_types/ endpoint with duplicate name."""
        create_data = {
            "name": "Existing Business Type",
            "description": "A duplicate business type",
            "is_active": True,
            "code": "EXT001",
            "related_words": "existing, duplicate"
        }
        
        # Mock existing business type with same name
        existing_business_type = Mock()
        existing_business_type.id = 1
        existing_business_type.name = create_data["name"]
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = existing_business_type
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        def override_require_admin_or_director_role():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            response = client.post("/v1/business_types/", json=create_data)
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            data = response.json()
            assert "already exists" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_create_business_type_duplicate_code(self, client, mock_db_session, mock_user):
        """Test POST /business_types/ endpoint with duplicate SCIAN code."""
        create_data = {
            "name": "New Business Type",
            "description": "A new business type",
            "is_active": True,
            "code": "EXISTING001",
            "related_words": "new, business"
        }
        
        # Mock first query (no existing name) returns None
        # Mock second query (existing code) returns existing business type
        existing_business_type = Mock()
        existing_business_type.id = 1
        existing_business_type.code = create_data["code"]
        
        # Create side effect for multiple execute calls
        mock_results = [
            Mock(scalar_one_or_none=Mock(return_value=None)),  # No existing name
            Mock(scalar_one_or_none=Mock(return_value=existing_business_type))  # Existing code
        ]
        mock_db_session.execute.side_effect = mock_results
        
        def override_get_db():
            return mock_db_session
        
        def override_require_admin_or_director_role():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            response = client.post("/v1/business_types/", json=create_data)
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            data = response.json()
            assert "SCIAN code" in data["detail"]
            assert "already exists" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_create_business_type_unauthorized(self, client, mock_db_session):
        """Test POST /business_types/ endpoint without proper authorization."""
        create_data = {
            "name": "New Business Type",
            "description": "A new business type",
            "is_active": True
        }
        
        # Mock user without admin/director privileges
        unauthorized_user = Mock()
        unauthorized_user.role_name = "user"
        unauthorized_user.role_id = 5
        
        def override_get_db():
            return mock_db_session
        
        def override_require_admin_or_director_role():
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin or director privileges required for this operation"
            )
        
        app.dependency_overrides[get_db] = override_get_db
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            response = client.post("/v1/business_types/", json=create_data)
            
            assert response.status_code == status.HTTP_403_FORBIDDEN
            data = response.json()
            assert "Admin or director privileges required" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_create_business_type_validation_error(self, client, mock_user):
        """Test POST /business_types/ endpoint with invalid data."""
        # Missing required field 'name'
        create_data = {
            "description": "A business type without name",
            "is_active": True
        }
        
        def override_require_admin_or_director_role():
            return mock_user
        
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            response = client.post("/v1/business_types/", json=create_data)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        finally:
            app.dependency_overrides.clear()

    def test_update_business_type_impact_success(self, client, mock_db_session, mock_user):
        """Test PATCH /business_types/impact endpoint - successful update."""
        impact_data = {
            "business_type_id": 1,
            "impact_level": 3
        }
        
        # Mock existing business type
        mock_business_type = Mock()
        mock_business_type.id = 1
        
        # Mock existing configuration
        mock_config = Mock()
        mock_config.id = 1
        mock_config.business_type_id = 1
        mock_config.municipality_id = 1
        mock_config.is_disabled = False
        mock_config.has_certificate = True
        mock_config.impact_level = 1  # Will be updated to 3
        mock_config.name = "Restaurant"
        mock_config.description = "Food service establishment"
        mock_config.code = "REST001"
        mock_config.related_words = "food, dining, restaurant"
        
        # Mock business_type relationship
        mock_config.business_type = Mock()
        mock_config.business_type.name = "Restaurant"
        mock_config.business_type.description = "Food service establishment"
        mock_config.business_type.code = "REST001"
        mock_config.business_type.related_words = "food, dining, restaurant"
        
        # Mock database operations
        mock_business_type_result = Mock()
        mock_business_type_result.scalar_one_or_none.return_value = mock_business_type
        
        mock_config_result = Mock()
        mock_config_result.scalar_one_or_none.return_value = mock_config
        
        mock_db_session.execute.side_effect = [mock_business_type_result, mock_config_result]
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_require_admin_or_director_role():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            response = client.patch("/v1/business_types/impact", json=impact_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["impact_level"] == 3
            assert data["business_type_id"] == 1
            assert mock_config.impact_level == 3
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_update_business_type_impact_create_new_config(self, client, mock_db_session, mock_user):
        """Test PATCH /business_types/impact endpoint - create new configuration."""
        impact_data = {
            "business_type_id": 2,
            "impact_level": 2
        }
        
        # Mock existing business type
        mock_business_type = Mock()
        mock_business_type.id = 2
        
        # Mock new configuration (will be created)
        mock_config = Mock()
        mock_config.id = 1
        mock_config.business_type_id = 2
        mock_config.municipality_id = 1
        mock_config.is_disabled = False
        mock_config.has_certificate = False
        mock_config.impact_level = 2
        mock_config.name = "Retail Store"
        mock_config.description = "General retail establishment"
        mock_config.code = "RET001"
        mock_config.related_words = "store, retail, shop"
        
        # Mock business_type relationship
        mock_config.business_type = Mock()
        mock_config.business_type.name = "Retail Store"
        mock_config.business_type.description = "General retail establishment"
        mock_config.business_type.code = "RET001"
        mock_config.business_type.related_words = "store, retail, shop"
        
        # Mock database operations - three execute calls in the endpoint
        mock_business_type_result = Mock()
        mock_business_type_result.scalar_one_or_none.return_value = mock_business_type
        
        mock_config_result = Mock()
        mock_config_result.scalar_one_or_none.return_value = None  # No existing config
        
        mock_final_config_result = Mock()
        mock_final_config_result.scalar_one.return_value = mock_config
        
        mock_db_session.execute.side_effect = [
            mock_business_type_result, 
            mock_config_result,
            mock_final_config_result
        ]
        
        # Mock the add method to simulate adding the new config
        def mock_add(obj):
            # Set basic attributes on the added object (avoid relationship attributes)
            obj.id = mock_config.id
            obj.municipality_id = mock_config.municipality_id
            obj.is_disabled = mock_config.is_disabled
            obj.has_certificate = mock_config.has_certificate
            obj.name = mock_config.name
            obj.description = mock_config.description
            obj.code = mock_config.code
            obj.related_words = mock_config.related_words
        
        mock_db_session.add = Mock(side_effect=mock_add)
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_require_admin_or_director_role():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            # Use patch to mock the BusinessTypeConfig constructor
            with patch('app.routers.business_types.BusinessTypeConfig', return_value=mock_config):
                response = client.patch("/v1/business_types/impact", json=impact_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["impact_level"] == 2
            assert data["business_type_id"] == 2
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_update_business_type_impact_business_type_not_found(self, client, mock_db_session, mock_user):
        """Test PATCH /business_types/impact endpoint - business type not found."""
        impact_data = {
            "business_type_id": 999,
            "impact_level": 2
        }
        
        # Mock business type not found
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        def override_require_admin_or_director_role():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            response = client.patch("/v1/business_types/impact", json=impact_data)
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            data = response.json()
            assert "Business type with ID '999' not found" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_update_business_type_impact_unauthorized(self, client, mock_db_session):
        """Test PATCH /business_types/impact endpoint - unauthorized user."""
        impact_data = {
            "business_type_id": 1,
            "impact_level": 2
        }
        
        def override_get_db():
            return mock_db_session
        
        def override_require_admin_or_director_role():
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin or director privileges required for this operation"
            )
        
        app.dependency_overrides[get_db] = override_get_db
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            response = client.patch("/v1/business_types/impact", json=impact_data)
            
            assert response.status_code == status.HTTP_403_FORBIDDEN
            data = response.json()
            assert "Admin or director privileges required" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_update_business_type_impact_validation_error(self, client, mock_user):
        """Test PATCH /business_types/impact endpoint - validation error."""
        # Missing required impact_level field
        invalid_data = {
            "business_type_id": 1
        }
        
        def override_require_admin_or_director_role():
            return mock_user
        
        from app.utils.role_validation import require_admin_or_director_role
        app.dependency_overrides[require_admin_or_director_role] = override_require_admin_or_director_role
        
        try:
            response = client.patch("/v1/business_types/impact", json=invalid_data)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        finally:
            app.dependency_overrides.clear()


if __name__ == "__main__":
    pytest.main([__file__])
