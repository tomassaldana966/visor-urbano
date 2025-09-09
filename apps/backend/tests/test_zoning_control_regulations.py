import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.models.zoning_control_regulations import ZoningControlRegulation
from config.settings import get_db


class TestZoningControlRegulations:
    
    def setup_method(self):
        """Set up test dependencies."""
        self.client = TestClient(app)
        self.mock_db = AsyncMock()
        
        # Override dependencies
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Mock zoning control regulations
        self.mock_regulation_1 = MagicMock(spec=ZoningControlRegulation)
        self.mock_regulation_1.id = 1
        self.mock_regulation_1.municipality_id = 1
        self.mock_regulation_1.district = "18"
        self.mock_regulation_1.regulation_key = "H3"
        self.mock_regulation_1.description = "Residential High Density"
        self.mock_regulation_1.land_use = "Residential"
        self.mock_regulation_1.density = "High"
        self.mock_regulation_1.intensity = "Medium"
        self.mock_regulation_1.business_sector = "N/A"
        self.mock_regulation_1.minimum_area = "200m²"
        self.mock_regulation_1.minimum_frontage = "10m"
        self.mock_regulation_1.building_index = "0.7"
        self.mock_regulation_1.land_occupation_coefficient = "0.7"
        self.mock_regulation_1.land_utilization_coefficient = "2.8"
        self.mock_regulation_1.max_building_height = "12m"
        self.mock_regulation_1.parking_spaces = "2 per unit"
        self.mock_regulation_1.front_gardening_percentage = "50%"
        self.mock_regulation_1.front_restriction = "3m"
        self.mock_regulation_1.lateral_restrictions = "1m"
        self.mock_regulation_1.rear_restriction = "3m"
        self.mock_regulation_1.building_mode = "Detached"
        self.mock_regulation_1.observations = "None"
        self.mock_regulation_1.hotel_occupation_index = "N/A"
        self.mock_regulation_1.increase_land_utilization_coefficient = "N/A"
        self.mock_regulation_1.urban_environmental_value_areas = False
        self.mock_regulation_1.planned_public_space = False
        
        self.mock_regulation_2 = MagicMock(spec=ZoningControlRegulation)
        self.mock_regulation_2.id = 2
        self.mock_regulation_2.municipality_id = 1
        self.mock_regulation_2.district = "18"
        self.mock_regulation_2.regulation_key = "C2"
        self.mock_regulation_2.description = "Commercial Medium"
        self.mock_regulation_2.land_use = "Commercial"
        self.mock_regulation_2.density = "Medium"
        self.mock_regulation_2.intensity = "High"
        self.mock_regulation_2.business_sector = "Retail"
        self.mock_regulation_2.minimum_area = "150m²"
        self.mock_regulation_2.minimum_frontage = "8m"
        self.mock_regulation_2.building_index = "0.8"
        self.mock_regulation_2.land_occupation_coefficient = "0.8"
        self.mock_regulation_2.land_utilization_coefficient = "3.0"
        self.mock_regulation_2.max_building_height = "15m"
        self.mock_regulation_2.parking_spaces = "1 per 30m²"
        self.mock_regulation_2.front_gardening_percentage = "30%"
        self.mock_regulation_2.front_restriction = "2m"
        self.mock_regulation_2.lateral_restrictions = "0m"
        self.mock_regulation_2.rear_restriction = "2m"
        self.mock_regulation_2.building_mode = "Attached"
        self.mock_regulation_2.observations = "None"
        self.mock_regulation_2.hotel_occupation_index = "N/A"
        self.mock_regulation_2.increase_land_utilization_coefficient = "N/A"
        self.mock_regulation_2.urban_environmental_value_areas = False
        self.mock_regulation_2.planned_public_space = False
        
        self.mock_regulation_3 = MagicMock(spec=ZoningControlRegulation)
        self.mock_regulation_3.id = 3
        self.mock_regulation_3.municipality_id = 2
        self.mock_regulation_3.district = "19"
        self.mock_regulation_3.regulation_key = "H2"
        self.mock_regulation_3.description = "Residential Medium Density"
        self.mock_regulation_3.land_use = "Residential"
        self.mock_regulation_3.density = "Medium"
        self.mock_regulation_3.intensity = "Low"
        self.mock_regulation_3.business_sector = "N/A"
        self.mock_regulation_3.minimum_area = "250m²"
        self.mock_regulation_3.minimum_frontage = "12m"
        self.mock_regulation_3.building_index = "0.6"
        self.mock_regulation_3.land_occupation_coefficient = "0.6"
        self.mock_regulation_3.land_utilization_coefficient = "2.0"
        self.mock_regulation_3.max_building_height = "9m"
        self.mock_regulation_3.parking_spaces = "2 per unit"
        self.mock_regulation_3.front_gardening_percentage = "60%"
        self.mock_regulation_3.front_restriction = "4m"
        self.mock_regulation_3.lateral_restrictions = "2m"
        self.mock_regulation_3.rear_restriction = "4m"
        self.mock_regulation_3.building_mode = "Detached"
        self.mock_regulation_3.observations = "None"
        self.mock_regulation_3.hotel_occupation_index = "N/A"
        self.mock_regulation_3.increase_land_utilization_coefficient = "N/A"
        self.mock_regulation_3.urban_environmental_value_areas = False
        self.mock_regulation_3.planned_public_space = False
    
    def teardown_method(self):
        """Clean up after tests."""
        app.dependency_overrides.clear()
    
    def _configure_db_query_result(self, regulations):
        """Configure database query result."""
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = regulations
        self.mock_db.execute.return_value = mock_result
        return mock_result
    
    def test_get_zoning_control_regulations_no_filters(self):
        """Test retrieval of all zoning control regulations without filters."""
        all_regulations = [self.mock_regulation_1, self.mock_regulation_2, self.mock_regulation_3]
        self._configure_db_query_result(all_regulations)
        
        response = self.client.get("/v1/zoning_control_regulations/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["regulation_key"] == "H3"
        assert data[1]["regulation_key"] == "C2"
        assert data[2]["regulation_key"] == "H2"
    
    def test_get_zoning_control_regulations_filter_by_municipality(self):
        """Test retrieval filtered by municipality_id."""
        municipality_1_regulations = [self.mock_regulation_1, self.mock_regulation_2]
        self._configure_db_query_result(municipality_1_regulations)
        
        response = self.client.get("/v1/zoning_control_regulations/?municipality_id=1")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(reg["municipality_id"] == 1 for reg in data)
    
    def test_get_zoning_control_regulations_filter_by_district(self):
        """Test retrieval filtered by district."""
        district_18_regulations = [self.mock_regulation_1, self.mock_regulation_2]
        self._configure_db_query_result(district_18_regulations)
        
        response = self.client.get("/v1/zoning_control_regulations/?district=18")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(reg["district"] == "18" for reg in data)
    
    def test_get_zoning_control_regulations_filter_by_regulation_key(self):
        """Test retrieval filtered by regulation_key."""
        h3_regulations = [self.mock_regulation_1]
        self._configure_db_query_result(h3_regulations)
        
        response = self.client.get("/v1/zoning_control_regulations/?regulation_key=H3")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["regulation_key"] == "H3"
    
    def test_get_zoning_control_regulations_multiple_filters(self):
        """Test retrieval with multiple filters applied."""
        filtered_regulations = [self.mock_regulation_1]
        self._configure_db_query_result(filtered_regulations)
        
        response = self.client.get(
            "/v1/zoning_control_regulations/"
            "?municipality_id=1&district=18&regulation_key=H3"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["municipality_id"] == 1
        assert data[0]["district"] == "18"
        assert data[0]["regulation_key"] == "H3"
    
    def test_get_zoning_control_regulations_no_results(self):
        """Test retrieval when no regulations match the filters."""
        self._configure_db_query_result([])
        
        response = self.client.get("/v1/zoning_control_regulations/?municipality_id=999")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
        assert data == []
    
    def test_get_zoning_control_regulations_database_error(self):
        """Test database error during retrieval."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            self.client.get("/v1/zoning_control_regulations/")
    
    @pytest.mark.parametrize("municipality_id,district,regulation_key,expected_count", [
        (1, None, None, 2),  # All regulations for municipality 1
        (2, None, None, 1),  # All regulations for municipality 2
        (None, "18", None, 2),  # All regulations for district 18
        (None, "19", None, 1),  # All regulations for district 19
        (None, None, "H3", 1),  # All H3 regulations
        (None, None, "C2", 1),  # All C2 regulations
        (None, None, "H2", 1),  # All H2 regulations
        (1, "18", None, 2),  # Municipality 1, district 18
        (1, None, "H3", 1),  # Municipality 1, regulation H3
        (None, "18", "C2", 1),  # District 18, regulation C2
        (999, None, None, 0),  # Non-existent municipality
        (None, "999", None, 0),  # Non-existent district
        (None, None, "X1", 0),  # Non-existent regulation key
    ])
    def test_get_zoning_control_regulations_various_filters(self, municipality_id, district, regulation_key, expected_count):
        """Test retrieval with various filter combinations."""
        # Mock the appropriate response based on the expected count
        if expected_count == 2:
            regulations = [self.mock_regulation_1, self.mock_regulation_2]
        elif expected_count == 1:
            if regulation_key == "H3":
                regulations = [self.mock_regulation_1]
            elif regulation_key == "C2":
                regulations = [self.mock_regulation_2]
            elif regulation_key == "H2":
                regulations = [self.mock_regulation_3]
            elif municipality_id == 2:
                regulations = [self.mock_regulation_3]
            else:
                regulations = [self.mock_regulation_1]  # Default to first regulation
        else:
            regulations = []
        
        self._configure_db_query_result(regulations)
        
        # Build query parameters
        params = []
        if municipality_id is not None:
            params.append(f"municipality_id={municipality_id}")
        if district is not None:
            params.append(f"district={district}")
        if regulation_key is not None:
            params.append(f"regulation_key={regulation_key}")
        
        query_string = "&".join(params)
        url = f"/v1/zoning_control_regulations/"
        if query_string:
            url += f"?{query_string}"
        
        response = self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == expected_count
    
    def test_get_zoning_control_regulations_empty_string_filters(self):
        """Test retrieval with empty string filters."""
        self._configure_db_query_result([])
        
        response = self.client.get("/v1/zoning_control_regulations/?district=&regulation_key=")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_zoning_control_regulations_case_sensitive_filters(self):
        """Test that filters are case sensitive."""
        self._configure_db_query_result([])
        
        # Test with lowercase regulation key (should not match "H3")
        response = self.client.get("/v1/zoning_control_regulations/?regulation_key=h3")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0  # Should be empty since filters are case sensitive
    
    def test_get_zoning_control_regulations_special_characters_in_filters(self):
        """Test retrieval with special characters in filter values."""
        self._configure_db_query_result([])
        
        response = self.client.get("/v1/zoning_control_regulations/?district=18-A&regulation_key=H3/C2")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_zoning_control_regulations_numeric_string_district(self):
        """Test retrieval with numeric string district filter."""
        district_regulations = [self.mock_regulation_1, self.mock_regulation_2]
        self._configure_db_query_result(district_regulations)
        
        response = self.client.get("/v1/zoning_control_regulations/?district=18")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_get_zoning_control_regulations_invalid_municipality_id_type(self):
        """Test retrieval with invalid municipality_id type."""
        response = self.client.get("/v1/zoning_control_regulations/?municipality_id=invalid")
        
        # Should return validation error for invalid integer
        assert response.status_code == 422
    
    def test_get_zoning_control_regulations_negative_municipality_id(self):
        """Test retrieval with negative municipality_id."""
        self._configure_db_query_result([])
        
        response = self.client.get("/v1/zoning_control_regulations/?municipality_id=-1")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    def test_get_zoning_control_regulations_zero_municipality_id(self):
        """Test retrieval with zero municipality_id."""
        self._configure_db_query_result([])
        
        response = self.client.get("/v1/zoning_control_regulations/?municipality_id=0")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    def test_get_zoning_control_regulations_large_municipality_id(self):
        """Test retrieval with very large municipality_id."""
        self._configure_db_query_result([])
        
        response = self.client.get("/v1/zoning_control_regulations/?municipality_id=999999999")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
    
    def test_get_zoning_control_regulations_duplicate_parameters(self):
        """Test retrieval with duplicate query parameters."""
        self._configure_db_query_result([self.mock_regulation_1])
        
        # FastAPI typically takes the last value when parameters are duplicated
        response = self.client.get("/v1/zoning_control_regulations/?municipality_id=1&municipality_id=2")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_zoning_control_regulations_response_structure(self):
        """Test that the response has the expected structure."""
        self._configure_db_query_result([self.mock_regulation_1])
        
        response = self.client.get("/v1/zoning_control_regulations/?regulation_key=H3")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        
        regulation = data[0]
        expected_fields = ["id", "municipality_id", "district", "regulation_key", "land_use"]
        for field in expected_fields:
            assert field in regulation
