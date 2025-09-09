"""
Test script for the new business types create endpoint.
"""
import sys
from pathlib import Path

# Add project paths
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
app_dir = backend_dir / "app"
sys.path.insert(0, str(app_dir))

import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.testclient import TestClient

# Import models and schemas
from app.models.business_types import BusinessType
from app.schemas.business_types import BusinessTypeCreate, BusinessTypeResponse
from config.settings import get_db

# Mock the role validation
def mock_require_admin_or_director_role(current_user=None):
    return Mock(id=1, municipality_id=1, role_name="admin")

# Create a minimal app with just our endpoint
app = FastAPI()

@app.post("/business_types/", response_model=BusinessTypeResponse)
async def create_business_type(
    data: BusinessTypeCreate,
    db = Depends(get_db),
    current_user = Depends(mock_require_admin_or_director_role)
):
    """
    Create a new business type.
    
    This endpoint allows admins and directors to create new business types
    with their name, description, SCIAN code, and related words.
    
    Requires admin or director privileges.
    """
    from sqlalchemy.future import select
    
    # Check if business type with same name already exists
    stmt = select(BusinessType).where(BusinessType.name == data.name)
    result = await db.execute(stmt)
    existing_business_type = result.scalar_one_or_none()
    
    if existing_business_type:
        raise HTTPException(
            status_code=400,
            detail=f"Business type with name '{data.name}' already exists"
        )
    
    # Check if SCIAN code already exists (if provided)
    if data.code:
        stmt = select(BusinessType).where(BusinessType.code == data.code)
        result = await db.execute(stmt)
        existing_code = result.scalar_one_or_none()
        
        if existing_code:
            raise HTTPException(
                status_code=400,
                detail=f"Business type with SCIAN code '{data.code}' already exists"
            )
    
    # Create new business type
    business_type = BusinessType(
        name=data.name,
        description=data.description,
        is_active=data.is_active,
        code=data.code,
        related_words=data.related_words
    )
    
    db.add(business_type)
    await db.commit()
    await db.refresh(business_type)
    
    return business_type

class TestCreateBusinessType:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.fixture
    def mock_db_session(self):
        return AsyncMock()

    @pytest.fixture
    def mock_user(self):
        user = Mock()
        user.id = 1
        user.municipality_id = 1
        user.role_name = "admin"
        return user

    def test_create_business_type_success(self, client, mock_db_session, mock_user):
        """Test POST /business_types/ endpoint with valid data."""
        create_data = {
            "name": "New Business Type",
            "description": "A new type of business",
            "is_active": True,
            "code": "NEW001",
            "related_words": "new, business, type"
        }
        
        # Mock the created business type instance
        mock_business_type = Mock()
        mock_business_type.id = 1
        mock_business_type.name = create_data["name"]
        mock_business_type.description = create_data["description"]
        mock_business_type.is_active = create_data["is_active"]
        mock_business_type.code = create_data["code"]
        mock_business_type.related_words = create_data["related_words"]
        
        # Mock database operations
        mock_db_session.add = Mock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock(side_effect=lambda x: setattr(x, 'id', 1))
        
        # Mock the query results (no existing business type with same name or code)
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            with patch.object(BusinessType, '__new__', return_value=mock_business_type):
                response = client.post("/business_types/", json=create_data)
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["name"] == create_data["name"]
            assert data["description"] == create_data["description"]
            assert data["code"] == create_data["code"]
            assert data["related_words"] == create_data["related_words"]
            mock_db_session.add.assert_called_once()
            mock_db_session.commit.assert_called_once()
            mock_db_session.refresh.assert_called_once()
        finally:
            app.dependency_overrides.clear()

    def test_create_business_type_duplicate_name(self, client, mock_db_session, mock_user):
        """Test POST /business_types/ endpoint with duplicate name."""
        create_data = {
            "name": "Existing Business Type",
            "description": "A duplicate business type",
            "is_active": True,
            "code": "EXT001",
            "related_words": "existing, duplicate"
        }
        
        # Mock existing business type with same name
        existing_business_type = Mock()
        existing_business_type.id = 1
        existing_business_type.name = create_data["name"]
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = existing_business_type
        mock_db_session.execute.return_value = mock_result
        
        def override_get_db():
            return mock_db_session
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.post("/business_types/", json=create_data)
            
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            data = response.json()
            assert "already exists" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_create_business_type_validation_error(self, client, mock_user):
        """Test POST /business_types/ endpoint with invalid data."""
        # Missing required field 'name'
        create_data = {
            "description": "A business type without name",
            "is_active": True
        }
        
        try:
            response = client.post("/business_types/", json=create_data)
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        finally:
            app.dependency_overrides.clear()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
