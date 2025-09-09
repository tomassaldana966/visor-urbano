"""
Comprehensive tests for municipality router endpoints.

This test suite covers:
1. GET /municipalities/geom - Get municipality geometries
2. GET /municipalities/ - List municipalities  
3. POST /municipalities/ - Create municipality
4. GET /municipalities/{municipality_id} - Get municipality by ID
5. PUT /municipalities/{municipality_id} - Update municipality
6. DELETE /municipalities/{municipality_id} - Delete municipality
7. POST /municipalities/{municipality_id}/image - Upload municipality image

Tests include success cases, error scenarios, validation, and edge cases.
"""
import sys
from pathlib import Path
from unittest.mock import PropertyMock

# Add project paths
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
app_dir = backend_dir / "app"
sys.path.insert(0, str(app_dir))

import pytest
import pytest_asyncio
from fastapi import FastAPI, status, UploadFile
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timezone
import io
from httpx import AsyncClient

from app.routers.municipality import municipalities
from app.models.municipality import Municipality
from app.schemas.municipality import MunicipalityCreate, MunicipalityUpdate, MunicipalityResponse
from config.settings import get_db
from config.security import get_current_user

# Create test app
app = FastAPI()
app.include_router(municipalities, prefix="/v1/municipalities")

# Mock data with updated geometry interface
MOCK_MUNICIPALITIES = [
    {
        "id": 1,
        "name": "Test Municipality 1",
        "image": "test1.jpg",
        "director": "Test Director 1",
        "director_signature": "signature1.jpg",
        "process_sheet": 1,
        "solving_days": 30,
        "issue_license": 1,
        "address": "Test Address 1",
        "phone": "123-456-7890",
        "email": "test1@municipality.gov",
        "website": "https://municipality1.gov",
        "responsible_area": "Test Area 1",
        "window_license_generation": 1,
        "license_restrictions": "Test restrictions 1",
        "license_price": "100.00",
        "initial_folio": 1000,
        "has_zoning": True,
        "allow_online_procedures": True,
        "allow_window_reviewer_licenses": True,
        "low_impact_license_cost": "50.00",
        "license_additional_text": "Additional license text 1",
        "theme_color": "#FF0000",
        "signatures": [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "deleted_at": None,
        "__geo_interface__": {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
            },
            "properties": {
                "id": 1,
                "name": "Test Municipality 1"
            }
        }
    },
    {
        "id": 2,
        "name": "Test Municipality 2",
        "image": "test2.jpg",
        "director": "Test Director 2",
        "director_signature": "signature2.jpg",
        "process_sheet": 1,
        "solving_days": 30,
        "issue_license": 1,
        "address": "Test Address 2",
        "phone": "123-456-7891",
        "email": "test2@municipality.gov",
        "website": "https://municipality2.gov",
        "responsible_area": "Test Area 2",
        "window_license_generation": 1,
        "license_restrictions": "Test restrictions 2",
        "license_price": "200.00",
        "initial_folio": 2000,
        "has_zoning": True,
        "allow_online_procedures": False,
        "allow_window_reviewer_licenses": False,
        "low_impact_license_cost": "75.00",
        "license_additional_text": "Additional license text 2",
        "theme_color": "#00FF00",
        "signatures": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "deleted_at": None,
        "geom": {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
        }
    }
]

