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
from fastapi import status, FastAPI, HTTPException
from unittest.mock import Mock, AsyncMock, patch, MagicMock, ANY
import base64
import json
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal

# Import the router for testing
from app.routers.requirements_queries import router as requirements_queries_router


# Test fixtures for sample data
@pytest.fixture
def sample_requirements_query_data():
    """Sample data for creating requirements queries"""
    return {
        "street": "Calle Principal 123",
        "neighborhood": "Centro",
        "municipality_name": "Test Municipality",  # Added required field
        "business_name": "Tienda de Abarrotes La Esquina",
        "business_activity": "Venta de abarrotes y comestibles",
        "applicant_name": "Juan Pérez García",
        "contact_phone": "6641234567",
        "contact_email": "juan.perez@email.com",
        "municipality_id": 1,
        "scian_code": "461110",
        "scian_name": "Comercio al por menor de abarrotes",
        "property_area": "150.50",
        "activity_area": "120.00",
        "has_alcohol": False
    }


@pytest.fixture
def encoded_folio_valid():
    """Valid base64 encoded folio"""
    return base64.b64encode("REQ-001-2024".encode()).decode()


@pytest.fixture
def encoded_folio_alcohol():
    """Base64 encoded folio for business with alcohol"""
    return base64.b64encode("REQ-002-2024".encode()).decode()


@pytest.fixture
def encoded_folio_invalid():
    """Base64 encoded invalid folio"""
    return base64.b64encode("INVALID-FOLIO".encode()).decode()


@pytest_asyncio.fixture
async def async_client():
    """Create an async HTTP client for testing with proper dependency overrides"""
    app = FastAPI()
    app.include_router(requirements_queries_router, prefix="/requirements-queries", tags=["requirements-queries"])
    
    # Mock database dependency
    async def mock_get_db():
        mock_db = AsyncMock(spec=AsyncSession)
        yield mock_db
    
    # Mock authentication dependency
    async def mock_get_current_user():
        return {
            "id": 1,
            "email": "test@example.com",
            "role_id": 1,
            "role_name": "admin",
            "municipality_id": 1
        }
    
    # Override dependencies
    from config.settings import get_db
    from config.security import get_current_user
    app.dependency_overrides[get_db] = mock_get_db
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    # Clean up
    app.dependency_overrides.clear()


class TestRequirementsQueriesEndpoints:
    """Test suite for Requirements Queries API endpoints"""

    @pytest.mark.asyncio
    async def test_get_procedure_info_success(self, async_client: AsyncClient, encoded_folio_valid):
        """Test successful procedure information retrieval"""
        folio = encoded_folio_valid
        decoded_folio = "REQ-001-2024"
        
        expected_response = {
            "folio": decoded_folio,
            "procedure_data": {
                "street": "Calle Principal 123",
                "neighborhood": "Centro",
                "business_name": "Tienda de Abarrotes La Esquina",
                "municipality": "Test Municipality"
            },
            "requirements": [
                {"id": 1, "name": "Business License", "status": "pending"},
                {"id": 2, "name": "Fire Safety Certificate", "status": "approved"}
            ],
            "status": "active"
        }
        
        with patch('app.routers.requirements_queries.get_procedure_info', return_value=expected_response) as mock_service:
            response = await async_client.get(f"/requirements-queries/{folio}/info")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            
            assert data["folio"] == decoded_folio
            assert data["procedure_data"]["street"] == "Calle Principal 123"
            mock_service.assert_called_once_with(decoded_folio, ANY)

    @pytest.mark.asyncio
    async def test_get_procedure_info_invalid_base64(self, async_client: AsyncClient):
        """Test procedure info retrieval with invalid base64 folio"""
        invalid_folio = "invalid-base64!!!"
        
        response = await async_client.get(f"/requirements-queries/{invalid_folio}/info")
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "Invalid folio format" in data["detail"]

    @pytest.mark.asyncio
    async def test_submit_requirements_query_success(self, async_client: AsyncClient, sample_requirements_query_data):
        """Test successful requirements query submission"""
        query_data = sample_requirements_query_data
        
        expected_response = {
            "id": 1, "folio": "REQ-NEW-001-2024", "status": 1, "user_id": 1,
            "created_at": datetime.now().isoformat(), "year_folio": 1,
            "street": query_data["street"], "neighborhood": query_data["neighborhood"],
            "municipality_name": "Test Municipality", "municipality_id": query_data["municipality_id"],
            "scian_code": query_data["scian_code"], "scian_name": query_data["scian_name"],
            "property_area": "150.50", "activity_area": "120.00",
            "applicant_name": query_data["applicant_name"], "alcohol_sales": 0
        }
        
        with patch('app.routers.requirements_queries.submit_requirements_query', return_value=expected_response) as mock_submit_service:
            response = await async_client.post("/requirements-queries/", json=query_data)
            
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["status"] == 1
            assert "REQ-NEW" in data["folio"]
            
            # Verify the service was called - it should be called with the schema object, not raw dict
            mock_submit_service.assert_called_once()
            call_args = mock_submit_service.call_args[0]  # Get positional args
            assert call_args[0].street == query_data["street"]
            assert call_args[0].municipality_name == query_data["municipality_name"]


