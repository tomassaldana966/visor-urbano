import pytest
import asyncio
import tempfile
import os
from unittest.mock import Mock, patch, AsyncMock
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from io import BytesIO

from app.models.business_signatures import BusinessSignature
from app.models.user import UserModel
from app.routers.business_signatures import (
    validate_curp,
    validate_file_extension,
    validate_file_content,
    validate_file_size,
    secure_filename,
    create_secure_temp_dir,
    cleanup_files,
    run_openssl_command,
    handle_electronic_signature
)
from tests.models_for_testing import UserTestModel, ModelBase


class BusinessSignatureTestModel:
    """Test model for BusinessSignature"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 1)
        self.procedure_id = kwargs.get('procedure_id', 1)
        self.user_id = kwargs.get('user_id', 1)
        self.role = kwargs.get('role', 1)
        self.hash_to_sign = kwargs.get('hash_to_sign', 'test_hash_to_sign')
        self.signed_hash = kwargs.get('signed_hash', 'test_signed_hash')
        self.response = kwargs.get('response', {
            "signed_hash": "test_signed_hash",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "curp": "ABCD123456HDFRRL09",
            "procedure_id": 1
        })
        self.deleted_at = kwargs.get('deleted_at', None)
        self.created_at = kwargs.get('created_at', datetime.now(timezone.utc))
        self.updated_at = kwargs.get('updated_at', datetime.now(timezone.utc))


class TestBusinessSignatureValidation:
    """Test validation functions"""
    
    def test_validate_curp_valid(self):
        """Test CURP validation with valid CURPs"""
        valid_curps = [
            "ABCD123456HDFRRL09",
            "XYZW654321MDFGGR08",
            "JUAN850315HDFRNT02"
        ]
        
        for curp in valid_curps:
            assert validate_curp(curp), f"Valid CURP {curp} should pass validation"
    
    def test_validate_curp_invalid(self):
        """Test CURP validation with invalid CURPs"""
        invalid_curps = [
            "",
            "ABCD123456HDFRRL0",  # Too short
            "ABCD123456HDFRRL099",  # Too long
            "abcd123456hdfrrl09",  # Lowercase
            "ABCD123456XDFRRL09",  # Invalid gender
            "123456789012345678",  # All numbers
            None,
            "ABCD-23456HDFRRL09",  # Invalid character
        ]
        
        for curp in invalid_curps:
            assert not validate_curp(curp), f"Invalid CURP {curp} should fail validation"
    
    def test_validate_file_extension_valid(self):
        """Test file extension validation with valid extensions"""
        valid_files = [
            ("certificate.cer", {'.cer', '.key'}),
            ("private.key", {'.cer', '.key'}),
            ("test.CER", {'.cer', '.key'}),  # Case insensitive
        ]
        
        for filename, allowed in valid_files:
            assert validate_file_extension(filename, allowed), f"Valid file {filename} should pass"
    
    def test_validate_file_extension_invalid(self):
        """Test file extension validation with invalid extensions"""
        invalid_files = [
            ("file.txt", {'.cer', '.key'}),
            ("file.pdf", {'.cer', '.key'}),
            ("", {'.cer', '.key'}),
            (None, {'.cer', '.key'}),
            ("file", {'.cer', '.key'}),  # No extension
        ]
        
        for filename, allowed in invalid_files:
            assert not validate_file_extension(filename, allowed), f"Invalid file {filename} should fail"
    
    def test_validate_file_content_cer(self):
        """Test certificate file content validation"""
        # Valid DER certificate start
        valid_cer = b'\x30\x82\x05\x94\x30\x82'
        assert validate_file_content(valid_cer, '.cer')
        
        # Invalid content
        invalid_cer = b'invalid certificate content'
        assert not validate_file_content(invalid_cer, '.cer')
    
    def test_validate_file_content_key(self):
        """Test private key file content validation"""
        # Valid PKCS#8 key start
        valid_key = b'\x30\x82\x02\x5d\x02\x01'
        assert validate_file_content(valid_key, '.key')
        
        # Valid PEM key
        valid_pem_key = b'-----BEGIN PRIVATE KEY-----\nMIIEvg'
        assert validate_file_content(valid_pem_key, '.key')
        
        # Invalid content
        invalid_key = b'invalid key content'
        assert not validate_file_content(invalid_key, '.key')
    
    def test_validate_file_size(self):
        """Test file size validation"""
        # Small file that should pass
        small_file = Mock()
        small_file.file = Mock()
        small_file.file.seek = Mock()
        small_file.file.read = Mock(side_effect=[b'a' * 1024, b''])  # 1KB file
        assert validate_file_size(small_file, 2048)
        
        # Large file that should fail
        large_file = Mock()
        large_file.file = Mock()
        large_file.file.seek = Mock()
        # Simulate reading chunks that exceed max_size
        chunk_data = [b'a' * 8192] * 10  # 10 chunks of 8KB each = ~80KB
        chunk_data.append(b'')  # End marker
        large_file.file.read = Mock(side_effect=chunk_data)
        assert not validate_file_size(large_file, 2048)  # 2KB limit
        
        # File that causes read error
        error_file = Mock()
        error_file.file = Mock()
        error_file.file.seek = Mock(side_effect=Exception("Read error"))
        assert not validate_file_size(error_file, 2048)  # Should return False on error
    
    def test_secure_filename(self):
        """Test secure filename generation"""
        test_cases = [
            ("certificate.cer", "certificate.cer"),
            ("../../../etc/passwd", "passwd"),
            ("file with spaces.key", "filewithspaces.key"),
            ("file@#$%^&*().cer", "file.cer"),
            ("", "unknown"),
            (None, "unknown"),
            ("a" * 200 + ".cer", "a" * 96 + ".cer"),  # Length limit
        ]
        
        for input_name, expected in test_cases:
            result = secure_filename(input_name)
            assert result == expected, f"secure_filename({input_name}) should return {expected}, got {result}"


class TestBusinessSignatureUtilities:
    """Test utility functions"""
    
    def test_create_secure_temp_dir(self):
        """Test secure temporary directory creation"""
        temp_dir = create_secure_temp_dir()
        
        try:
            assert os.path.exists(temp_dir)
            assert os.path.isdir(temp_dir)
            assert "business_sig_" in os.path.basename(temp_dir)
            
            # Check permissions (on Unix systems)
            if hasattr(os, 'stat'):
                stat_info = os.stat(temp_dir)
                # Should be 0o700 (owner read/write/execute only)
                assert (stat_info.st_mode & 0o777) == 0o700
        finally:
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
    
    @pytest.mark.asyncio
    async def test_cleanup_files(self):
        """Test file cleanup functionality"""
        # Create temporary files
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "test_file.txt")
        
        with open(temp_file, "w") as f:
            f.write("test content")
        
        assert os.path.exists(temp_file)
        assert os.path.exists(temp_dir)
        
        # Cleanup
        await cleanup_files(temp_file, temp_dir)
        
        assert not os.path.exists(temp_file)
        assert not os.path.exists(temp_dir)
    
    @pytest.mark.asyncio
    async def test_cleanup_files_nonexistent(self):
        """Test cleanup with non-existent files"""
        # Should not raise exception
        await cleanup_files("/nonexistent/file.txt", "/nonexistent/dir")
    
    @patch('subprocess.run')
    def test_run_openssl_command_success(self, mock_run):
        """Test successful OpenSSL command execution"""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "success output"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = run_openssl_command(["openssl", "version"])
        
        assert result.returncode == 0
        assert result.stdout == "success output"
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_run_openssl_command_failure(self, mock_run):
        """Test failed OpenSSL command execution"""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "error message"
        mock_run.return_value = mock_result
        
        result = run_openssl_command(["openssl", "invalid"])
        
        assert result.returncode == 1
    
    def test_run_openssl_command_invalid_command(self):
        """Test OpenSSL command with invalid format"""
        with pytest.raises(ValueError, match="Invalid command format"):
            run_openssl_command("invalid command")
        
        with pytest.raises(ValueError, match="Only OpenSSL commands are allowed"):
            run_openssl_command(["malicious", "command"])
    
    @patch('subprocess.run')
    def test_run_openssl_command_timeout(self, mock_run):
        """Test OpenSSL command timeout"""
        from subprocess import TimeoutExpired
        from fastapi import HTTPException
        
        mock_run.side_effect = TimeoutExpired("openssl", 30)
        
        with pytest.raises(HTTPException) as exc_info:
            run_openssl_command(["openssl", "version"])
        
        assert exc_info.value.status_code == 408


class TestBusinessSignatureEndpoint:
    """Test the main electronic signature endpoint"""
    
    def create_mock_upload_file(self, filename: str, content: bytes, content_type: str = "application/octet-stream"):
        """Create a mock UploadFile for testing"""
        file_obj = BytesIO(content)
        upload_file = UploadFile(
            filename=filename,
            file=file_obj,
            size=len(content),
            headers={"content-type": content_type}
        )
        return upload_file
    
    @pytest.mark.asyncio
    @patch('app.routers.business_signatures.run_openssl_command')
    @patch('app.routers.business_signatures.create_secure_temp_dir')
    @patch('app.routers.business_signatures.cleanup_files')
    async def test_handle_electronic_signature_success(self, mock_cleanup, mock_temp_dir, mock_openssl):
        """Test successful electronic signature creation"""
        # Setup mocks
        mock_temp_dir.return_value = "/tmp/test_dir"
        mock_cleanup.return_value = None
        
        # Mock successful OpenSSL commands
        mock_openssl_results = [
            Mock(returncode=0, stdout="", stderr=""),  # Certificate conversion
            Mock(returncode=0, stdout="", stderr=""),  # Key conversion
            Mock(returncode=0, stdout="hash_output", stderr=""),  # Hash creation
            Mock(returncode=0, stdout="encoded_signature", stderr=""),  # Base64 encoding
        ]
        mock_openssl.side_effect = mock_openssl_results
        
        # Create mock files
        cer_content = b'\x30\x82\x05\x94\x30\x82'  # Valid DER certificate start
        key_content = b'\x30\x82\x02\x5d\x02\x01'  # Valid PKCS#8 key start
        
        file_cer = self.create_mock_upload_file("test.cer", cer_content)
        file_key = self.create_mock_upload_file("test.key", key_content)
        
        # Mock database and user
        mock_db = AsyncMock()
        # Configure async database methods
        mock_db.add = Mock()  # add is synchronous
        mock_db.commit = AsyncMock()  # commit is async
        mock_db.refresh = AsyncMock()  # refresh is async
        
        mock_user = UserTestModel(id=1)
        mock_user.user_roles = Mock()
        mock_user.user_roles.id = 1
        
        # Mock file operations
        with patch('builtins.open', create=True) as mock_open, \
             patch('os.chmod') as mock_chmod, \
             patch('os.path.join', side_effect=lambda *args: '/'.join(args)):
            
            result = await handle_electronic_signature(
                password="test_password_123",
                chain="test_chain_data",
                curp="ABCD123456HDFRRL09",
                procedure_id=1,
                procedure_part="part1",
                file_cer=file_cer,
                file_key=file_key,
                db=mock_db,
                current_user=mock_user
            )
            
            # Verify database operations
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()
            
            # Verify cleanup was called
            mock_cleanup.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_handle_electronic_signature_invalid_curp(self):
        """Test electronic signature with invalid CURP"""
        from fastapi import HTTPException
        
        file_cer = self.create_mock_upload_file("test.cer", b'\x30\x82\x05\x94')
        file_key = self.create_mock_upload_file("test.key", b'\x30\x82\x02\x5d')
        
        mock_db = AsyncMock()
        mock_user = UserTestModel(id=1)
        
        with pytest.raises(HTTPException) as exc_info:
            await handle_electronic_signature(
                password="test_password_123",
                chain="test_chain",
                curp="INVALID_CURP",
                procedure_id=1,
                procedure_part="part1",
                file_cer=file_cer,
                file_key=file_key,
                db=mock_db,
                current_user=mock_user
            )
        
        assert exc_info.value.status_code == 400
        assert "Invalid CURP format" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_handle_electronic_signature_invalid_file_extension(self):
        """Test electronic signature with invalid file extensions"""
        from fastapi import HTTPException
        
        file_cer = self.create_mock_upload_file("test.txt", b'\x30\x82\x05\x94')  # Wrong extension
        file_key = self.create_mock_upload_file("test.key", b'\x30\x82\x02\x5d')
        
        mock_db = AsyncMock()
        mock_user = UserTestModel(id=1)
        
        with pytest.raises(HTTPException) as exc_info:
            await handle_electronic_signature(
                password="test_password_123",
                chain="test_chain",
                curp="ABCD123456HDFRRL09",
                procedure_id=1,
                procedure_part="part1",
                file_cer=file_cer,
                file_key=file_key,
                db=mock_db,
                current_user=mock_user
            )
        
        assert exc_info.value.status_code == 400
        assert "Certificate file must have .cer extension" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    async def test_handle_electronic_signature_invalid_file_content(self):
        """Test electronic signature with invalid file content"""
        from fastapi import HTTPException
        
        file_cer = self.create_mock_upload_file("test.cer", b'invalid content')
        file_key = self.create_mock_upload_file("test.key", b'\x30\x82\x02\x5d')
        
        mock_db = AsyncMock()
        mock_user = UserTestModel(id=1)
        mock_user.user_roles = Mock()
        mock_user.user_roles.id = 1
        
        with pytest.raises(HTTPException) as exc_info:
            await handle_electronic_signature(
                password="test_password_123",
                chain="test_chain",
                curp="ABCD123456HDFRRL09",
                procedure_id=1,
                procedure_part="part1",
                file_cer=file_cer,
                file_key=file_key,
                db=mock_db,
                current_user=mock_user
            )
        
        assert exc_info.value.status_code == 400
        assert "Invalid certificate file format" in str(exc_info.value.detail)
    
    @pytest.mark.asyncio
    @patch('app.routers.business_signatures.run_openssl_command')
    @patch('app.routers.business_signatures.create_secure_temp_dir')
    @patch('app.routers.business_signatures.cleanup_files')
    async def test_handle_electronic_signature_wrong_password(self, mock_cleanup, mock_temp_dir, mock_openssl):
        """Test electronic signature with wrong private key password"""
        from fastapi import HTTPException
        
        mock_temp_dir.return_value = "/tmp/test_dir"
        mock_cleanup.return_value = None
        
        # Mock OpenSSL commands - certificate conversion succeeds, key conversion fails
        mock_openssl_results = [
            Mock(returncode=0, stdout="", stderr=""),  # Certificate conversion succeeds
            Mock(returncode=1, stdout="", stderr="wrong password"),  # Key conversion fails
        ]
        mock_openssl.side_effect = mock_openssl_results
        
        cer_content = b'\x30\x82\x05\x94\x30\x82'
        key_content = b'\x30\x82\x02\x5d\x02\x01'
        
        file_cer = self.create_mock_upload_file("test.cer", cer_content)
        file_key = self.create_mock_upload_file("test.key", key_content)
        
        mock_db = AsyncMock()
        mock_user = UserTestModel(id=1)
        mock_user.user_roles = Mock()
        mock_user.user_roles.id = 1
        
        with patch('builtins.open', create=True), \
             patch('os.chmod'), \
             patch('os.path.join', side_effect=lambda *args: '/'.join(args)):
            
            with pytest.raises(HTTPException) as exc_info:
                await handle_electronic_signature(
                    password="wrong_password",
                    chain="test_chain",
                    curp="ABCD123456HDFRRL09",
                    procedure_id=1,
                    procedure_part="part1",
                    file_cer=file_cer,
                    file_key=file_key,
                    db=mock_db,
                    current_user=mock_user
                )
            
            assert exc_info.value.status_code == 401
            assert "Invalid private key password" in str(exc_info.value.detail)
            
            # Verify cleanup was called even on failure
            mock_cleanup.assert_called_once()


class TestBusinessSignatureModel:
    """Test BusinessSignature model functionality"""
    
    def test_business_signature_creation(self):
        """Test BusinessSignature model creation"""
        signature = BusinessSignatureTestModel(
            procedure_id=1,
            user_id=1,
            role=1,
            hash_to_sign="test_hash",
            signed_hash="test_signature"
        )
        
        assert signature.procedure_id == 1
        assert signature.user_id == 1
        assert signature.role == 1
        assert signature.hash_to_sign == "test_hash"
        assert signature.signed_hash == "test_signature"
        assert signature.deleted_at is None
        assert signature.created_at is not None
        assert signature.updated_at is not None
    
    def test_business_signature_response_data(self):
        """Test BusinessSignature response data structure"""
        response_data = {
            "signed_hash": "test_signature",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "curp": "ABCD123456HDFRRL09",
            "procedure_id": 1,
            "procedure_part": "part1"
        }
        
        signature = BusinessSignatureTestModel(
            procedure_id=1,
            user_id=1,
            role=1,
            response=response_data
        )
        
        assert signature.response["signed_hash"] == "test_signature"
        assert signature.response["curp"] == "ABCD123456HDFRRL09"
        assert signature.response["procedure_id"] == 1
        assert "generated_at" in signature.response


if __name__ == "__main__":
    pytest.main([__file__])
