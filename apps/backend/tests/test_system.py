import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import re

from app.main import app


class TestSystem:
    def setup_method(self):
        """Setup for each test method."""
        self.client = TestClient(app)

    def teardown_method(self):
        """Cleanup after each test method."""
        app.dependency_overrides.clear()

    def test_generate_key_success(self):
        """Test successful key generation."""
        # Act
        response = self.client.get("/v1/system/key")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "key" in result
        assert isinstance(result["key"], str)
        assert len(result["key"]) == 32  # 16 bytes = 32 hex characters
        
        # Verify it's a valid hex string
        assert re.match(r'^[0-9a-f]{32}$', result["key"])

    def test_generate_key_uniqueness(self):
        """Test that generated keys are unique."""
        # Act
        response1 = self.client.get("/v1/system/key")
        response2 = self.client.get("/v1/system/key")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        key1 = response1.json()["key"]
        key2 = response2.json()["key"]
        
        assert key1 != key2  # Keys should be different
        assert len(key1) == 32
        assert len(key2) == 32

    def test_generate_key_multiple_requests(self):
        """Test multiple key generation requests."""
        keys = []
        
        # Act - Generate multiple keys
        for _ in range(10):
            response = self.client.get("/v1/system/key")
            assert response.status_code == 200
            key = response.json()["key"]
            keys.append(key)

        # Assert - All keys should be unique
        assert len(set(keys)) == 10  # All keys are unique
        for key in keys:
            assert len(key) == 32
            assert re.match(r'^[0-9a-f]{32}$', key)

    @patch('secrets.token_hex')
    def test_generate_key_mocked(self, mock_token_hex):
        """Test key generation with mocked secrets module."""
        # Arrange
        mock_token_hex.return_value = "abcdef1234567890abcdef1234567890"

        # Act
        response = self.client.get("/v1/system/key")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["key"] == "abcdef1234567890abcdef1234567890"
        mock_token_hex.assert_called_once_with(16)

    def test_get_news_success(self):
        """Test successful news data retrieval."""
        # Act
        response = self.client.get("/v1/system/news")

        # Assert
        assert response.status_code == 200
        result = response.json()
        
        # Check structure
        assert "data" in result
        assert "status" in result
        assert result["status"] is True
        
        # Check data content
        data = result["data"]
        assert "href" in data
        assert "src" in data
        assert "src_xs" in data
        
        # Check specific values
        assert data["href"] == "https://visorurbano.com"
        assert data["src"] == "https://visorurbano.jalisco.gob.mx/assets/images/planes.png"
        assert data["src_xs"] == "https://visorurbano.jalisco.gob.mx/assets/images/planes.png"

    def test_get_news_response_format(self):
        """Test that news response has correct format."""
        # Act
        response = self.client.get("/v1/system/news")

        # Assert
        assert response.status_code == 200
        result = response.json()
        
        # Validate data types
        assert isinstance(result["data"], dict)
        assert isinstance(result["status"], bool)
        assert isinstance(result["data"]["href"], str)
        assert isinstance(result["data"]["src"], str)
        assert isinstance(result["data"]["src_xs"], str)

    def test_get_news_urls_validity(self):
        """Test that URLs in news response are valid format."""
        # Act
        response = self.client.get("/v1/system/news")

        # Assert
        assert response.status_code == 200
        result = response.json()
        data = result["data"]
        
        # Check URL formats
        assert data["href"].startswith("https://")
        assert data["src"].startswith("https://")
        assert data["src_xs"].startswith("https://")
        
        # Check that image URLs point to images
        assert data["src"].endswith(".png")
        assert data["src_xs"].endswith(".png")

    def test_news_data_consistency(self):
        """Test that news data is consistent across multiple requests."""
        # Act
        response1 = self.client.get("/v1/system/news")
        response2 = self.client.get("/v1/system/news")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Data should be identical
        assert response1.json() == response2.json()

    @pytest.mark.parametrize("endpoint", ["/v1/system/key", "/v1/system/news"])
    def test_endpoints_accessibility(self, endpoint):
        """Test that both endpoints are accessible."""
        # Act
        response = self.client.get(endpoint)

        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_key_entropy(self):
        """Test that generated keys have sufficient entropy."""
        keys = []
        
        # Generate many keys to test entropy
        for _ in range(100):
            response = self.client.get("/v1/system/key")
            key = response.json()["key"]
            keys.append(key)

        # Check that we have good character distribution
        all_chars = ''.join(keys)
        char_counts = {}
        for char in '0123456789abcdef':
            char_counts[char] = all_chars.count(char)

        # Each hex character should appear roughly equally
        # With 100 keys * 32 chars = 3200 total chars
        # Each of 16 hex chars should appear ~200 times
        total_chars = len(all_chars)
        expected_per_char = total_chars / 16
        
        for char, count in char_counts.items():
            # Allow 50% deviation from expected
            assert count > expected_per_char * 0.5
            assert count < expected_per_char * 1.5

    def test_concurrent_key_generation(self):
        """Test concurrent key generation requests."""
        import threading
        import queue
        
        results = queue.Queue()
        
        def generate_key():
            response = self.client.get("/v1/system/key")
            if response.status_code == 200:
                results.put(response.json()["key"])
        
        # Start multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=generate_key)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Collect results
        keys = []
        while not results.empty():
            keys.append(results.get())
        
        # Assert all keys are unique
        assert len(keys) == 10
        assert len(set(keys)) == 10

    def test_news_endpoint_tags(self):
        """Test that endpoints have correct tags in OpenAPI spec."""
        # Act
        response = self.client.get("/v1/system/openapi.json")
        
        # Assert
        if response.status_code == 200:
            openapi_spec = response.json()
            paths = openapi_spec.get("paths", {})
            
            # Check key endpoint
            if "/key" in paths and "get" in paths["/key"]:
                key_tags = paths["/key"]["get"].get("tags", [])
                assert "system" in key_tags
            
            # Check news endpoint  
            if "/news" in paths and "get" in paths["/news"]:
                news_tags = paths["/news"]["get"].get("tags", [])
                assert "system" in news_tags

    def test_error_handling_robustness(self):
        """Test that system endpoints are robust to various conditions."""
        # These endpoints are simple and shouldn't fail under normal conditions
        
        # Test multiple rapid requests
        for _ in range(20):
            key_response = self.client.get("/v1/system/key")
            news_response = self.client.get("/v1/system/news")
            
            assert key_response.status_code == 200
            assert news_response.status_code == 200

    def test_response_headers(self):
        """Test that endpoints return appropriate response headers."""
        # Act
        key_response = self.client.get("/v1/system/key")
        news_response = self.client.get("/v1/system/news")

        # Assert
        assert key_response.status_code == 200
        assert news_response.status_code == 200
        
        # Check content-type headers
        assert "application/json" in key_response.headers.get("content-type", "")
        assert "application/json" in news_response.headers.get("content-type", "")
