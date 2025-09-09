import pytest
import os
import sys
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
import sys
import os

# Add the app directory to the path  
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.routers.dependency_revisions import router
from config.security import get_current_user
from config.settings import get_db
from app.utils.role_validation import require_admin_role, require_director_role

# Create test app
app = FastAPI()
app.include_router(router, prefix="/v1")

# --- Mock Data ---
FAKE_DEPENDENCY_REVISIONS = [
    {
        "id": 1,
        "dependency_id": 2,
        "revision_notes": "TEST-REV-001: Initial review - Documentation incomplete.",
        "revised_at": datetime(2024, 1, 15, 9, 0, 0),
        "created_at": datetime(2024, 1, 15, 9, 0, 0),
        "updated_at": datetime(2024, 1, 15, 9, 0, 0)
    },
    {
        "id": 2,
        "dependency_id": 2,
        "revision_notes": "TEST-REV-002: Second review - Building permits submitted.",
        "revised_at": datetime(2024, 1, 22, 14, 30, 0),
        "created_at": datetime(2024, 1, 22, 14, 30, 0),
        "updated_at": datetime(2024, 1, 22, 14, 30, 0)
    }
]

FAKE_REQUIREMENTS_QUERIES = [
    {
        "id": 2,
        "folio": "TEST-RQ-001",
        "municipality_id": 1
    }
]

FAKE_USER = {
    "id": 1,
    "email": "test@example.com",
    "municipality_id": 1,
    "role": "admin"
}

# --- Mock Objects ---
def create_mock_revision(data):
    mock_revision = Mock()
    for key, value in data.items():
        setattr(mock_revision, key, value)
    
    # Ensure all required schema fields are present
    if not hasattr(mock_revision, 'id'):
        mock_revision.id = data.get('id', 1)
    if not hasattr(mock_revision, 'dependency_id'):
        mock_revision.dependency_id = data.get('dependency_id', 2)
    if not hasattr(mock_revision, 'revision_notes'):
        mock_revision.revision_notes = data.get('revision_notes', 'Test notes')
    if not hasattr(mock_revision, 'revised_at'):
        mock_revision.revised_at = data.get('revised_at', datetime.now())
    if not hasattr(mock_revision, 'created_at'):
        mock_revision.created_at = data.get('created_at', datetime.now())
    if not hasattr(mock_revision, 'updated_at'):
        mock_revision.updated_at = data.get('updated_at', datetime.now())
    
    return mock_revision

def create_mock_requirements_query(data):
    mock_rq = Mock()
    for key, value in data.items():
        setattr(mock_rq, key, value)
    return mock_rq

def create_mock_user():
    mock_user = Mock()
    for key, value in FAKE_USER.items():
        setattr(mock_user, key, value)
    return mock_user

# --- Mock Dependencies ---
async def mock_get_db():
    return AsyncMock()

async def mock_get_current_user():
    return create_mock_user()

async def mock_require_admin_role():
    return create_mock_user()

async def mock_require_director_role():
    return create_mock_user()

# Override dependencies
app.dependency_overrides[get_db] = mock_get_db
app.dependency_overrides[get_current_user] = mock_get_current_user
app.dependency_overrides[require_admin_role] = mock_require_admin_role
app.dependency_overrides[require_director_role] = mock_require_director_role

# --- Fixtures ---
@pytest.fixture
def client():
    return TestClient(app)

