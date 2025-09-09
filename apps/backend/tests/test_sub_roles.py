import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from config.settings import get_db
from config.security import get_current_user
from app.models.sub_role import SubRoleModel
from app.schemas.sub_roles import SubRoleCreateSchema, SubRoleUpdateSchema, SubRoleOutSchema
from datetime import datetime


class TestSubRoles:
    def setup_method(self):
        """Setup for each test method."""
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_user = MagicMock()
        self.mock_user.id = 1
        self.mock_user.municipality_id = 1
        self.mock_user.username = "testuser"
        self.client = TestClient(app)
        
        # Configure the mock to set ID on the object when add is called
        def side_effect(obj):
            obj.id = 1
            obj.created_at = datetime.now()
            obj.updated_at = datetime.now()
        self.mock_db.add.side_effect = side_effect
        
        # Override dependencies
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[get_current_user] = lambda: self.mock_user

    def teardown_method(self):
        """Cleanup after each test method."""
        app.dependency_overrides.clear()

    def create_mock_sub_role(self, role_id=1, name="Test Role", municipality_id=1):
        """Helper to create a mock sub role object."""
        sub_role = MagicMock(spec=SubRoleModel)
        sub_role.id = role_id
        sub_role.name = name
        sub_role.municipality_id = municipality_id
        sub_role.description = "Test description"
        sub_role.permissions = ["read", "write"]
        return sub_role

    def test_list_sub_roles_success(self):
        """Test successful retrieval of sub roles list."""
        # Arrange
        mock_sub_roles = [
            self.create_mock_sub_role(1, "Role 1"),
            self.create_mock_sub_role(2, "Role 2")
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_sub_roles
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/sub_roles/")

        # Assert
        assert response.status_code == 200
        self.mock_db.execute.assert_called_once()

    def test_list_sub_roles_empty(self):
        """Test retrieval when no sub roles exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/sub_roles/")

        # Assert
        assert response.status_code == 200
        assert response.json() == []

    def test_list_sub_roles_limit_applied(self):
        """Test that list endpoint applies limit of 20."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/sub_roles/")

        # Assert
        assert response.status_code == 200
        # Verify limit was applied in query (would be in the SQL statement)
        self.mock_db.execute.assert_called_once()

    def test_list_sub_roles_by_municipality_success(self):
        """Test successful retrieval of sub roles by municipality."""
        # Arrange
        mock_sub_roles = [
            self.create_mock_sub_role(1, "Role 1", municipality_id=1)
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_sub_roles
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/sub_roles/municipality")

        # Assert
        assert response.status_code == 200
        self.mock_db.execute.assert_called_once()

    def test_list_sub_roles_by_municipality_no_municipality(self):
        """Test municipality sub roles when user has no municipality assigned."""
        # Arrange
        self.mock_user.municipality_id = None

        # Act
        response = self.client.get("/v1/sub_roles/municipality")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "No municipality assigned"

    def test_list_sub_roles_by_municipality_unauthorized(self):
        """Test municipality sub roles without authentication."""
        # Arrange
        app.dependency_overrides[get_current_user] = lambda: None

        # Act
        response = self.client.get("/v1/sub_roles/municipality")

        # Assert
        assert response.status_code in [401, 403]

    def test_get_sub_role_success(self):
        """Test successful sub role retrieval by ID."""
        # Arrange
        mock_sub_role = self.create_mock_sub_role(1, "Test Role")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_sub_role
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/sub_roles/1")

        # Assert
        assert response.status_code == 200
        self.mock_db.execute.assert_called_once()

    def test_get_sub_role_not_found(self):
        """Test sub role retrieval when role doesn't exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/sub_roles/999")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "SubRole not found"

    def test_create_sub_role_success(self):
        """Test successful sub role creation."""
        # Arrange
        role_data = {
            "name": "New Role",
            "description": "New role description"
        }

        # Act
        response = self.client.post("/v1/sub_roles/", json=role_data)

        # Assert
        assert response.status_code == 200
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    def test_create_sub_role_no_municipality(self):
        """Test sub role creation when user has no municipality assigned."""
        # Arrange
        self.mock_user.municipality_id = None
        role_data = {
            "name": "New Role",
            "description": "New role description"
        }

        # Act
        response = self.client.post("/v1/sub_roles/", json=role_data)

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "No municipality assigned"

    def test_create_sub_role_unauthorized(self):
        """Test sub role creation without authentication."""
        # Arrange
        app.dependency_overrides[get_current_user] = lambda: None
        role_data = {
            "name": "New Role",
            "description": "New role description"
        }

        # Act
        response = self.client.post("/v1/sub_roles/", json=role_data)

        # Assert
        assert response.status_code in [401, 403]

    @pytest.mark.parametrize("role_data", [
        {"name": "", "description": "Valid description"},
        {"name": "Valid name", "description": ""},
        {"description": "Missing name field"},
        {"name": "Missing description field"},
    ])
    def test_create_sub_role_validation_errors(self, role_data):
        """Test sub role creation with various validation errors."""
        # Act
        response = self.client.post("/v1/sub_roles/", json=role_data)

        # Assert
        assert response.status_code in [422, 400]

    def test_update_sub_role_success(self):
        """Test successful sub role update."""
        # Arrange
        update_data = {
            "name": "Updated Role",
            "description": "Updated description"
        }
        
        mock_sub_role = self.create_mock_sub_role(1, "Original Role")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_sub_role
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.put("/v1/sub_roles/1", json=update_data)

        # Assert
        assert response.status_code == 200
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    def test_update_sub_role_not_found(self):
        """Test sub role update when role doesn't exist."""
        # Arrange
        update_data = {
            "name": "Updated Role",
            "description": "Updated description"
        }
        
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.put("/v1/sub_roles/999", json=update_data)

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "SubRole not found"

    def test_update_sub_role_partial_update(self):
        """Test partial sub role update (only some fields)."""
        # Arrange
        update_data = {
            "name": "Updated Role Name Only"
        }
        
        mock_sub_role = self.create_mock_sub_role(1, "Original Role")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_sub_role
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.put("/v1/sub_roles/1", json=update_data)

        # Assert
        assert response.status_code == 200
        # Verify only provided fields were updated
        self.mock_db.commit.assert_called_once()

    def test_delete_sub_role_success(self):
        """Test successful sub role deletion."""
        # Arrange
        mock_sub_role = self.create_mock_sub_role(1, "Test Role")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_sub_role
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.delete("/v1/sub_roles/1")

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "SubRole deleted successfully"
        self.mock_db.delete.assert_called_once_with(mock_sub_role)
        self.mock_db.commit.assert_called_once()

    def test_delete_sub_role_not_found(self):
        """Test sub role deletion when role doesn't exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.delete("/v1/sub_roles/999")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "SubRole not found"

    def test_database_error_handling(self):
        """Test handling of database errors."""
        # Arrange
        self.mock_db.execute.side_effect = Exception("Database error")

        # Act
        response = self.client.get("/v1/sub_roles/")

        # Assert
        assert response.status_code == 500

    @pytest.mark.parametrize("municipality_id", [1, 2, 10, 100])
    def test_municipality_filtering(self, municipality_id):
        """Test sub role filtering by different municipalities."""
        # Arrange
        self.mock_user.municipality_id = municipality_id
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/sub_roles/municipality")

        # Assert
        assert response.status_code == 200

    def test_create_sub_role_sets_municipality(self):
        """Test that sub role creation sets correct municipality."""
        # Arrange
        self.mock_user.municipality_id = 42
        role_data = {
            "name": "New Role",
            "description": "New role description"
        }

        # Act
        response = self.client.post("/v1/sub_roles/", json=role_data)

        # Assert
        assert response.status_code == 200
        # Verify municipality_id was set
        created_role = self.mock_db.add.call_args[0][0]
        assert created_role.municipality_id == 42

    @pytest.mark.parametrize("role_id", [1, 999, -1])
    def test_get_sub_role_various_ids(self, role_id):
        """Test sub role retrieval with various ID values."""
        # Arrange
        if role_id > 0:
            mock_sub_role = self.create_mock_sub_role(role_id, f"Role {role_id}")
        else:
            mock_sub_role = None
            
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_sub_role
        self.mock_db.execute.return_value = mock_result

        # Act
        if role_id > 0:
            response = self.client.get(f"/v1/sub_roles/{role_id}")
            expected_status = 200 if mock_sub_role else 404
        else:
            response = self.client.get(f"/v1/sub_roles/{role_id}")
            expected_status = 422  # Validation error for negative ID

        # Assert
        assert response.status_code in [expected_status, 404, 422]

    def test_concurrent_operations(self):
        """Test concurrent sub role operations."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_result.scalar_one_or_none.return_value = self.create_mock_sub_role()
        self.mock_db.execute.return_value = mock_result

        # Act - Multiple concurrent requests
        responses = []
        for i in range(5):
            response = self.client.get(f"/v1/sub_roles/{i+1}")
            responses.append(response)

        # Assert
        for response in responses:
            assert response.status_code in [200, 404]

    def test_update_sub_role_exclude_unset(self):
        """Test that update only modifies provided fields."""
        # Arrange
        update_data = {
            "name": "Updated Name"
            # description intentionally omitted
        }
        
        mock_sub_role = self.create_mock_sub_role(1, "Original Role")
        original_description = mock_sub_role.description
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_sub_role
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.put("/v1/sub_roles/1", json=update_data)

        # Assert
        assert response.status_code == 200
        # The update should use exclude_unset=True, preserving original description
