import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.routers.dependency_reviews import router
from app.schemas.dependency_reviews import DependencyReviewCreate, DependencyReviewUpdate
from app.models.dependency_reviews import DependencyReview
from app.models.technical_sheet_downloads import TechnicalSheetDownload
from config.security import get_current_user
from config.settings import get_db
from app.utils.role_validation import validate_admin_role, validate_director_role, validate_admin_or_director_role

# Create test app
app = FastAPI()
app.include_router(router)

# --- Mock Data ---
FAKE_DEPENDENCY_REVIEWS = [
    {
        "id": 1,
        "folio": "TEST-DR-001",
        "procedure_id": 1,
        "municipality_id": 1,
        "role": 1,
        "start_date": datetime(2024, 1, 15, 9, 0, 0),
        "update_date": datetime(2024, 1, 15, 9, 0, 0),
        "current_status": 1,
        "current_file": "file_001.pdf",
        "signature": "signature_001",
        "user_id": 1,
        "created_at": datetime(2024, 1, 15, 9, 0, 0),
        "updated_at": datetime(2024, 1, 15, 9, 0, 0)
    },
    {
        "id": 2,
        "folio": "TEST-DR-002",
        "procedure_id": 2,
        "municipality_id": 1,
        "role": 2,
        "start_date": datetime(2024, 1, 16, 10, 30, 0),
        "update_date": datetime(2024, 1, 16, 14, 20, 0),
        "current_status": 2,
        "current_file": "file_002.pdf",
        "signature": "signature_002",
        "user_id": 2,
        "created_at": datetime(2024, 1, 16, 10, 30, 0),
        "updated_at": datetime(2024, 1, 16, 14, 20, 0)
    }
]

FAKE_TECHNICAL_SHEET_DOWNLOADS = [
    {
        "id": 1,
        "folio": "TEST-DR-001",
        "download_date": datetime(2024, 1, 15, 9, 30, 0),
        "user_id": 1
    }
]

# --- Mock Users ---
FAKE_ADMIN_USER = {
    "id": 1,
    "email": "admin@test.com",
    "role_id": 1,  # Admin role
    "role_name": "admin",
    "municipality_id": 1
}

FAKE_DIRECTOR_USER = {
    "id": 2,
    "email": "director@test.com",
    "role_id": 2,  # Director role  
    "role_name": "director",
    "municipality_id": 1
}

FAKE_REGULAR_USER = {
    "id": 3,
    "email": "user@test.com",
    "role_id": 3,  # Regular user role
    "role_name": "user",
    "municipality_id": 1
}

# --- Mock Database Session ---
class FakeAsyncSession:
    def __init__(self, data=None):
        self.data = data if data is not None else FAKE_DEPENDENCY_REVIEWS
        self.downloads_data = FAKE_TECHNICAL_SHEET_DOWNLOADS
        
    async def execute(self, statement):
        # Convert the statement to string to understand what's being queried
        query_str = str(statement)
        
        # Handle different types of queries
        if 'extract' in query_str.lower() or 'month' in query_str.lower():
            # Handle func.extract queries for line_time endpoints
            if len(self.data) == 0:
                return FakeResult([])
            mock_data = [
                type('Row', (), {
                    'month': 1, 'year': 2024, 'role': 1, 'total': 5,
                    'current_status': 1, 'municipality_id': 1
                })()
            ]
            return FakeResult(mock_data)
        elif 'technical_sheet_downloads' in query_str.lower():
            # Handle technical sheet downloads
            if len(self.data) == 0:
                return FakeResult([])
            return FakeResult(self.downloads_data)
        elif 'WHERE dependency_reviews.folio' in query_str:
            # Handle single folio lookup queries
            if len(self.data) == 0:
                return FakeResult([])
            return FakeResult(self.data)
        else:
            # Default to returning dependency reviews
            return FakeResult(self.data)
    
    async def commit(self):
        pass
    
    async def rollback(self):
        pass
    
    async def refresh(self, obj):
        pass

