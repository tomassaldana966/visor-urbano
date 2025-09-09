import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
import httpx

from app.main import app


class TestGeocode:
    def setup_method(self):
        """Setup for each test method."""
        self.client = TestClient(app)

    def teardown_method(self):
        """Cleanup after each test method."""
        app.dependency_overrides.clear()

    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_geocode_address_success(self, mock_get):
        """Test successful geocoding of an address."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [
                {
                    "formatted_address": "Test Address, Test Municipality, Jalisco, Mexico",
                    "geometry": {
                        "location": {
                            "lat": 20.6596988,
                            "lng": -103.3496092
                        }
                    },
                    "place_id": "test_place_id"
                }
            ]
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/geocode",
            params={
                "address": "Calle Test 123",
                "municipality": "Guadalajara"
            }
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["formatted_address"] == "Test Address, Test Municipality, Jalisco, Mexico"
        assert result["geometry"]["location"]["lat"] == 20.6596988
        assert result["geometry"]["location"]["lng"] == -103.3496092

    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_geocode_address_no_results(self, mock_get):
        """Test geocoding when no results are found."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ZERO_RESULTS",
            "results": []
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/geocode",
            params={
                "address": "Nonexistent Address 999",
                "municipality": "Unknown Municipality"
            }
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "No results found"

    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_geocode_address_rate_limit_exceeded(self, mock_get):
        """Test handling of Google API rate limit exceeded."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OVER_QUERY_LIMIT",
            "results": []
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/geocode",
            params={
                "address": "Calle Test 123",
                "municipality": "Guadalajara"
            }
        )

        # Assert
        assert response.status_code == 429
        assert "API rate limit exceeded" in response.json()["detail"]

    def test_geocode_address_missing_parameters(self):
        """Test geocoding with missing required parameters."""
        # Test missing address
        response = self.client.get(
            "/v1/geocode",
            params={"municipality": "Guadalajara"}
        )
        assert response.status_code == 422

        # Test missing municipality
        response = self.client.get(
            "/v1/geocode",
            params={"address": "Calle Test 123"}
        )
        assert response.status_code == 422

        # Test both missing
        response = self.client.get("/v1/geocode")
        assert response.status_code == 422

    def test_geocode_address_too_short(self):
        """Test geocoding with address that's too short."""
        # Act
        response = self.client.get(
            "/v1/geocode",
            params={
                "address": "Test",  # Less than 6 characters
                "municipality": "Guadalajara"
            }
        )

        # Assert
        assert response.status_code == 422

    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_reverse_geocode_success(self, mock_get):
        """Test successful reverse geocoding."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [
                {
                    "formatted_address": "Test Address, Guadalajara, Jalisco, Mexico",
                    "geometry": {
                        "location": {
                            "lat": 20.6596988,
                            "lng": -103.3496092
                        }
                    },
                    "place_id": "test_place_id"
                }
            ]
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/reverse-geocode",
            params={
                "lat": 20.6596988,
                "lng": -103.3496092
            }
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["formatted_address"] == "Test Address, Guadalajara, Jalisco, Mexico"

    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_reverse_geocode_no_results(self, mock_get):
        """Test reverse geocoding when no results are found."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "ZERO_RESULTS",
            "results": []
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/reverse-geocode",
            params={
                "lat": 0.0,  # Invalid coordinates
                "lng": 0.0
            }
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "No results found"

    def test_reverse_geocode_missing_parameters(self):
        """Test reverse geocoding with missing required parameters."""
        # Test missing lat
        response = self.client.get(
            "/v1/reverse-geocode",
            params={"lng": -103.3496092}
        )
        assert response.status_code == 422

        # Test missing lng
        response = self.client.get(
            "/v1/reverse-geocode",
            params={"lat": 20.6596988}
        )
        assert response.status_code == 422

        # Test both missing
        response = self.client.get("/v1/reverse-geocode")
        assert response.status_code == 422

    @pytest.mark.parametrize("lat,lng", [
        (20.6596988, -103.3496092),  # Guadalajara coordinates
        (-90, -180),  # Extreme valid coordinates
        (90, 180),   # Extreme valid coordinates
        (0, 0),      # Null Island
    ])
    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_reverse_geocode_various_coordinates(self, mock_get, lat, lng):
        """Test reverse geocoding with various coordinate combinations."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [{"formatted_address": "Test Address"}]
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/reverse-geocode",
            params={"lat": lat, "lng": lng}
        )

        # Assert
        assert response.status_code == 200

    @pytest.mark.parametrize("lat,lng", [
        (91, 0),     # Invalid latitude > 90
        (-91, 0),    # Invalid latitude < -90
        (0, 181),    # Invalid longitude > 180
        (0, -181),   # Invalid longitude < -180
        ("invalid", 0),  # Non-numeric latitude
        (0, "invalid"),  # Non-numeric longitude
    ])
    def test_reverse_geocode_invalid_coordinates(self, lat, lng):
        """Test reverse geocoding with invalid coordinates."""
        # Act
        response = self.client.get(
            "/v1/reverse-geocode",
            params={"lat": lat, "lng": lng}
        )

        # Assert - FastAPI validation will return 422 Unprocessable Entity
        assert response.status_code == 422

    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_httpx_client_error(self, mock_get):
        """Test handling of HTTP client errors."""
        # Arrange
        mock_get.side_effect = httpx.RequestError("Connection failed")

        # Act
        response = self.client.get(
            "/v1/geocode",
            params={
                "address": "Calle Test 123",
                "municipality": "Guadalajara"
            }
        )

        # Assert
        assert response.status_code == 500
        assert "Connection error" in response.json()["detail"]

    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_google_api_error_status(self, mock_get):
        """Test handling of various Google API error statuses."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "REQUEST_DENIED",
            "error_message": "API key invalid"
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/geocode",
            params={
                "address": "Calle Test 123",
                "municipality": "Guadalajara"
            }
        )

        # Assert
        assert response.status_code == 404  # Falls through to "No results found"

    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_address_formatting(self, mock_get):
        """Test that address is properly formatted with Jalisco suffix."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [{"formatted_address": "Test"}]
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/geocode",
            params={
                "address": "Calle Principal 100",
                "municipality": "Zapopan"
            }
        )

        # Assert
        assert response.status_code == 200
        # Verify the call was made with proper address formatting
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "Calle Principal 100, Zapopan, Jalisco" in str(call_args)

    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    @patch('app.routers.geocode.logging.warning')
    def test_rate_limit_logging(self, mock_logging, mock_get):
        """Test that rate limit events are properly logged."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OVER_QUERY_LIMIT"
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/geocode",
            params={
                "address": "Calle Test 123",
                "municipality": "Guadalajara"
            }
        )

        # Assert
        assert response.status_code == 429
        mock_logging.assert_called_once()

    @pytest.mark.parametrize("address,municipality", [
        ("Avenida López Mateos 1234", "Guadalajara"),
        ("Calle Morelos 567", "Zapopan"),
        ("Boulevard Puerta de Hierro 890", "Zapopan"),
        ("Periférico Norte 123", "Tlaquepaque"),
    ])
    @patch('config.settings.settings.GOOGLE_API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient.get')
    def test_various_address_formats(self, mock_get, address, municipality):
        """Test geocoding with various address and municipality combinations."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "OK",
            "results": [{"formatted_address": f"{address}, {municipality}, Jalisco"}]
        }
        mock_get.return_value = mock_response

        # Act
        response = self.client.get(
            "/v1/geocode",
            params={
                "address": address,
                "municipality": municipality
            }
        )

        # Assert
        assert response.status_code == 200