class TestRequirementsQueriesValidation:
    """Test suite for input validation and edge cases"""
    
    @pytest.mark.parametrize("folio_param, expected_status_code_router", [
        ("not-base64!", status.HTTP_400_BAD_REQUEST),
        ("AA==", status.HTTP_400_BAD_REQUEST),
        ("VkFMSUQtRk9MSU8=", status.HTTP_404_NOT_FOUND),  # Valid base64 "VALID-FOLIO" but not found
    ])
    @pytest.mark.asyncio
    async def test_folio_base64_validation_edge_cases(self, async_client: AsyncClient, folio_param, expected_status_code_router):
        """Test various base64 edge cases for folio parameter in /info endpoint."""
        
        if expected_status_code_router == status.HTTP_404_NOT_FOUND:
            # Mock the service to return 404
            with patch('app.routers.requirements_queries.get_procedure_info', side_effect=HTTPException(status_code=404, detail="Not found")):
                response = await async_client.get(f"/requirements-queries/{folio_param}/info")
        else:
            # For invalid base64, service should not be called
            with patch('app.routers.requirements_queries.get_procedure_info', side_effect=AssertionError("Service should not be called")) as mock_get_info:
                response = await async_client.get(f"/requirements-queries/{folio_param}/info")
                mock_get_info.assert_not_called()
    
        assert response.status_code == expected_status_code_router
        data = response.json()
        if expected_status_code_router == status.HTTP_400_BAD_REQUEST:
            assert "Invalid folio format" in data["detail"]

    @pytest.mark.parametrize("endpoint_template", [
        "/requirements-queries/{folio}/info",
        "/requirements-queries/{folio}/type",
        "/requirements-queries/{folio}/renewal",
        "/requirements-queries/{folio}/requirements/1/pdf"
    ])
    @pytest.mark.asyncio
    async def test_endpoints_with_malformed_folio(self, async_client: AsyncClient, endpoint_template):
        """Test all GET endpoints with malformed folio parameter (not valid base64)."""
        malformed_folio = "notvalidbase64"  # Simple invalid base64 without special chars
        
        service_method_to_mock_path = None
        if "/info" in endpoint_template:
            service_method_to_mock_path = 'app.routers.requirements_queries.get_procedure_info'
        elif "/type" in endpoint_template:
            service_method_to_mock_path = 'app.routers.requirements_queries.get_procedure_info_type'
        elif "/renewal" in endpoint_template:
            service_method_to_mock_path = 'app.routers.requirements_queries.get_procedure_info_renewal'
        elif "/pdf" in endpoint_template:
            service_method_to_mock_path = 'app.routers.requirements_queries.get_requirements_pdf'

        # Patch the identified service method to ensure it's not called.
        if service_method_to_mock_path:
            with patch(service_method_to_mock_path, side_effect=AssertionError("Service should not be called for malformed folio")) as mock_service_call:
                response = await async_client.get(endpoint_template.format(folio=malformed_folio))
                mock_service_call.assert_not_called()
        else:
            response = await async_client.get(endpoint_template.format(folio=malformed_folio))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Invalid folio format"
