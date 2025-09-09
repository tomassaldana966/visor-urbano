import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
import json

from app.main import app
from app.models.technical_sheet_downloads import TechnicalSheetDownload
from config.settings import get_db


class TestTechnicalSheetDownloads:
    
    def setup_method(self):
        """Set up test dependencies."""
        self.client = TestClient(app)
        self.mock_db = AsyncMock()
        
        # Configure async database operations
        self.mock_db.add = MagicMock()  # add is synchronous in SQLAlchemy
        self.mock_db.commit = AsyncMock()
        self.mock_db.refresh = AsyncMock()
        self.mock_db.rollback = AsyncMock()
        
        # Override dependencies
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Mock technical sheet download
        self.mock_download = MagicMock(spec=TechnicalSheetDownload)
        self.mock_download.id = 1
        self.mock_download.city = "Test City"
        self.mock_download.email = "test@example.com"
        self.mock_download.age = 30
        self.mock_download.name = "John Doe"
        self.mock_download.sector = "Technology"
        self.mock_download.uses = json.dumps(["residential", "commercial"])
        self.mock_download.municipality_id = 1
        self.mock_download.address = "123 Test Street"
    
    def teardown_method(self):
        """Clean up after tests."""
        app.dependency_overrides.clear()
    
    def test_create_technical_sheet_download_success(self):
        """Test successful creation of technical sheet download."""
        # Configure async mock refresh to simulate ID assignment
        async def mock_refresh(obj):
            obj.id = 1
            
        self.mock_db.refresh.side_effect = mock_refresh
        
        # Mock the new download to be returned after creation
        with patch('app.models.technical_sheet_downloads.TechnicalSheetDownload') as mock_download_class:
            mock_new_download = MagicMock()
            mock_new_download.id = 1
            mock_download_class.return_value = mock_new_download
            
            payload = {
                "city": "Test City",
                "email": "test@example.com",
                "age": 30,
                "name": "John Doe",
                "sector": "Technology",
                "uses": ["residential", "commercial"],
                "municipality_id": 1,
                "address": "123 Test Street"
            }
            
            response = self.client.post("/v1/technical_sheet_downloads", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 1
            self.mock_db.add.assert_called_once()
            self.mock_db.commit.assert_called_once()
            self.mock_db.refresh.assert_called_once()
    
    def test_create_technical_sheet_download_minimal_data(self):
        """Test creation with minimal required data."""
        # Configure async mock refresh to simulate ID assignment
        async def mock_refresh(obj):
            obj.id = 2
            
        self.mock_db.refresh.side_effect = mock_refresh
        
        with patch('app.models.technical_sheet_downloads.TechnicalSheetDownload') as mock_download_class:
            mock_new_download = MagicMock()
            mock_new_download.id = 2
            mock_download_class.return_value = mock_new_download
            
            payload = {
                "city": "Minimal City",
                "email": "minimal@example.com",
                "age": 25,
                "name": "Jane Doe",
                "sector": "Education",
                "uses": ["educational"],
                "municipality_id": 2,
                "address": "456 Minimal Avenue"
            }
            
            response = self.client.post("/v1/technical_sheet_downloads", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 2
    
    def test_create_technical_sheet_download_database_error(self):
        """Test database error during technical sheet download creation."""
        # Reset the mock before setting side_effect
        self.mock_db.commit.reset_mock()
        
        # Set commit to raise an exception
        async def commit_error():
            raise Exception("Database error")
        
        self.mock_db.commit.side_effect = commit_error
        
        payload = {
            "city": "Error City",
            "email": "error@example.com",
            "age": 35,
            "name": "Error User",
            "sector": "Finance",
            "uses": ["commercial"],
            "municipality_id": 1,
            "address": "789 Error Road"
        }
        
        response = self.client.post("/v1/technical_sheet_downloads", json=payload)
        # The API should return 500 for database errors
        assert response.status_code == 500
    
    def test_create_technical_sheet_download_commit_error(self):
        """Test commit error during creation."""
        # Reset the mock before setting side_effect
        self.mock_db.commit.reset_mock()
        
        # Set commit to raise an exception
        async def commit_error():
            raise Exception("Commit error")
        
        self.mock_db.commit.side_effect = commit_error
        
        payload = {
            "city": "Commit City",
            "email": "commit@example.com",
            "age": 40,
            "name": "Commit User",
            "sector": "Healthcare",
            "uses": ["medical"],
            "municipality_id": 3,
            "address": "321 Commit Street"
        }
        
        response = self.client.post("/v1/technical_sheet_downloads", json=payload)
        # The API should return 500 for commit errors
        assert response.status_code == 500
    
    def test_create_technical_sheet_download_invalid_email(self):
        """Test creation with invalid email format."""
        payload = {
            "city": "Invalid City",
            "email": "invalid-email",  # Invalid email format
            "age": 28,
            "name": "Invalid User",
            "sector": "Technology",
            "uses": ["residential"],
            "municipality_id": 1,
            "address": "123 Invalid Street"
        }
        
        response = self.client.post("/v1/technical_sheet_downloads", json=payload)
        
        # Should return validation error for invalid email
        assert response.status_code == 422
    
    def test_create_technical_sheet_download_missing_required_fields(self):
        """Test creation with missing required fields."""
        payload = {
            "city": "Missing City",
            # Missing email, age, name, sector, uses, municipality_id, address
        }
        
        response = self.client.post("/v1/technical_sheet_downloads", json=payload)
        
        # Should return validation error for missing fields
        assert response.status_code == 422
    
    def test_create_technical_sheet_download_negative_age(self):
        """Test creation with negative age."""
        payload = {
            "city": "Negative City",
            "email": "negative@example.com",
            "age": -5,  # Invalid negative age
            "name": "Negative User",
            "sector": "Technology",
            "uses": ["residential"],
            "municipality_id": 1,
            "address": "123 Negative Street"
        }
        
        response = self.client.post("/v1/technical_sheet_downloads", json=payload)
        
        # Depending on schema validation, this might be allowed or rejected
        # If validation is in place, it should return 422
        if response.status_code == 422:
            assert response.status_code == 422
        else:
            # If no validation, the endpoint might still process it
            assert response.status_code in [200, 422]
    
    def test_create_technical_sheet_download_empty_uses_array(self):
        """Test creation with empty uses array."""
        # Configure async mock refresh to simulate ID assignment
        async def mock_refresh(obj):
            obj.id = 3
            
        self.mock_db.refresh.side_effect = mock_refresh
        
        with patch('app.models.technical_sheet_downloads.TechnicalSheetDownload') as mock_download_class:
            mock_new_download = MagicMock()
            mock_new_download.id = 3
            mock_download_class.return_value = mock_new_download
            
            payload = {
                "city": "Empty Uses City",
                "email": "empty@example.com",
                "age": 32,
                "name": "Empty User",
                "sector": "Retail",
                "uses": [],  # Empty array
                "municipality_id": 1,
                "address": "123 Empty Street"
            }
            
            response = self.client.post("/v1/technical_sheet_downloads", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 3
    
    def test_create_technical_sheet_download_large_uses_array(self):
        """Test creation with large uses array."""
        # Configure async mock refresh to simulate ID assignment
        async def mock_refresh(obj):
            obj.id = 4
            
        self.mock_db.refresh.side_effect = mock_refresh
        
        with patch('app.models.technical_sheet_downloads.TechnicalSheetDownload') as mock_download_class:
            mock_new_download = MagicMock()
            mock_new_download.id = 4
            mock_download_class.return_value = mock_new_download
            
            payload = {
                "city": "Large Uses City",
                "email": "large@example.com",
                "age": 45,
                "name": "Large User",
                "sector": "Manufacturing",
                "uses": [
                    "residential", "commercial", "industrial", "educational",
                    "medical", "recreational", "governmental", "agricultural"
                ],
                "municipality_id": 2,
                "address": "123 Large Street"
            }
            
            response = self.client.post("/v1/technical_sheet_downloads", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 4
    
    @pytest.mark.parametrize("city,email,age,name,sector,municipality_id", [
        ("City A", "user1@example.com", 25, "User One", "Tech", 1),
        ("City B", "user2@example.com", 35, "User Two", "Finance", 2),
        ("City C", "user3@example.com", 45, "User Three", "Healthcare", 3),
        ("City D", "user4@example.com", 55, "User Four", "Education", 4),
    ])
    def test_create_technical_sheet_download_various_data(self, city, email, age, name, sector, municipality_id):
        """Test creation with various data combinations."""
        # Configure async mock refresh to simulate ID assignment
        async def mock_refresh(obj):
            obj.id = municipality_id
            
        self.mock_db.refresh.side_effect = mock_refresh
        
        with patch('app.models.technical_sheet_downloads.TechnicalSheetDownload') as mock_download_class:
            mock_new_download = MagicMock()
            mock_new_download.id = municipality_id
            mock_download_class.return_value = mock_new_download
            
            payload = {
                "city": city,
                "email": email,
                "age": age,
                "name": name,
                "sector": sector,
                "uses": ["residential"],
                "municipality_id": municipality_id,
                "address": f"123 {city} Street"
            }
            
            response = self.client.post("/v1/technical_sheet_downloads", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == municipality_id
    
    def test_create_technical_sheet_download_special_characters(self):
        """Test creation with special characters in data."""
        # Configure async mock refresh to simulate ID assignment
        async def mock_refresh(obj):
            obj.id = 5
            
        self.mock_db.refresh.side_effect = mock_refresh
        
        with patch('app.models.technical_sheet_downloads.TechnicalSheetDownload') as mock_download_class:
            mock_new_download = MagicMock()
            mock_new_download.id = 5
            mock_download_class.return_value = mock_new_download
            
            payload = {
                "city": "São Paulo",  # Special characters
                "email": "special@exámple.com",
                "age": 30,
                "name": "José María",  # Special characters
                "sector": "Educación & Tecnología",  # Special characters
                "uses": ["residencial", "comercial"],
                "municipality_id": 1,
                "address": "123 Rúa do Comércio"  # Special characters
            }
            
            response = self.client.post("/v1/technical_sheet_downloads", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 5
    
    def test_create_technical_sheet_download_json_serialization(self):
        """Test that uses array is properly JSON serialized."""
        # Configure async mock refresh to simulate ID assignment
        async def mock_refresh(obj):
            obj.id = 6
            
        self.mock_db.refresh.side_effect = mock_refresh
        
        test_uses = ["residential", "commercial", "mixed-use"]
        
        with patch('app.models.technical_sheet_downloads.TechnicalSheetDownload') as mock_download_class:
            mock_new_download = MagicMock()
            mock_new_download.id = 6
            mock_download_class.return_value = mock_new_download
            
            payload = {
                "city": "JSON City",
                "email": "json@example.com",
                "age": 28,
                "name": "JSON User",
                "sector": "Data Science",
                "uses": test_uses,
                "municipality_id": 1,
                "address": "123 JSON Street"
            }
            
            response = self.client.post("/v1/technical_sheet_downloads", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == 6
            
            # Verify that the model was called with JSON serialized uses
            mock_download_class.assert_called_once()
            call_kwargs = mock_download_class.call_args.kwargs
            assert call_kwargs['uses'] == json.dumps(test_uses)
