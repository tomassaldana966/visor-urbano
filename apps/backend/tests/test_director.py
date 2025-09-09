import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.routers.director import router
from config.security import get_current_user
from config.settings import get_db
from app.utils.role_validation import require_director_role

# Create test app
app = FastAPI()
app.include_router(router)


class TestDirector:
    """Test suite for director router endpoints"""

    def setup_method(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
        self.app = app
        
        # Mock user with director role
        self.mock_director_user = Mock()
        self.mock_director_user.id = 1
        self.mock_director_user.role = 3  # Director role
        self.mock_director_user.municipality_id = 1
        self.mock_director_user.id_municipality = 1

    @patch('app.routers.director.require_director_role')
    @patch('app.routers.director.get_db')
    @patch('app.routers.director.get_current_user')
    def test_get_director_facets_success(self, mock_get_user, mock_get_db, mock_require_director):
        """Test successful retrieval of director facets"""
        # Mock authentication and authorization
        mock_get_user.return_value = self.mock_director_user
        mock_require_director.return_value = True

        # Mock database session
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        # Mock query results for different counts
        # Order: total_this_month, pending, completed_today, construction, commercial, total
        mock_results = [
            # total_procedures_this_month
            AsyncMock(scalar=Mock(return_value=25)),
            # pending_procedures
            AsyncMock(scalar=Mock(return_value=8)),
            # procedures_completed_today
            AsyncMock(scalar=Mock(return_value=3)),
            # construction_count
            AsyncMock(scalar=Mock(return_value=10)),
            # commercial_count
            AsyncMock(scalar=Mock(return_value=12)),
            # total_procedures
            AsyncMock(scalar=Mock(return_value=25))
        ]
        
        mock_db.execute = AsyncMock(side_effect=mock_results)
        
        # Override dependencies
        self.app.dependency_overrides[get_current_user] = lambda: self.mock_director_user
        self.app.dependency_overrides[get_db] = lambda: mock_db
        
        response = self.client.get("/facets")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure and values
        assert data["total_procedures_this_month"] == 25
        assert data["pending_procedures"] == 8
        assert data["procedures_completed_today"] == 3
        assert data["procedures_by_type"]["construction"] == 10
        assert data["procedures_by_type"]["commercial"] == 12
        assert data["procedures_by_type"]["others"] == 3  # 25 - 10 - 12 = 3
        
        # Verify role validation was called
        mock_require_director.assert_called_once_with(self.mock_director_user)
        
        # Verify database was called the expected number of times
        assert mock_db.execute.call_count == 6

    @patch('app.routers.director.require_director_role')
    @patch('app.routers.director.get_db')
    @patch('app.routers.director.get_current_user')
    def test_get_director_facets_unauthorized(self, mock_get_user, mock_get_db, mock_require_director):
        """Test director facets with unauthorized user"""
        # Mock non-director user
        mock_user = Mock()
        mock_user.id = 2
        mock_user.role = 1  # Regular user role
        
        mock_get_user.return_value = mock_user
        mock_require_director.side_effect = HTTPException(status_code=403, detail="Insufficient permissions")
        
        # Override dependencies
        self.app.dependency_overrides[get_current_user] = lambda: mock_user
        
        response = self.client.get("/facets")
        
        assert response.status_code == 403
        assert "Insufficient permissions" in response.json()["detail"]

    @patch('app.routers.director.require_director_role')
    @patch('app.routers.director.get_db')
    @patch('app.routers.director.get_current_user')
    def test_get_director_facets_no_municipality(self, mock_get_user, mock_get_db, mock_require_director):
        """Test director facets with user without municipality"""
        # Mock user without municipality
        mock_user = Mock()
        mock_user.id = 1
        mock_user.role = 3
        mock_user.municipality_id = None
        mock_user.id_municipality = None
        
        mock_get_user.return_value = mock_user
        mock_require_director.return_value = True
        
        # Mock database session
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        # Mock empty results
        mock_results = [
            AsyncMock(scalar=Mock(return_value=0)),  # total_this_month
            AsyncMock(scalar=Mock(return_value=0)),  # pending
            AsyncMock(scalar=Mock(return_value=0)),  # completed_today
            AsyncMock(scalar=Mock(return_value=0)),  # construction
            AsyncMock(scalar=Mock(return_value=0)),  # commercial
            AsyncMock(scalar=Mock(return_value=0))   # total
        ]
        
        mock_db.execute = AsyncMock(side_effect=mock_results)
        
        # Override dependencies
        self.app.dependency_overrides[get_current_user] = lambda: mock_user
        self.app.dependency_overrides[get_db] = lambda: mock_db
        
        response = self.client.get("/facets")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return zeros for all counts
        assert data["total_procedures_this_month"] == 0
        assert data["pending_procedures"] == 0
        assert data["procedures_completed_today"] == 0
        assert data["procedures_by_type"]["construction"] == 0
        assert data["procedures_by_type"]["commercial"] == 0
        assert data["procedures_by_type"]["others"] == 0

    @patch('app.routers.director.require_director_role')
    @patch('app.routers.director.get_db')
    @patch('app.routers.director.get_current_user')
    def test_get_director_facets_database_error(self, mock_get_user, mock_get_db, mock_require_director):
        """Test director facets with database error"""
        mock_get_user.return_value = self.mock_director_user
        mock_require_director.return_value = True
        
        # Mock database session that raises an error
        mock_db = AsyncMock()
        mock_db.execute = AsyncMock(side_effect=Exception("Database connection failed"))
        mock_get_db.return_value = mock_db
        
        # Override dependencies
        self.app.dependency_overrides[get_current_user] = lambda: self.mock_director_user
        self.app.dependency_overrides[get_db] = lambda: mock_db
        
        response = self.client.get("/facets")
        
        assert response.status_code == 500
        assert "Error retrieving director dashboard data" in response.json()["detail"]

    @patch('app.routers.director.require_director_role')
    @patch('app.routers.director.get_db')
    @patch('app.routers.director.get_current_user')
    def test_get_director_facets_none_results(self, mock_get_user, mock_get_db, mock_require_director):
        """Test director facets when database returns None results"""
        mock_get_user.return_value = self.mock_director_user
        mock_require_director.return_value = True

        # Mock database session
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        # Mock query results that return None (should be converted to 0)
        mock_results = [
            AsyncMock(scalar=Mock(return_value=None)),  # total_this_month
            AsyncMock(scalar=Mock(return_value=None)),  # pending
            AsyncMock(scalar=Mock(return_value=None)),  # completed_today
            AsyncMock(scalar=Mock(return_value=None)),  # construction
            AsyncMock(scalar=Mock(return_value=None)),  # commercial
            AsyncMock(scalar=Mock(return_value=None))   # total
        ]
        
        mock_db.execute = AsyncMock(side_effect=mock_results)
        
        # Override dependencies
        self.app.dependency_overrides[get_current_user] = lambda: self.mock_director_user
        self.app.dependency_overrides[get_db] = lambda: mock_db
        
        response = self.client.get("/facets")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should convert None results to 0
        assert data["total_procedures_this_month"] == 0
        assert data["pending_procedures"] == 0
        assert data["procedures_completed_today"] == 0
        assert data["procedures_by_type"]["construction"] == 0
        assert data["procedures_by_type"]["commercial"] == 0
        assert data["procedures_by_type"]["others"] == 0

    @patch('app.routers.director.require_director_role')
    @patch('app.routers.director.get_db')
    @patch('app.routers.director.get_current_user')
    def test_get_director_facets_edge_case_others_negative(self, mock_get_user, mock_get_db, mock_require_director):
        """Test director facets when others calculation would be negative"""
        mock_get_user.return_value = self.mock_director_user
        mock_require_director.return_value = True

        # Mock database session
        mock_db = AsyncMock()
        mock_get_db.return_value = mock_db
        
        # Mock results where construction + commercial > total (edge case)
        mock_results = [
            AsyncMock(scalar=Mock(return_value=10)),  # total_this_month
            AsyncMock(scalar=Mock(return_value=5)),   # pending
            AsyncMock(scalar=Mock(return_value=2)),   # completed_today
            AsyncMock(scalar=Mock(return_value=8)),   # construction
            AsyncMock(scalar=Mock(return_value=7)),   # commercial (8+7=15 > 10 total)
            AsyncMock(scalar=Mock(return_value=10))   # total
        ]
        
        mock_db.execute = AsyncMock(side_effect=mock_results)
        
        # Override dependencies
        self.app.dependency_overrides[get_current_user] = lambda: self.mock_director_user
        self.app.dependency_overrides[get_db] = lambda: mock_db
        
        response = self.client.get("/facets")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should use max(0, ...) to prevent negative others count
        assert data["procedures_by_type"]["others"] == 0  # max(0, 10-8-7) = max(0, -5) = 0

    def teardown_method(self):
        """Clean up after each test"""
        # Clear dependency overrides
        self.app.dependency_overrides.clear()
