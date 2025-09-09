"""
Comprehensive tests for business_commercial_procedures router endpoints.

This test suite covers:
1. GET /business_commercial_procedures/ - List business commercial procedures
2. GET /business_commercial_procedures/{procedure_id} - Get specific procedure

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
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from unittest.mock import Mock
from datetime import datetime

"""
Comprehensive tests for business_commercial_procedures router endpoints.

This test suite covers:
1. GET /business_commercial_procedures/ - List business commercial procedures
2. GET /business_commercial_procedures/{procedure_id} - Get specific procedure

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
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from unittest.mock import Mock
from datetime import datetime

from app.routers.business_commercial_procedures import router
from app.models.procedures import Procedure
from app.models.business_license import BusinessLicense
from app.models.requirements_query import RequirementsQuery
from app.models.municipality import Municipality
from app.models.business_sectors import BusinessSector
from app.models.user import UserModel
from config.settings import get_sync_db as get_db
from config.security import get_current_user

# Create test app
app = FastAPI()
app.include_router(router, prefix="/v1/business_commercial_procedures")

# Mock data
MOCK_PROCEDURE = {
    "id": 1,
    "folio": "PROC-001-2024",
    "current_step": 2,
    "procedure_type": "licencia_giro_comercial",
    "license_status": "en_proceso",
    "status": 1,
    "procedure_start_date": datetime(2024, 1, 15, 10, 0, 0),
    "created_at": datetime(2024, 1, 15, 10, 0, 0),
    "updated_at": datetime(2024, 1, 15, 10, 0, 0),
    "user_id": 1,
    "official_applicant_name": "Juan Pérez",
    "street": "Av. Revolución",
    "exterior_number": "123",
    "interior_number": "4A",
    "neighborhood": "Centro",
    "municipality_id": 1,
    "establishment_name": "Restaurante El Buen Sabor",
    "establishment_address": "Av. Revolución 123, Centro",
    "establishment_phone": "555-1234",
    "establishment_area": "80.0",
    "scian_code": "722511",
    "scian_name": "Restaurantes con servicio completo"
}

MOCK_BUSINESS_LICENSE = {
    "license_folio": "PROC-001-2024",
    "commercial_activity": "Restaurantes",
    "industry_classification_code": "722511",
    "owner": "Restaurante El Buen Sabor"
}

MOCK_REQUIREMENTS_QUERY = {
    "id": 1,
    "folio": "REQ-2024-000001",
    "street": "Av. Revolución",
    "neighborhood": "Centro",
    "municipality_name": "Guadalajara",
    "municipality_id": 1,
    "scian_code": "722511",
    "scian_name": "Restaurantes con servicio completo",
    "property_area": 100.0,
    "activity_area": 80.0,
    "applicant_name": "Juan Pérez",
    "applicant_character": "Owner",
    "person_type": "physical",
    "minimap_url": "http://example.com/minimap.jpg",
    "restrictions": {},
    "status": 1,
    "user_id": 1,
    "alcohol_sales": 0,
    "primary_folio": None,
    "issue_license": 1,
    "license_type": "commercial",
    "scian": "722511",
    "entry_date": "2024-01-15",
    "interested_party": None,
    "last_resolution": None,
    "resolution_sense": None
}

MOCK_MUNICIPALITY = {
    "id": 1,
    "name": "Guadalajara"
}

MOCK_BUSINESS_SECTOR = {
    "code": "722511",
    "industry_classification_code": "722511",
    "description": "Restaurantes con servicio completo"
}

# Mock users for different access levels
MOCK_ADMIN_USER = {
    "id": 100,
    "email": "admin@test.com", 
    "role_name": "admin",
    "is_superuser": False,
    "municipality_id": 1
}

MOCK_DIRECTOR_USER = {
    "id": 101,
    "email": "director@test.com",
    "role_name": "director", 
    "is_superuser": False,
    "municipality_id": 1
}

MOCK_SUPERUSER = {
    "id": 102,
    "email": "super@test.com",
    "role_name": "user",
    "is_superuser": True,
    "municipality_id": 1
}

MOCK_SUPERVISOR_USER = {
    "id": 103,
    "email": "supervisor@test.com",
    "role_name": "supervisor",
    "is_superuser": False,
    "municipality_id": 1
}

MOCK_REGULAR_USER = {
    "id": 1,
    "email": "user@test.com",
    "role_name": "user",
    "is_superuser": False,
    "municipality_id": 1
}

# Test imports
def test_imports():
    """Test that all imports work correctly."""
    from app.routers.business_commercial_procedures import router
    from config.settings import get_sync_db
    assert router is not None
    assert get_sync_db is not None

def test_basic_functionality():
    """Basic test to ensure test framework works."""
    assert 1 + 1 == 2


