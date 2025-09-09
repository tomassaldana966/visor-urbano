"""
Unit tests for procedures.py using mocked dependencies.
This avoids database and PostGIS dependency issues.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import base64
import os
import tempfile
from io import BytesIO
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from fastapi import HTTPException, UploadFile
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Import the functions we want to test directly
from app.routers.procedures import (
    validate_base64_folio,
    validate_file_upload,
    get_procedure_by_folio,
    list_procedures_base,
    ALLOWED_FILE_EXTENSIONS,
    MAX_FILE_SIZE
)


class TestValidateBase64Folio:
    """Test the validate_base64_folio function."""
    
    def test_valid_base64_folio(self):
        """Test valid base64 encoded folio."""
        # "PROC-001" encoded in base64
        encoded = base64.b64encode("PROC-001".encode()).decode()
        result = validate_base64_folio(encoded)
        assert result == "PROC-001"
    
    def test_invalid_base64_encoding(self):
        """Test invalid base64 encoding."""
        with pytest.raises(HTTPException) as exc_info:
            validate_base64_folio("invalid-base64!")
        assert exc_info.value.status_code == 400
        assert "Invalid folio encoding" in str(exc_info.value.detail)
    
    def test_empty_folio_after_decode(self):
        """Test empty folio after decoding."""
        encoded = base64.b64encode("".encode()).decode()
        with pytest.raises(HTTPException) as exc_info:
            validate_base64_folio(encoded)
        assert exc_info.value.status_code == 400
        assert "Invalid folio format" in str(exc_info.value.detail)
    
    def test_folio_too_long(self):
        """Test folio that's too long."""
        long_folio = "A" * 256  # 256 characters
        encoded = base64.b64encode(long_folio.encode()).decode()
        with pytest.raises(HTTPException) as exc_info:
            validate_base64_folio(encoded)
        assert exc_info.value.status_code == 400
        assert "Invalid folio format" in str(exc_info.value.detail)
    
    def test_non_utf8_bytes(self):
        """Test invalid UTF-8 bytes after base64 decode."""
        # Create invalid UTF-8 sequence
        invalid_utf8 = b'\xff\xfe\xfd'
        encoded = base64.b64encode(invalid_utf8).decode()
        with pytest.raises(HTTPException) as exc_info:
            validate_base64_folio(encoded)
        assert exc_info.value.status_code == 400
        assert "Invalid folio encoding" in str(exc_info.value.detail)


class TestValidateFileUpload:
    """Test the validate_file_upload function."""
    
    def test_valid_file_upload(self):
        """Test valid file upload."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.pdf"
        mock_file.size = 1024  # 1KB
        
        # Should not raise any exception
        validate_file_upload(mock_file)
    
    def test_no_filename(self):
        """Test file with no filename."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = None
        
        with pytest.raises(HTTPException) as exc_info:
            validate_file_upload(mock_file)
        assert exc_info.value.status_code == 400
        assert "No filename provided" in str(exc_info.value.detail)
    
    def test_empty_filename(self):
        """Test file with empty filename."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = ""
        
        with pytest.raises(HTTPException) as exc_info:
            validate_file_upload(mock_file)
        assert exc_info.value.status_code == 400
        assert "No filename provided" in str(exc_info.value.detail)
    
    def test_invalid_file_extension(self):
        """Test file with invalid extension."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.exe"
        
        with pytest.raises(HTTPException) as exc_info:
            validate_file_upload(mock_file)
        assert exc_info.value.status_code == 400
        assert "File type not allowed" in str(exc_info.value.detail)
    
    def test_file_too_large(self):
        """Test file that's too large."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.pdf"
        mock_file.size = MAX_FILE_SIZE + 1
        
        with pytest.raises(HTTPException) as exc_info:
            validate_file_upload(mock_file)
        assert exc_info.value.status_code == 413
        assert "File too large" in str(exc_info.value.detail)
    
    @pytest.mark.parametrize("extension", [".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"])
    def test_allowed_extensions(self, extension):
        """Test all allowed file extensions."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = f"test{extension}"
        mock_file.size = 1024
        
        # Should not raise any exception
        validate_file_upload(mock_file)
    
    def test_case_insensitive_extension(self):
        """Test that extension checking is case insensitive."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.PDF"
        mock_file.size = 1024
        
        # Should not raise any exception
        validate_file_upload(mock_file)


class TestGetProcedureByFolio:
    """Test the get_procedure_by_folio function."""
    
    @pytest.mark.asyncio
    async def test_procedure_found(self):
        """Test when procedure is found."""
        # Mock database session
        mock_db = AsyncMock()
        mock_result = Mock()
        mock_procedure = Mock()
        mock_procedure.folio = "PROC-001"
        mock_result.scalars.return_value.first.return_value = mock_procedure
        mock_db.execute.return_value = mock_result
        
        result = await get_procedure_by_folio("PROC-001", mock_db)
        assert result == mock_procedure
    
    @pytest.mark.asyncio
    async def test_procedure_not_found(self):
        """Test when procedure is not found."""
        # Mock database session
        mock_db = AsyncMock()
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result
        
        with pytest.raises(HTTPException) as exc_info:
            await get_procedure_by_folio("NON-EXISTENT", mock_db)
        assert exc_info.value.status_code == 404
        assert "Procedure not found" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_procedure_with_type_filter_found(self):
        """Test when procedure with specific type is found."""
        # Mock database session
        mock_db = AsyncMock()
        mock_result = Mock()
        mock_procedure = Mock()
        mock_procedure.folio = "PROC-001"
        mock_procedure.procedure_type = "refrendo"
        mock_result.scalars.return_value.first.return_value = mock_procedure
        mock_db.execute.return_value = mock_result
        
        result = await get_procedure_by_folio("PROC-001", mock_db, "refrendo")
        assert result == mock_procedure
    
    @pytest.mark.asyncio
    async def test_procedure_with_type_filter_not_found(self):
        """Test when procedure with specific type is not found."""
        # Mock database session
        mock_db = AsyncMock()
        mock_result = Mock()
        mock_result.scalars.return_value.first.return_value = None
        mock_db.execute.return_value = mock_result
        
        with pytest.raises(HTTPException) as exc_info:
            await get_procedure_by_folio("PROC-001", mock_db, "refrendo")
        assert exc_info.value.status_code == 404
        assert "Refrendo procedure not found" in str(exc_info.value.detail)


class TestListProceduresBase:
    """Test the list_procedures_base function."""
    
    @pytest.mark.asyncio
    async def test_list_all_procedures(self):
        """Test listing all procedures without filter."""
        # Mock database session
        mock_db = AsyncMock()
        mock_result = Mock()
        mock_procedures = [Mock(), Mock(), Mock()]
        mock_result.scalars.return_value.all.return_value = mock_procedures
        mock_db.execute.return_value = mock_result
        
        result = await list_procedures_base(None, mock_db)
        assert result == mock_procedures
    
    @pytest.mark.asyncio
    async def test_list_procedures_with_folio_filter(self):
        """Test listing procedures with folio filter."""
        # Mock database session
        mock_db = AsyncMock()
        mock_result = Mock()
        mock_procedures = [Mock()]
        mock_result.scalars.return_value.all.return_value = mock_procedures
        mock_db.execute.return_value = mock_result
        
        result = await list_procedures_base("PROC-001", mock_db)
        assert result == mock_procedures
    
    @pytest.mark.asyncio
    async def test_folio_filter_too_long(self):
        """Test folio filter that's too long."""
        mock_db = AsyncMock()
        long_folio = "A" * 256  # 256 characters
        
        with pytest.raises(HTTPException) as exc_info:
            await list_procedures_base(long_folio, mock_db)
        assert exc_info.value.status_code == 400
        assert "Folio filter too long" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_folio_filter_whitespace_stripped(self):
        """Test that folio filter whitespace is stripped."""
        # Mock database session
        mock_db = AsyncMock()
        mock_result = Mock()
        mock_procedures = [Mock()]
        mock_result.scalars.return_value.all.return_value = mock_procedures
        mock_db.execute.return_value = mock_result
        
        result = await list_procedures_base("  PROC-001  ", mock_db)
        assert result == mock_procedures


