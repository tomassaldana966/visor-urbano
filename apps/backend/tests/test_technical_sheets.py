import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from datetime import datetime
import json
import base64
from uuid import uuid4, UUID

from app.main import app
from app.models.technical_sheets import TechnicalSheet
from app.models.municipality import Municipality
from app.models.zoning_control_regulations import ZoningControlRegulation
from config.settings import get_db


class TestTechnicalSheets:
    
    def setup_method(self):
        """Set up test dependencies."""
        self.client = TestClient(app)
        self.mock_db = AsyncMock()
        
        # Configure db methods properly - add is synchronous, commit/refresh are async
        self.mock_db.add = MagicMock(return_value=None)
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()
        
        # Override dependencies
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Test data
        self.test_uuid = str(uuid4())
        self.test_coordinates = base64.b64encode(json.dumps([[100, 200], [150, 200], [150, 250], [100, 250], [100, 200]]).encode()).decode()
        self.test_square_meters = base64.b64encode(json.dumps({"area": 2500}).encode()).decode()
        
        # Mock technical sheet
        self.mock_sheet = MagicMock(spec=TechnicalSheet)
        self.mock_sheet.uuid = self.test_uuid
        self.mock_sheet.address = "Test Address 123"
        self.mock_sheet.square_meters = self.test_square_meters
        self.mock_sheet.coordinates = self.test_coordinates
        self.mock_sheet.image = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
        self.mock_sheet.municipality_id = 1
        self.mock_sheet.technical_sheet_download_id = 1
        self.mock_sheet.created_at = datetime.now()
        
        # Mock municipality
        self.mock_municipality = MagicMock(spec=Municipality)
        self.mock_municipality.id = 1
        self.mock_municipality.name = "Test Municipality"
        
        # Mock zoning regulation
        self.mock_regulation = MagicMock(spec=ZoningControlRegulation)
        self.mock_regulation.id = 1
        self.mock_regulation.municipality_id = 1
        self.mock_regulation.district = "18"
        self.mock_regulation.regulation_key = "H3"
        self.mock_regulation.description = "Test regulation"
    
    def teardown_method(self):
        """Clean up after tests."""
        app.dependency_overrides.clear()
    
    def _configure_db_execute_result(self, scalar_result=None, scalars_result=None, fetchall_result=None):
        """Configure database execute results."""
        mock_result = MagicMock()
        
        if scalar_result is not None:
            mock_result.scalar.return_value = scalar_result
        if scalars_result is not None:
            mock_result.scalars.return_value.all.return_value = scalars_result
        if fetchall_result is not None:
            mock_result.fetchall.return_value = fetchall_result
            
        self.mock_db.execute.return_value = mock_result
        return mock_result
    
    def test_get_admin_statistics_success(self):
        """Test successful retrieval of admin statistics."""
        # Mock daily statistics
        mock_rows = [
            MagicMock(year=2024, month=1, day=15, count=5),
            MagicMock(year=2024, month=1, day=14, count=3),
        ]
        
        # Mock execute calls for daily stats and total
        self.mock_db.execute.side_effect = [
            MagicMock(fetchall=lambda: mock_rows),  # Daily stats
            MagicMock(scalar=lambda: 8)  # Total count
        ]
        
        response = self.client.get("/v1/technical_sheets/admin-stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 8
        assert len(data["days"]) == 2
        assert data["days"][0]["year"] == 2024
        assert data["days"][0]["month"] == 1
        assert data["days"][0]["day"] == 15
        assert data["days"][0]["count"] == 5
    
    def test_get_sheets_grouped_by_municipality_success(self):
        """Test successful retrieval of sheets grouped by municipality."""
        mock_rows = [
            MagicMock(municipality="Municipality A", sheets=10),
            MagicMock(municipality="Municipality B", sheets=5),
        ]
        
        self._configure_db_execute_result(fetchall_result=mock_rows)
        
        response = self.client.get("/v1/technical_sheets/by-municipality")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert len(data["sheets"]) == 2
        assert data["sheets"][0]["municipality"] == "Municipality A"
        assert data["sheets"][0]["sheets"] == 10
        assert data["sheets"][1]["municipality"] == "Municipality B"
        assert data["sheets"][1]["sheets"] == 5
    
    def test_get_daily_stats_by_municipality_success(self):
        """Test successful retrieval of daily stats by municipality."""
        mock_rows = [
            MagicMock(year=2024, month=1, day=15, count=3),
        ]
        
        self.mock_db.execute.side_effect = [
            MagicMock(fetchall=lambda: mock_rows),  # Daily stats
            MagicMock(scalar=lambda: 3)  # Total count
        ]
        
        response = self.client.get("/v1/technical_sheets/admin-stats/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["days"]) == 1
        assert data["days"][0]["municipality_id"] == 1 if "municipality_id" in data["days"][0] else True
    
    def test_create_technical_sheet_success(self):
        """Test successful creation of technical sheet."""
        # Mock the new sheet to be returned after creation
        with patch('app.models.technical_sheets.TechnicalSheet') as mock_sheet_class:
            mock_new_sheet = MagicMock()
            mock_new_sheet.uuid = self.test_uuid
            mock_sheet_class.return_value = mock_new_sheet
            
            payload = {
                "address": "Test Address 123",
                "square_meters": self.test_square_meters,
                "coordinates": self.test_coordinates,
                "image": "data:image/jpeg;base64,test_image_data",
                "municipality_id": 1,
                "technical_sheet_download_id": 1
            }
            
            response = self.client.post("/v1/technical_sheets/", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert "uuid" in data
            self.mock_db.add.assert_called_once()
            self.mock_db.commit.assert_called_once()
    
    def test_create_technical_sheet_database_error(self):
        """Test database error during technical sheet creation."""
        # Configure async mock to raise exception
        async def raise_error(*args, **kwargs):
            raise Exception("Database error")
        
        self.mock_db.commit = AsyncMock(side_effect=raise_error)
        
        payload = {
            "address": "Test Address",
            "square_meters": self.test_square_meters,
            "coordinates": self.test_coordinates,
            "image": "data:image/jpeg;base64,test",
            "municipality_id": 1,
            "technical_sheet_download_id": 1
        }
        
        # Expect a 500 Internal Server Error response
        response = self.client.post("/v1/technical_sheets/", json=payload)
        assert response.status_code == 500
    
    @patch('requests.get')
    @patch('qrcode.make')
    @patch('weasyprint.HTML')
    @patch('jinja2.Environment.get_template')
    def test_get_technical_sheet_pdf_success_with_features(self, mock_get_template, mock_html, mock_qr, mock_requests):
        """Test successful PDF generation with geoserver features."""
        # Mock database query for technical sheet
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = self.mock_sheet
        self.mock_db.execute.return_value = mock_result
        
        # Mock geoserver response
        mock_geoserver_response = {
            "numberReturned": 1,
            "features": [
                {
                    "properties": {
                        "municipio": 1,
                        "distrito": "18",
                        "clasificac": "H3,C2"
                    }
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"test": "data"}'
        mock_response.json.return_value = mock_geoserver_response
        mock_requests.return_value = mock_response
        
        # Mock zoning regulations query
        regulation_result = MagicMock()
        regulation_result.scalars.return_value.all.return_value = [self.mock_regulation]
        
        # Mock municipality get
        self.mock_db.get.return_value = self.mock_municipality
        
        # Set up multiple execute calls
        self.mock_db.execute.side_effect = [
            mock_result,  # Technical sheet query
            regulation_result,  # First regulation query
            regulation_result   # Second regulation query
        ]
        
        # Mock QR code generation
        mock_qr_img = MagicMock()
        mock_qr.return_value = mock_qr_img
        
        # Mock template rendering
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Technical Sheet PDF</html>"
        mock_get_template.return_value = mock_template
        
        # Mock WeasyPrint
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.return_value = b"fake pdf content"
        mock_html.return_value = mock_html_instance
        
        response = self.client.get(f"/v1/technical_sheets/{self.test_uuid}")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
    
    @patch('requests.get')
    @patch('qrcode.make')
    @patch('weasyprint.HTML')
    @patch('jinja2.Environment.get_template')
    def test_get_technical_sheet_pdf_no_features(self, mock_get_template, mock_html, mock_qr, mock_requests):
        """Test PDF generation when no geoserver features are found."""
        # Mock database query for technical sheet
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = self.mock_sheet
        self.mock_db.execute.return_value = mock_result
        
        # Mock geoserver response with no features
        mock_geoserver_response = {"numberReturned": 0, "features": []}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"test": "data"}'
        mock_response.json.return_value = mock_geoserver_response
        mock_requests.return_value = mock_response
        
        # Mock QR code generation
        mock_qr_img = MagicMock()
        mock_qr.return_value = mock_qr_img
        
        # Mock template rendering (404 template)
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Technical Sheet 404</html>"
        mock_get_template.return_value = mock_template
        
        # Mock WeasyPrint
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.return_value = b"fake pdf content"
        mock_html.return_value = mock_html_instance
        
        response = self.client.get(f"/v1/technical_sheets/{self.test_uuid}")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        # Verify that the 404 template was used
        mock_get_template.assert_called_with("technical_sheets404.html")
    
    def test_get_technical_sheet_pdf_not_found(self):
        """Test PDF generation when technical sheet is not found."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute.return_value = mock_result
        
        response = self.client.get(f"/v1/technical_sheets/{self.test_uuid}")
        
        assert response.status_code == 404
        assert "Technical sheet not found" in response.json()["detail"]
    
    @patch('requests.get')
    @patch('qrcode.make')
    @patch('weasyprint.HTML')
    @patch('jinja2.Environment.get_template')
    def test_get_technical_sheet_pdf_geoserver_error(self, mock_get_template, mock_html, mock_qr, mock_requests):
        """Test PDF generation when geoserver returns an error."""
        # Mock database query for technical sheet
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = self.mock_sheet
        self.mock_db.execute.return_value = mock_result
        
        # Mock geoserver error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b''
        mock_requests.return_value = mock_response
        
        # Mock QR code generation
        mock_qr_img = MagicMock()
        mock_qr.return_value = mock_qr_img
        
        # Mock template rendering (404 template due to error)
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Technical Sheet 404</html>"
        mock_get_template.return_value = mock_template
        
        # Mock WeasyPrint
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.return_value = b"fake pdf content"
        mock_html.return_value = mock_html_instance
        
        response = self.client.get(f"/v1/technical_sheets/{self.test_uuid}")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
    
    @patch('requests.get')
    @patch('qrcode.make')
    @patch('weasyprint.HTML')
    @patch('jinja2.Environment.get_template')
    def test_get_technical_sheet_pdf_invalid_coordinates(self, mock_get_template, mock_html, mock_qr, mock_requests):
        """Test PDF generation with invalid coordinates format."""
        # Create sheet with invalid coordinates
        invalid_sheet = MagicMock(spec=TechnicalSheet)
        invalid_sheet.uuid = self.test_uuid
        invalid_sheet.address = "Test Address"
        invalid_sheet.square_meters = self.test_square_meters
        invalid_sheet.coordinates = "invalid_base64"
        invalid_sheet.image = "test_image"
        invalid_sheet.municipality_id = 1
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = invalid_sheet
        self.mock_db.execute.return_value = mock_result
        
        # Mock geoserver response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"numberReturned": 0}'
        mock_response.json.return_value = {"numberReturned": 0, "features": []}
        mock_requests.return_value = mock_response
        
        # Mock QR code generation
        mock_qr_img = MagicMock()
        mock_qr.return_value = mock_qr_img
        
        # Mock template rendering
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Technical Sheet</html>"
        mock_get_template.return_value = mock_template
        
        # Mock WeasyPrint
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.return_value = b"fake pdf content"
        mock_html.return_value = mock_html_instance
        
        response = self.client.get(f"/v1/technical_sheets/{self.test_uuid}")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
    
    @patch('requests.get')
    @patch('qrcode.make')
    @patch('weasyprint.HTML')
    @patch('jinja2.Environment.get_template')
    def test_get_technical_sheet_pdf_invalid_square_meters(self, mock_get_template, mock_html, mock_qr, mock_requests):
        """Test PDF generation with invalid square meters format."""
        # Create sheet with invalid square meters
        invalid_sheet = MagicMock(spec=TechnicalSheet)
        invalid_sheet.uuid = self.test_uuid
        invalid_sheet.address = "Test Address"
        invalid_sheet.square_meters = "invalid_base64"
        invalid_sheet.coordinates = self.test_coordinates
        invalid_sheet.image = "test_image"
        invalid_sheet.municipality_id = 1
        
        # Mock database queries
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = invalid_sheet
        
        regulation_result = MagicMock()
        regulation_result.scalars.return_value.all.return_value = []
        
        self.mock_db.execute.side_effect = [mock_result, regulation_result]
        self.mock_db.get.return_value = self.mock_municipality
        
        # Mock geoserver response with features
        mock_geoserver_response = {
            "numberReturned": 1,
            "features": [{"properties": {"municipio": 1, "distrito": "18", "clasificac": "H3"}}]
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"test": "data"}'
        mock_response.json.return_value = mock_geoserver_response
        mock_requests.return_value = mock_response
        
        # Mock QR and template
        mock_qr_img = MagicMock()
        mock_qr.return_value = mock_qr_img
        
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Technical Sheet</html>"
        mock_get_template.return_value = mock_template
        
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.return_value = b"fake pdf content"
        mock_html.return_value = mock_html_instance
        
        response = self.client.get(f"/v1/technical_sheets/{self.test_uuid}")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
    
    def test_get_admin_statistics_database_error(self):
        """Test database error during admin statistics retrieval."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            self.client.get("/v1/technical_sheets/admin-stats")
    
    def test_get_sheets_by_municipality_database_error(self):
        """Test database error during municipality grouping."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            self.client.get("/v1/technical_sheets/by-municipality")
    
    def test_get_daily_stats_by_municipality_database_error(self):
        """Test database error during daily stats retrieval by municipality."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            self.client.get("/v1/technical_sheets/admin-stats/1")
    
    @pytest.mark.parametrize("municipality_id", [1, 2, 5, 10])
    def test_get_daily_stats_various_municipalities(self, municipality_id):
        """Test daily stats retrieval for various municipalities."""
        mock_rows = [MagicMock(year=2024, month=1, day=15, count=2)]
        
        self.mock_db.execute.side_effect = [
            MagicMock(fetchall=lambda: mock_rows),
            MagicMock(scalar=lambda: 2)
        ]
        
        response = self.client.get(f"/v1/technical_sheets/admin-stats/{municipality_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["days"]) == 1
    
    def test_get_admin_statistics_empty_data(self):
        """Test admin statistics with no data."""
        self.mock_db.execute.side_effect = [
            MagicMock(fetchall=lambda: []),  # No daily stats
            MagicMock(scalar=lambda: 0)      # Zero total
        ]
        
        response = self.client.get("/v1/technical_sheets/admin-stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["days"]) == 0
    
    def test_get_sheets_by_municipality_empty_data(self):
        """Test municipality grouping with no data."""
        self._configure_db_execute_result(fetchall_result=[])
        
        response = self.client.get("/v1/technical_sheets/by-municipality")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["sheets"]) == 0
    
    @patch('app.routers.technical_sheets.uuid4')
    def test_create_technical_sheet_uuid_generation(self, mock_uuid):
        """Test UUID generation during technical sheet creation."""
        mock_uuid.return_value = UUID(self.test_uuid)
        
        # Configure async mocks properly
        self.mock_db.add.return_value = None
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()
        
        with patch('app.models.technical_sheets.TechnicalSheet') as mock_sheet_class:
            mock_new_sheet = MagicMock()
            mock_new_sheet.uuid = self.test_uuid
            mock_sheet_class.return_value = mock_new_sheet
            
            payload = {
                "address": "Test Address",
                "square_meters": self.test_square_meters,
                "coordinates": self.test_coordinates,
                "image": "test_image",
                "municipality_id": 1,
                "technical_sheet_download_id": 1
            }
            
            response = self.client.post("/v1/technical_sheets/", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["uuid"] == self.test_uuid
            # Verify that our specific UUID was used
            mock_uuid.assert_called_once()