class TestMunicipalityEndpoints:
    """Tests for municipality router endpoints."""

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
    def sample_municipality(self):
        """Create a sample municipality object with proper attribute values."""
        created_time = datetime.now(timezone.utc)
        updated_time = datetime.now(timezone.utc)
        
        # Create a real-like municipality object that returns actual values, not mocks
        class MockMunicipality:
            def __init__(self):
                self.id = 1
                self.name = "Test Municipality 1"
                self.image = "test1.jpg"
                self.director = "Test Director 1"
                self.director_signature = "signature1.jpg"
                self.process_sheet = 1
                self.solving_days = 30
                self.issue_license = 1
                self.address = "Test Address 1"
                self.phone = "123-456-7890"
                self.email = "test@municipality.gov"
                self.website = "https://municipality.gov"
                self.responsible_area = "Test Area 1"
                self.window_license_generation = 1
                self.license_restrictions = "Test restrictions 1"
                self.license_price = "100.00"
                self.initial_folio = 1000
                self.has_zoning = True
                self.population = 50000  # Add population attribute
                self.allow_online_procedures = True
                self.allow_window_reviewer_licenses = True
                self.low_impact_license_cost = "50.00"
                self.license_additional_text = "Additional license text"
                self.theme_color = "#FF0000"
                self.signatures = []  # Empty list for signatures
                self.created_at = created_time
                self.updated_at = updated_time
                self.deleted_at = None
                
                # Create geometry with proper interface
                geojson = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
                    },
                    "properties": {
                        "id": self.id,
                        "name": self.name
                    }
                }
                
                self.geom = MagicMock()
                self.geom.geom_type = "Polygon"
                self.geom.__geo_interface__ = geojson
                self.__geo_interface__ = geojson
                self.geom_type = "Polygon"
                self.coordinates = geojson["geometry"]["coordinates"]
        
        return MockMunicipality()

    def test_get_municipalities_geom(self, client, mock_db_session):
        """Test GET /municipalities/geom endpoint."""
        # Mock database query
        mock_result = Mock()
        mock_municipalities = []
        
        # Create mock municipalities with proper geometry
        for i, data in enumerate(MOCK_MUNICIPALITIES, 1):
            municipality = Mock(spec=Municipality)
            
            # Prepare the base GeoJSON structure
            geojson = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
                },
                "properties": {
                    "id": i,
                    "name": f"Test Municipality {i}"
                }
            }
            
            # Set up all attributes with actual values
            attrs = {
                'id': i,
                'name': f"Test Municipality {i}",
                'has_zoning': True,
                'geom_type': "Polygon",
                '__geo_interface__': geojson,
                'coordinates': geojson["geometry"]["coordinates"]
            }
            
            # Set all attributes and their getters at once
            for attr, value in attrs.items():
                setattr(municipality, attr, value)
                mock_getter = Mock(return_value=value)
                setattr(municipality, f'_get_{attr}', mock_getter)
            
            # Set up geometry mock
            mock_geom = Mock()
            mock_geom.geom_type = "Polygon"
            mock_geom.__geo_interface__ = geojson
            municipality.geom = mock_geom
            
            mock_municipalities.append(municipality)
        
        mock_result.scalars.return_value.all.return_value = mock_municipalities
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/municipalities/geom")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, dict)  # Should be a FeatureCollection
            assert data["type"] == "FeatureCollection"
            assert "features" in data
            assert isinstance(data["features"], list)
            assert len(data["features"]) == 2
        finally:
            app.dependency_overrides.clear()

    def test_list_municipalities(self, client, mock_db_session):
        """Test GET /municipalities/ endpoint."""
        # Mock database query
        mock_result = Mock()
        mock_municipalities = []
        for data in MOCK_MUNICIPALITIES:
            municipality = Mock(spec=Municipality)
            for key, value in data.items():
                setattr(municipality, key, value)
            mock_municipalities.append(municipality)
        
        mock_result.scalars.return_value.all.return_value = mock_municipalities
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/municipalities/")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["name"] == "Test Municipality 1"
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_create_municipality(self, client, mock_db_session, mock_user):
        """Test POST /municipalities/ endpoint."""
        from unittest.mock import PropertyMock, AsyncMock
        
        # Setup mock municipality data
        new_municipality_data = {
            "name": "New Municipality",
            "image": "new.jpg",
            "director": "New Director",
            "director_signature": "newsig.jpg",
            "process_sheet": 1,
            "solving_days": 30,
            "issue_license": 1,
            "address": "New Address",
            "phone": "123-456-7890",
            "responsible_area": "New Area",
            "window_license_generation": 1,
            "license_restrictions": "New restrictions",
            "license_price": "150.00",
            "initial_folio": 3000,
            "has_zoning": True
        }
        
        # Mock database operations
        mock_db_session.add = MagicMock()  # add is synchronous
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            with patch('app.routers.municipality.Municipality') as MockMunicipality:
                # Configure mock municipality with PropertyMock for each attribute
                mock_instance = Mock(spec=Municipality)
                
                # Set regular attributes
                for key, value in new_municipality_data.items():
                    mock_prop = PropertyMock(return_value=value)
                    setattr(type(mock_instance), key, mock_prop)
                    setattr(mock_instance, key, value)
                
                # Set required fields for response validation including all missing fields
                required_fields = {
                    'id': 3,
                    'email': 'new@municipality.gov',
                    'website': 'https://newmunicipality.gov',
                    'allow_online_procedures': True,
                    'allow_window_reviewer_licenses': True,
                    'low_impact_license_cost': '50.00',
                    'license_additional_text': 'Additional text',
                    'theme_color': '#0000FF',
                    'signatures': [],
                    'created_at': datetime.now(timezone.utc),
                    'updated_at': datetime.now(timezone.utc),
                    'deleted_at': None
                }
                
                for key, value in required_fields.items():
                    mock_prop = PropertyMock(return_value=value)
                    setattr(type(mock_instance), key, mock_prop)
                    setattr(mock_instance, key, value)
                
                # Set up geometry interface
                geojson = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
                    },
                    "properties": {
                        "id": required_fields["id"],
                        "name": new_municipality_data["name"]
                    }
                }
                
                # Configure geometry on the instance
                mock_instance.__geo_interface__ = geojson
                mock_instance.geom_type = "Polygon"
                mock_instance.coordinates = geojson["geometry"]["coordinates"]
                
                MockMunicipality.return_value = mock_instance
                
                # Make request
                response = client.post("/v1/municipalities/", json=new_municipality_data)
                
                # Validate response
                assert response.status_code == status.HTTP_201_CREATED
                data = response.json()
                
                # Verify response data
                assert data["id"] == required_fields["id"]
                assert data["name"] == new_municipality_data["name"]
                assert data["has_zoning"] == new_municipality_data["has_zoning"]
                assert isinstance(data["created_at"], str)
                assert isinstance(data["updated_at"], str)
                
                # Verify database operations
                mock_db_session.add.assert_called_once()  # add is synchronous
                mock_db_session.commit.assert_awaited_once()
                mock_db_session.refresh.assert_awaited_once()
                
        finally:
            app.dependency_overrides.clear()

    def test_get_municipality_by_id(self, client, mock_db_session, sample_municipality):
        """Test getting a municipality by ID."""
        municipality_id = 1
        
        # Mock database query
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = sample_municipality
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get(f"/v1/municipalities/{municipality_id}")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["id"] == municipality_id
            assert data["name"] == sample_municipality.name
        finally:
            app.dependency_overrides.clear()

    def test_get_municipality_not_found(self, client, mock_db_session):
        """Test GET /municipalities/{municipality_id} with non-existent ID."""
        # Mock database query - not found
        mock_result = Mock()
        mock_scalars = Mock()
        mock_scalars.first.return_value = None
        mock_result.scalars.return_value = mock_scalars
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/municipalities/999")
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            data = response.json()
            assert "Municipality not found" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_update_municipality(self, client, mock_db_session, sample_municipality, mock_user):
        """Test PUT /municipalities/{municipality_id} endpoint."""
        update_data = {
            "name": "Updated Municipality",
            "population": 60000
        }
        
        # Mock database query
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = sample_municipality
        mock_db_session.execute.return_value = mock_result
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.put("/v1/municipalities/1", json=update_data)
            
            assert response.status_code == status.HTTP_200_OK
            # Since we're using a mock object, the setattr calls happen but we can't easily verify them
            # Just verify the response is successful and the mock methods were called
            mock_db_session.commit.assert_awaited_once()
            mock_db_session.refresh.assert_awaited_once()
        finally:
            app.dependency_overrides.clear()

    def test_delete_municipality(self, client, mock_db_session, sample_municipality, mock_user):
        """Test deleting a municipality."""
        municipality_id = 1
        
        # Mock database query
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = sample_municipality
        mock_db_session.execute.return_value = mock_result
        mock_db_session.delete = AsyncMock()
        mock_db_session.commit = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.delete(f"/v1/municipalities/{municipality_id}")
            
            assert response.status_code == status.HTTP_204_NO_CONTENT
            
            mock_db_session.delete.assert_awaited_once()
            mock_db_session.commit.assert_awaited_once()
        finally:
            app.dependency_overrides.clear()

    def test_upload_municipality_image(self, client, mock_db_session, sample_municipality, mock_user):
        """Test uploading a municipality image."""
        municipality_id = 1
        
        # Mock database query
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = sample_municipality
        mock_db_session.execute.return_value = mock_result
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            # Mock file system operations
            with patch('app.routers.municipality.os.makedirs'), \
                 patch('app.routers.municipality.os.path.exists', return_value=False), \
                 patch('builtins.open', mock_create_file_handler()):
                
                # Create test image file
                image_content = b"fake image content"
                files = {
                    "image": ("test_image.jpg", image_content, "image/jpeg")
                }

                response = client.post(
                    f"/v1/municipalities/{municipality_id}/image",
                    files=files
                )
                
                assert response.status_code == status.HTTP_200_OK
                data = response.json()
                assert data["id"] == municipality_id
                
                mock_db_session.commit.assert_awaited_once()
                # Note: The endpoint doesn't call refresh, it reloads via another execute call
                assert mock_db_session.execute.call_count >= 2  # Initial load + reload
        finally:
            app.dependency_overrides.clear()

    def test_create_municipality_validation_error(self, client, mock_db_session):
        """Test POST /municipalities/ with invalid data."""
        invalid_data = {
            # Send completely invalid data that will fail Pydantic validation
            "invalid_field": "invalid_value"
        }
        
        # Mock database operations to prevent actual execution
        mock_db_session.add = MagicMock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.post("/v1/municipalities/", json=invalid_data)
            
            # Should fail validation due to unknown field
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        finally:
            app.dependency_overrides.clear()

    def test_upload_invalid_image_type(self, client, mock_user):
        """Test image upload with invalid file type."""
        # Create a mock text file
        text_file = io.BytesIO(b"not an image")
        
        def override_get_current_user():
            return mock_user
        
        app.dependency_overrides[get_current_user] = override_get_current_user
        
        try:
            response = client.post(
                "/v1/municipalities/1/image",
                files={"file": ("test.txt", text_file, "text/plain")}
            )
            
            # Should fail due to invalid file type (depending on validation)
            assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]
        finally:
            app.dependency_overrides.clear()

    @pytest.mark.parametrize("municipality_id,expected_status", [
        (1, status.HTTP_200_OK),
        (999, status.HTTP_404_NOT_FOUND),
        (-1, status.HTTP_404_NOT_FOUND),  # FastAPI treats negative integers as valid path params
        (0, status.HTTP_404_NOT_FOUND),   # FastAPI treats 0 as valid path param
    ])
    def test_get_municipality_various_ids(self, client, mock_db_session, sample_municipality, municipality_id, expected_status):
        """Test GET municipality with various ID values."""
        # Mock database query
        mock_result = Mock()
        if municipality_id == 1:
            mock_result.scalars.return_value.first.return_value = sample_municipality
        else:
            mock_result.scalars.return_value.first.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get(f"/v1/municipalities/{municipality_id}")
            assert response.status_code == expected_status
        finally:
            app.dependency_overrides.clear()


def mock_create_file_handler():
    """Helper function to mock file operations."""
    def mock_open(filename, mode='r', **kwargs):
        mock_file = Mock()
        mock_file.write = Mock()
        mock_file.__enter__ = Mock(return_value=mock_file)
        mock_file.__exit__ = Mock(return_value=None)
        return mock_file
    return mock_open


if __name__ == "__main__":
    pytest.main([__file__])
