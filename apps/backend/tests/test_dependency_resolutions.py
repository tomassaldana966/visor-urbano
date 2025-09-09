import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.routers.dependency_resolutions import router
from config.security import get_current_user
from config.settings import get_db
from app.utils.role_validation import validate_admin_or_director_role

# Create test app
app = FastAPI()
app.include_router(router)

# --- Test Data ---
FAKE_DEPENDENCY_RESOLUTIONS = [
    {
        "id": 1,
        "procedure_id": 1,
        "role": 1,
        "user_id": 1,
        "resolution_status": 1,
        "resolution_text": "Resolution approved",
        "resolution_file": "resolution_001.pdf",
        "signature": "signature_001",
        "created_at": datetime(2024, 1, 15, 9, 0, 0),
        "updated_at": datetime(2024, 1, 15, 9, 0, 0),
        "deleted_at": None,
        "review_id": 1,
        "additional_files": None,
        "is_final_resolution": True,
        "user_name": "Test User 1"
    },
    {
        "id": 2,
        "procedure_id": 2,
        "role": 2,
        "user_id": 2,
        "resolution_status": 2,
        "resolution_text": "Resolution rejected",
        "resolution_file": "resolution_002.pdf",
        "signature": "signature_002",
        "created_at": datetime(2024, 1, 16, 10, 30, 0),
        "updated_at": datetime(2024, 1, 16, 14, 20, 0),
        "deleted_at": None,
        "review_id": 2,
        "additional_files": None,
        "is_final_resolution": False,
        "user_name": "Test User 2"
    }
]

FAKE_PROCEDURES = [
    {"id": 1, "folio": "TEST-DR-001"},
    {"id": 2, "folio": "TEST-DR-002"},
]

# --- Mock Users ---
FAKE_ADMIN_USER = {
    "id": 1,
    "email": "admin@test.com",
    "role_id": 1,
    "role_name": "admin",
    "municipality_id": 1
}

FAKE_DIRECTOR_USER = {
    "id": 2,
    "email": "director@test.com",
    "role_id": 2,
    "role_name": "director",
    "municipality_id": 1
}

FAKE_REGULAR_USER = {
    "id": 3,
    "email": "user@test.com",
    "role_id": 3,
    "role_name": "user",
    "municipality_id": 1
}

# --- Mock Database Classes ---
class FakeAsyncSession:
    def __init__(self, data=None):
        self.data = data if data is not None else FAKE_DEPENDENCY_RESOLUTIONS
        self._committed = False
        self._added_objects = []
        
    async def execute(self, statement):
        # Convert the statement to string to understand what's being queried
        query_str = str(statement)
        
        # Handle different types of queries
        if "WHERE dependency_resolutions.id" in query_str:
            # This is an UPDATE query looking for a specific resolution by ID
            # Extract ID from query context or return empty for 404 test cases
            if len(self.data) == 0:
                return FakeResult([])
            return FakeResult(self.data)
        elif "procedure" in query_str.lower() and "folio" in query_str.lower():
            # This is the main GET by folio query with joins
            if len(self.data) == 0:
                return FakeResult([])  # Empty results for empty database
            return FakeResult(self.data)
        elif "WHERE procedures.id" in query_str:
            # This is a procedure existence check in POST
            if len(self.data) == 0:
                return FakeResult([])  # No procedure found
            # Return a fake procedure for successful operations
            return FakeResult([{"id": 1, "folio": "TEST-DR-001"}])
        else:
            # Default case
            return FakeResult(self.data)
    
    async def commit(self):
        self._committed = True
        # Assign IDs to any added objects
        for obj in self._added_objects:
            if not hasattr(obj, 'id') or obj.id is None:
                obj.id = len(self.data) + len(self._added_objects) + 1
                # Add created_at and updated_at timestamps
                from datetime import datetime
                obj.created_at = datetime.now()
                obj.updated_at = datetime.now()
    
    async def rollback(self):
        self._added_objects.clear()
    
    async def refresh(self, obj):
        # Simulate refreshing the object from database
        if obj in self._added_objects and not hasattr(obj, 'id'):
            obj.id = len(self.data) + len(self._added_objects)
    
    def add(self, obj):
        # Simulate adding an object to the session
        # Set default values for required fields that might be missing
        if not hasattr(obj, 'user_id') or obj.user_id is None:
            obj.user_id = 1
        if not hasattr(obj, 'review_id') or obj.review_id is None:
            obj.review_id = 1
        if not hasattr(obj, 'is_final_resolution') or obj.is_final_resolution is None:
            obj.is_final_resolution = False
        if not hasattr(obj, 'deleted_at'):
            obj.deleted_at = None
        if not hasattr(obj, 'additional_files'):
            obj.additional_files = None
        if not hasattr(obj, 'created_at'):
            obj.created_at = datetime.now()
        if not hasattr(obj, 'updated_at'):
            obj.updated_at = datetime.now()
        if not hasattr(obj, 'id') or obj.id is None:
            obj.id = len(self._added_objects) + 1
        self._added_objects.append(obj)
    
    async def commit(self):
        # Simulate committing the transaction
        self._committed = True
    
    async def refresh(self, obj):
        # Simulate refreshing object from database
        pass
    
    async def rollback(self):
        # Simulate rolling back the transaction
        pass

class FakeResult:
    def __init__(self, data):
        self.data = data
        
    def scalars(self):
        return FakeScalars(self.data)
    
    def scalar_one_or_none(self):
        # For procedures table lookups and single resolution lookups
        if self.data:
            if isinstance(self.data[0], dict):
                return FakeResolution(self.data[0])
            else:
                # For procedure lookups, return a fake procedure
                return type('Procedure', (), {'id': 1, 'folio': 'TEST-DR-001'})()
        return None

