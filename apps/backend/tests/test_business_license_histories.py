import pytest
from unittest.mock import MagicMock, patch, mock_open
from fastapi.testclient import TestClient
from datetime import datetime
import io
import pandas as pd

from app.main import app
from app.models.business_license_histories import BusinessLicenseHistory
from config.settings import get_sync_db


class TestBusinessLicenseHistories:
    
    def setup_method(self):
        """Set up test dependencies."""
        self.client = TestClient(app)
        self.mock_db = MagicMock()
        
        # Override dependencies
        app.dependency_overrides[get_sync_db] = lambda: self.mock_db
        
        # Mock business license history with all required fields properly set
        self.mock_history = MagicMock(spec=BusinessLicenseHistory)
        self.mock_history.id = 1
        self.mock_history.license_folio = "LIC-2024-001"
        self.mock_history.issue_date = "2024-01-01"  # String format as expected by schema
        self.mock_history.business_line = "Retail"
        self.mock_history.detailed_description = "Test description"
        self.mock_history.business_line_code = "R001"
        self.mock_history.business_area = "Commercial"
        self.mock_history.street = "Main Street"
        self.mock_history.exterior_number = "123"
        self.mock_history.interior_number = "A"
        self.mock_history.neighborhood = "Downtown"
        self.mock_history.cadastral_key = "CAD001"
        self.mock_history.reference = "Near park"
        self.mock_history.coordinate_x = "20.123456"
        self.mock_history.coordinate_y = "-103.654321"
        self.mock_history.business_name = "Test Business"
        self.mock_history.owner_first_name = "John"
        self.mock_history.owner_last_name_p = "Doe"
        self.mock_history.owner_last_name_m = "Smith"
        self.mock_history.user_tax_id = "TAX123456"
        self.mock_history.national_id = "NAT789012"
        self.mock_history.owner_phone = "555-1234"
        self.mock_history.owner_email = "john@example.com"
        self.mock_history.owner_street = "Oak Street"
        self.mock_history.owner_exterior_number = "456"
        self.mock_history.owner_interior_number = "B"
        self.mock_history.owner_neighborhood = "Suburb"
        self.mock_history.alcohol_sales = "No"
        self.mock_history.schedule = "9-17"
        self.mock_history.municipality_id = 1
        self.mock_history.status = 1
        
        # Additional fields for comprehensive coverage
        self.mock_history.applicant_first_name = "Jane"
        self.mock_history.applicant_last_name_p = "Applicant"
        self.mock_history.applicant_last_name_m = "Test"
        self.mock_history.applicant_user_tax_id = "APP123"
        self.mock_history.applicant_national_id = "APP456"
        self.mock_history.applicant_phone = "555-9876"
        self.mock_history.applicant_street = "Second Street"
        self.mock_history.applicant_email = "jane@example.com"
        self.mock_history.applicant_postal_code = "12345"
        self.mock_history.owner_postal_code = "54321"
        self.mock_history.property_street = "Property St"
        self.mock_history.property_neighborhood = "Property Area"
        self.mock_history.property_interior_number = "C"
        self.mock_history.property_exterior_number = "789"
        self.mock_history.property_postal_code = "11111"
        self.mock_history.property_type = "Commercial"
        self.mock_history.business_trade_name = "Trade Name"
        self.mock_history.investment = "50000"
        self.mock_history.number_of_employees = "10"
        self.mock_history.number_of_parking_spaces = "5"
        self.mock_history.license_year = "2024"
        self.mock_history.license_type = "regular"
        self.mock_history.license_status = "active"
        self.mock_history.reason = "Test reason"
        self.mock_history.deactivation_status = "active"
        self.mock_history.payment_status = "paid"
        self.mock_history.opening_time = "09:00"
        self.mock_history.closing_time = "17:00"
        self.mock_history.alternate_license_year = "2023"
        self.mock_history.payment_user_id = 1
        self.mock_history.payment_date = datetime.now()
        self.mock_history.scanned_pdf = "http://example.com/pdf1.pdf"
        self.mock_history.step_1 = 1
        self.mock_history.step_2 = 1
        self.mock_history.step_3 = 1
        self.mock_history.step_4 = 1
        self.mock_history.minimap_url = "http://example.com/map.jpg"
        self.mock_history.reason_file = "http://example.com/reason.pdf"
        self.mock_history.status_change_date = datetime.now()
        self.mock_history.created_at = datetime.now()
        self.mock_history.updated_at = datetime.now()
        self.mock_history.deleted_at = None
    
    def teardown_method(self):
        """Clean up after tests."""
        app.dependency_overrides.clear()
    
    def test_list_business_license_histories_success(self):
        """Test successful listing of business license histories."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [self.mock_history]
        
        response = self.client.get("/v1/business_license_histories/?municipality_id=1")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["license_folio"] == "LIC-2024-001"
        assert data[0]["business_name"] == "Test Business"
    
    def test_list_business_license_histories_with_parameters(self):
        """Test listing with custom parameters."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        response = self.client.get("/v1/business_license_histories/?municipality_id=1&status=0&skip=10&limit=5")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_business_license_histories_missing_municipality_id(self):
        """Test listing without municipality_id parameter."""
        response = self.client.get("/v1/business_license_histories/")
        
        assert response.status_code == 422  # Validation error
    
    def test_list_business_license_histories_database_error(self):
        """Test database error during listing."""
        self.mock_db.query.side_effect = Exception("Database error")
        
        response = self.client.get("/v1/business_license_histories/?municipality_id=1")
        
        assert response.status_code == 500
        assert "An error occurred while retrieving business license histories" in response.json()["detail"]
    
    def test_get_business_license_history_success(self):
        """Test successful retrieval of single business license history."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = self.mock_history
        
        response = self.client.get("/v1/business_license_histories/1")
        
        assert response.status_code == 200
        data = response.json()
        assert data["license_folio"] == "LIC-2024-001"
        assert data["business_name"] == "Test Business"
    
    def test_get_business_license_history_not_found(self):
        """Test retrieval when business license history is not found."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = None
        
        response = self.client.get("/v1/business_license_histories/999")
        
        assert response.status_code == 404
        assert "Record not found" in response.json()["detail"]
    
    def test_create_business_license_history_success(self):
        """Test successful creation of business license history."""
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        # Mock the return value for the new entry
        mock_new_entry = MagicMock()
        mock_new_entry.id = 2
        mock_new_entry.license_folio = "LIC-2024-002"
        self.mock_db.refresh.side_effect = lambda obj: setattr(obj, 'id', 2)
        
        payload = {
            "license_folio": "LIC-2024-002",
            "issue_date": "2024-01-02",
            "business_line": "Services",
            "detailed_description": "New business description",
            "business_line_code": "S001",
            "business_area": "Service Area",
            "street": "New Street",
            "exterior_number": "456",
            "interior_number": "B",
            "neighborhood": "New Neighborhood",
            "cadastral_key": "CAD002",
            "reference": "Near mall",
            "coordinate_x": "20.654321",
            "coordinate_y": "-103.123456",
            "business_name": "New Business",
            "owner_first_name": "Jane",
            "owner_last_name_p": "Smith",
            "owner_last_name_m": "Johnson",
            "user_tax_id": "TAX654321",
            "national_id": "NAT012345",
            "owner_phone": "555-5678",
            "owner_email": "jane@newbusiness.com",
            "owner_street": "Owner Street",
            "owner_exterior_number": "789",
            "owner_interior_number": "C",
            "owner_neighborhood": "Owner Area",
            "alcohol_sales": "Yes",
            "schedule": "10-18",
            "municipality_id": 1,
            "status": 1,
            "applicant_first_name": "Bob",
            "applicant_last_name_p": "Builder",
            "applicant_last_name_m": "Architect",
            "applicant_user_tax_id": "APP789",
            "applicant_national_id": "APP012",
            "applicant_phone": "555-0000",
            "applicant_street": "Applicant St",
            "applicant_email": "bob@applicant.com",
            "applicant_postal_code": "67890",
            "owner_postal_code": "09876",
            "property_street": "Property Avenue",
            "property_neighborhood": "Property Zone",
            "property_interior_number": "D",
            "property_exterior_number": "101",
            "property_postal_code": "22222",
            "property_type": "Retail",
            "business_trade_name": "New Trade Name",
            "investment": "75000",
            "number_of_employees": "15",
            "number_of_parking_spaces": "8",
            "license_year": "2024",
            "license_type": "new",
            "license_status": "pending",
            "reason": "New application",
            "deactivation_status": "active",
            "payment_status": "pending",
            "opening_time": "10:00",
            "closing_time": "18:00",
            "alternate_license_year": "2023",
            "payment_user_id": 1,
            "payment_date": "2024-01-02T10:00:00",
            "scanned_pdf": "http://example.com/newpdf.pdf",
            "step_1": 1,
            "step_2": 0,
            "step_3": 0,
            "step_4": 0,
            "minimap_url": "http://example.com/newmap.jpg",
            "reason_file": "http://example.com/newreason.pdf",
            "status_change_date": "2024-01-02T10:00:00"
        }
        
        response = self.client.post("/v1/business_license_histories/", json=payload)
        
        assert response.status_code == 200
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
    
    def test_create_business_license_history_database_error(self):
        """Test database error during creation."""
        self.mock_db.add.side_effect = Exception("Database error")
        
        # Use the same comprehensive payload as the success test
        payload = {
            "license_folio": "LIC-2024-002",
            "issue_date": "2024-01-02",
            "business_line": "Services",
            "detailed_description": "New business description",
            "business_line_code": "S001",
            "business_area": "Service Area",
            "street": "New Street",
            "exterior_number": "456",
            "interior_number": "B",
            "neighborhood": "New Neighborhood",
            "cadastral_key": "CAD002",
            "reference": "Near mall",
            "coordinate_x": "20.654321",
            "coordinate_y": "-103.123456",
            "business_name": "New Business",
            "owner_first_name": "Jane",
            "owner_last_name_p": "Smith",
            "owner_last_name_m": "Johnson",
            "user_tax_id": "TAX654321",
            "national_id": "NAT012345",
            "owner_phone": "555-5678",
            "owner_email": "jane@newbusiness.com",
            "owner_street": "Owner Street",
            "owner_exterior_number": "789",
            "owner_interior_number": "C",
            "owner_neighborhood": "Owner Area",
            "alcohol_sales": "Yes",
            "schedule": "10-18",
            "municipality_id": 1,
            "status": 1,
            "applicant_first_name": "Bob",
            "applicant_last_name_p": "Builder",
            "applicant_last_name_m": "Architect",
            "applicant_user_tax_id": "APP789",
            "applicant_national_id": "APP012",
            "applicant_phone": "555-0000",
            "applicant_street": "Applicant St",
            "applicant_email": "bob@applicant.com",
            "applicant_postal_code": "67890",
            "owner_postal_code": "09876",
            "property_street": "Property Avenue",
            "property_neighborhood": "Property Zone",
            "property_interior_number": "D",
            "property_exterior_number": "101",
            "property_postal_code": "22222",
            "property_type": "Retail",
            "business_trade_name": "New Trade Name",
            "investment": "75000",
            "number_of_employees": "15",
            "number_of_parking_spaces": "8",
            "license_year": "2024",
            "license_type": "new",
            "license_status": "pending",
            "reason": "New application",
            "deactivation_status": "active",
            "payment_status": "pending",
            "opening_time": "10:00",
            "closing_time": "18:00",
            "alternate_license_year": "2023",
            "payment_user_id": 1,
            "payment_date": "2024-01-02T10:00:00",
            "scanned_pdf": "http://example.com/newpdf.pdf",
            "step_1": 1,
            "step_2": 0,
            "step_3": 0,
            "step_4": 0,
            "minimap_url": "http://example.com/newmap.jpg",
            "reason_file": "http://example.com/newreason.pdf",
            "status_change_date": "2024-01-02T10:00:00"
        }
        
        response = self.client.post("/v1/business_license_histories/", json=payload)
        
        assert response.status_code == 400
        assert "An error occurred while creating the business license history" in response.json()["detail"]
        self.mock_db.rollback.assert_called_once()
    
    def test_update_business_license_history_success(self):
        """Test successful update of business license history."""
        self.mock_db.query.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        payload = {
            "business_name": "Updated Business Name",
            "license_status": "expired",
            "business_line": "Updated Services"
        }
        
        response = self.client.patch("/v1/business_license_histories/1", json=payload)
        
        assert response.status_code == 200
        self.mock_db.commit.assert_called_once()
    
    def test_update_business_license_history_not_found(self):
        """Test update when business license history is not found."""
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        payload = {"business_name": "Updated Business Name"}
        
        response = self.client.patch("/v1/business_license_histories/999", json=payload)
        
        assert response.status_code == 404
        assert "Record not found" in response.json()["detail"]
    
    def test_update_business_license_history_no_data(self):
        """Test update with no data provided."""
        response = self.client.patch("/v1/business_license_histories/1", json={})
        
        assert response.status_code == 400
        assert "No data provided for update" in response.json()["detail"]
    
    def test_update_business_license_history_database_error(self):
        """Test database error during update."""
        self.mock_db.query.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.commit.side_effect = Exception("Database error")
        
        payload = {"business_name": "Updated Business Name"}
        
        response = self.client.patch("/v1/business_license_histories/1", json=payload)
        
        assert response.status_code == 400
        assert "An error occurred while updating the business license history" in response.json()["detail"]
        self.mock_db.rollback.assert_called_once()
    
    @patch('pandas.DataFrame.to_excel')
    def test_export_business_license_histories_success(self, mock_to_excel):
        """Test successful export of business license histories."""
        self.mock_db.query.return_value.filter.return_value.all.return_value = [self.mock_history]
        
        # Mock to_excel to write to the stream
        def mock_excel_write(stream, *args, **kwargs):
            stream.write(b"fake excel content")
        
        mock_to_excel.side_effect = mock_excel_write
        
        response = self.client.get("/v1/business_license_histories/export?municipality_id=1")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        assert "attachment" in response.headers["content-disposition"]
    
    def test_delete_business_license_history_success(self):
        """Test successful soft deletion of business license history."""
        self.mock_db.query.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.commit.return_value = None
        
        response = self.client.delete("/v1/business_license_histories/1")
        
        assert response.status_code == 200
        assert response.json()["detail"] == "Record marked as inactive"
        assert self.mock_history.status == 0
        self.mock_db.commit.assert_called_once()
    
    def test_delete_business_license_history_not_found(self):
        """Test deletion when business license history is not found."""
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        response = self.client.delete("/v1/business_license_histories/999")
        
        assert response.status_code == 404
        assert "Record not found" in response.json()["detail"]
    
    def test_delete_business_license_history_database_error(self):
        """Test database error during deletion."""
        self.mock_db.query.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.commit.side_effect = Exception("Database error")
        
        response = self.client.delete("/v1/business_license_histories/1")
        
        assert response.status_code == 400
        assert "An error occurred while deactivating the business license history" in response.json()["detail"]
        self.mock_db.rollback.assert_called_once()
    
    @patch('qrcode.make')
    @patch('weasyprint.HTML')
    @patch('jinja2.Environment.get_template')
    def test_generate_business_license_pdf_success(self, mock_get_template, mock_html, mock_qr):
        """Test successful PDF generation."""
        self.mock_db.query.return_value.filter.return_value.first.return_value = self.mock_history
        
        # Mock QR code generation
        mock_qr_img = MagicMock()
        mock_qr.return_value = mock_qr_img
        
        # Mock template rendering
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test License PDF</html>"
        mock_get_template.return_value = mock_template
        
        # Mock WeasyPrint
        mock_html_instance = MagicMock()
        mock_html_instance.write_pdf.return_value = b"fake pdf content"
        mock_html.return_value = mock_html_instance
        
        response = self.client.get("/v1/business_license_histories/pdf/1/2024/regular")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "inline" in response.headers["content-disposition"]
    
    def test_generate_business_license_pdf_not_found(self):
        """Test PDF generation when license history is not found."""
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        response = self.client.get("/v1/business_license_histories/pdf/999/2024/regular")
        
        assert response.status_code == 404
        assert "License history not found" in response.json()["detail"]
    
    @patch('pandas.read_excel')
    def test_import_business_license_histories_success(self, mock_read_excel):
        """Test successful import of business license histories."""
        # Mock Excel data
        mock_df = pd.DataFrame([
            {
                "License Folio": "LIC-IMPORT-001",
                "Business Name": "Imported Business",
                "Owner": "Jane Doe Smith",
                "Issue Date": "2024-01-01",
                "Business Line": "Services",
                "Business Line Code": "S001"
            }
        ])
        mock_read_excel.return_value = mock_df
        
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        
        # Mock file upload
        file_content = b"fake excel content"
        files = {"file": ("test.xlsx", io.BytesIO(file_content), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        
        response = self.client.post("/v1/business_license_histories/import?municipality_id=1", files=files)
        
        assert response.status_code == 200
        assert "1 records successfully imported" in response.json()["detail"]
        self.mock_db.commit.assert_called_once()
    
    def test_import_business_license_histories_invalid_file(self):
        """Test import with invalid file type."""
        files = {"file": ("test.txt", io.BytesIO(b"text content"), "text/plain")}
        
        response = self.client.post("/v1/business_license_histories/import?municipality_id=1", files=files)
        
        assert response.status_code == 400
        assert "Only Excel files are supported" in response.json()["detail"]
    
    @patch('pandas.read_excel')
    def test_import_business_license_histories_database_error(self, mock_read_excel):
        """Test database error during import."""
        mock_df = pd.DataFrame([{"License Folio": "LIC-001", "Business Name": "Test"}])
        mock_read_excel.return_value = mock_df
        
        self.mock_db.add.side_effect = Exception("Database error")
        
        files = {"file": ("test.xlsx", io.BytesIO(b"fake excel content"), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        
        response = self.client.post("/v1/business_license_histories/import?municipality_id=1", files=files)
        
        assert response.status_code == 500
        assert "An error occurred while importing data" in response.json()["detail"]
        self.mock_db.rollback.assert_called_once()
    
    def test_update_business_license_status_success(self):
        """Test successful update of business license status."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        payload = {
            "license_status": "suspended",
            "reason": "Violation of regulations",
            "status_change_date": "2024-01-15T10:00:00"
        }
        
        response = self.client.patch("/v1/business_license_histories/1/status", json=payload)
        
        assert response.status_code == 200
        assert self.mock_history.license_status == "suspended"
        assert self.mock_history.reason == "Violation of regulations"
        self.mock_db.commit.assert_called_once()
    
    def test_update_business_license_status_not_found(self):
        """Test status update when license history is not found."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = None
        
        payload = {"license_status": "suspended"}
        
        response = self.client.patch("/v1/business_license_histories/999/status", json=payload)
        
        assert response.status_code == 404
        assert "Record not found" in response.json()["detail"]
    
    def test_mark_business_license_as_paid_success(self):
        """Test successful payment status update."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        payload = {
            "payment_status": "paid",
            "payment_user_id": 1,
            "payment_date": "2024-01-15T10:00:00"
        }
        
        response = self.client.patch("/v1/business_license_histories/1/paid", json=payload)
        
        assert response.status_code == 200
        assert self.mock_history.payment_status == "paid"
        assert self.mock_history.payment_user_id == 1
        self.mock_db.commit.assert_called_once()
    
    def test_mark_business_license_as_paid_not_found(self):
        """Test payment update when license history is not found."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = None
        
        payload = {"payment_status": "paid"}
        
        response = self.client.patch("/v1/business_license_histories/999/paid", json=payload)
        
        assert response.status_code == 404
        assert "Record not found" in response.json()["detail"]
    
    def test_get_business_license_files_success(self):
        """Test successful retrieval of business license files."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = self.mock_history
        
        response = self.client.get("/v1/business_license_histories/1/files")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 2
        assert len(data["files"]) == 2
        assert any(f["filename"] == "license_1_scanned.pdf" for f in data["files"])
        assert any(f["filename"] == "license_1_reason_file" for f in data["files"])
    
    def test_get_business_license_files_not_found(self):
        """Test file retrieval when license history is not found."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = None
        
        response = self.client.get("/v1/business_license_histories/999/files")
        
        assert response.status_code == 404
        assert "Record not found" in response.json()["detail"]
    
    def test_delete_business_license_file_success(self):
        """Test successful deletion of business license file."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.commit.return_value = None
        
        response = self.client.delete("/v1/business_license_histories/1/files/scanned_pdf")
        
        assert response.status_code == 200
        assert response.json()["detail"] == "scanned_pdf successfully deleted"
        assert self.mock_history.scanned_pdf is None
        self.mock_db.commit.assert_called_once()
    
    def test_delete_business_license_file_invalid_type(self):
        """Test file deletion with invalid file type."""
        response = self.client.delete("/v1/business_license_histories/1/files/invalid_type")
        
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]
    
    def test_delete_business_license_file_not_found(self):
        """Test file deletion when file doesn't exist."""
        history_without_file = MagicMock(spec=BusinessLicenseHistory)
        history_without_file.scanned_pdf = None
        
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = history_without_file
        
        response = self.client.delete("/v1/business_license_histories/1/files/scanned_pdf")
        
        assert response.status_code == 404
        assert "Scanned PDF file not found" in response.json()["detail"]
    
    def test_create_business_license_renewal_success(self):
        """Test successful creation of business license renewal."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        
        # Mock refresh to set an id on the new object
        def mock_refresh(obj):
            obj.id = 2
        self.mock_db.refresh.side_effect = mock_refresh
        
        payload = {
            "license_year": "2024",
            "license_type": "refrendo"
        }
        
        response = self.client.post("/v1/business_license_histories/1/refrendo", json=payload)
        
        assert response.status_code == 200
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
    
    def test_create_business_license_renewal_original_not_found(self):
        """Test renewal creation when original license is not found."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = None
        
        payload = {
            "license_year": "2024",
            "license_type": "refrendo"
        }
        
        response = self.client.post("/v1/business_license_histories/999/refrendo", json=payload)
        
        assert response.status_code == 404
        assert "Original license record not found" in response.json()["detail"]
    
    @pytest.mark.parametrize("municipality_id,status,skip,limit", [
        (1, 1, 0, 20),
        (2, 0, 10, 50),
        (1, 1, 5, 15)
    ])
    def test_list_business_license_histories_various_parameters(self, municipality_id, status, skip, limit):
        """Test listing with various parameter combinations."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        
        response = self.client.get(f"/v1/business_license_histories/?municipality_id={municipality_id}&status={status}&skip={skip}&limit={limit}")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_update_license_status_database_error(self):
        """Test database error during status update."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.commit.side_effect = Exception("Database error")
        
        payload = {"license_status": "suspended"}
        
        response = self.client.patch("/v1/business_license_histories/1/status", json=payload)
        
        assert response.status_code == 400
        assert "An error occurred while updating the license status" in response.json()["detail"]
        self.mock_db.rollback.assert_called_once()
    
    def test_mark_as_paid_database_error(self):
        """Test database error during payment update."""
        self.mock_db.query.return_value.filter.return_value.filter.return_value.first.return_value = self.mock_history
        self.mock_db.commit.side_effect = Exception("Database error")
        
        payload = {"payment_status": "paid"}
        
        response = self.client.patch("/v1/business_license_histories/1/paid", json=payload)
        
        assert response.status_code == 400
        assert "An error occurred while updating the payment status" in response.json()["detail"]
        self.mock_db.rollback.assert_called_once()
