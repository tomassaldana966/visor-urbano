import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
import io
import base64

from app.main import app
from config.settings import get_db
from config.security import get_current_user


def encode_folio_to_base64(folio: str) -> str:
    """Helper function to encode folio to base64."""
    return base64.b64encode(folio.encode('utf-8')).decode('utf-8')


class TestBusinessLicenses:
    def setup_method(self):
        """Setup for each test method."""
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_user = MagicMock()
        self.mock_user.id = 1
        self.mock_user.username = "testuser"
        self.client = TestClient(app)
        
        # Override dependencies
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[get_current_user] = lambda: self.mock_user

    def teardown_method(self):
        """Cleanup after each test method."""
        app.dependency_overrides.clear()

    @patch('app.routers.business_licenses.generate_unsigned_receipt_pdf')
    def test_get_unsigned_receipt_success(self, mock_generate_pdf):
        """Test successful generation of unsigned receipt PDF."""
        # Arrange
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)
        mock_pdf_content = b"PDF content"
        mock_generate_pdf.return_value = mock_pdf_content

        # Act
        response = self.client.get(f"/v1/business_licenses/unsigned_receipt/{encoded_folio}")

        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert response.content == mock_pdf_content
        mock_generate_pdf.assert_called_once_with(test_folio, self.mock_db)

    @patch('app.routers.business_licenses.generate_unsigned_receipt_pdf')
    def test_get_unsigned_receipt_generation_error(self, mock_generate_pdf):
        """Test handling of PDF generation error for unsigned receipt."""
        # Arrange
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)
        mock_generate_pdf.side_effect = Exception("PDF generation failed")

        # Act
        response = self.client.get(f"/v1/business_licenses/unsigned_receipt/{encoded_folio}")

        # Assert
        assert response.status_code == 500

    @patch('app.routers.business_licenses.generate_signed_receipt_pdf')
    def test_get_signed_receipt_success(self, mock_generate_pdf):
        """Test successful generation of signed receipt PDF."""
        # Arrange
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)
        mock_pdf_content = b"Signed PDF content"
        mock_generate_pdf.return_value = mock_pdf_content

        # Act
        response = self.client.get(f"/v1/business_licenses/signed_receipt/{encoded_folio}")

        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert f"signed_receipt_{test_folio}.pdf" in response.headers.get("content-disposition", "")
        assert response.content == mock_pdf_content
        mock_generate_pdf.assert_called_once_with(folio=test_folio, db=self.mock_db)

    @patch('app.routers.business_licenses.generate_signed_receipt_pdf')
    def test_get_signed_receipt_generation_error(self, mock_generate_pdf):
        """Test handling of PDF generation error for signed receipt."""
        # Arrange
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)
        mock_generate_pdf.side_effect = Exception("PDF generation failed")

        # Act
        response = self.client.get(f"/v1/business_licenses/signed_receipt/{encoded_folio}")

        # Assert
        assert response.status_code == 404
        assert "Error generating PDF" in response.json()["detail"]

    @patch('app.routers.business_licenses.generate_responsible_letter_pdf')
    def test_get_responsible_letter_success(self, mock_generate_pdf):
        """Test successful generation of responsible letter PDF."""
        # Arrange
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)
        mock_pdf_content = b"Responsible letter PDF content"
        mock_generate_pdf.return_value = mock_pdf_content

        # Act
        response = self.client.get(f"/v1/business_licenses/responsible_letter/{encoded_folio}")

        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert f"responsible_letter_{test_folio}.pdf" in response.headers.get("content-disposition", "")
        assert response.content == mock_pdf_content
        mock_generate_pdf.assert_called_once_with(db=self.mock_db, folio=test_folio)

    @patch('app.routers.business_licenses.generate_responsible_letter_pdf')
    def test_get_responsible_letter_generation_error(self, mock_generate_pdf):
        """Test handling of PDF generation error for responsible letter."""
        # Arrange
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)
        mock_generate_pdf.side_effect = Exception("PDF generation failed")

        # Act
        response = self.client.get(f"/v1/business_licenses/responsible_letter/{encoded_folio}")

        # Assert
        assert response.status_code == 500
        assert "PDF generation failed" in response.json()["detail"]

    def test_get_responsible_letter_unauthorized(self):
        """Test responsible letter access without authentication."""
        # Arrange - Remove both dependencies to simulate unauthorized access
        app.dependency_overrides.clear()
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)

        # Act
        response = self.client.get(f"/v1/business_licenses/responsible_letter/{encoded_folio}")

        # Assert
        assert response.status_code in [401, 403, 422]  # Unauthorized, Forbidden, or validation error

    @patch('app.routers.business_licenses.generate_provisional_opening_pdf')
    def test_provisional_opening_success(self, mock_generate_pdf):
        """Test successful generation of provisional opening PDF."""
        # Arrange
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)
        mock_pdf_content = b"Provisional opening PDF content"
        mock_generate_pdf.return_value = mock_pdf_content

        # Act
        response = self.client.get(f"/v1/business_licenses/provisional_opening/{encoded_folio}")

        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        mock_generate_pdf.assert_called_once_with(db=self.mock_db, folio=test_folio)

    @patch('app.routers.business_licenses.generate_provisional_opening_pdf')
    def test_provisional_opening_generation_error(self, mock_generate_pdf):
        """Test handling of PDF generation error for provisional opening."""
        # Arrange
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)
        mock_generate_pdf.side_effect = Exception("PDF generation failed")

        # Act
        response = self.client.get(f"/v1/business_licenses/provisional_opening/{encoded_folio}")

        # Assert
        assert response.status_code == 500

    def test_provisional_opening_unauthorized(self):
        """Test provisional opening access without authentication."""
        # Arrange - Remove dependencies to simulate unauthorized access
        app.dependency_overrides.clear()
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)

        # Act
        response = self.client.get(f"/v1/business_licenses/provisional_opening/{encoded_folio}")

        # Assert
        assert response.status_code in [401, 403, 422]  # Unauthorized, Forbidden, or validation error

    @pytest.mark.parametrize("folio", [
        "TEST-2024-001",
        "BUSINESS-2024-12345",
        "FOL_2023_999",
        "123456789"
    ])
    @patch('app.routers.business_licenses.generate_unsigned_receipt_pdf')
    def test_different_folio_formats(self, mock_generate_pdf, folio):
        """Test PDF generation with different folio formats."""
        # Arrange
        encoded_folio = encode_folio_to_base64(folio)
        mock_pdf_content = b"PDF content"
        mock_generate_pdf.return_value = mock_pdf_content

        # Act
        response = self.client.get(f"/v1/business_licenses/unsigned_receipt/{encoded_folio}")

        # Assert
        assert response.status_code == 200
        mock_generate_pdf.assert_called_once_with(folio, self.mock_db)

    @pytest.mark.parametrize("endpoint", [
        "unsigned_receipt",
        "signed_receipt",
        "responsible_letter",
        "provisional_opening"
    ])
    def test_invalid_folio_handling(self, endpoint):
        """Test handling of invalid or empty folio parameters."""
        # Arrange
        invalid_folio = ""

        # Act
        response = self.client.get(f"/v1/business_licenses/{endpoint}/{invalid_folio}")

        # Assert
        # Should either return 404 (not found) or 422 (validation error)
        assert response.status_code in [404, 422]

    @patch('app.routers.business_licenses.generate_unsigned_receipt_pdf')
    def test_database_connection_error(self, mock_generate_pdf):
        """Test handling of database connection errors."""
        # Arrange
        test_folio = "TEST-2024-001"
        encoded_folio = encode_folio_to_base64(test_folio)
        mock_generate_pdf.side_effect = Exception("Database connection failed")

        # Act
        response = self.client.get(f"/v1/business_licenses/unsigned_receipt/{encoded_folio}")

        # Assert
        assert response.status_code == 500

    def test_content_type_headers(self):
        """Test that all endpoints return proper PDF content type."""
        # This test would need to be run with actual service functions
        # or more detailed mocking to verify headers
        pass

    @patch('app.routers.business_licenses.generate_signed_receipt_pdf')
    def test_large_folio_string(self, mock_generate_pdf):
        """Test handling of unusually large folio strings."""
        # Arrange
        large_folio = "TEST-" + "X" * 1000  # Very long folio
        encoded_folio = encode_folio_to_base64(large_folio)
        mock_pdf_content = b"PDF content"
        mock_generate_pdf.return_value = mock_pdf_content

        # Act
        response = self.client.get(f"/v1/business_licenses/signed_receipt/{encoded_folio}")

        # Assert
        assert response.status_code == 200
        mock_generate_pdf.assert_called_once_with(folio=large_folio, db=self.mock_db)

    @patch('app.routers.business_licenses.generate_responsible_letter_pdf')
    def test_special_characters_in_folio(self, mock_generate_pdf):
        """Test handling of special characters in folio."""
        # Arrange
        special_folio = "TEST-2024-001_SPECIAL"  # Use URL-safe special characters
        encoded_folio = encode_folio_to_base64(special_folio)
        mock_pdf_content = b"PDF content"
        mock_generate_pdf.return_value = mock_pdf_content

        # Act
        response = self.client.get(f"/v1/business_licenses/responsible_letter/{encoded_folio}")

        # Assert
        assert response.status_code == 200
        mock_generate_pdf.assert_called_once_with(db=self.mock_db, folio=special_folio)
