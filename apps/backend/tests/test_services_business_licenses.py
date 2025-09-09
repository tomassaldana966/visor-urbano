import pytest
import base64
import io
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.services.formats.business_licenses import (
    generate_unsigned_receipt_pdf,
    generate_signed_receipt_pdf,
    generate_responsible_letter_pdf,
    generate_provisional_opening_pdf
)


class TestBusinessLicensesFormatService:
    """Test cases for business licenses format service."""

    @pytest.fixture
    def mock_db_session(self):
        """Create a mock database session."""
        return AsyncMock(spec=AsyncSession)

    @pytest.fixture
    def sample_requirements_query(self):
        """Create a sample requirements query."""
        query = Mock()
        query.folio = "TEST-001"
        query.municipality_name = "Test City"
        query.applicant_name = "John Doe"
        query.street = "Main Street 123"
        query.neighborhood = "Downtown"
        query.property_exterior_number = "123"
        query.property_interior_number = "A"
        query.created_at = datetime(2025, 6, 14, 12, 0, 0)
        query.minimap_url = "https://example.com/map.png"
        query.answers = []
        
        # Mock municipality
        municipality = Mock()
        municipality.logo_url = "https://example.com/logo.png"
        query.municipality = municipality
        
        return query

    @pytest.fixture
    def sample_provisional_opening(self):
        """Create a sample provisional opening."""
        opening = Mock()
        opening.folio = "TEST-001"
        opening.counter = 1
        opening.id = 1
        return opening

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.get_unsigned_receipt_data_async')
    @patch('app.services.formats.business_licenses.HTML')
    @patch('app.services.formats.business_licenses.env')
    async def test_generate_unsigned_receipt_pdf_success(self, mock_env, mock_html, mock_get_data, mock_db_session):
        """Test successful unsigned receipt PDF generation."""
        # Mock data
        mock_data = {
            "folio": "TEST-001",
            "municipality": "Test City",
            "applicant": "John Doe"
        }
        mock_get_data.return_value = mock_data
        
        # Mock template
        mock_template = Mock()
        mock_template.render.return_value = "<html>Test content</html>"
        mock_env.get_template.return_value = mock_template
        
        # Mock HTML and PDF generation
        mock_html_instance = Mock()
        mock_html_instance.write_pdf.return_value = b"fake_pdf_content"
        mock_html.return_value = mock_html_instance
        
        result = await generate_unsigned_receipt_pdf("TEST-001", mock_db_session)
        
        # Verify calls
        mock_get_data.assert_called_once_with("TEST-001", mock_db_session)
        mock_env.get_template.assert_called_once_with("unsigned_receipt_template.html")
        assert result == b"fake_pdf_content"

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.get_unsigned_receipt_data_async')
    async def test_generate_unsigned_receipt_pdf_no_data(self, mock_get_data, mock_db_session):
        """Test unsigned receipt PDF generation with no data."""
        mock_get_data.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await generate_unsigned_receipt_pdf("NONEXISTENT", mock_db_session)
        
        assert exc_info.value.status_code == 404
        assert "Folio not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.qrcode')
    @patch('app.services.formats.business_licenses.HTML')
    @patch('app.services.formats.business_licenses.env')
    @patch('app.services.formats.business_licenses.base64')
    async def test_generate_signed_receipt_pdf_success(self, mock_base64, mock_env, mock_html, mock_qrcode, mock_db_session, sample_requirements_query):
        """Test successful signed receipt PDF generation."""
        # Mock base64 decoding
        mock_base64.b64decode.return_value.decode.return_value = "TEST-001"
        mock_base64.b64encode.return_value.decode.return_value = "base64_qr_code"
        
        # Mock database query
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        # Mock QR code generation
        mock_qr = Mock()
        mock_img = Mock()
        mock_qr.make_image.return_value = mock_img
        mock_qrcode.QRCode.return_value = mock_qr
        
        # Mock BytesIO
        with patch('app.services.formats.business_licenses.BytesIO') as mock_bytesio:
            mock_buffer = Mock()
            mock_buffer.getvalue.return_value = b"qr_image_data"
            mock_bytesio.return_value = mock_buffer
            
            # Mock template
            mock_template = Mock()
            mock_template.render.return_value = "<html>Signed receipt</html>"
            mock_env.get_template.return_value = mock_template
            
            # Mock HTML
            mock_html_instance = Mock()
            mock_html_instance.write_pdf.return_value = b"signed_pdf_content"
            mock_html.return_value = mock_html_instance
            
            result = await generate_signed_receipt_pdf("encoded_folio", mock_db_session)
            
            assert result == b"signed_pdf_content"

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.base64')
    async def test_generate_signed_receipt_pdf_folio_not_found(self, mock_base64, mock_db_session):
        """Test signed receipt PDF generation with folio not found."""
        mock_base64.b64decode.return_value.decode.return_value = "NONEXISTENT"
        
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        with pytest.raises(Exception, match="Folio not found"):
            await generate_signed_receipt_pdf("encoded_folio", mock_db_session)

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.get_responsible_letter_data')
    @patch('app.services.formats.business_licenses.HTML')
    @patch('app.services.formats.business_licenses.Environment')
    async def test_generate_responsible_letter_pdf_success(self, mock_environment, mock_html, mock_get_data, mock_db_session):
        """Test successful responsible letter PDF generation."""
        # Mock data
        mock_data = {
            "government_logo": "https://example.com/gov_logo.png",
            "logo_url": "https://example.com/logo.png",
            "municipality": "Test City",
            "date": "2025-06-14",
            "applicant": "John Doe",
            "scian_name": "Test Business",
            "address": "123 Main St"
        }
        mock_get_data.return_value = mock_data
        
        # Mock environment and template
        mock_env_instance = Mock()
        mock_template = Mock()
        mock_template.render.return_value = "<html>Responsible letter</html>"
        mock_env_instance.get_template.return_value = mock_template
        mock_environment.return_value = mock_env_instance
        
        # Mock HTML
        mock_html_instance = Mock()
        mock_html_instance.write_pdf.return_value = b"responsible_letter_pdf"
        mock_html.return_value = mock_html_instance
        
        result = await generate_responsible_letter_pdf(mock_db_session, "TEST-001")
        
        assert result == b"responsible_letter_pdf"
        mock_get_data.assert_called_once_with(mock_db_session, "TEST-001")

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.get_responsible_letter_data')
    async def test_generate_responsible_letter_pdf_no_data(self, mock_get_data, mock_db_session):
        """Test responsible letter PDF generation with no data."""
        mock_get_data.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            await generate_responsible_letter_pdf(mock_db_session, "NONEXISTENT")
        
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.qrcode')
    @patch('app.services.formats.business_licenses.HTML')
    @patch('app.services.formats.business_licenses.env')
    @patch('app.services.formats.business_licenses.base64')
    async def test_generate_provisional_opening_pdf_success(self, mock_base64, mock_env, mock_html, mock_qrcode, mock_db_session, sample_provisional_opening, sample_requirements_query):
        """Test successful provisional opening PDF generation."""
        # Mock base64 decoding
        mock_base64.b64decode.return_value.decode.return_value = "TEST-001"
        mock_base64.b64encode.return_value.decode.return_value = "qr_base64"
        
        # Mock database queries
        mock_opening_result = Mock()
        mock_opening_result.scalars.return_value.first.return_value = sample_provisional_opening
        
        mock_req_result = Mock()
        mock_req_result.scalars.return_value.first.return_value = sample_requirements_query
        
        mock_db_session.execute.side_effect = [mock_opening_result, mock_req_result]
        
        # Mock QR code generation
        mock_qr = Mock()
        mock_qrcode.make.return_value = mock_qr
        
        # Mock BytesIO
        with patch('app.services.formats.business_licenses.io.BytesIO') as mock_bytesio:
            mock_buffer = Mock()
            mock_buffer.getvalue.return_value = b"qr_data"
            mock_bytesio.return_value = mock_buffer
            
            # Mock template
            mock_template = Mock()
            mock_template.render.return_value = "<html>Provisional opening</html>"
            mock_env.get_template.return_value = mock_template
            
            # Mock HTML
            mock_html_instance = Mock()
            mock_html_instance.write_pdf.return_value = b"provisional_pdf"
            mock_html.return_value = mock_html_instance
            
            result = await generate_provisional_opening_pdf(mock_db_session, "encoded_folio")
            
            assert result == b"provisional_pdf"

    @pytest.mark.asyncio
    async def test_generate_provisional_opening_pdf_invalid_encoding(self, mock_db_session):
        """Test provisional opening PDF generation with invalid encoding."""
        with patch('app.services.formats.business_licenses.base64.b64decode', side_effect=Exception("Invalid base64")):
            with pytest.raises(HTTPException) as exc_info:
                await generate_provisional_opening_pdf(mock_db_session, "invalid_folio")
            
            assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
            assert "Invalid folio encoding" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.base64')
    async def test_generate_provisional_opening_pdf_opening_not_found(self, mock_base64, mock_db_session):
        """Test provisional opening PDF generation with opening not found."""
        mock_base64.b64decode.return_value.decode.return_value = "TEST-001"
        
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        with pytest.raises(HTTPException) as exc_info:
            await generate_provisional_opening_pdf(mock_db_session, "encoded_folio")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Provisional opening not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.base64')
    async def test_generate_provisional_opening_pdf_requirements_not_found(self, mock_base64, mock_db_session, sample_provisional_opening):
        """Test provisional opening PDF generation with requirements not found."""
        mock_base64.b64decode.return_value.decode.return_value = "TEST-001"
        
        # Mock opening found, requirements not found
        mock_opening_result = Mock()
        mock_opening_result.scalars.return_value.first.return_value = sample_provisional_opening
        
        mock_req_result = Mock()
        mock_req_result.scalars.return_value.first.return_value = None
        
        mock_db_session.execute.side_effect = [mock_opening_result, mock_req_result]
        
        with pytest.raises(HTTPException) as exc_info:
            await generate_provisional_opening_pdf(mock_db_session, "encoded_folio")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Requirements not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    @patch('app.services.formats.business_licenses.qrcode')
    @patch('app.services.formats.business_licenses.env')
    @patch('app.services.formats.business_licenses.base64')
    async def test_generate_provisional_opening_pdf_template_not_found(self, mock_base64, mock_env, mock_qrcode, mock_db_session, sample_provisional_opening, sample_requirements_query):
        """Test provisional opening PDF generation with template not found."""
        mock_base64.b64decode.return_value.decode.return_value = "TEST-001"
        
        # Mock database queries
        mock_opening_result = Mock()
        mock_opening_result.scalars.return_value.first.return_value = sample_provisional_opening
        
        mock_req_result = Mock()
        mock_req_result.scalars.return_value.first.return_value = sample_requirements_query
        
        mock_db_session.execute.side_effect = [mock_opening_result, mock_req_result]
        
        # Mock QR generation
        mock_qrcode.make.return_value = Mock()
        
        with patch('app.services.formats.business_licenses.io.BytesIO'), \
             patch('app.services.formats.business_licenses.base64.b64encode'):
            
            # Mock template not found
            mock_env.get_template.side_effect = Exception("Template not found")
            
            with pytest.raises(HTTPException) as exc_info:
                await generate_provisional_opening_pdf(mock_db_session, "encoded_folio")
            
            assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert "Template not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_signed_receipt_pdf_with_municipality_no_logo(self, mock_db_session):
        """Test signed receipt PDF generation with municipality without logo."""
        sample_query = Mock()
        sample_query.folio = "TEST-001"
        sample_query.municipality_name = "Test City"
        sample_query.applicant_name = "John Doe"
        sample_query.street = "Main Street"
        sample_query.neighborhood = "Downtown"
        sample_query.created_at = datetime(2025, 6, 14)
        sample_query.answers = []
        
        # Municipality without logo_url
        municipality = Mock()
        municipality.logo_url = None
        sample_query.municipality = municipality
        
        with patch('app.services.formats.business_licenses.base64') as mock_base64, \
             patch('app.services.formats.business_licenses.qrcode'), \
             patch('app.services.formats.business_licenses.BytesIO'), \
             patch('app.services.formats.business_licenses.env') as mock_env, \
             patch('app.services.formats.business_licenses.HTML') as mock_html:
            
            mock_base64.b64decode.return_value.decode.return_value = "TEST-001"
            mock_base64.b64encode.return_value.decode.return_value = "qr_code"
            
            mock_result = Mock()
            mock_result.scalars.return_value.first.return_value = sample_query
            mock_db_session.execute.return_value = mock_result
            
            mock_template = Mock()
            mock_template.render.return_value = "<html>Content</html>"
            mock_env.get_template.return_value = mock_template
            
            mock_html_instance = Mock()
            mock_html_instance.write_pdf.return_value = b"pdf_content"
            mock_html.return_value = mock_html_instance
            
            result = await generate_signed_receipt_pdf("encoded_folio", mock_db_session)
            
            # Verify that default logo is used when municipality has no logo
            mock_template.render.assert_called_once()
            call_args = mock_template.render.call_args
            assert "logo" in call_args[1]
            assert "https://visorurbano.com/assets/img/logo.png" in call_args[1]["logo"]


if __name__ == "__main__":
    pytest.main([__file__])