class FakeResult:
    def __init__(self, data):
        self.data = data
        
    def scalars(self):
        return FakeScalars(self.data)
    
    def scalar_one_or_none(self):
        # For single object lookups (by folio, etc.)
        if self.data:
            if isinstance(self.data[0], dict):
                return FakeReview(self.data[0])
            else:
                return self.data[0]
        return None
    
    def all(self):
        # Handle both dict objects and row objects
        if self.data and isinstance(self.data[0], dict):
            return [FakeRow(item) for item in self.data]
        else:
            # Return the data as-is if it's already row objects
            return self.data

class FakeScalars:
    def __init__(self, data):
        self.data = data
        
    def all(self):
        return [FakeReview(item) for item in self.data] if self.data else []
    
    def first(self):
        return FakeReview(self.data[0]) if self.data else None

class FakeReview:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        # Add mock relationships
        self.procedure = type('Procedure', (), {'id': data.get('procedure_id', 1)})()
        self.municipality = type('Municipality', (), {
            'id': data.get('municipality_id', 1),
            'name': 'Test Municipality'
        })()
        self.user = type('User', (), {'id': data.get('user_id', 1)})()
        self.resolutions = []
        self.prevention_requests = []
        self.notifications = []
        # Add missing attributes that might be accessed
        if not hasattr(self, 'director_approved'):
            self.director_approved = 0
        if not hasattr(self, 'license_issued'):
            self.license_issued = False

