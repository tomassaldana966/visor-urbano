import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from app.services.data.business_license_data import (
    get_unsigned_receipt_data_async,
    get_responsible_letter_data
)


class TestBusinessLicenseData:
    """Test suite for business license data service functions"""

    @pytest.mark.asyncio
    async def test_get_unsigned_receipt_data_async_success(self):
        """Test successful retrieval of unsigned receipt data"""
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock RequirementsQuery data
        mock_rq = MagicMock()
        mock_rq.folio = "FOL-001"
        mock_rq.street = "Calle Principal"
        mock_rq.neighborhood = "Centro"
        mock_rq.municipality_name = "Test Municipality"
        mock_rq.scian_code = "123456"
        mock_rq.scian_name = "Commercial Activity"
        mock_rq.applicant_name = "Juan Pérez"
        mock_rq.applicant_character = "Owner"
        mock_rq.person_type = "Natural"
        mock_rq.property_area = 100.5
        mock_rq.activity_area = 50.0
        mock_rq.alcohol_sales = 1
        mock_rq.created_at = datetime(2024, 1, 15, 10, 30, 0)
        
        # Mock the database execution chain
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = mock_rq
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Call the function
        result = await get_unsigned_receipt_data_async("FOL-001", mock_db)
        
        # Assertions
        assert result is not None
        assert result["folio"] == "FOL-001"
        assert result["street"] == "Calle Principal"
        assert result["neighborhood"] == "Centro"
        assert result["municipality_name"] == "Test Municipality"
        assert result["scian_code"] == "123456"
        assert result["scian_name"] == "Commercial Activity"
        assert result["applicant_name"] == "Juan Pérez"
        assert result["applicant_character"] == "Owner"
        assert result["person_type"] == "Natural"
        assert result["property_area"] == 100.5
        assert result["activity_area"] == 50.0
        assert result["alcohol_sales"] is True  # bool(1) = True
        assert result["created_at"] == "2024-01-15T10:30:00"

    @pytest.mark.asyncio
    async def test_get_unsigned_receipt_data_async_not_found(self):
        """Test retrieval of unsigned receipt data when folio not found"""
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock the database execution chain returning None
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = None
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Call the function
        result = await get_unsigned_receipt_data_async("NONEXISTENT", mock_db)
        
        # Assertions
        assert result is None

    @pytest.mark.asyncio
    async def test_get_unsigned_receipt_data_async_with_nulls(self):
        """Test unsigned receipt data with null/None values"""
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock RequirementsQuery data with some None values
        mock_rq = MagicMock()
        mock_rq.folio = "FOL-002"
        mock_rq.street = "Avenida Central"
        mock_rq.neighborhood = "Norte"
        mock_rq.municipality_name = "Test Municipality"
        mock_rq.scian_code = "654321"
        mock_rq.scian_name = "Another Activity"
        mock_rq.applicant_name = None  # None value
        mock_rq.applicant_character = None  # None value
        mock_rq.person_type = None  # None value
        mock_rq.property_area = 200.0
        mock_rq.activity_area = 75.0
        mock_rq.alcohol_sales = 0  # False
        mock_rq.created_at = None  # None value
        
        # Mock the database execution chain
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = mock_rq
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Call the function
        result = await get_unsigned_receipt_data_async("FOL-002", mock_db)
        
        # Assertions
        assert result is not None
        assert result["folio"] == "FOL-002"
        assert result["applicant_name"] == "N/A"  # Default for None
        assert result["applicant_character"] == "N/A"  # Default for None
        assert result["person_type"] == "N/A"  # Default for None
        assert result["alcohol_sales"] is False  # bool(0) = False
        assert result["created_at"] is None  # None stays None

    @pytest.mark.asyncio
    @patch('app.services.data.business_license_data.select')
    @patch('app.services.data.business_license_data.joinedload')
    async def test_get_responsible_letter_data_mocked(self, mock_joinedload, mock_select):
        """Test responsible letter data using mocked dependencies"""
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock municipality data
        mock_municipality = MagicMock()
        mock_municipality.name = "Test Municipality"
        mock_municipality.address = "Municipal Address"
        mock_municipality.image = "https://example.com/municipal_logo.png"
        
        # Mock license data
        mock_license = MagicMock()
        mock_license.license_folio = "LIC-001"
        mock_license.owner = "María"
        mock_license.owner_last_name_p = "García"
        mock_license.owner_last_name_m = "López"
        mock_license.national_id = "12345678901"
        mock_license.commercial_activity = "Restaurant Services"
        mock_license.logo_image = "https://example.com/business_logo.png"
        mock_license.municipality = mock_municipality
        
        # Mock the database execution chain
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = mock_license
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Mock datetime.now() to have consistent output
        with patch('app.services.data.business_license_data.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "15/01/2024"
            
            # Call the function
            result = await get_responsible_letter_data(mock_db, "LIC-001")
        
        # Assertions
        assert result is not None
        assert result["government_logo"] == "https://example.com/municipal_logo.png"
        assert result["logo_url"] == "https://example.com/business_logo.png"
        assert result["municipality"] == "Test Municipality"
        assert result["date"] == "15/01/2024"
        assert result["applicant"]["name"] == "María García López"
        assert result["applicant"]["id_type"] == "National ID"
        assert result["applicant"]["id_number"] == "12345678901"
        assert result["applicant"]["id_issuer"] == ""
        assert result["scian_name"] == "Restaurant Services"
        assert result["address"]["neighborhood"] == "Municipal Address"
        assert result["address"]["cp"] == ""

    @pytest.mark.asyncio
    @patch('app.services.data.business_license_data.select')
    @patch('app.services.data.business_license_data.joinedload')
    async def test_get_responsible_letter_data_not_found_mocked(self, mock_joinedload, mock_select):
        """Test responsible letter data when license not found"""
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock the database execution chain returning None
        mock_scalars = MagicMock()
        mock_scalars.first.return_value = None
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Call the function
        result = await get_responsible_letter_data(mock_db, "NONEXISTENT")
        
        # Assertions
        assert result is None