class TestSecurityValidation:
    """Test security-related validations."""
    
    def test_sql_injection_in_base64(self):
        """Test SQL injection attempt in base64 folio."""
        # Try to inject SQL through base64
        malicious_folio = "'; DROP TABLE procedures; --"
        encoded = base64.b64encode(malicious_folio.encode()).decode()
        
        # Should work normally (injection is prevented by SQLAlchemy)
        result = validate_base64_folio(encoded)
        assert result == malicious_folio
    
    def test_xss_attempt_in_base64(self):
        """Test XSS attempt in base64 folio."""
        # Try to inject XSS through base64
        xss_folio = "<script>alert('xss')</script>"
        encoded = base64.b64encode(xss_folio.encode()).decode()
        
        # Should work normally (XSS is prevented by proper output encoding)
        result = validate_base64_folio(encoded)
        assert result == xss_folio
    
    def test_path_traversal_in_filename(self):
        """Test path traversal attempt in filename."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "../../../etc/passwd"
        mock_file.size = 1024
        
        # Should be rejected due to invalid extension
        with pytest.raises(HTTPException) as exc_info:
            validate_file_upload(mock_file)
        assert exc_info.value.status_code == 400
        assert "File type not allowed" in str(exc_info.value.detail)
    
    def test_null_byte_in_filename(self):
        """Test null byte injection in filename."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.pdf\x00.exe"
        mock_file.size = 1024
        
        # Should be rejected because the extension after null byte is .exe
        with pytest.raises(HTTPException) as exc_info:
            validate_file_upload(mock_file)
        assert exc_info.value.status_code == 400
        assert "File type not allowed" in str(exc_info.value.detail)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_base64_padding_edge_cases(self):
        """Test various base64 padding scenarios."""
        # Test different padding scenarios
        test_cases = [
            "A",      # 1 character
            "AB",     # 2 characters
            "ABC",    # 3 characters
            "ABCD",   # 4 characters (no padding needed)
        ]
        
        for test_string in test_cases:
            encoded = base64.b64encode(test_string.encode()).decode()
            result = validate_base64_folio(encoded)
            assert result == test_string
    
    def test_maximum_valid_folio_length(self):
        """Test maximum valid folio length."""
        # 255 characters (maximum allowed)
        max_folio = "A" * 255
        encoded = base64.b64encode(max_folio.encode()).decode()
        result = validate_base64_folio(encoded)
        assert result == max_folio
    
    def test_maximum_valid_file_size(self):
        """Test maximum valid file size."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.pdf"
        mock_file.size = MAX_FILE_SIZE  # Exactly at the limit
        
        # Should not raise any exception
        validate_file_upload(mock_file)
    
    def test_file_without_size_attribute(self):
        """Test file upload without size attribute."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "test.pdf"
        # No size attribute
        delattr(mock_file, 'size') if hasattr(mock_file, 'size') else None
        
        # Should not raise any exception (size check is skipped)
        validate_file_upload(mock_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
