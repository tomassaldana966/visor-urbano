import pytest
import base64
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image
from app.utils.qr import generate_qr_code


class TestQRUtils:
    """Test cases for QR code utility functions."""

    @patch('qrcode.QRCode')
    def test_generate_qr_code_success(self, mock_qr_code_class):
        """Test successful QR code generation."""
        # Mock the QR code instance
        mock_qr = MagicMock()
        mock_qr_code_class.return_value = mock_qr
        
        # Mock the image
        mock_image = MagicMock()
        mock_qr.make_image.return_value = mock_image
        
        # Mock the BytesIO buffer
        with patch('app.utils.qr.BytesIO') as mock_bytesio, \
             patch('app.utils.qr.base64.b64encode') as mock_b64encode:
            
            mock_buffer = MagicMock()
            mock_bytesio.return_value = mock_buffer
            mock_buffer.getvalue.return_value = b'fake_image_data'
            mock_b64encode.return_value = b'ZmFrZV9pbWFnZV9kYXRh'  # base64 encoded 'fake_image_data'
            
            result = generate_qr_code("test_data")
            
            # Verify QR code was configured correctly
            mock_qr_code_class.assert_called_once_with(version=1, box_size=6, border=2)
            mock_qr.add_data.assert_called_once_with("test_data")
            mock_qr.make.assert_called_once_with(fit=True)
            mock_qr.make_image.assert_called_once_with(fill="black", back_color="white")
            
            # Verify image was saved to buffer
            mock_image.save.assert_called_once_with(mock_buffer, format="PNG")
            
            # Verify result format
            assert result == "data:image/png;base64,ZmFrZV9pbWFnZV9kYXRh"

    @patch('qrcode.QRCode')
    def test_generate_qr_code_with_empty_data(self, mock_qr_code_class):
        """Test QR code generation with empty data."""
        mock_qr = MagicMock()
        mock_qr_code_class.return_value = mock_qr
        mock_image = MagicMock()
        mock_qr.make_image.return_value = mock_image
        
        with patch('app.utils.qr.BytesIO') as mock_bytesio, \
             patch('app.utils.qr.base64.b64encode') as mock_b64encode:
            
            mock_buffer = MagicMock()
            mock_bytesio.return_value = mock_buffer
            mock_buffer.getvalue.return_value = b'empty_data'
            mock_b64encode.return_value = b'ZW1wdHlfZGF0YQ=='
            
            result = generate_qr_code("")
            
            mock_qr.add_data.assert_called_once_with("")
            assert result.startswith("data:image/png;base64,")

    @patch('qrcode.QRCode')
    def test_generate_qr_code_with_long_data(self, mock_qr_code_class):
        """Test QR code generation with long data."""
        mock_qr = MagicMock()
        mock_qr_code_class.return_value = mock_qr
        mock_image = MagicMock()
        mock_qr.make_image.return_value = mock_image
        
        with patch('app.utils.qr.BytesIO') as mock_bytesio, \
             patch('app.utils.qr.base64.b64encode') as mock_b64encode:
            
            mock_buffer = MagicMock()
            mock_bytesio.return_value = mock_buffer
            mock_buffer.getvalue.return_value = b'long_data'
            mock_b64encode.return_value = b'bG9uZ19kYXRh'
            
            long_data = "A" * 1000  # Long string
            result = generate_qr_code(long_data)
            
            mock_qr.add_data.assert_called_once_with(long_data)
            assert result.startswith("data:image/png;base64,")

    @patch('qrcode.QRCode')
    def test_generate_qr_code_with_special_characters(self, mock_qr_code_class):
        """Test QR code generation with special characters."""
        mock_qr = MagicMock()
        mock_qr_code_class.return_value = mock_qr
        mock_image = MagicMock()
        mock_qr.make_image.return_value = mock_image
        
        with patch('app.utils.qr.BytesIO') as mock_bytesio, \
             patch('app.utils.qr.base64.b64encode') as mock_b64encode:
            
            mock_buffer = MagicMock()
            mock_bytesio.return_value = mock_buffer
            mock_buffer.getvalue.return_value = b'special_data'
            mock_b64encode.return_value = b'c3BlY2lhbF9kYXRh'
            
            special_data = "测试数据!@#$%^&*()_+{}|:<>?[]\\;'\",./"
            result = generate_qr_code(special_data)
            
            mock_qr.add_data.assert_called_once_with(special_data)
            assert result.startswith("data:image/png;base64,")

    def test_generate_qr_code_qr_parameters(self):
        """Test that QR code is created with correct parameters."""
        with patch('qrcode.QRCode') as mock_qr_code_class:
            mock_qr = MagicMock()
            mock_qr_code_class.return_value = mock_qr
            mock_image = MagicMock()
            mock_qr.make_image.return_value = mock_image
            
            with patch('app.utils.qr.BytesIO'), \
                 patch('app.utils.qr.base64.b64encode', return_value=b'test'):
                
                generate_qr_code("test")
                
                # Verify QR code parameters
                mock_qr_code_class.assert_called_once_with(version=1, box_size=6, border=2)
                mock_qr.make_image.assert_called_once_with(fill="black", back_color="white")


if __name__ == "__main__":
    pytest.main([__file__])