class FakeScalars:
    def __init__(self, data):
        self.data = data
        
    def all(self):
        return [FakeResolution(item) for item in self.data]
    
    def first(self):
        return FakeResolution(self.data[0]) if self.data else None

class FakeResolution:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        # Add mock procedure relationship
        self.procedure = type('Procedure', (), {'folio': f'TEST-DR-{str(data.get("id", "001")).zfill(3)}'})()
        
    def dict(self, **kwargs):
        # Return dictionary representation for JSON serialization
        data = {}
        for key, value in self.__dict__.items():
            if key != 'procedure':  # Skip the mock procedure
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                else:
                    data[key] = value
        return data

# --- Mock Functions ---
async def get_fake_db():
    return FakeAsyncSession()

async def get_fake_empty_db():
    return FakeAsyncSession([])

async def get_fake_admin_user():
    return FAKE_ADMIN_USER

async def get_fake_director_user():
    return FAKE_DIRECTOR_USER

async def get_fake_regular_user():
    return FAKE_REGULAR_USER

# --- Test Class ---
class TestDependencyResolutions:
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = TestClient(app)
        app.dependency_overrides.clear()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        app.dependency_overrides.clear()

    def test_get_dependency_resolutions_by_folio_success(self):
        """Test successful retrieval of dependency resolutions by folio"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.return_value = None
            response = self.client.get("/dependency_resolutions/by_folio/TEST-DR-001")
            
            if response.status_code != 200:
                print(f"Response status: {response.status_code}")
                print(f"Response content: {response.text}")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["procedure_id"] == 1
            assert data[1]["procedure_id"] == 2

    def test_get_dependency_resolutions_by_folio_unauthorized(self):
        """Test dependency resolutions retrieval by folio with unauthorized user"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_regular_user
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.side_effect = HTTPException(status_code=403, detail="Insufficient permissions")
            response = self.client.get("/dependency_resolutions/by_folio/TEST-DR-001")
            
            assert response.status_code == 403

    def test_get_dependency_resolutions_by_folio_empty(self):
        """Test dependency resolutions retrieval by folio with empty database"""
        app.dependency_overrides[get_db] = get_fake_empty_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.return_value = None  # Success case
            response = self.client.get("/dependency_resolutions/by_folio/TEST-DR-999")
            
            assert response.status_code == 404

    def test_get_dependency_resolutions_by_folio_not_found(self):
        """Test retrieval of non-existent dependency resolution by folio"""
        app.dependency_overrides[get_db] = get_fake_empty_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.return_value = None  # Success case
            response = self.client.get("/dependency_resolutions/by_folio/NONEXISTENT")
            
            assert response.status_code == 404

    def test_create_dependency_resolution_success(self):
        """Test successful creation of dependency resolution"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        new_resolution = {
            "procedure_id": 3,
            "role": 1,
            "user_id": 1,
            "resolution_status": 1,
            "resolution_text": "New resolution approved",
            "resolution_file": "resolution_003.pdf",
            "signature": "signature_003"
        }
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.return_value = None  # Success case
            response = self.client.post("/dependency_resolutions/", json=new_resolution)
            
            assert response.status_code == 200

    def test_create_dependency_resolution_invalid_data(self):
        """Test creation with invalid data"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        invalid_resolution = {
            "procedure_id": "invalid",  # Should be integer
            "role": 1,
            "resolution_text": "Test resolution"
        }
        
        # This should fail validation before reaching role validation
        response = self.client.post("/dependency_resolutions/", json=invalid_resolution)
        
        assert response.status_code == 422

    def test_create_dependency_resolution_unauthorized(self):
        """Test dependency resolution creation with unauthorized user"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_regular_user
        
        new_resolution = {
            "procedure_id": 3,
            "role": 1,
            "user_id": 1,
            "resolution_status": 1,
            "resolution_text": "New resolution",
            "resolution_file": "file.pdf",
            "signature": "signature"
        }
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.side_effect = HTTPException(status_code=403, detail="Insufficient permissions")
            response = self.client.post("/dependency_resolutions/", json=new_resolution)
            
            assert response.status_code == 403

    def test_update_dependency_resolution_success(self):
        """Test successful update of dependency resolution"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        update_data = {
            "resolution_status": 2,
            "resolution_text": "Updated resolution text",
            "resolution_file": "updated_file.pdf"
        }
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.return_value = None  # Success case
            response = self.client.patch("/dependency_resolutions/1", json=update_data)
            
            if response.status_code != 200:
                print(f"Response status: {response.status_code}")
                print(f"Response content: {response.content}")
            
            assert response.status_code == 200

    def test_update_dependency_resolution_not_found(self):
        """Test update of non-existent dependency resolution"""
        app.dependency_overrides[get_db] = get_fake_empty_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        update_data = {
            "resolution_status": 2,
            "resolution_text": "Updated text"
        }
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.return_value = None  # Success case
            response = self.client.patch("/dependency_resolutions/999", json=update_data)
            
            assert response.status_code == 404

    def test_update_dependency_resolution_unauthorized(self):
        """Test dependency resolution update with unauthorized user"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_regular_user
        
        update_data = {
            "resolution_status": 2,
            "resolution_text": "Updated text"
        }
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.side_effect = HTTPException(status_code=403, detail="Insufficient permissions")
            response = self.client.patch("/dependency_resolutions/1", json=update_data)
            
            assert response.status_code == 403

    def test_director_user_access(self):
        """Test that director users can access the endpoints"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_director_user
        
        with patch('app.routers.dependency_resolutions.validate_admin_or_director_role') as mock_validate:
            mock_validate.return_value = None  # Success case
            response = self.client.get("/dependency_resolutions/by_folio/TEST-DR-001")
            
            assert response.status_code == 200