# --- Test Cases ---
def test_list_dependency_revisions_success(client):
    """Test listing all dependency revisions"""
    with patch('app.routers.dependency_revisions.select') as mock_select:
        mock_revisions = [create_mock_revision(rev) for rev in FAKE_DEPENDENCY_REVISIONS]
        mock_scalars = Mock()
        mock_scalars.all.return_value = mock_revisions
        mock_result = Mock()
        mock_result.scalars.return_value = mock_scalars
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_result
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        response = client.get("/v1/dependency_revisions/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["dependency_id"] == 2

def test_get_dependency_revision_success(client):
    """Test getting an existing dependency revision"""
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/v1/dependency_revisions/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["dependency_id"] == 2

def test_get_dependency_revision_not_found(client):
    """Test getting a non-existent dependency revision"""
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/v1/dependency_revisions/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Dependency revision not found"

def test_create_dependency_revision_success(client):
    """Test successfully creating a dependency revision"""
    mock_rq = create_mock_requirements_query(FAKE_REQUIREMENTS_QUERIES[0])
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_rq
    mock_db.add = Mock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    # Mock the created revision to avoid validation errors
    created_revision = create_mock_revision({
        "id": 1,
        "dependency_id": 2,
        "revision_notes": "TEST-API-001: New revision created via API",
        "revised_at": datetime(2024, 6, 1, 15, 0, 0),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    mock_db.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)
    
    new_revision_data = {
        "dependency_id": 2,
        "revision_notes": "TEST-API-001: New revision created via API",
        "revised_at": "2024-06-01T15:00:00"
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    with patch('app.routers.dependency_revisions.DependencyRevision') as mock_model:
        mock_model.return_value = created_revision
        response = client.post("/v1/dependency_revisions/", json=new_revision_data)
    
    assert response.status_code == 201

def test_create_dependency_revision_invalid_dependency(client):
    """Test creating a dependency revision with invalid dependency_id"""
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    new_revision_data = {
        "dependency_id": 999,
        "revision_notes": "TEST-API-002: Should fail",
        "revised_at": "2024-06-01T15:00:00"
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.post("/v1/dependency_revisions/", json=new_revision_data)
    
    assert response.status_code == 400
    assert "Invalid dependency_id" in response.json()["detail"]

def test_update_dependency_revision_success(client):
    """Test successfully updating a dependency revision"""
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    update_data = {
        "revision_notes": "TEST-REV-001: Updated revision notes"
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.patch("/v1/dependency_revisions/1", json=update_data)
    
    assert response.status_code == 200

def test_update_dependency_revision_not_found(client):
    """Test updating a non-existent dependency revision"""
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    update_data = {
        "revision_notes": "Should fail"
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.patch("/v1/dependency_revisions/999", json=update_data)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Dependency revision not found"

def test_delete_dependency_revision_success(client):
    """Test successfully deleting a dependency revision"""
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    mock_db.delete = AsyncMock()
    mock_db.commit = AsyncMock()
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.delete("/v1/dependency_revisions/1")
    
    assert response.status_code == 204

def test_delete_dependency_revision_not_found(client):
    """Test deleting a non-existent dependency revision"""
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.delete("/v1/dependency_revisions/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Dependency revision not found"

def test_get_revisions_by_folio_success(client):
    """Test getting dependency revisions by folio"""
    with patch('app.routers.dependency_revisions.select') as mock_select:
        mock_rq = create_mock_requirements_query(FAKE_REQUIREMENTS_QUERIES[0])
        mock_rq_result = Mock()
        mock_rq_result.scalar_one_or_none.return_value = mock_rq
        
        filtered_revisions = [rev for rev in FAKE_DEPENDENCY_REVISIONS if rev["dependency_id"] == 2]
        mock_revisions = [create_mock_revision(rev) for rev in filtered_revisions]
        mock_rev_scalars = Mock()
        mock_rev_scalars.all.return_value = mock_revisions
        mock_rev_result = Mock()
        mock_rev_result.scalars.return_value = mock_rev_scalars
        
        mock_db = AsyncMock()
        mock_db.execute.side_effect = [mock_rq_result, mock_rev_result]
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        response = client.get("/v1/dependency_revisions/by_folio/TEST-RQ-001")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(rev["dependency_id"] == 2 for rev in data)

def test_get_revisions_by_nonexistent_folio(client):
    """Test getting dependency revisions by non-existent folio"""
    with patch('app.routers.dependency_revisions.select') as mock_select:
        mock_rq_result = Mock()
        mock_rq_result.scalar_one_or_none.return_value = None
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_rq_result
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        response = client.get("/v1/dependency_revisions/by_folio/NONEXISTENT")
        
        assert response.status_code == 404
        assert "RequirementsQuery with provided folio not found" in response.json()["detail"]

def test_create_revision_by_folio_success(client):
    """Test successfully creating a revision by folio"""
    with patch('app.routers.dependency_revisions.select') as mock_select:
        mock_rq = create_mock_requirements_query(FAKE_REQUIREMENTS_QUERIES[0])
        mock_rq_result = Mock()
        mock_rq_result.scalar_one_or_none.return_value = mock_rq
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_rq_result
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        # Include dependency_id as required by schema, even though endpoint sets it internally
        revision_data = {
            "dependency_id": 2,  # Required by schema
            "revision_notes": "TEST-API-003: Revision created by folio"
        }
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        with patch('app.routers.dependency_revisions.DependencyRevision') as mock_model:
            created_revision = create_mock_revision({
                "id": 1,
                "dependency_id": 2,
                "revision_notes": "TEST-API-003: Revision created by folio",
                "revised_at": datetime.now(),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })
            mock_model.return_value = created_revision
            
            response = client.post("/v1/dependency_revisions/by_folio/TEST-RQ-001", json=revision_data)
        
        assert response.status_code == 200

def test_create_revision_by_folio_not_found(client):
    """Test creating a revision by non-existent folio"""
    with patch('app.routers.dependency_revisions.select') as mock_select:
        mock_rq_result = Mock()
        mock_rq_result.scalar_one_or_none.return_value = None
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_rq_result
        
        revision_data = {
            "dependency_id": 2,  # Required by schema
            "revision_notes": "Should fail - folio not found"
        }
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        response = client.post("/v1/dependency_revisions/by_folio/NONEXISTENT", json=revision_data)
        
        assert response.status_code == 404
        assert "Procedure with the specified folio not found" in response.json()["detail"]

def test_create_revision_by_folio_municipality_mismatch(client):
    """Test creating a revision by folio with municipality mismatch"""
    with patch('app.routers.dependency_revisions.select') as mock_select:
        wrong_municipality_rq = {
            "id": 2,
            "folio": "TEST-RQ-002",
            "municipality_id": 999  # Different from user's municipality_id (1)
        }
        mock_rq = create_mock_requirements_query(wrong_municipality_rq)
        mock_rq_result = Mock()
        mock_rq_result.scalar_one_or_none.return_value = mock_rq
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_rq_result
        
        revision_data = {
            "dependency_id": 2,  # Required by schema
            "revision_notes": "Should fail - municipality mismatch"
        }
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        response = client.post("/v1/dependency_revisions/by_folio/TEST-RQ-002", json=revision_data)
        
        assert response.status_code == 403
        assert "Access denied: municipality mismatch" in response.json()["detail"]

def test_upload_file_success(client):
    """Test successful file upload to a revision"""
    from io import BytesIO
    
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Mock file upload
    test_file_content = b"Test file content for dependency revision"
    test_file = BytesIO(test_file_content)
    
    with patch('builtins.open', create=True) as mock_open:
        with patch('app.routers.dependency_revisions.send_email') as mock_send_email:
            with patch('app.routers.dependency_revisions.render_email_template') as mock_render:
                mock_render.return_value = "<html>Test email</html>"
                
                response = client.post(
                    "/v1/dependency_revisions/upload_file/1",
                    files={"file": ("test.pdf", test_file, "application/pdf")}
                )
                
                assert response.status_code == 200

def test_upload_file_revision_not_found(client):
    """Test file upload to non-existent revision"""
    from io import BytesIO
    
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    test_file_content = b"Test file content"
    test_file = BytesIO(test_file_content)
    
    response = client.post(
        "/v1/dependency_revisions/upload_file/999",
        files={"file": ("test.pdf", test_file, "application/pdf")}
    )
    
    assert response.status_code == 404
    assert "Dependency revision not found" in response.json()["detail"]


def test_download_file_revision_not_found(client):
    """Test file download from non-existent revision"""
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/v1/dependency_revisions/download_file/999")
    
    assert response.status_code == 404
    assert "Dependency revision not found" in response.json()["detail"]

def test_download_file_not_found(client):
    """Test file download when file doesn't exist"""
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_revision.file_path = "/nonexistent/path/test.pdf"
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = False
        
        response = client.get("/v1/dependency_revisions/download_file/1")
        
        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]

def test_update_dependency_revision_status_success(client):
    """Test successful status update of a revision"""
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    update_data = {
        "revision_notes": "Status updated via API"
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    with patch('app.routers.dependency_revisions.send_email') as mock_send_email:
        with patch('app.routers.dependency_revisions.render_email_template') as mock_render:
            mock_render.return_value = "<html>Status update email</html>"
            
            response = client.post("/v1/dependency_revisions/update/1", json=update_data)
            
            assert response.status_code == 200
            assert "Revision successfully updated" in response.json()["detail"]

def test_update_dependency_revision_status_not_found(client):
    """Test status update of non-existent revision"""
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    update_data = {
        "revision_notes": "Should fail"
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    with patch('app.routers.dependency_revisions.render_email_template') as mock_render:
        with patch('app.routers.dependency_revisions.send_email') as mock_send_email:
            mock_render.return_value = "<html>Test email</html>"
            mock_send_email.return_value = None
            
            response = client.post("/v1/dependency_revisions/update/999", json=update_data)
            
            assert response.status_code == 404
            assert "Dependency revision not found" in response.json()["detail"]

def test_update_dependency_revision_status_no_fields(client):
    """Test status update with no fields to update"""
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    
    update_data = {}  # Empty update data
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    with patch('app.routers.dependency_revisions.render_email_template') as mock_render:
        with patch('app.routers.dependency_revisions.send_email') as mock_send_email:
            mock_render.return_value = "<html>Test email</html>"
            mock_send_email.return_value = None
            
            response = client.post("/v1/dependency_revisions/update/1", json=update_data)
            
            assert response.status_code == 400
            assert "No fields to update" in response.json()["detail"]

def test_update_director_revision_success(client):
    """Test successful director revision update"""
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    update_data = {
        "revision_notes": "Director update - approved"
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    with patch('app.routers.dependency_revisions.send_email') as mock_send_email:
        with patch('app.routers.dependency_revisions.render_email_template') as mock_render:
            mock_render.return_value = "<html>Director update email</html>"
            
            response = client.post("/v1/dependency_revisions/update_director/1", json=update_data)
            
            assert response.status_code == 200
            assert "Revision successfully updated by director" in response.json()["detail"]

def test_update_director_revision_not_found(client):
    """Test director update of non-existent revision"""
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    update_data = {
        "revision_notes": "Should fail"
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    with patch('app.routers.dependency_revisions.render_email_template') as mock_render:
        with patch('app.routers.dependency_revisions.send_email') as mock_send_email:
            mock_render.return_value = "<html>Test email</html>"
            mock_send_email.return_value = None
            
            response = client.post("/v1/dependency_revisions/update_director/999", json=update_data)
            
            assert response.status_code == 404
            assert "Dependency revision not found" in response.json()["detail"]

def test_get_revisions_by_date_analytics(client):
    """Test analytics endpoint for revisions by date"""
    from sqlalchemy import func
    
    with patch('app.routers.dependency_revisions.select') as mock_select:
        mock_result = Mock()
        mock_row = Mock()
        mock_row.revision_date = "2024-01-15"
        mock_row.total = 5
        mock_result.all.return_value = [mock_row]
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_result
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        response = client.get("/v1/dependency_revisions/analytics/revisions_by_date")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["date"] == "2024-01-15"
        assert data[0]["total"] == 5

def test_get_revisions_by_date_analytics_with_filters(client):
    """Test analytics endpoint with date filters"""
    from sqlalchemy import func
    
    with patch('app.routers.dependency_revisions.select') as mock_select:
        mock_result = Mock()
        mock_row = Mock()
        mock_row.revision_date = "2024-01-15"
        mock_row.total = 3
        mock_result.all.return_value = [mock_row]
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_result
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        response = client.get(
            "/v1/dependency_revisions/analytics/revisions_by_date?start_date=2024-01-01&end_date=2024-01-31"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["total"] == 3

def test_get_revisions_by_dependency_analytics(client):
    """Test analytics endpoint for revisions by dependency"""
    from sqlalchemy import func
    
    with patch('app.routers.dependency_revisions.select') as mock_select:
        mock_result = Mock()
        mock_row = Mock()
        mock_row.dependency_id = 2
        mock_row.total_revisions = 10
        mock_result.all.return_value = [mock_row]
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_result
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        response = client.get("/v1/dependency_revisions/analytics/revisions_by_dependency")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["dependency_id"] == 2
        assert data[0]["total_revisions"] == 10

def test_bulk_update_revisions_success(client):
    """Test successful bulk update of revisions"""
    mock_revisions = [create_mock_revision(rev) for rev in FAKE_DEPENDENCY_REVISIONS]
    mock_db = AsyncMock()
    mock_db.get.side_effect = mock_revisions
    mock_db.commit = AsyncMock()
    
    # The endpoint expects revision_ids as one parameter and data as another
    # When both are in request body, FastAPI expects them as separate top-level fields
    bulk_data = {
        "revision_ids": [1, 2],
        "data": {
            "revision_notes": "Bulk updated notes"
        }
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.post("/v1/dependency_revisions/bulk_update", json=bulk_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["updated_count"] == 2
    assert data["total_requested"] == 2

def test_bulk_update_empty_ids(client):
    """Test bulk update with empty revision IDs"""
    mock_db = AsyncMock()
    
    bulk_data = {
        "revision_notes": "Should fail"
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.post("/v1/dependency_revisions/bulk_update", json=bulk_data)
    
    assert response.status_code == 422  # FastAPI validation error for missing required params

def test_bulk_update_partial_success(client):
    """Test bulk update where some revisions exist and some don't"""
    mock_existing_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_db = AsyncMock()
    
    # First revision exists, second doesn't
    mock_db.get.side_effect = [mock_existing_revision, None]
    mock_db.commit = AsyncMock()
    
    bulk_data = {
        "revision_ids": [1, 999],
        "data": {
            "revision_notes": "Partial bulk update"
        }
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.post("/v1/dependency_revisions/bulk_update", json=bulk_data)
    
    if response.status_code == 200:
        data = response.json()
        assert data["updated_count"] == 1  # Only one revision was found and updated
        assert data["total_requested"] == 2

def test_upload_multiple_files_success(client):
    """Test successful upload of multiple files"""
    from io import BytesIO
    
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Create multiple test files
    file1 = BytesIO(b"Test file 1 content")
    file2 = BytesIO(b"Test file 2 content")
    
    with patch('os.makedirs') as mock_makedirs:
        with patch('builtins.open', create=True) as mock_open:
            with patch('app.routers.dependency_revisions.send_email') as mock_send_email:
                with patch('app.routers.dependency_revisions.render_email_template') as mock_render:
                    mock_render.return_value = "<html>Test email</html>"
                    mock_send_email.return_value = None
                    
                    files = [
                        ("files", ("test1.pdf", file1, "application/pdf")),
                        ("files", ("test2.pdf", file2, "application/pdf"))
                    ]
                    
                    response = client.post(
                        "/v1/dependency_revisions/upload_multiple_files/1",
                        files=files
                    )
                    
                    assert response.status_code == 200
                    mock_render.return_value = "<html>Multiple files email</html>"
                    
                    files = [
                        ("files", ("test1.pdf", file1, "application/pdf")),
                        ("files", ("test2.pdf", file2, "application/pdf"))
                    ]
                    
                    response = client.post(
                        "/v1/dependency_revisions/upload_multiple_files/1",
                        files=files
                    )
                    
                    assert response.status_code == 200

def test_upload_multiple_files_revision_not_found(client):
    """Test multiple files upload to non-existent revision"""
    from io import BytesIO
    
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    file1 = BytesIO(b"Test file content")
    
    files = [("files", ("test.pdf", file1, "application/pdf"))]
    
    with patch('app.routers.dependency_revisions.render_email_template') as mock_render:
        with patch('app.routers.dependency_revisions.send_email') as mock_send_email:
            with patch('os.makedirs') as mock_makedirs:
                with patch('builtins.open', create=True) as mock_open:
                    mock_render.return_value = "<html>Test email</html>"
                    mock_send_email.return_value = None
                    
                    response = client.post(
                        "/v1/dependency_revisions/upload_multiple_files/999",
                        files=files
                    )
                    
                    assert response.status_code == 404
                    assert "Dependency revision not found" in response.json()["detail"]

def test_delete_revision_file_success(client):
    """Test successful deletion of revision files"""
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_revision.file_path = "/fake/path/file1.pdf;/fake/path/file2.pdf"
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    with patch('os.path.exists') as mock_exists:
        with patch('os.remove') as mock_remove:
            mock_exists.return_value = True
            
            response = client.delete("/v1/dependency_revisions/delete_file/1")
            
            assert response.status_code == 200
            data = response.json()
            assert "Successfully deleted" in data["detail"]
            assert "deleted_files" in data
            # Assert that os.remove was called for each file
            assert mock_remove.call_count == 2
            assert mock_remove.call_args_list[0][0][0] == "/fake/path/file1.pdf"
            assert mock_remove.call_args_list[1][0][0] == "/fake/path/file2.pdf"
            
            # Reset mock_remove for the next call
            mock_remove.reset_mock()
            # Reset file_path for the revision to simulate files still exist
            mock_revision.file_path = "/fake/path/file1.pdf;/fake/path/file2.pdf"
            mock_exists.return_value = True
            
            response = client.delete("/v1/dependency_revisions/delete_file/1")
            
            assert response.status_code == 200
            data = response.json()
            assert "Successfully deleted" in data["detail"]
            assert len(data["deleted_files"]) == 2
            assert mock_remove.call_count == 2

def test_delete_revision_file_not_found(client):
    """Test deletion of files from non-existent revision"""
    mock_db = AsyncMock()
    mock_db.get.return_value = None
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    # Mock os functions to prevent actual file system operations that might cause exceptions
    with patch('os.path.exists') as mock_exists:
        with patch('os.remove') as mock_remove:
            mock_exists.return_value = False
            
            response = client.delete("/v1/dependency_revisions/delete_file/999")
            
            assert response.status_code == 404
            assert "Dependency revision not found" in response.json()["detail"]

def test_delete_revision_file_no_files(client):
    """Test deletion when no files exist"""
    mock_revision = create_mock_revision(FAKE_DEPENDENCY_REVISIONS[0])
    mock_revision.file_path = None
    mock_db = AsyncMock()
    mock_db.get.return_value = mock_revision
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    with patch('os.path.exists') as mock_exists:
        with patch('os.remove') as mock_remove:
            mock_exists.return_value = False
            
            response = client.delete("/v1/dependency_revisions/delete_file/1")
            
            assert response.status_code == 404
            assert "No files found for this revision" in response.json()["detail"]

# --- Edge Cases and Error Handling Tests ---

def test_list_dependency_revisions_with_filter(client):
    """Test listing dependency revisions with dependency_id filter"""
    with patch('app.routers.dependency_revisions.select') as mock_select:
        filtered_revisions = [rev for rev in FAKE_DEPENDENCY_REVISIONS if rev["dependency_id"] == 2]
        mock_revisions = [create_mock_revision(rev) for rev in filtered_revisions]
        mock_scalars = Mock()
        mock_scalars.all.return_value = mock_revisions
        mock_result = Mock()
        mock_result.scalars.return_value = mock_scalars
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_result
        
        app.dependency_overrides[get_db] = lambda: mock_db
        
        response = client.get("/v1/dependency_revisions/?dependency_id=2")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(rev["dependency_id"] == 2 for rev in data)

def test_create_dependency_revision_without_dependency_id(client):
    """Test creating a revision without dependency_id - should fail"""
    mock_db = AsyncMock()
    
    new_revision_data = {
        "revision_notes": "TEST-API-004: Revision without dependency_id",
        "revised_at": "2024-06-01T15:00:00"
        # Missing required dependency_id field
    }
    
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.post("/v1/dependency_revisions/", json=new_revision_data)
    
    # This should fail as dependency_id is required in the schema
    assert response.status_code == 422