class FakeRow:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

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
class TestDependencyReviews:
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = TestClient(app)
        app.dependency_overrides.clear()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        app.dependency_overrides.clear()

    def test_get_dependency_review_by_folio_success(self):
        """Test successful retrieval of dependency review by folio"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        response = self.client.get("/dependency_reviews/by_folio/TEST-DR-001")
        
        assert response.status_code == 200
        data = response.json()
        assert data["folio"] == "TEST-DR-001"
        assert data["procedure_id"] == 1

    def test_get_dependency_review_by_folio_not_found(self):
        """Test retrieval of non-existent dependency review"""
        app.dependency_overrides[get_db] = get_fake_empty_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        response = self.client.get("/dependency_reviews/by_folio/NON-EXISTENT")
        
        assert response.status_code == 404

    def test_get_line_time_data_success(self):
        """Test successful retrieval of line time data"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        response = self.client.get("/dependency_reviews/line_time")
        
        assert response.status_code == 200

    def test_get_line_time_admin_success(self):
        """Test line time admin endpoint with admin user"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        with patch('app.routers.dependency_reviews.validate_admin_role') as mock_validate:
            mock_validate.return_value = None
            response = self.client.get("/dependency_reviews/line_time_admin")
            
            assert response.status_code == 200

    def test_get_line_time_admin_unauthorized(self):
        """Test line time admin endpoint with unauthorized user"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_regular_user
        
        with patch('app.routers.dependency_reviews.validate_admin_role') as mock_validate:
            mock_validate.side_effect = HTTPException(status_code=403, detail="Insufficient permissions")
            response = self.client.get("/dependency_reviews/line_time_admin")
            
            assert response.status_code == 403

    def test_update_director_review_success(self):
        """Test successful director review update"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_director_user
        
        update_data = {
            "resolution_status": 2,
            "resolution_file": "updated_file.pdf"
        }
        
        with patch('app.routers.dependency_reviews.validate_director_role') as mock_validate:
            mock_validate.return_value = None
            response = self.client.post(
                "/dependency_reviews/update_director/TEST-DR-001",
                json=update_data
            )
            
            assert response.status_code == 200

    def test_update_director_review_unauthorized(self):
        """Test director review update with unauthorized user"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_regular_user
        
        update_data = {
            "resolution_status": 2,
            "resolution_file": "updated_file.pdf"
        }
        
        with patch('app.routers.dependency_reviews.validate_director_role') as mock_validate:
            mock_validate.side_effect = HTTPException(status_code=403, detail="Insufficient permissions")
            response = self.client.post(
                "/dependency_reviews/update_director/TEST-DR-001",
                json=update_data
            )
            
            assert response.status_code == 403

    def test_get_full_report_success(self):
        """Test successful full report retrieval"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_admin_user
        
        with patch('app.routers.dependency_reviews.validate_admin_role') as mock_validate:
            mock_validate.return_value = None
            response = self.client.get("/dependency_reviews/full_report")
            
            assert response.status_code == 200

    def test_get_full_report_unauthorized(self):
        """Test full report with unauthorized user"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_regular_user
        
        with patch('app.routers.dependency_reviews.validate_admin_role') as mock_validate:
            mock_validate.side_effect = HTTPException(status_code=403, detail="Insufficient permissions")
            response = self.client.get("/dependency_reviews/full_report")
            
            assert response.status_code == 403

    def test_get_bar_chart_success(self):
        """Test successful bar chart retrieval"""
        # Create a mock database session
        async def mock_db_session():
            mock_db = Mock()
            mock_result = Mock()
            mock_row1 = Mock()
            mock_row1.current_status = 1
            mock_row1.role = 1
            mock_row1.total = 5
            mock_row2 = Mock()
            mock_row2.current_status = 2
            mock_row2.role = 2
            mock_row2.total = 3
            mock_result.all.return_value = [mock_row1, mock_row2]
            mock_db.execute = AsyncMock(return_value=mock_result)
            return mock_db
        
        # Override the dependency
        from config.settings import get_db
        app.dependency_overrides[get_db] = mock_db_session
        
        try:
            response = self.client.get("/dependency_reviews/bar_chart")
            
            if response.status_code != 200:
                print(f"Response status: {response.status_code}")
                print(f"Response content: {response.content}")
                
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["status"] == 1
            assert data[0]["role"] == 1
            assert data[0]["total"] == 5
        finally:
            # Clean up the override
            app.dependency_overrides.clear()

    def test_get_technical_sheet_downloads_success(self):
        """Test successful technical sheet downloads retrieval"""
        # Create mock database session for technical sheet downloads
        async def mock_db_session():
            mock_db = Mock()
            mock_download = Mock()
            mock_download.id = 1
            mock_download.technical_sheet_uuid = "test-uuid-123"
            mock_download.user_email = "test@example.com"
            mock_download.download_count = 3
            mock_download.created_at = datetime(2024, 1, 15, 9, 0, 0)
            mock_download.updated_at = datetime(2024, 1, 15, 9, 0, 0)
            
            mock_scalars = Mock()
            mock_scalars.all.return_value = [mock_download]
            mock_result = Mock()
            mock_result.scalars.return_value = mock_scalars
            mock_db.execute = AsyncMock(return_value=mock_result)
            return mock_db
        
        # Mock admin user
        async def mock_admin_user():
            user = Mock()
            user.id = 1
            user.role = "admin"
            user.role_name = "admin"
            user.role_id = 1
            return user
        
        # Override dependencies
        from config.settings import get_db
        from config.security import get_current_user
        app.dependency_overrides[get_db] = mock_db_session
        app.dependency_overrides[get_current_user] = mock_admin_user
        
        try:
            response = self.client.get("/dependency_reviews/technical_sheet_downloads")
            
            if response.status_code != 200:
                print(f"Response status: {response.status_code}")
                print(f"Response content: {response.content}")
            
            assert response.status_code == 200
            data = response.json()
            assert "downloads" in data
            assert len(data["downloads"]) == 1
            assert data["downloads"][0]["technical_sheet_uuid"] == "test-uuid-123"
            assert data["downloads"][0]["user_email"] == "test@example.com"
        finally:
            app.dependency_overrides.clear()

    def test_get_technical_sheet_downloads_unauthorized(self):
        """Test technical sheet downloads with unauthorized user"""
        app.dependency_overrides[get_db] = get_fake_db
        app.dependency_overrides[get_current_user] = get_fake_regular_user
        
        with patch('app.routers.dependency_reviews.validate_admin_role') as mock_validate:
            mock_validate.side_effect = HTTPException(status_code=403, detail="Insufficient permissions")
            response = self.client.get("/dependency_reviews/technical_sheet_downloads")
            
            assert response.status_code == 403
