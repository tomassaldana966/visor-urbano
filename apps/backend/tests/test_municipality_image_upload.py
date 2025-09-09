import pytest
import os
from unittest.mock import Mock, AsyncMock, patch, mock_open
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.municipality import upload_municipality_image, validate_image_upload
from app.models.municipality import Municipality
from app.models.user import UserModel


class TestMunicipalityImageUpload:
    """Test cases for municipality image upload endpoint"""

    @pytest.fixture
    def mock_municipality(self):
        municipality = Mock(spec=Municipality)
        municipality.id = 1
        municipality.name = "Test Municipality"
        municipality.director = "Test Director"
        municipality.address = "Test Address"
        municipality.phone = "123-456-7890"
        municipality.email = "test@municipality.gov"
        municipality.website = "https://municipality.gov"
        municipality.responsible_area = "Test Area"
        municipality.solving_days = 30
        municipality.initial_folio = 1000
        municipality.low_impact_license_cost = "50.00"
        municipality.license_additional_text = "Additional text"
        municipality.allow_online_procedures = True
        municipality.allow_window_reviewer_licenses = True
        municipality.theme_color = "#FF0000"
        municipality.image = None
        municipality.signatures = []  # Mock signatures as empty list, not Mock object
        municipality.created_at = "2023-01-01T00:00:00Z"
        municipality.updated_at = "2023-01-01T00:00:00Z"
        return municipality

    @pytest.fixture
    def mock_user_with_municipality(self):
        user = Mock(spec=UserModel)
        user.id = 1
        user.email = "test@example.com"
        user.municipality_id = 1
        return user

    @pytest.fixture
    def mock_user_without_municipality(self):
        user = Mock(spec=UserModel)
        user.id = 2
        user.email = "test2@example.com"
        user.municipality_id = None
        return user

    @pytest.fixture
    def mock_valid_image_file(self):
        """Create a mock valid image file"""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test_image.jpg"
        mock_file.size = 1024 * 1024  # 1MB
        
        # Track read calls to simulate proper file behavior
        self.read_count = 0
        
        async def mock_read(size=8192):
            self.read_count += 1
            # First few reads return data, then empty to simulate end of file
            if self.read_count <= 2:
                return b"x" * min(size, 1024 * 512)  # Return up to 512KB chunks
            else:
                return b""  # End of file
        
        mock_file.read = mock_read
        mock_file.seek = AsyncMock()
        return mock_file

    @pytest.fixture
    def mock_invalid_image_file(self):
        """Create a mock invalid image file"""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test_document.pdf"
        mock_file.size = 1024 * 1024
        mock_file.read = AsyncMock(return_value=b"")
        mock_file.seek = AsyncMock()
        return mock_file

    @pytest.fixture
    def mock_large_image_file(self):
        """Create a mock image file that's too large"""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "large_image.jpg"
        mock_file.size = 10 * 1024 * 1024  # 10MB (exceeds 5MB limit)
        
        # Track read calls to simulate large file
        self.large_read_count = 0
        
        async def mock_large_read(size=8192):
            self.large_read_count += 1
            # Return 1MB chunks until we exceed the limit
            if self.large_read_count <= 8:  # Will exceed 5MB limit
                return b"x" * min(size, 1024 * 1024)  # 1MB chunks
            else:
                return b""  # End of file
        
        mock_file.read = mock_large_read
        mock_file.seek = AsyncMock()
        return mock_file

    @pytest.mark.asyncio
    async def test_validate_image_upload_valid_file(self, mock_valid_image_file):
        """Test that valid image files pass validation"""
        # Should not raise any exception
        await validate_image_upload(mock_valid_image_file)

    @pytest.mark.asyncio
    async def test_validate_image_upload_invalid_extension(self, mock_invalid_image_file):
        """Test that invalid file extensions are rejected"""
        with pytest.raises(HTTPException) as exc_info:
            await validate_image_upload(mock_invalid_image_file)
        assert exc_info.value.status_code == 400
        assert "Invalid image format" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_validate_image_upload_no_filename(self):
        """Test that files without filename are rejected"""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = None
        
        with pytest.raises(HTTPException) as exc_info:
            await validate_image_upload(mock_file)
        assert exc_info.value.status_code == 400
        assert "No filename provided" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_validate_image_upload_file_too_large(self, mock_large_image_file):
        """Test that files exceeding size limit are rejected"""
        with pytest.raises(HTTPException) as exc_info:
            await validate_image_upload(mock_large_image_file)
        assert exc_info.value.status_code == 413
        assert "Image too large" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_upload_municipality_image_success(
        self, 
        mock_municipality, 
        mock_user_with_municipality, 
        mock_valid_image_file
    ):
        """Test successful municipality image upload"""
        # Mock database session
        mock_db = AsyncMock(spec=AsyncSession)
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_municipality
        mock_db.execute.return_value = mock_result
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        # Mock file operations
        with patch('os.makedirs'), \
             patch('builtins.open', mock_open()), \
             patch('os.path.exists', return_value=False):
            
            result = await upload_municipality_image(
                municipality_id=1,
                image=mock_valid_image_file,
                current_user=mock_user_with_municipality,
                db=mock_db
            )

        # Assertions
        assert isinstance(result, dict)
        assert result['id'] == mock_municipality.id
        assert result['name'] == mock_municipality.name
        assert result['email'] == mock_municipality.email
        mock_db.commit.assert_called_once()
        # Note: refresh is not called in the current implementation, only commit

    @pytest.mark.asyncio
    async def test_upload_municipality_image_municipality_not_found(
        self, 
        mock_user_with_municipality, 
        mock_valid_image_file
    ):
        """Test upload when municipality doesn't exist"""
        # Mock database session returning no municipality
        mock_db = AsyncMock(spec=AsyncSession)
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result

        with pytest.raises(HTTPException) as exc_info:
            await upload_municipality_image(
                municipality_id=999,
                image=mock_valid_image_file,
                current_user=mock_user_with_municipality,
                db=mock_db
            )

        assert exc_info.value.status_code == 404
        assert "Municipality not found" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_upload_municipality_image_user_no_municipality(
        self, 
        mock_municipality, 
        mock_user_without_municipality, 
        mock_valid_image_file
    ):
        """Test upload when user has no municipality assigned"""
        # Mock database session
        mock_db = AsyncMock(spec=AsyncSession)
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = mock_municipality
        mock_db.execute.return_value = mock_result

        with pytest.raises(HTTPException) as exc_info:
            await upload_municipality_image(
                municipality_id=1,
                image=mock_valid_image_file,
                current_user=mock_user_without_municipality,
                db=mock_db
            )

        assert exc_info.value.status_code == 404
        assert "User has no municipality assigned" in exc_info.value.detail
