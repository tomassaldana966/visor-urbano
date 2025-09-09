import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import base64
import json

from app.main import app
from app.models.provisional_openings import ProvisionalOpening
from app.models.municipality import Municipality
from app.models.user import UserModel
from app.models.procedures import Procedure
from config.settings import get_db, get_sync_db


class TestProvisionalOpenings:
    
    def setup_method(self):
        """Set up test dependencies."""
        self.client = TestClient(app)
        self.mock_db = AsyncMock()
        self.mock_sync_db = MagicMock()
        
        # Configure AsyncMock database operations
        self.mock_db.add = MagicMock()  # Use MagicMock for sync-style operations
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()
        self.mock_db.rollback = AsyncMock()
        
        # Override dependencies
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[get_sync_db] = lambda: self.mock_sync_db
        
        # Test data
        self.test_folio = "TEST-FOLIO-2024"
        self.encoded_folio = base64.b64encode(self.test_folio.encode()).decode()
        
        # Create proper datetime objects for comparison
        now = datetime.now()
        start_date = now
        end_date = now + timedelta(days=30)
        created_at = now
        updated_at = now
        
        # Mock provisional opening
        self.mock_opening = MagicMock(spec=ProvisionalOpening)
        self.mock_opening.id = 1
        self.mock_opening.folio = self.test_folio
        self.mock_opening.procedure_id = 1
        self.mock_opening.counter = 1
        self.mock_opening.granted_by_user_id = 1
        self.mock_opening.granted_role = 1  # Use integer role ID (1=admin)
        self.mock_opening.start_date = start_date
        self.mock_opening.end_date = end_date
        self.mock_opening.status = 1
        self.mock_opening.municipality_id = 1
        self.mock_opening.created_at = created_at
        self.mock_opening.updated_at = updated_at
        
        # Mock municipality
        self.mock_municipality = MagicMock(spec=Municipality)
        self.mock_municipality.id = 1
        self.mock_municipality.name = "Test Municipality"
        self.mock_opening.municipality = self.mock_municipality
        
        # Mock user
        self.mock_user = MagicMock(spec=UserModel)
        self.mock_user.id = 1
        self.mock_user.name = "Test"
        self.mock_user.paternal_last_name = "User"
        self.mock_opening.granted_by_user = self.mock_user
        
        # Mock procedure
        self.mock_procedure = MagicMock(spec=Procedure)
        self.mock_procedure.id = 1
        self.mock_procedure.folio = "PROC-001"
        self.mock_opening.procedure = self.mock_procedure
    
    def teardown_method(self):
        """Clean up after tests."""
        app.dependency_overrides.clear()
    
    def _configure_db_query_result(self, result_data=None, scalar_result=None, count_result=None):
        """Configure database query results."""
        mock_result = MagicMock()
        
        # Configure scalars() method to return a mock with proper all() and first() methods
        mock_scalars = MagicMock()
        if result_data is not None:
            mock_scalars.all.return_value = result_data
        if scalar_result is not None:
            mock_scalars.first.return_value = scalar_result
        else:
            # Ensure first() returns None when scalar_result is None
            mock_scalars.first.return_value = None
        
        mock_result.scalars.return_value = mock_scalars
        
        if count_result is not None:
            mock_result.scalar.return_value = count_result
            
        self.mock_db.execute.return_value = mock_result
        return mock_result
    
    def test_list_provisional_openings_success(self):
        """Test successful listing of provisional openings."""
        # Configure database mocks
        openings = [self.mock_opening]
        
        # Mock count query result
        count_mock = MagicMock()
        count_mock.scalar.return_value = 1
        
        # Mock openings query result
        openings_mock = MagicMock()
        openings_mock.scalars.return_value.all.return_value = openings
        
        self.mock_db.execute.side_effect = [count_mock, openings_mock]
        
        response = self.client.get(
            "/v1/provisional_openings/?municipality_id=1&page=1&size=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["folio"] == self.test_folio
        assert data["page"] == 1
        assert data["size"] == 10
    
    def test_list_provisional_openings_with_filters(self):
        """Test listing provisional openings with status and search filters."""
        count_mock = MagicMock()
        count_mock.scalar.return_value = 0
        
        openings_mock = MagicMock()
        openings_mock.scalars.return_value.all.return_value = []
        
        self.mock_db.execute.side_effect = [count_mock, openings_mock]
        
        response = self.client.get(
            "/v1/provisional_openings/?municipality_id=1&status=1&search=TEST&page=1&size=10"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["items"]) == 0
    
    def test_list_provisional_openings_missing_municipality_id(self):
        """Test listing provisional openings without municipality_id."""
        response = self.client.get("/v1/provisional_openings/?page=1&size=10")
        
        assert response.status_code == 422  # Validation error
    
    def test_list_provisional_openings_database_error(self):
        """Test database error during listing."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        response = self.client.get(
            "/v1/provisional_openings/?municipality_id=1&page=1&size=10"
        )
        
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]
    
    def test_get_provisional_opening_by_folio_success(self):
        """Test successful retrieval of provisional opening by folio."""
        self._configure_db_query_result(scalar_result=self.mock_opening)
        
        response = self.client.get(f"/v1/provisional_openings/by_folio/{self.encoded_folio}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["folio"] == self.test_folio
        assert data["municipality_name"] == "Test Municipality"
        assert data["granted_by_user_name"] == "Test User"
    
    def test_get_provisional_opening_by_folio_invalid_encoding(self):
        """Test retrieval with invalid base64 encoding."""
        invalid_folio = "invalid-base64!"
        
        response = self.client.get(f"/v1/provisional_openings/by_folio/{invalid_folio}")
        
        assert response.status_code == 400
        assert "Invalid encoded folio" in response.json()["detail"]
    
    def test_get_provisional_opening_by_folio_not_found(self):
        """Test retrieval when provisional opening is not found."""
        self._configure_db_query_result(scalar_result=None)
        
        response = self.client.get(f"/v1/provisional_openings/by_folio/{self.encoded_folio}")
        
        assert response.status_code == 404
        assert "Provisional opening not found" in response.json()["detail"]
    
    def test_get_provisional_opening_by_folio_database_error(self):
        """Test database error during retrieval by folio."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        response = self.client.get(f"/v1/provisional_openings/by_folio/{self.encoded_folio}")
        
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]
    
    @patch('qrcode.QRCode')
    @patch('jinja2.Environment')
    @patch('weasyprint.HTML')
    @patch('builtins.open')
    @patch('os.path.exists')
    @patch('subprocess.run')
    def test_generate_pdf_success(self, mock_subprocess, mock_exists, mock_open, 
                                 mock_html, mock_jinja_env, mock_qr):
        """Test successful PDF generation."""
        # Mock QR code generation
        mock_qr_instance = MagicMock()
        mock_qr.return_value = mock_qr_instance
        mock_qr_img = MagicMock()
        mock_qr_instance.make_image.return_value = mock_qr_img
        
        # Mock Jinja2 template
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test Content</html>"
        mock_env = MagicMock()
        mock_env.get_template.return_value = mock_template
        mock_jinja_env.return_value = mock_env
        
        # Mock WeasyPrint
        mock_html_doc = MagicMock()
        mock_html.return_value = mock_html_doc
        
        # Mock file operations
        mock_file = MagicMock()
        mock_file.read.return_value = b"fake pdf content"
        mock_open.return_value.__enter__.return_value = mock_file
        mock_exists.return_value = True
        
        # Configure sync database
        sync_result = MagicMock()
        sync_result.scalars.return_value.first.return_value = self.mock_opening
        self.mock_sync_db.execute.return_value = sync_result
        
        response = self.client.get(f"/v1/provisional_openings/pdf/{self.encoded_folio}")
        
        assert response.status_code == 200
        data = response.json()
        assert "pdf_content" in data
        assert data["filename"] == f"provisional_opening_{self.test_folio.replace('/', '_')}.pdf"
        assert "qr_code" in data
    
    def test_generate_pdf_invalid_folio(self):
        """Test PDF generation with invalid folio encoding."""
        invalid_folio = "invalid-base64!"
        
        response = self.client.get(f"/v1/provisional_openings/pdf/{invalid_folio}")
        
        assert response.status_code == 400
        assert "Invalid encoded folio" in response.json()["detail"]
    
    def test_generate_pdf_not_found(self):
        """Test PDF generation when provisional opening is not found."""
        sync_result = MagicMock()
        sync_result.scalars.return_value.first.return_value = None
        self.mock_sync_db.execute.return_value = sync_result
        
        response = self.client.get(f"/v1/provisional_openings/pdf/{self.encoded_folio}")
        
        assert response.status_code == 404
        assert "Provisional opening not found" in response.json()["detail"]
    
    @patch('qrcode.QRCode')
    def test_generate_pdf_error(self, mock_qr):
        """Test PDF generation error handling."""
        mock_qr.side_effect = Exception("QR generation error")
        
        sync_result = MagicMock()
        sync_result.scalars.return_value.first.return_value = self.mock_opening
        self.mock_sync_db.execute.return_value = sync_result
        
        response = self.client.get(f"/v1/provisional_openings/pdf/{self.encoded_folio}")
        
        assert response.status_code == 500
        assert "Error generating PDF" in response.json()["detail"]
    
    def test_create_provisional_opening_success(self):
        """Test successful creation of provisional opening."""
        # Mock existing check (no existing opening)
        existing_result = MagicMock()
        existing_result.scalars.return_value.first.return_value = None
        
        # Mock municipality validation
        municipality_result = MagicMock()
        municipality_result.scalars.return_value.first.return_value = self.mock_municipality
        
        # Mock user validation
        user_result = MagicMock()
        user_result.scalars.return_value.first.return_value = self.mock_user
        
        # Mock final query with relations
        final_result = MagicMock()
        final_result.scalars.return_value.first.return_value = self.mock_opening
        
        self.mock_db.execute.side_effect = [
            existing_result, municipality_result, user_result, final_result
        ]
        
        payload = {
            "folio": self.test_folio,
            "procedure_id": 1,
            "counter": 1,
            "granted_by_user_id": 1,
            "granted_role": 1,  # Use integer role ID (1=admin)
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-01-31T23:59:59",
            "status": 1,
            "municipality_id": 1,
            "created_by": 1
        }
        
        response = self.client.post("/v1/provisional_openings/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["folio"] == self.test_folio
        assert data["municipality_name"] == "Test Municipality"
    
    def test_create_provisional_opening_existing_active(self):
        """Test creation when active provisional opening already exists."""
        # Mock existing active opening
        existing_result = MagicMock()
        existing_result.scalars.return_value.first.return_value = self.mock_opening
        
        self.mock_db.execute.return_value = existing_result
        
        payload = {
            "folio": self.test_folio,
            "procedure_id": 1,
            "counter": 1,
            "granted_by_user_id": 1,
            "granted_role": 1,  # Use integer role ID (1=admin)
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-01-31T23:59:59",
            "status": 1,
            "municipality_id": 1,
            "created_by": 1
        }
        
        response = self.client.post("/v1/provisional_openings/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["folio"] == self.test_folio
    
    def test_create_provisional_opening_municipality_not_found(self):
        """Test creation with invalid municipality."""
        # Mock existing check (no existing opening)
        existing_result = MagicMock()
        existing_result.scalars.return_value.first.return_value = None
        
        # Mock municipality not found
        municipality_result = MagicMock()
        municipality_result.scalars.return_value.first.return_value = None
        
        self.mock_db.execute.side_effect = [existing_result, municipality_result]
        
        payload = {
            "folio": self.test_folio,
            "procedure_id": 1,
            "counter": 1,
            "granted_by_user_id": 1,
            "granted_role": 1,  # Use integer role ID (1=admin)
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-01-31T23:59:59",
            "status": 1,
            "municipality_id": 999,
            "created_by": 1
        }
        
        response = self.client.post("/v1/provisional_openings/", json=payload)
        
        assert response.status_code == 400
        assert "Municipality not found" in response.json()["detail"]
    
    def test_create_provisional_opening_user_not_found(self):
        """Test creation with invalid granting user."""
        # Mock existing check
        existing_result = MagicMock()
        existing_result.scalars.return_value.first.return_value = None
        
        # Mock municipality found
        municipality_result = MagicMock()
        municipality_result.scalars.return_value.first.return_value = self.mock_municipality
        
        # Mock user not found
        user_result = MagicMock()
        user_result.scalars.return_value.first.return_value = None
        
        self.mock_db.execute.side_effect = [existing_result, municipality_result, user_result]
        
        payload = {
            "folio": self.test_folio,
            "procedure_id": 1,
            "counter": 1,
            "granted_by_user_id": 999,
            "granted_role": 1,  # Use integer role ID (1=admin)
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-01-31T23:59:59",
            "status": 1,
            "municipality_id": 1,
            "created_by": 1
        }
        
        response = self.client.post("/v1/provisional_openings/", json=payload)
        
        assert response.status_code == 400
        assert "Granting user not found" in response.json()["detail"]
    
    def test_create_provisional_opening_database_error(self):
        """Test database error during creation."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        payload = {
            "folio": self.test_folio,
            "procedure_id": 1,
            "counter": 1,
            "granted_by_user_id": 1,
            "granted_role": 1,
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-01-31T23:59:59",
            "status": 1,
            "municipality_id": 1,
            "created_by": 1
        }
        
        response = self.client.post("/v1/provisional_openings/", json=payload)
        
        assert response.status_code == 500
        assert "Error creating provisional opening" in response.json()["detail"]
    
    def test_update_provisional_opening_success(self):
        """Test successful update of provisional opening."""
        # Mock finding existing opening
        opening_result = MagicMock()
        opening_result.scalars.return_value.first.return_value = self.mock_opening
        
        # Mock final query with relations
        final_result = MagicMock()
        final_result.scalars.return_value.first.return_value = self.mock_opening
        
        self.mock_db.execute.side_effect = [opening_result, final_result]
        
        payload = {
            "status": 0,
            "granted_role": 3  # Use integer role ID (3=supervisor)
        }
        
        response = self.client.patch(f"/v1/provisional_openings/{self.mock_opening.id}", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["folio"] == self.test_folio
    
    def test_update_provisional_opening_not_found(self):
        """Test update when provisional opening is not found."""
        opening_result = MagicMock()
        opening_result.scalars.return_value.first.return_value = None
        self.mock_db.execute.return_value = opening_result
        
        payload = {"status": 0}
        
        response = self.client.patch("/v1/provisional_openings/999", json=payload)
        
        assert response.status_code == 404
        assert "Provisional opening not found" in response.json()["detail"]
    
    def test_update_provisional_opening_database_error(self):
        """Test database error during update."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        payload = {"status": 0}
        
        response = self.client.patch(f"/v1/provisional_openings/{self.mock_opening.id}", json=payload)
        
        assert response.status_code == 500
        assert "Error updating provisional opening" in response.json()["detail"]
    
    def test_delete_provisional_opening_success(self):
        """Test successful soft deletion of provisional opening."""
        opening_result = MagicMock()
        opening_result.scalars.return_value.first.return_value = self.mock_opening
        self.mock_db.execute.return_value = opening_result
        
        response = self.client.delete(f"/v1/provisional_openings/{self.mock_opening.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["detail"] == "Provisional opening marked as inactive"
        assert data["id"] == self.mock_opening.id
    
    def test_delete_provisional_opening_not_found(self):
        """Test deletion when provisional opening is not found."""
        opening_result = MagicMock()
        opening_result.scalars.return_value.first.return_value = None
        self.mock_db.execute.return_value = opening_result
        
        response = self.client.delete("/v1/provisional_openings/999")
        
        assert response.status_code == 404
        assert "Provisional opening not found" in response.json()["detail"]
    
    def test_delete_provisional_opening_database_error(self):
        """Test database error during deletion."""
        self.mock_db.execute.side_effect = Exception("Database error")
        
        response = self.client.delete(f"/v1/provisional_openings/{self.mock_opening.id}")
        
        assert response.status_code == 500
        assert "Error deleting provisional opening" in response.json()["detail"]
    
    @pytest.mark.parametrize("municipality_id,status,search,page,size", [
        (1, None, None, 1, 10),
        (1, 1, "TEST", 1, 10),
        (1, 0, None, 2, 20),
        (2, 1, "FOLIO", 1, 5)
    ])
    def test_list_provisional_openings_various_parameters(self, municipality_id, status, search, page, size):
        """Test listing with various parameter combinations."""
        count_mock = MagicMock()
        count_mock.scalar.return_value = 0
        
        openings_mock = MagicMock()
        openings_mock.scalars.return_value.all.return_value = []
        
        self.mock_db.execute.side_effect = [count_mock, openings_mock]
        
        params = {
            "municipality_id": municipality_id,
            "page": page,
            "size": size
        }
        if status is not None:
            params["status"] = status
        if search:
            params["search"] = search
        
        response = self.client.get("/v1/provisional_openings/", params=params)
        
        assert response.status_code == 200
    
    def test_days_remaining_calculation(self):
        """Test days remaining calculation in enriched data."""
        # Set end date to 5 days from now
        self.mock_opening.end_date = datetime.now() + timedelta(days=5)
        
        self._configure_db_query_result(scalar_result=self.mock_opening)
        
        response = self.client.get(f"/v1/provisional_openings/by_folio/{self.encoded_folio}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["days_remaining"] >= 4  # Should be around 5 days, allowing for test execution time
        assert data["is_expired"] is False
    
    def test_expired_provisional_opening(self):
        """Test expired provisional opening detection."""
        # Set end date to past
        self.mock_opening.end_date = datetime.now() - timedelta(days=1)
        
        self._configure_db_query_result(scalar_result=self.mock_opening)
        
        response = self.client.get(f"/v1/provisional_openings/by_folio/{self.encoded_folio}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["days_remaining"] == 0
        assert data["is_expired"] is True