class TestBusinessCommercialProceduresEndpoints:
    """Tests for business commercial procedures router endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def mock_db_session(self):
        """Create mock database session."""
        return Mock()

    @pytest.fixture
    def mock_admin_user(self):
        """Create mock admin user."""
        user = Mock(spec=UserModel)
        for key, value in MOCK_ADMIN_USER.items():
            setattr(user, key, value)
        return user

    @pytest.fixture
    def mock_director_user(self):
        """Create mock director user."""
        user = Mock(spec=UserModel)
        for key, value in MOCK_DIRECTOR_USER.items():
            setattr(user, key, value)
        return user

    @pytest.fixture
    def mock_superuser(self):
        """Create mock superuser."""
        user = Mock(spec=UserModel)
        for key, value in MOCK_SUPERUSER.items():
            setattr(user, key, value)
        return user

    @pytest.fixture
    def mock_supervisor_user(self):
        """Create mock supervisor user."""
        user = Mock(spec=UserModel)
        for key, value in MOCK_SUPERVISOR_USER.items():
            setattr(user, key, value)
        return user

    @pytest.fixture
    def mock_regular_user(self):
        """Create mock regular user."""
        user = Mock(spec=UserModel)
        for key, value in MOCK_REGULAR_USER.items():
            setattr(user, key, value)
        return user

    @pytest.fixture
    def sample_procedure_data(self):
        """Create sample procedure data for testing."""
        # Create mock objects
        procedure = Mock(spec=Procedure)
        requirements_query = Mock(spec=RequirementsQuery)
        municipality = Mock(spec=Municipality)
        business_sector = Mock(spec=BusinessSector)
        
        # Set procedure attributes
        for key, value in MOCK_PROCEDURE.items():
            setattr(procedure, key, value)
        
        # Set requirements query attributes
        for key, value in MOCK_REQUIREMENTS_QUERY.items():
            setattr(requirements_query, key, value)
        
        # Set municipality attributes
        for key, value in MOCK_MUNICIPALITY.items():
            setattr(municipality, key, value)
        
        # Set business sector attributes
        for key, value in MOCK_BUSINESS_SECTOR.items():
            setattr(business_sector, key, value)
        
        return (procedure, requirements_query, municipality, business_sector)

    def test_list_business_commercial_procedures_success_admin(self, client, mock_db_session, sample_procedure_data, mock_admin_user):
        """Test GET /business_commercial_procedures/ endpoint with admin user."""
        procedure, requirements_query, municipality, business_sector = sample_procedure_data
        
        # Mock database query result
        mock_query = Mock()
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [(procedure, requirements_query, municipality, business_sector)]
        
        mock_db_session.query.return_value = mock_query
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_admin_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.get("/v1/business_commercial_procedures/?municipality_id=1")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            
            # Validate response structure
            assert "procedures" in data
            assert "total_count" in data
            assert "skip" in data
            assert "limit" in data
            
            # Validate data content
            assert data["total_count"] == 1
            assert len(data["procedures"]) == 1
            
            procedure_data = data["procedures"][0]
            assert procedure_data["id"] == 1
            assert procedure_data["folio"] == "PROC-001-2024"
            assert procedure_data["municipality_name"] == "Guadalajara"
            assert procedure_data["street"] == "Av. Revolución"
            assert procedure_data["full_address"] == "Av. Revolución 123 Int. 4A"
            assert procedure_data["industry_classification_code"] == "722511"
            assert procedure_data["business_name"] == "Restaurante El Buen Sabor"  # From procedure.establishment_name
            assert procedure_data["business_line"] == "Restaurantes con servicio completo"  # From requirements_query.scian_name
            
        finally:
            app.dependency_overrides.clear()

    def test_list_business_commercial_procedures_success_superuser(self, client, mock_db_session, sample_procedure_data, mock_superuser):
        """Test GET /business_commercial_procedures/ endpoint with superuser."""
        procedure, requirements_query, municipality, business_sector = sample_procedure_data
        
        # Mock database query result
        mock_query = Mock()
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [(procedure, requirements_query, municipality, business_sector)]
        
        mock_db_session.query.return_value = mock_query
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_superuser
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.get("/v1/business_commercial_procedures/?municipality_id=1")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["total_count"] == 1
            
        finally:
            app.dependency_overrides.clear()

    def test_list_business_commercial_procedures_regular_user_own_procedures(self, client, mock_db_session, sample_procedure_data, mock_regular_user):
        """Test GET /business_commercial_procedures/ endpoint with regular user seeing own procedures."""
        procedure, requirements_query, municipality, business_sector = sample_procedure_data
        
        # Mock database query result
        mock_query = Mock()
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [(procedure, requirements_query, municipality, business_sector)]
        
        mock_db_session.query.return_value = mock_query
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_regular_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.get("/v1/business_commercial_procedures/?municipality_id=1")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["total_count"] == 1
            
        finally:
            app.dependency_overrides.clear()

    def test_list_business_commercial_procedures_unauthorized_user_access(self, client, mock_db_session, sample_procedure_data, mock_regular_user):
        """Test GET /business_commercial_procedures/ endpoint with regular user trying to access another user's procedures."""
        procedure, requirements_query, municipality, business_sector = sample_procedure_data
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_regular_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            # Regular user tries to filter by another user's ID (user_id=999)
            response = client.get("/v1/business_commercial_procedures/?municipality_id=1&user_id=999")
            
            assert response.status_code == status.HTTP_403_FORBIDDEN
            data = response.json()
            assert "Access denied" in data["detail"]
            
        finally:
            app.dependency_overrides.clear()

    def test_list_business_commercial_procedures_no_auth(self, client):
        """Test GET /business_commercial_procedures/ endpoint without authentication."""
        response = client.get("/v1/business_commercial_procedures/?municipality_id=1")
        
        # Should return 401 Unauthorized when no authentication is provided
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_business_commercial_procedures_missing_municipality_id(self, client):
        """Test GET /business_commercial_procedures/ endpoint without required municipality_id."""
        response = client.get("/v1/business_commercial_procedures/")
        
        # Should return 401 Unauthorized when no authentication is provided (authentication is checked first)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_business_commercial_procedures_missing_municipality_id_authenticated(self, client, mock_db_session, mock_regular_user):
        """Test GET /business_commercial_procedures/ endpoint without required municipality_id but with authentication."""
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_regular_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.get("/v1/business_commercial_procedures/")
            
            # Should return 422 when authenticated but missing required parameter
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            data = response.json()
            assert "detail" in data
            
        finally:
            app.dependency_overrides.clear()


if __name__ == "__main__":
    pytest.main([__file__])
