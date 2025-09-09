import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from datetime import datetime
import base64


def encode_folio_to_base64(folio: str) -> str:
    """Helper function to encode folio to base64."""
    return base64.b64encode(folio.encode('utf-8')).decode('utf-8')


class TestBusinessLicensesRouter:
    """Test suite for business licenses router endpoints"""

    def setup_method(self):
        """Set up test fixtures"""
        # Create a more realistic mock license with proper attributes as simple values
        self.mock_license = MagicMock()
        self.mock_license.id = 1
        self.mock_license.license_folio = "BL-2024-001"
        self.mock_license.commercial_activity = "Restaurant"
        self.mock_license.industry_classification_code = "722001"
        self.mock_license.license_status = "active"
        self.mock_license.license_type = "Commercial"
        self.mock_license.municipality_id = 1
        self.mock_license.municipality_name = None  # This is excluded from the model  
        self.mock_license.deleted_at = None
        self.mock_license.created_at = datetime.now()
        self.mock_license.updated_at = datetime.now()

    @pytest.mark.asyncio
    @patch('app.routers.business_licenses.BusinessLicensePublic')
    @patch('app.routers.business_licenses.get_db')
    async def test_list_business_licenses_public_success(self, mock_get_db, mock_business_license_public):
        """Test successful listing of public business licenses"""
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db

        # Mock count query result
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1

        # Mock main query result
        mock_result = MagicMock()
        mock_result.all.return_value = [(self.mock_license, "Test Municipality")]

        # Setup db.execute to return appropriate results for each query
        mock_db.execute = AsyncMock(side_effect=[mock_count_result, mock_result])

        # Mock the Pydantic model
        mock_license_model = MagicMock()
        mock_license_model.model_dump.return_value = {
            "license_folio": "BL-2024-001",
            "commercial_activity": "Restaurant",
            "industry_classification_code": "722001",
            "license_status": "active",
            "license_type": "Commercial",
            "municipality_id": 1
        }
        mock_business_license_public.model_validate.return_value = mock_license_model

        from app.routers.business_licenses import list_business_licenses_public

        result = await list_business_licenses_public(
            page=1,
            per_page=10,
            search="",
            municipality_id=None,
            db=mock_db
        )

        # Verify the result structure
        assert result["total"] == 1
        assert result["total_pages"] == 1
        assert result["page"] == 1
        assert result["per_page"] == 10
        assert len(result["items"]) == 1
        assert result["items"][0]["license_folio"] == "BL-2024-001"
        assert result["items"][0]["municipality_name"] == "Test Municipality"

    @pytest.mark.asyncio
    @patch('app.routers.business_licenses.BusinessLicensePublic')
    @patch('app.routers.business_licenses.get_db')
    async def test_list_business_licenses_public_with_search(self, mock_get_db, mock_business_license_public):
        """Test listing business licenses with search filter"""
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        # Mock count query result
        mock_count_result = MagicMock()
        mock_count_result.scalar.return_value = 1
        
        # Mock main query result
        mock_result = MagicMock()
        mock_result.all.return_value = [(self.mock_license, "Test Municipality")]
        
        mock_db.execute = AsyncMock(side_effect=[mock_count_result, mock_result])

        # Mock the Pydantic model
        mock_license_model = MagicMock()
        mock_license_model.model_dump.return_value = {
            "license_folio": "BL-2024-001",
            "commercial_activity": "Restaurant",
            "industry_classification_code": "722001",
            "license_status": "active",
            "license_type": "Commercial",
            "municipality_id": 1
        }
        mock_business_license_public.model_validate.return_value = mock_license_model
        
        from app.routers.business_licenses import list_business_licenses_public
        
        result = await list_business_licenses_public(
            page=1,
            per_page=10,
            search="Restaurant",
            municipality_id=None,
            db=mock_db
        )

        # Verify calls were made correctly
        assert mock_db.execute.call_count == 2
        assert result["total"] == 1

    @pytest.mark.asyncio
    @patch('app.routers.business_licenses.generate_unsigned_receipt_pdf')
    async def test_get_unsigned_receipt_success(self, mock_generate_pdf):
        """Test successful unsigned receipt generation"""
        # Mock the service function response
        mock_generate_pdf.return_value = b"PDF content"
        
        from app.routers.business_licenses import get_unsigned_receipt
        
        mock_db = AsyncMock()
        folio = "LIC-001"
        encoded_folio = encode_folio_to_base64(folio)
        
        result = await get_unsigned_receipt(
            encoded_folio=encoded_folio,
            db=mock_db
        )

        # Verify service was called
        mock_generate_pdf.assert_called_once_with(folio, mock_db)

    @pytest.mark.asyncio
    @patch('app.routers.business_licenses.generate_unsigned_receipt_pdf')
    async def test_get_unsigned_receipt_error(self, mock_generate_pdf):
        """Test unsigned receipt generation with error"""
        # Mock the service to raise an exception
        mock_generate_pdf.side_effect = Exception("PDF generation failed")
        
        from app.routers.business_licenses import get_unsigned_receipt
        
        mock_db = AsyncMock()
        folio = "LIC-001"
        encoded_folio = encode_folio_to_base64(folio)
        
        with pytest.raises(HTTPException) as exc_info:
            await get_unsigned_receipt(
                encoded_folio=encoded_folio,
                db=mock_db
            )
        
        assert exc_info.value.status_code == 500
        assert "PDF generation failed" in str(exc_info.value.detail)

    @patch('app.routers.business_licenses.get_sync_db')
    @patch('app.routers.business_licenses.pd.DataFrame.to_excel')
    def test_export_business_licenses_success(self, mock_to_excel, mock_get_sync_db):
        """Test successful export of business licenses"""
        from app.routers.business_licenses import export_business_licenses
        
        # Setup mock database
        mock_db = MagicMock()
        mock_get_sync_db.return_value = mock_db
        
        # Setup mock query result
        mock_db.query.return_value.filter.return_value.all.return_value = [self.mock_license]
        
        # Mock to_excel to avoid actual file writing
        def mock_excel_write(stream, *args, **kwargs):
            stream.write(b"fake excel content")
        
        mock_to_excel.side_effect = mock_excel_write
        
        # Call the function
        response = export_business_licenses(
            municipality_id=1,
            db=mock_db
        )
        
        # Verify response
        assert response.media_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        assert "attachment" in response.headers["Content-Disposition"]
        assert "business_licenses_" in response.headers["Content-Disposition"]

    @patch('app.routers.business_licenses.get_sync_db')  
    def test_export_business_licenses_empty(self, mock_get_sync_db):
        """Test export with no results"""
        from app.routers.business_licenses import export_business_licenses
        
        # Setup mock database
        mock_db = MagicMock()
        mock_get_sync_db.return_value = mock_db
        
        # Setup mock query to return empty list
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        # Call the function
        response = export_business_licenses(
            municipality_id=1,
            db=mock_db
        )
        
        # Verify response
        assert response.media_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
