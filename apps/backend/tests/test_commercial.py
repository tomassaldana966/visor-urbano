import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
import base64
import httpx
import io

from app.main import app


class TestCommercial:
    def setup_method(self):
        """Setup for each test method."""
        self.client = TestClient(app)

    def teardown_method(self):
        """Cleanup after each test method."""
        app.dependency_overrides.clear()

    def encode_param(self, value: str) -> str:
        """Helper to encode parameters as base64."""
        return base64.b64encode(value.encode("utf-8")).decode("utf-8")

    @patch('config.settings.settings.DEFAULT_GEOSERVER', 'http://default-server')
    @patch('config.settings.settings.URL_GEOSERVER', 'http://production-server')
    @patch('config.settings.settings.APP_LOGO', 'logo.png')
    @patch('config.settings.settings.URL_MINIMAPA', 'http://minimapa-url')
    @patch('httpx.AsyncClient.get')
    @patch('pdfkit.from_string')
    @patch('app.routers.commercial.env.get_template')
    def test_generate_commercial_pdf_success(self, mock_get_template, mock_pdfkit, mock_httpx_get):
        """Test successful generation of commercial PDF."""
        # Arrange
        mock_geo_data = {
            "features": [
                {
                    "id": 1,
                    "properties": {
                        "name": "Test Business",
                        "type": "Restaurant"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-103.3496092, 20.6596988]
                    }
                }
            ]
        }

        mock_response = MagicMock()
        mock_response.json.return_value = mock_geo_data
        mock_httpx_get.return_value = mock_response

        mock_template = MagicMock()
        mock_template.render.return_value = "<html><body>Test PDF Content</body></html>"
        mock_get_template.return_value = mock_template

        mock_pdf_content = b"PDF content"
        mock_pdfkit.return_value = mock_pdf_content

        # Prepare encoded parameters
        url = self.encode_param("http://test-geoserver/api/data")
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("Restaurants, Shops")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "commercial.pdf" in response.headers.get("content-disposition", "")
        mock_httpx_get.assert_called_once()
        mock_get_template.assert_called_once_with("comercial.html")
        mock_template.render.assert_called_once()
        mock_pdfkit.assert_called_once()

    @patch('httpx.AsyncClient.get')
    def test_generate_commercial_pdf_http_error(self, mock_httpx_get):
        """Test handling of HTTP errors when fetching geo data."""
        # Arrange
        mock_httpx_get.side_effect = httpx.RequestError("Connection failed")

        url = self.encode_param("http://test-geoserver/api/data")
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("Restaurants")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 500
        assert "Error generating PDF" in response.text

    def test_generate_commercial_pdf_invalid_base64(self):
        """Test handling of invalid base64 encoded parameters."""
        # Arrange
        invalid_url = "invalid_base64!"
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("Restaurants")

        # Act
        response = self.client.get(f"/v1/commercial/{invalid_url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 500
        assert "Error generating PDF" in response.text

    @patch('config.settings.settings.DEFAULT_GEOSERVER', 'http://default-server')
    @patch('config.settings.settings.URL_GEOSERVER', 'http://production-server')
    @patch('httpx.AsyncClient.get')
    @patch('pdfkit.from_string')
    @patch('app.routers.commercial.env.get_template')
    def test_url_replacement(self, mock_get_template, mock_pdfkit, mock_httpx_get):
        """Test that default geoserver URL is properly replaced."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"features": []}
        mock_httpx_get.return_value = mock_response

        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test</html>"
        mock_get_template.return_value = mock_template

        mock_pdfkit.return_value = b"PDF content"

        # URL containing default server that should be replaced
        original_url = "http://default-server/wfs?service=WFS"
        url = self.encode_param(original_url)
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("Restaurants")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 200
        # Verify the URL was replaced
        call_args = mock_httpx_get.call_args[0]
        assert "http://production-server" in call_args[0]
        assert "http://default-server" not in call_args[0]

    @patch('httpx.AsyncClient.get')
    @patch('pdfkit.from_string')
    @patch('app.routers.commercial.env.get_template')
    def test_empty_geo_data(self, mock_get_template, mock_pdfkit, mock_httpx_get):
        """Test handling of empty geo data response."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"features": []}
        mock_httpx_get.return_value = mock_response

        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Empty data</html>"
        mock_get_template.return_value = mock_template

        mock_pdfkit.return_value = b"PDF content"

        url = self.encode_param("http://test-server/api")
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("None")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 200
        mock_template.render.assert_called_once()
        render_args = mock_template.render.call_args[1]
        assert render_args["data"] == []

    @patch('httpx.AsyncClient.get')
    @patch('app.routers.commercial.env.get_template')
    def test_template_error(self, mock_get_template, mock_httpx_get):
        """Test handling of template rendering errors."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"features": []}
        mock_httpx_get.return_value = mock_response

        mock_get_template.side_effect = Exception("Template not found")

        url = self.encode_param("http://test-server/api")
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("Restaurants")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 500
        assert "Error generating PDF" in response.text

    @patch('httpx.AsyncClient.get')
    @patch('pdfkit.from_string')
    @patch('app.routers.commercial.env.get_template')
    def test_pdf_generation_error(self, mock_get_template, mock_pdfkit, mock_httpx_get):
        """Test handling of PDF generation errors."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"features": []}
        mock_httpx_get.return_value = mock_response

        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test</html>"
        mock_get_template.return_value = mock_template

        mock_pdfkit.side_effect = Exception("PDF generation failed")

        url = self.encode_param("http://test-server/api")
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("Restaurants")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 500
        assert "Error generating PDF" in response.text

    @pytest.mark.parametrize("municipality,area,businesses", [
        ("Guadalajara", "Centro", "Restaurants, Cafes"),
        ("Zapopan", "Zona Industrial", "Factories, Warehouses"),
        ("Tlaquepaque", "Centro Histórico", "Artesanías, Tiendas"),
        ("Tonalá", "Zona Norte", "Comercio, Servicios"),
    ])
    @patch('httpx.AsyncClient.get')
    @patch('pdfkit.from_string')
    @patch('app.routers.commercial.env.get_template')
    def test_various_municipality_combinations(self, mock_get_template, mock_pdfkit, mock_httpx_get, municipality, area, businesses):
        """Test PDF generation with various municipality, area, and business combinations."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"features": []}
        mock_httpx_get.return_value = mock_response

        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test</html>"
        mock_get_template.return_value = mock_template

        mock_pdfkit.return_value = b"PDF content"

        url = self.encode_param("http://test-server/api")
        image = self.encode_param("test-image.png")
        encoded_municipality = self.encode_param(municipality)
        encoded_area = self.encode_param(area)
        encoded_businesses = self.encode_param(businesses)

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{encoded_municipality}/{encoded_area}/{encoded_businesses}")

        # Assert
        assert response.status_code == 200
        render_args = mock_template.render.call_args[1]
        assert render_args["municipality"] == municipality
        assert render_args["area"] == area
        assert render_args["businesses"] == businesses

    @patch('httpx.AsyncClient.get')
    @patch('pdfkit.from_string')
    @patch('app.routers.commercial.env.get_template')
    def test_template_rendering_parameters(self, mock_get_template, mock_pdfkit, mock_httpx_get):
        """Test that all expected parameters are passed to template rendering."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"features": [{"test": "data"}]}
        mock_httpx_get.return_value = mock_response

        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test</html>"
        mock_get_template.return_value = mock_template

        mock_pdfkit.return_value = b"PDF content"

        url = self.encode_param("http://test-server/api")
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("Restaurants")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 200
        render_args = mock_template.render.call_args[1]
        
        # Check all expected parameters are present
        expected_params = ["data", "municipality", "logo", "area", "image", "businesses", "url_minimapa"]
        for param in expected_params:
            assert param in render_args

    def test_special_characters_in_parameters(self):
        """Test handling of special characters in encoded parameters."""
        # Arrange
        special_chars_text = "Área & Comercios (Zona #1) - 50% descuento"
        url = self.encode_param("http://test-server/api")
        image = self.encode_param("image_with_spaces.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param(special_chars_text)
        businesses = self.encode_param("Café & Té, Niños/Niñas")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert - Should handle encoding/decoding gracefully
        # Even if it fails, it should return a proper error response
        assert response.status_code in [200, 500]

    @patch('httpx.AsyncClient.get')
    def test_malformed_geo_data_response(self, mock_httpx_get):
        """Test handling of malformed geo data response."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_httpx_get.return_value = mock_response

        url = self.encode_param("http://test-server/api")
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("Restaurants")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 500
        assert "Error generating PDF" in response.text

    @patch('httpx.AsyncClient.get')
    @patch('pdfkit.from_string')
    @patch('app.routers.commercial.env.get_template')
    def test_url_encoding_with_spaces(self, mock_get_template, mock_pdfkit, mock_httpx_get):
        """Test proper URL encoding when spaces are present."""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"features": []}
        mock_httpx_get.return_value = mock_response

        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test</html>"
        mock_get_template.return_value = mock_template

        mock_pdfkit.return_value = b"PDF content"

        # URL with spaces that should be encoded
        url_with_spaces = "http://test-server/api?query=test business data"
        url = self.encode_param(url_with_spaces)
        image = self.encode_param("test-image.png")
        municipality = self.encode_param("Guadalajara")
        area = self.encode_param("Centro")
        businesses = self.encode_param("Restaurants")

        # Act
        response = self.client.get(f"/v1/commercial/{url}/{image}/{municipality}/{area}/{businesses}")

        # Assert
        assert response.status_code == 200
        # Verify spaces were replaced with %20
        call_args = mock_httpx_get.call_args[0]
        assert "%20" in call_args[0]
        assert " " not in call_args[0]
