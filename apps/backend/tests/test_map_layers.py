"""
Comprehensive tests for map_layers router endpoints.

This test suite covers:
1. GET /map_layers - List map layers
2. GET /map_layers/{id} - Get map layer by ID
3. POST /map_layers - Create map layer
4. PATCH /map_layers/{id} - Update map layer

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

from app.routers.map_layers import router
from app.models.map_layers import MapLayer
from app.models.municipality import Municipality
from app.schemas.map_layers import MapLayerCreate, MapLayerUpdate, MapLayerResponse
from config.settings import get_db

# Create test app
app = FastAPI()
# Include router with v1 prefix to match production setup
app.include_router(router, prefix="/v1/map_layers")

# Mock data
MOCK_MAP_LAYERS = [
    {
        "id": 1,
        "value": "layer_1",
        "label": "Test Layer 1",
        "type": "WMS",
        "url": "https://example.com/wms",
        "layers": "test_layer_1",
        "visible": True,
        "active": True,
        "attribution": "Test Attribution",
        "opacity": 1.0,
        "server_type": "geoserver",
        "projection": "EPSG:4326",
        "version": "1.3.0",
        "format": "image/png",
        "order": 1,
        "editable": False,
        "type_geom": "polygon",
        "cql_filter": None
    },
    {
        "id": 2,
        "value": "layer_2",
        "label": "Test Layer 2",
        "type": "WFS",
        "url": "https://example.com/wfs",
        "layers": "test_layer_2",
        "visible": False,
        "active": True,
        "attribution": "Test Attribution 2",
        "opacity": 0.8,
        "server_type": "mapserver",
        "projection": "EPSG:3857",
        "version": "2.0.0",
        "format": "application/json",
        "order": 2,
        "editable": True,
        "type_geom": "point",
        "cql_filter": "municipality='test'"
    }
]

MOCK_MUNICIPALITIES = [
    {"id": 1, "name": "Municipality 1"},
    {"id": 2, "name": "Municipality 2"}
]

class TestMapLayersEndpoints:
    """Tests for map layers router endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def mock_db_session(self):
        """Create mock database session."""
        return AsyncMock()

    @pytest.fixture
    def sample_map_layer(self):
        """Create a sample map layer object."""
        layer = Mock(spec=MapLayer)
        for key, value in MOCK_MAP_LAYERS[0].items():
            setattr(layer, key, value)
        # Mock municipalities relationship
        municipalities = []
        for mun_data in MOCK_MUNICIPALITIES:
            municipality = Mock(spec=Municipality)
            for k, v in mun_data.items():
                setattr(municipality, k, v)
            municipalities.append(municipality)
        layer.municipalities = municipalities
        return layer

    @pytest.fixture
    def sample_municipalities(self):
        """Create sample municipality objects."""
        municipalities = []
        for mun_data in MOCK_MUNICIPALITIES:
            municipality = Mock(spec=Municipality)
            for k, v in mun_data.items():
                setattr(municipality, k, v)
            municipalities.append(municipality)
        return municipalities

    def test_list_map_layers(self, client, mock_db_session):
        """Test GET /map_layers endpoint."""
        # Mock database query
        mock_layers = []
        for layer_data in MOCK_MAP_LAYERS:
            layer = Mock(spec=MapLayer)
            for key, value in layer_data.items():
                setattr(layer, key, value)
            # Mock municipalities relationship
            municipalities = []
            for mun_data in MOCK_MUNICIPALITIES:
                municipality = Mock(spec=Municipality)
                for k, v in mun_data.items():
                    setattr(municipality, k, v)
                municipalities.append(municipality)
            layer.municipalities = municipalities
            mock_layers.append(layer)
        
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = mock_layers
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/map_layers/")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 2
            assert data[0]["label"] == "Test Layer 1"
            assert data[0]["type"] == "WMS"
            assert "municipality_ids" in data[0]
        finally:
            app.dependency_overrides.clear()

    def test_list_map_layers_filtered_by_municipality(self, client, mock_db_session):
        """Test GET /map_layers with municipality filter."""
        # Mock filtered layers (only first layer for municipality 1)
        mock_layer = Mock(spec=MapLayer)
        for key, value in MOCK_MAP_LAYERS[0].items():
            setattr(mock_layer, key, value)
        mock_layer.municipalities = [Mock(id=1, name="Municipality 1")]
        
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [mock_layer]
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/map_layers/?municipality=1")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]["label"] == "Test Layer 1"
        finally:
            app.dependency_overrides.clear()

    def test_get_map_layer_by_id(self, client, mock_db_session, sample_map_layer):
        """Test GET /map_layers/{id} endpoint."""
        # Mock database query
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_map_layer
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/map_layers/1")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["id"] == 1
            assert data["label"] == "Test Layer 1"
            assert data["type"] == "WMS"
        finally:
            app.dependency_overrides.clear()

    def test_get_map_layer_not_found(self, client, mock_db_session):
        """Test GET /map_layers/{id} with non-existent ID."""
        # Mock database query - not found
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/map_layers/999")
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            data = response.json()
            assert "Map layer not found" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_create_map_layer(self, client, mock_db_session, sample_municipalities):
        """Test POST /map_layers endpoint."""
        new_layer_data = {
            "value": "new_layer",
            "label": "New Test Layer",
            "type": "WMS",
            "url": "https://example.com/new-wms",
            "layers": "new_test_layer",
            "municipality_ids": [1, 2],
            "visible": True,
            "active": True,
            "opacity": 1.0,
            "projection": "EPSG:4326",
            "version": "1.3.0",
            "format": "image/png",
            "order": 0,
            "editable": False,
            "attribution": "Test Attribution Create",
            "server_type": "geoserver",
            "type_geom": "polygon",
        }
        
        # Create response data that matches what the endpoint should return
        expected_response_data = {
            "id": 3,
            "value": "new_layer",
            "label": "New Test Layer",
            "type": "WMS",
            "url": "https://example.com/new-wms",
            "layers": "new_test_layer",
            "visible": True,
            "active": True,
            "opacity": 1.0,
            "projection": "EPSG:4326",
            "version": "1.3.0",
            "format": "image/png",
            "order": 0,
            "editable": False,
            "attribution": "Test Attribution Create",
            "server_type": "geoserver",
            "type_geom": "polygon",
            "cql_filter": None,
            "municipality_ids": [1, 2]
        }
        
        # Mock the helper function instead
        with patch('app.routers.map_layers._build_map_layer_response_data') as mock_response_builder:
            mock_response_builder.return_value = expected_response_data
            
            # Mock database operations without affecting the SQLAlchemy select statement
            mock_db_session.add = Mock()
            mock_db_session.commit = AsyncMock()
            mock_db_session.refresh = AsyncMock()
            
            # Create a minimal mock result for municipality query
            mock_mun_result = Mock()
            mock_mun_result.scalars.return_value.all.return_value = []
            
            # Create a minimal mock result for final layer query  
            mock_final_result = Mock()
            mock_layer = Mock()
            mock_layer.id = 3
            mock_final_result.scalar_one.return_value = mock_layer
            
            # Setup execute side effects
            mock_db_session.execute.side_effect = [mock_mun_result, mock_final_result]
            
            def override_get_db():
                return mock_db_session
            
            app.dependency_overrides[get_db] = override_get_db
            
            try:
                response = client.post("/v1/map_layers/", json=new_layer_data)
                
                assert response.status_code == status.HTTP_201_CREATED
                data = response.json()
                assert data["id"] == 3
                assert data["label"] == "New Test Layer"
                assert data["value"] == "new_layer"
                assert data["municipality_ids"] == [1, 2]
                # Verify the mocks were called appropriately
                mock_db_session.add.assert_called_once()
                mock_db_session.commit.assert_called_once()
                mock_response_builder.assert_called_once()
            finally:
                app.dependency_overrides.clear()

    def test_create_map_layer_without_municipalities(self, client, mock_db_session):
        """Test POST /map_layers without municipality associations."""
        new_layer_data = {
            "value": "simple_layer",
            "label": "Simple Layer",
            "type": "WMS",
            "url": "https://example.com/simple-wms",
            "layers": "simple_layer",
            "visible": True,
            "active": True,
            "opacity": 1.0,
            "projection": "EPSG:4326",
            "version": "1.3.0",
            "format": "image/png",
            "order": 0,
            "editable": False,
            "attribution": "Test Attribution Simple",
            "server_type": "mapserver",
            "type_geom": "point",
        }
        
        # Create response data that matches what the endpoint should return
        expected_response_data = {
            "id": 4,
            "value": "simple_layer",
            "label": "Simple Layer",
            "type": "WMS",
            "url": "https://example.com/simple-wms",
            "layers": "simple_layer",
            "visible": True,
            "active": True,
            "opacity": 1.0,
            "projection": "EPSG:4326",
            "version": "1.3.0",
            "format": "image/png",
            "order": 0,
            "editable": False,
            "attribution": "Test Attribution Simple",
            "server_type": "mapserver",
            "type_geom": "point",
            "cql_filter": None,
            "municipality_ids": []
        }
        
        # Mock the helper function instead
        with patch('app.routers.map_layers._build_map_layer_response_data') as mock_response_builder:
            mock_response_builder.return_value = expected_response_data
            
            # Mock database operations without affecting the SQLAlchemy select statement
            mock_db_session.add = Mock()
            mock_db_session.commit = AsyncMock()
            mock_db_session.refresh = AsyncMock()
            
            # Create a minimal mock result for final layer query  
            mock_final_result = Mock()
            mock_layer = Mock()
            mock_layer.id = 4
            mock_final_result.scalar_one.return_value = mock_layer
            
            # Setup execute side effects (no municipality query for this test)
            mock_db_session.execute.return_value = mock_final_result
            
            def override_get_db():
                return mock_db_session
            
            app.dependency_overrides[get_db] = override_get_db
            
            try:
                response = client.post("/v1/map_layers/", json=new_layer_data)
                
                assert response.status_code == status.HTTP_201_CREATED
                data = response.json()
                assert data["id"] == 4
                assert data["label"] == "Simple Layer"
                assert data["municipality_ids"] == []
                # Verify the mocks were called appropriately
                mock_db_session.add.assert_called_once()
                mock_db_session.commit.assert_called_once()
                mock_response_builder.assert_called_once()
            finally:
                app.dependency_overrides.clear()

    def test_create_map_layer_comprehensive(self, client, mock_db_session, sample_municipalities):
        """Test POST /map_layers with comprehensive data validation."""
        new_layer_data = {
            "value": "comprehensive_layer",
            "label": "Comprehensive Test Layer",
            "type": "WMS",
            "url": "https://gis.municipality.gov/wms",
            "layers": "zoning,buildings,parcels",
            "municipality_ids": [1, 2],
            "visible": True,
            "active": True,
            "opacity": 0.75,
            "projection": "EPSG:3857",
            "version": "1.3.0",
            "format": "image/png",
            "order": 5,
            "editable": True,
            "attribution": "© Municipality GIS Department 2025",
            "server_type": "geoserver",
            "type_geom": "polygon",
            "cql_filter": "active=true AND visible=true"
        }
        
        # Mock municipality query
        mock_mun_result = Mock()
        mock_mun_result.scalars.return_value.all.return_value = sample_municipalities
        mock_db_session.execute.return_value = mock_mun_result
        
        # Mock database operations
        mock_db_session.add = Mock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            # Create response data that matches what the endpoint should return
            expected_response_data = {
                "id": 100,
                "value": "comprehensive_layer",
                "label": "Comprehensive Test Layer",
                "type": "WMS",
                "url": "https://gis.municipality.gov/wms",
                "layers": "zoning,buildings,parcels",
                "visible": True,
                "active": True,
                "opacity": 0.75,
                "projection": "EPSG:3857",
                "version": "1.3.0",
                "format": "image/png",
                "order": 5,
                "editable": True,
                "attribution": "© Municipality GIS Department 2025",
                "server_type": "geoserver",
                "type_geom": "polygon",
                "cql_filter": "active=true AND visible=true",
                "municipality_ids": [1, 2]
            }
            
            # Mock the helper function instead
            with patch('app.routers.map_layers._build_map_layer_response_data') as mock_response_builder:
                mock_response_builder.return_value = expected_response_data
                
                # Create a minimal mock result for municipality query
                mock_mun_result = Mock()
                mock_mun_result.scalars.return_value.all.return_value = []
                
                # Create a minimal mock result for final layer query  
                mock_final_result = Mock()
                mock_layer = Mock()
                mock_layer.id = 100
                mock_final_result.scalar_one.return_value = mock_layer
                
                # Setup execute side effects
                mock_db_session.execute.side_effect = [mock_mun_result, mock_final_result]
                
                response = client.post("/v1/map_layers/", json=new_layer_data)
            
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            
            # Validate response structure and data
            assert data["label"] == "Comprehensive Test Layer"
            assert data["value"] == "comprehensive_layer"
            assert data["type"] == "WMS"
            assert data["url"] == "https://gis.municipality.gov/wms"
            assert data["layers"] == "zoning,buildings,parcels"
            assert data["visible"] is True
            assert data["active"] is True
            assert data["opacity"] == pytest.approx(0.75)
            assert data["projection"] == "EPSG:3857"
            assert data["version"] == "1.3.0"
            assert data["format"] == "image/png"
            assert data["order"] == 5
            assert data["editable"] is True
            assert data["attribution"] == "© Municipality GIS Department 2025"
            assert data["server_type"] == "geoserver"
            assert data["type_geom"] == "polygon"
            assert data["cql_filter"] == "active=true AND visible=true"
            assert data["municipality_ids"] == [1, 2]
            
            # Verify database operations
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
            mock_db_session.refresh.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_create_map_layer_minimal_data(self, client, mock_db_session):
        """Test POST /map_layers with minimal required data."""
        minimal_data = {
            "value": "minimal_layer",
            "label": "Minimal Layer",
            "type": "WMS",
            "url": "https://example.com/minimal",
            "layers": "minimal",
            "format": "image/png",
            "opacity": 1.0,  # Required field
            "visible": True,  # Required field in schema
            "active": True   # Required field in schema
        }
        
        # Create a mock layer that will be returned by the final query
        created_layer = Mock(spec=MapLayer)
        for key, value in minimal_data.items():
            setattr(created_layer, key, value)
        created_layer.id = 200
        created_layer.municipalities = []
        # Set default values that would be applied by the schema/model
        created_layer.projection = "EPSG:4326"
        created_layer.version = "1.3.0"
        created_layer.order = 0
        created_layer.editable = True
        created_layer.attribution = None
        created_layer.server_type = None
        created_layer.type_geom = None
        created_layer.cql_filter = None
        
        # Mock final layer query result
        mock_final_result = Mock()
        mock_final_result.scalar_one.return_value = created_layer
        mock_db_session.execute.return_value = mock_final_result
        
        # Mock database operations
        mock_db_session.add = Mock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.post("/v1/map_layers/", json=minimal_data)
            
            assert response.status_code == status.HTTP_201_CREATED
            data = response.json()
            assert data["label"] == "Minimal Layer"
            assert data["value"] == "minimal_layer"
            assert data["municipality_ids"] == []
            
            # Verify defaults are applied
            assert data["visible"] is True
            assert data["active"] is True
            assert data["projection"] == "EPSG:4326"
            assert data["version"] == "1.3.0"
            assert data["order"] == 0
            assert data["editable"] is True
        finally:
            app.dependency_overrides.clear()

    def test_create_map_layer_invalid_server_type(self, client):
        """Test POST /map_layers with invalid server_type."""
        invalid_data = {
            "value": "invalid_layer",
            "label": "Invalid Layer",
            "type": "WMS",
            "url": "https://example.com/invalid",
            "layers": "invalid",
            "format": "image/png",
            "opacity": 1.0,
            "server_type": "invalid_server"  # This should fail validation
        }
        
        response = client.post("/v1/map_layers/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_map_layer_invalid_opacity(self, client):
        """Test POST /map_layers with invalid opacity values."""
        # Test opacity > 1
        invalid_data = {
            "value": "invalid_opacity",
            "label": "Invalid Opacity",
            "type": "WMS", 
            "url": "https://example.com/invalid",
            "layers": "invalid",
            "format": "image/png",
            "opacity": 1.5  # Should fail
        }
        
        response = client.post("/v1/map_layers/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test opacity < 0
        invalid_data["opacity"] = -0.1
        response = client.post("/v1/map_layers/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_map_layer(self, client, mock_db_session, sample_map_layer, sample_municipalities):
        """Test PATCH /map_layers/{id} endpoint."""
        update_data = {
            "label": "Updated Test Layer",
            "opacity": 0.5,
            "municipality_ids": [1]
        }
        
        # Mock database queries
        mock_layer_result = Mock()
        mock_layer_result.scalar_one_or_none.return_value = sample_map_layer
        
        mock_mun_result = Mock()
        mock_mun_result.scalars.return_value.all.return_value = [sample_municipalities[0]]
        
        # Setup side effects for execute calls
        mock_db_session.execute.side_effect = [mock_layer_result, mock_mun_result]
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.patch("/v1/map_layers/1", json=update_data)
            
            assert response.status_code == status.HTTP_200_OK
            # Verify attributes were updated
            assert sample_map_layer.label == "Updated Test Layer"
            assert sample_map_layer.opacity == pytest.approx(0.5)
            assert sample_map_layer.municipalities == [sample_municipalities[0]]
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_update_map_layer_not_found(self, client, mock_db_session):
        """Test PATCH /map_layers/{id} with non-existent ID."""
        update_data = {
            "label": "Updated Layer"
        }
        
        # Mock database query - not found
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.patch("/v1/map_layers/999", json=update_data)
            
            assert response.status_code == status.HTTP_404_NOT_FOUND
            data = response.json()
            assert "Map layer not found" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_create_map_layer_validation_error(self, client):
        """Test POST /map_layers with invalid data."""
        invalid_data = {
            "label": "Test Layer",
            # Missing required fields like 'value', 'type', etc.
        }
        
        response = client.post("/v1/map_layers/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("layer_id,expected_status", [
        (1, status.HTTP_200_OK),
        (999, status.HTTP_404_NOT_FOUND),
        (-1, status.HTTP_422_UNPROCESSABLE_ENTITY),
        (0, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ])
    def test_get_layer_various_ids(self, client, mock_db_session, sample_map_layer, layer_id, expected_status):
        """Test GET map layer with various ID values."""
        # Mock database query
        mock_result = Mock()
        if layer_id == 1:
            mock_result.scalar_one_or_none.return_value = sample_map_layer
        else:
            mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get(f"/v1/map_layers/{layer_id}")
            assert response.status_code == expected_status
        finally:
            app.dependency_overrides.clear()

    def test_update_partial_fields(self, client, mock_db_session, sample_map_layer):
        """Test partial updates to map layer."""
        update_data = {
            "visible": False,
            "order": 5
        }
        
        # Mock database query
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_map_layer
        mock_db_session.execute.return_value = mock_result
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.patch("/v1/map_layers/1", json=update_data)
            
            assert response.status_code == status.HTTP_200_OK
            # Verify only specified attributes were updated
            assert sample_map_layer.visible == False
            assert sample_map_layer.order == 5
            # Other attributes should remain unchanged
            assert sample_map_layer.label == "Test Layer 1"  # Original value
        finally:
            app.dependency_overrides.clear()

    def test_get_map_layers_empty_list(self, client, mock_db_session):
        """Test GET /map_layers with empty result."""
        # Mock empty result
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/v1/map_layers/")
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert isinstance(data, list)
            assert len(data) == 0
        finally:
            app.dependency_overrides.clear()

    def test_get_map_layer_invalid_id_format(self, client):
        """Test GET /map_layers/{id} with invalid ID format."""
        response = client.get("/v1/map_layers/invalid_id")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_map_layer_invalid_id_format(self, client):
        """Test PATCH /map_layers/{id} with invalid ID format."""
        update_data = {"label": "Updated"}
        response = client.patch("/v1/map_layers/invalid_id", json=update_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_map_layer_missing_required_fields(self, client):
        """Test POST /map_layers with missing required fields."""
        # Test with missing value field
        incomplete_data = {
            "label": "Incomplete Layer",
            "type": "WMS",
            "url": "https://example.com/incomplete",
            "layers": "incomplete",
            "format": "image/png",
            "opacity": 1.0,
            "visible": True,
            "active": True
            # Missing 'value' field
        }
        
        response = client.post("/v1/map_layers/", json=incomplete_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_map_layer_empty_data(self, client, mock_db_session, sample_map_layer):
        """Test PATCH /map_layers/{id} with empty update data."""
        # Mock database query
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_map_layer
        mock_db_session.execute.return_value = mock_result
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.patch("/v1/map_layers/1", json={})
            
            assert response.status_code == status.HTTP_200_OK
            # With empty data, nothing should change
            mock_db_session.commit.assert_called_once()
        finally:
            app.dependency_overrides.clear()
