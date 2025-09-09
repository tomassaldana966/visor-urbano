import pytest
import os
from unittest.mock import patch
from app.utils.logo import get_logo


class TestLogoUtils:
    """Test cases for logo utility functions."""

    def test_get_logo_with_default_url(self):
        """Test getting logo with default URL when no environment variable is set."""
        with patch.dict(os.environ, {}, clear=True):
            result = get_logo("test_folio")
            assert result == "/logos/visor-urbano.svg"

    def test_get_logo_with_custom_url(self):
        """Test getting logo with custom URL from environment variable."""
        custom_url = "https://custom.example.com/logo.svg"
        with patch.dict(os.environ, {"DEFAULT_LOGO_URL": custom_url}):
            result = get_logo("test_folio")
            assert result == custom_url

    def test_get_logo_with_empty_folio(self):
        """Test getting logo with empty folio."""
        with patch.dict(os.environ, {}, clear=True):
            result = get_logo("")
            assert result == "/logos/visor-urbano.svg"

    def test_get_logo_with_none_folio(self):
        """Test getting logo with None folio."""
        with patch.dict(os.environ, {}, clear=True):
            result = get_logo(None)
            assert result == "/logos/visor-urbano.svg"

    def test_get_logo_ignores_folio_parameter(self):
        """Test that the folio parameter doesn't affect the result."""
        with patch.dict(os.environ, {}, clear=True):
            folio1 = "FOLIO001"
            folio2 = "FOLIO002"

            result1 = get_logo(folio1)
            result2 = get_logo(folio2)

            assert result1 == result2
            assert result1 == "/logos/visor-urbano.svg"


if __name__ == "__main__":
    pytest.main([__file__])
