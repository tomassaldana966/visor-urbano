import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.models.zoning_impact_level import ZoningImpactLevel
from config.settings import get_db
from geoalchemy2.elements import WKBElement


class TestZoningImpactLevels:
    
    def setup_method(self):
        """Set up test dependencies."""
        self.client = TestClient(app)
        self.mock_db = AsyncMock()
        
        # Configure db methods properly - add is synchronous, commit/refresh are async
        self.mock_db.add = MagicMock(return_value=None)
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()
        self.mock_db.delete = AsyncMock()
        
        # Override dependencies
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Setup global patches for geometry handling
        self.shape_patcher = patch('app.routers.zoning_impact_levels.to_shape')
        self.mock_to_shape = self.shape_patcher.start()
        self.mock_to_shape.return_value = MagicMock()
        
        self.mapping_patcher = patch('app.routers.zoning_impact_levels.mapping')
        self.mock_mapping = self.mapping_patcher.start()
        self.mock_mapping.return_value = {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}
        
        # Mock zoning impact levels
        self.mock_zone_1 = MagicMock(spec=ZoningImpactLevel)
        self.mock_zone_1.id = 1
        self.mock_zone_1.impact_level = 3  # HIGH = 3
        self.mock_zone_1.municipality_id = 1
        # Use a proper mock for WKBElement
        mock_geometry = MagicMock(spec=WKBElement)
        self.mock_zone_1.geom = mock_geometry
        
        self.mock_zone_2 = MagicMock(spec=ZoningImpactLevel)
        self.mock_zone_2.id = 2
        self.mock_zone_2.impact_level = 2  # MEDIUM = 2
        self.mock_zone_2.municipality_id = 1
        self.mock_zone_2.geom = None  # No geometry
        
        self.mock_zone_3 = MagicMock(spec=ZoningImpactLevel)
        self.mock_zone_3.id = 3
        self.mock_zone_3.impact_level = 1  # LOW = 1
        self.mock_zone_3.municipality_id = 2
        self.mock_zone_3.geom = MagicMock(spec=WKBElement)
    
    def teardown_method(self):
        """Clean up after tests."""
        # Stop the patches
        self.shape_patcher.stop()
        self.mapping_patcher.stop()
        app.dependency_overrides.clear()
    
    def _configure_db_query_result(self, zones=None, single_zone=None):
        """Configure database query result."""
        mock_result = MagicMock()
        if zones is not None:
            mock_result.scalars.return_value.all.return_value = zones
        if single_zone is not None:
            mock_result.scalar_one_or_none.return_value = single_zone
        self.mock_db.execute = AsyncMock(return_value=mock_result)
        return mock_result
    
    def test_list_zoning_impact_levels_success(self):
        """Test successful listing of zoning impact levels."""
        # We already have the geometry mocks set up in setup_method
        
        zones = [self.mock_zone_1, self.mock_zone_2]
        self._configure_db_query_result(zones=zones)
        
        response = self.client.get("/v1/zoning_impact_levels/?municipality_id=1")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[0]["impact_level"] == 3  # HIGH = 3
        assert data[0]["municipality_id"] == 1
        assert data[0]["geom"] is not None
        assert data[1]["id"] == 2
        assert data[1]["impact_level"] == 2  # MEDIUM = 2
        assert data[1]["geom"] is None  # No geometry for this zone
    
    def test_list_zoning_impact_levels_missing_municipality_id(self):
        """Test listing without municipality_id parameter."""
        response = self.client.get("/v1/zoning_impact_levels/")
        
        assert response.status_code == 422  # Validation error
    
    def test_list_zoning_impact_levels_no_results(self):
        """Test listing when no zones are found."""
        self._configure_db_query_result(zones=[])
        
        response = self.client.get("/v1/zoning_impact_levels/?municipality_id=999")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        assert data == []
    
    def test_list_zoning_impact_levels_database_error(self):
        """Test database error during listing."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            self.client.get("/v1/zoning_impact_levels/?municipality_id=1")
    
    def test_get_zoning_impact_level_success(self):
        """Test successful retrieval of single zoning impact level."""
        # We already have the geometry mocks set up in setup_method
        
        self._configure_db_query_result(single_zone=self.mock_zone_1)
        
        response = self.client.get("/v1/zoning_impact_levels/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["impact_level"] == 3  # HIGH = 3
        assert data["municipality_id"] == 1
        assert data["geom"] is not None
    
    def test_get_zoning_impact_level_not_found(self):
        """Test retrieval when zoning impact level is not found."""
        # Configure the mock to return None for a non-existent zone
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute.return_value = mock_result
        
        # Make sure our to_shape and mapping functions won't be called
        # since the zone doesn't exist
        with patch('app.routers.zoning_impact_levels.to_shape') as patched_to_shape, \
             patch('app.routers.zoning_impact_levels.mapping') as patched_mapping:
            
            response = self.client.get("/v1/zoning_impact_levels/999")
            
            patched_to_shape.assert_not_called()
            patched_mapping.assert_not_called()
            
            assert response.status_code == 404
            assert "Zoning impact level not found" in response.json()["detail"]
    
    def test_get_zoning_impact_level_no_geometry(self):
        """Test retrieval of zone without geometry."""
        # Reset our mock objects to track calls
        self.mock_to_shape.reset_mock()
        self.mock_mapping.reset_mock()
        
        self._configure_db_query_result(single_zone=self.mock_zone_2)
        
        response = self.client.get("/v1/zoning_impact_levels/2")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 2
        assert data["impact_level"] == 2  # MEDIUM = 2
        assert data["geom"] is None
        # to_shape and mapping should not be called when geom is None
        # These assertions will use the class-level mocks
        # If there are any calls to these functions for the None geometry, the call count would be > 0
        assert self.mock_to_shape.call_count == 0
        assert self.mock_mapping.call_count == 0
    
    @patch('app.routers.zoning_impact_levels.mapping')
    @patch('app.routers.zoning_impact_levels.to_shape')
    def test_create_zoning_impact_level_success(self, mock_to_shape, mock_mapping):
        """Test successful creation of zoning impact level."""
        mock_to_shape.return_value = MagicMock()
        mock_mapping.return_value = {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}
        
        # Mock the new zone to be returned after creation
        with patch('app.models.zoning_impact_level.ZoningImpactLevel') as mock_zone_class:
            mock_new_zone = MagicMock()
            mock_new_zone.id = 4
            mock_new_zone.impact_level = 4  # CRITICAL = 4
            mock_new_zone.municipality_id = 1
            mock_new_zone.geom = MagicMock()
            mock_zone_class.return_value = mock_new_zone
            
            # Configure the refresh mock to ensure the object has the id after refresh
            async def mock_refresh(obj):
                obj.id = 4  # Simulate DB assigning an ID
                
            self.mock_db.refresh = AsyncMock(side_effect=mock_refresh)
            
            payload = {
                "impact_level": 4,  # CRITICAL = 4
                "municipality_id": 1,
                "geom": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}
            }
            
            response = self.client.post("/v1/zoning_impact_levels/", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 4
            assert data["impact_level"] == 4  # CRITICAL = 4
            assert data["municipality_id"] == 1
            assert data["geom"] is not None
            self.mock_db.add.assert_called_once()
            self.mock_db.commit.assert_called_once()
    
    def test_create_zoning_impact_level_database_error(self):
        """Test database error during creation."""
        # Mock the ZoningImpactLevel class to return a mock object
        with patch('app.models.zoning_impact_level.ZoningImpactLevel') as mock_zone_class:
            mock_new_zone = MagicMock()
            mock_zone_class.return_value = mock_new_zone
            
            # Configure the add method to raise an exception
            self.mock_db.add.side_effect = Exception("Database error")
            
            payload = {
                "impact_level": 3,  # HIGH = 3
                "municipality_id": 1
            }
            
            with pytest.raises(Exception, match="Database error"):
                self.client.post("/v1/zoning_impact_levels/", json=payload)
    
    def test_create_zoning_impact_level_commit_error(self):
        """Test commit error during creation."""
        # Mock the ZoningImpactLevel class to return a mock object
        with patch('app.models.zoning_impact_level.ZoningImpactLevel') as mock_zone_class:
            mock_new_zone = MagicMock()
            mock_zone_class.return_value = mock_new_zone
            
            self.mock_db.add.return_value = None
            self.mock_db.commit.side_effect = Exception("Commit error")
            
            payload = {
                "impact_level": 2,  # MEDIUM = 2
                "municipality_id": 2
            }
            
            with pytest.raises(Exception, match="Commit error"):
                self.client.post("/v1/zoning_impact_levels/", json=payload)
    
    @patch('app.routers.zoning_impact_levels.mapping')
    @patch('app.routers.zoning_impact_levels.to_shape')
    def test_update_zoning_impact_level_success(self, mock_to_shape, mock_mapping):
        """Test successful update of zoning impact level."""
        mock_to_shape.return_value = MagicMock()
        mock_mapping.return_value = {"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}
        
        self._configure_db_query_result(single_zone=self.mock_zone_1)
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        payload = {
            "impact_level": 4,  # CRITICAL = 4
            "municipality_id": 1
        }
        
        response = self.client.patch("/v1/zoning_impact_levels/1", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        # The mock object should have been updated
        assert self.mock_zone_1.impact_level == 4  # CRITICAL = 4
        assert self.mock_zone_1.municipality_id == 1
        self.mock_db.commit.assert_called_once()
    
    def test_update_zoning_impact_level_not_found(self):
        """Test update when zoning impact level is not found."""
        # Explicitly configure the mock to return None for scalar_one_or_none
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute = AsyncMock(return_value=mock_result)
        
        payload = {
            "impact_level": 1  # LOW = 1
        }
        
        response = self.client.patch("/v1/zoning_impact_levels/999", json=payload)
        
        assert response.status_code == 404
        assert "Zoning Impact level not found" in response.json()["detail"]
    
    def test_update_zoning_impact_level_partial_update(self):
        """Test partial update of zoning impact level."""
        self._configure_db_query_result(single_zone=self.mock_zone_1)
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        # Only update impact_level, leave municipality_id unchanged
        payload = {
            "impact_level": 5  # EXTREME = 5
        }
        
        with patch('app.routers.zoning_impact_levels.mapping') as mock_mapping, \
             patch('app.routers.zoning_impact_levels.to_shape') as mock_to_shape:
            mock_to_shape.return_value = MagicMock()
            mock_mapping.return_value = {"type": "Polygon", "coordinates": []}
            
            response = self.client.patch("/v1/zoning_impact_levels/1", json=payload)
            
            assert response.status_code == 200
            assert self.mock_zone_1.impact_level == 5  # EXTREME = 5
            # municipality_id should remain unchanged
            assert self.mock_zone_1.municipality_id == 1
    
    def test_update_zoning_impact_level_database_error(self):
        """Test database error during update."""
        self._configure_db_query_result(single_zone=self.mock_zone_1)
        self.mock_db.commit.side_effect = Exception("Database error")
        
        payload = {
            "impact_level": 1  # LOW = 1
        }
        
        with pytest.raises(Exception):
            self.client.patch("/v1/zoning_impact_levels/1", json=payload)
    
    def test_delete_zoning_impact_level_success(self):
        """Test successful deletion of zoning impact level."""
        self._configure_db_query_result(single_zone=self.mock_zone_1)
        self.mock_db.delete.return_value = None
        self.mock_db.commit.return_value = None
        
        response = self.client.delete("/v1/zoning_impact_levels/1")
        
        assert response.status_code == 204
        self.mock_db.delete.assert_called_once_with(self.mock_zone_1)
        self.mock_db.commit.assert_called_once()
    
    def test_delete_zoning_impact_level_not_found(self):
        """Test deletion when zoning impact level is not found."""
        # Explicitly configure the mock to return None for scalar_one_or_none
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute = AsyncMock(return_value=mock_result)
        
        response = self.client.delete("/v1/zoning_impact_levels/999")
        
        assert response.status_code == 404
        assert "Zoning Impact level not found" in response.json()["detail"]
        self.mock_db.delete.assert_not_called()
    
    def test_delete_zoning_impact_level_database_error(self):
        """Test database error during deletion."""
        self._configure_db_query_result(single_zone=self.mock_zone_1)
        self.mock_db.delete.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            self.client.delete("/v1/zoning_impact_levels/1")
    
    def test_delete_zoning_impact_level_commit_error(self):
        """Test commit error during deletion."""
        self._configure_db_query_result(single_zone=self.mock_zone_1)
        self.mock_db.delete.return_value = None
        self.mock_db.commit.side_effect = Exception("Commit error")
        
        with pytest.raises(Exception):
            self.client.delete("/v1/zoning_impact_levels/1")
    
    @pytest.mark.parametrize("municipality_id,expected_zones", [
        (1, 2),  # Municipality 1 has 2 zones
        (2, 1),  # Municipality 2 has 1 zone
        (999, 0),  # Non-existent municipality has 0 zones
    ])
    def test_list_zoning_impact_levels_various_municipalities(self, municipality_id, expected_zones):
        """Test listing for various municipalities."""
        if municipality_id == 1:
            zones = [self.mock_zone_1, self.mock_zone_2]
        elif municipality_id == 2:
            zones = [self.mock_zone_3]
        else:
            zones = []
        
        self._configure_db_query_result(zones=zones)
        
        with patch('app.routers.zoning_impact_levels.mapping') as mock_mapping, \
             patch('app.routers.zoning_impact_levels.to_shape') as mock_to_shape:
            mock_to_shape.return_value = MagicMock()
            mock_mapping.return_value = {"type": "Polygon", "coordinates": []}
            
            response = self.client.get(f"/v1/zoning_impact_levels/?municipality_id={municipality_id}")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == expected_zones
    
    @pytest.mark.parametrize("impact_level", [
        1,  # LOW
        2,  # MEDIUM
        3,  # HIGH
        4,  # CRITICAL
        5,  # EXTREME
        0   # MINIMAL
    ])
    def test_create_zoning_impact_level_various_levels(self, impact_level):
        """Test creation with various impact levels."""
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        
        with patch('app.models.zoning_impact_level.ZoningImpactLevel') as mock_zone_class, \
             patch('app.routers.zoning_impact_levels.mapping') as mock_mapping, \
             patch('app.routers.zoning_impact_levels.to_shape') as mock_to_shape:
            
            mock_new_zone = MagicMock()
            mock_new_zone.id = 10
            mock_new_zone.impact_level = impact_level
            mock_new_zone.municipality_id = 1
            mock_new_zone.geom = None
            mock_zone_class.return_value = mock_new_zone
            
            # Mock the refresh to simulate DB setting the ID
            async def mock_refresh(obj):
                obj.id = 10
                obj.impact_level = impact_level
                obj.municipality_id = 1
                obj.geom = None
            
            self.mock_db.refresh = AsyncMock(side_effect=mock_refresh)
            
            payload = {
                "impact_level": impact_level,
                "municipality_id": 1
            }
            
            response = self.client.post("/v1/zoning_impact_levels/", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["impact_level"] == impact_level
            assert data["id"] == 10
            assert data["municipality_id"] == 1
    
    def test_create_zoning_impact_level_missing_required_field(self):
        """Test creation with missing required fields."""
        payload = {
            "impact_level": 3  # HIGH = 3
            # Missing municipality_id
        }
        
        response = self.client.post("/v1/zoning_impact_levels/", json=payload)
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_update_zoning_impact_level_empty_payload(self):
        """Test update with empty payload."""
        self._configure_db_query_result(single_zone=self.mock_zone_1)
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        payload = {}
        
        with patch('app.routers.zoning_impact_levels.mapping') as mock_mapping, \
             patch('app.routers.zoning_impact_levels.to_shape') as mock_to_shape:
            mock_to_shape.return_value = MagicMock()
            mock_mapping.return_value = {"type": "Polygon", "coordinates": []}
            
            response = self.client.patch("/v1/zoning_impact_levels/1", json=payload)
            
            assert response.status_code == 200
            # No changes should be applied
            self.mock_db.commit.assert_called_once()
    
    def test_list_zoning_impact_levels_invalid_municipality_id_type(self):
        """Test listing with invalid municipality_id type."""
        response = self.client.get("/v1/zoning_impact_levels/?municipality_id=invalid")
        
        # Should return validation error for invalid integer
        assert response.status_code == 422
    
    def test_get_zoning_impact_level_invalid_id_type(self):
        """Test retrieval with invalid ID type."""
        response = self.client.get("/v1/zoning_impact_levels/invalid")
        
        # Should return validation error for invalid integer
        assert response.status_code == 422
    
    def test_update_zoning_impact_level_invalid_id_type(self):
        """Test update with invalid ID type."""
        payload = {"impact_level": 3}  # HIGH = 3
        
        response = self.client.patch("/v1/zoning_impact_levels/invalid", json=payload)
        
        # Should return validation error for invalid integer
        assert response.status_code == 422
    
    def test_delete_zoning_impact_level_invalid_id_type(self):
        """Test deletion with invalid ID type."""
        response = self.client.delete("/v1/zoning_impact_levels/invalid")
        
        # Should return validation error for invalid integer
        assert response.status_code == 422
    
    @patch('app.routers.zoning_impact_levels.mapping')
    @patch('app.routers.zoning_impact_levels.to_shape')
    def test_geometry_processing_error(self, mock_to_shape, mock_mapping):
        """Test handling of geometry processing errors."""
        mock_to_shape.side_effect = Exception("Geometry processing error")
        
        self._configure_db_query_result(zones=[self.mock_zone_1])
        
        with pytest.raises(Exception):
            self.client.get("/v1/zoning_impact_levels/?municipality_id=1")
    
    @patch('app.routers.zoning_impact_levels.mapping')
    @patch('app.routers.zoning_impact_levels.to_shape')
    def test_response_structure_validation(self, mock_to_shape, mock_mapping):
        """Test that responses have the expected structure."""
        mock_to_shape.return_value = MagicMock()
        mock_mapping.return_value = {"type": "Polygon", "coordinates": []}
        
        self._configure_db_query_result(zones=[self.mock_zone_1])
        
        response = self.client.get("/v1/zoning_impact_levels/?municipality_id=1")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        
        zone = data[0]
        expected_fields = ["id", "impact_level", "municipality_id", "geom"]
        for field in expected_fields:
            assert field in zone
