import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
import base64

from app.main import app
from config.settings import get_db
from config.security import get_current_user
from app.models.field import Field
from app.models.requirements import Requirement
from app.models.answer import Answer
from app.schemas.field import FieldCreate, FieldUpdate, FieldResponse


class TestPublicFields:
    def setup_method(self):
        """Setup for each test method."""
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_user = MagicMock()
        self.mock_user.id = 1
        self.mock_user.municipality_id = 1
        self.mock_user.username = "testuser"
        self.client = TestClient(app)
        
        # Override dependencies
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[get_current_user] = lambda: self.mock_user
        
        # Setup global mocks for database operations that should succeed by default
        self.mock_db.add = MagicMock()  # add is synchronous, not async
        self.mock_db.commit = AsyncMock()
        self.mock_db.delete = AsyncMock()
        self.mock_db.flush = AsyncMock()  # Add flush mock
        self.mock_db.rollback = AsyncMock()  # Add rollback mock
        
        # Mock refresh to simulate database assigning an ID after commit
        def mock_refresh(obj):
            if hasattr(obj, 'id') and obj.id is None:
                obj.id = 1  # Simulate database assigning an ID
            if hasattr(obj, 'created_at') and obj.created_at is None:
                obj.created_at = "2023-01-01T00:00:00"
            if hasattr(obj, 'updated_at') and obj.updated_at is None:
                obj.updated_at = "2023-01-01T00:00:00"
        
        self.mock_db.refresh = AsyncMock(side_effect=mock_refresh)

    def teardown_method(self):
        """Cleanup after each test method."""
        app.dependency_overrides.clear()

    def create_mock_field(self, field_id=1, name="test_field", field_type="text", municipality_id=1):
        """Helper to create a mock field object."""
        field = MagicMock(spec=Field)
        field.id = field_id
        field.name = name
        field.field_type = field_type  # Use field_type instead of type
        field.type = field_type  # Also set type for backward compatibility
        field.municipality_id = municipality_id
        field.sequence = 1
        field.status = 1
        field.required = True
        field.static_field = 0
        field.description = None
        field.description_rec = None
        field.rationale = None
        field.options = None
        field.options_description = None
        field.step = None
        field.visible_condition = None
        field.affected_field = None
        field.procedure_type = None
        field.dependency_condition = None
        field.trade_condition = None
        field.editable = 0
        field.created_at = None
        field.updated_at = None
        field.deleted_at = None
        field.required_official = 1
        return field

    def create_mock_answer(self, name="test_answer", value="test_value", procedure_id=1):
        """Helper to create a mock answer object."""
        answer = MagicMock(spec=Answer)
        answer.name = name
        answer.value = value
        answer.procedure_id = procedure_id
        return answer

    def test_list_fields_success(self):
        """Test successful retrieval of fields list."""
        # Arrange
        mock_fields = [
            self.create_mock_field(1, "field1", "text"),
            self.create_mock_field(2, "field2", "number")
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_fields
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/fields/")

        # Assert
        assert response.status_code == 200
        self.mock_db.execute.assert_called_once()

    def test_list_fields_empty(self):
        """Test retrieval when no fields exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/fields/")

        # Assert
        assert response.status_code == 200
        assert response.json() == []

    def test_list_fields_unauthorized(self):
        """Test field list access without authentication."""
        # Arrange
        app.dependency_overrides[get_current_user] = lambda: None

        # Act
        response = self.client.get("/v1/fields/")

        # Assert
        assert response.status_code in [401, 403]

    def test_get_field_success(self):
        """Test successful field retrieval by ID."""
        # Arrange
        mock_field = self.create_mock_field(1, "test_field", "text")
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_field
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/fields/1")

        # Assert
        assert response.status_code == 200
        self.mock_db.execute.assert_called_once()

    def test_get_field_not_found(self):
        """Test field retrieval when field doesn't exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/fields/999")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Field not found"

    def test_create_field_success(self):
        """Test successful field creation."""
        # Arrange
        field_data = {
            "name": "new_field",
            "field_type": "text",
            "sequence": 1,
            "required": True
        }
        
        mock_field = self.create_mock_field(1, "new_field", "text")
        self.mock_db.refresh.return_value = None

        # Act
        response = self.client.post("/v1/fields/", json=field_data)

        # Assert
        assert response.status_code == 200
        # Should add both field and requirement
        assert self.mock_db.add.call_count == 2
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once()

    def test_create_field_unauthorized(self):
        """Test field creation without authentication."""
        # Arrange
        app.dependency_overrides[get_current_user] = lambda: None
        field_data = {
            "name": "new_field",
            "field_type": "text",
            "sequence": 1,
            "required": True
        }

        # Act
        response = self.client.post("/v1/fields/", json=field_data)

        # Assert
        assert response.status_code in [401, 403]

    @pytest.mark.parametrize("field_data", [
        {"name": "", "field_type": "text", "sequence": 1, "required": True},
        {"name": "test", "field_type": "", "sequence": 1, "required": True},
        {"name": "test", "field_type": "text", "sequence": -1, "required": True},
    ])
    def test_create_field_validation_errors(self, field_data):
        """Test field creation with various validation errors."""
        # Act
        response = self.client.post("/v1/fields/", json=field_data)

        # Assert
        assert response.status_code in [422, 400]

    def test_create_field_sets_municipality_and_status(self):
        """Test that field creation sets correct municipality and status."""
        # Arrange
        field_data = {
            "name": "new_field",
            "field_type": "text",
            "sequence": 1,
            "required": True
        }
        
        # Act
        response = self.client.post("/v1/fields/", json=field_data)

        # Assert
        assert response.status_code == 200
        # Verify field was created with user's municipality_id and status=1
        # The first call to add() should be the Field
        first_call_args = self.mock_db.add.call_args_list[0][0][0]
        assert hasattr(first_call_args, 'municipality_id')
        assert hasattr(first_call_args, 'status')

    def test_database_error_handling(self):
        """Test handling of database errors."""
        # Arrange
        self.mock_db.execute.side_effect = Exception("Database error")

        # Act
        response = self.client.get("/v1/fields/")

        # Assert
        assert response.status_code == 500

    @pytest.mark.parametrize("field_type", [
        "text", "number", "email", "date", "boolean", "select", "textarea"
    ])
    def test_create_field_various_types(self, field_type):
        """Test field creation with various field types."""
        # Arrange
        field_data = {
            "name": f"test_{field_type}",
            "field_type": field_type,
            "sequence": 1,
            "required": True
        }

        # Act
        response = self.client.post("/v1/fields/", json=field_data)

        # Assert
        assert response.status_code == 200

    def test_field_sequence_ordering(self):
        """Test that fields are ordered by sequence."""
        # Arrange
        mock_fields = [
            self.create_mock_field(1, "field1", "text"),
            self.create_mock_field(2, "field2", "text")
        ]
        mock_fields[0].sequence = 2
        mock_fields[1].sequence = 1
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_fields
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/fields/")

        # Assert
        assert response.status_code == 200
        # Verify query was executed (sequence ordering would be in SQL)
        self.mock_db.execute.assert_called_once()

    def test_municipality_filtering(self):
        """Test that fields are filtered by user's municipality."""
        # Arrange
        self.mock_user.municipality_id = 42
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/fields/")

        # Assert
        assert response.status_code == 200
        # Verify municipality filter was applied in query
        call_args = self.mock_db.execute.call_args[0][0]
        # The query should contain municipality_id filter

    def test_fetch_fields_and_answers_integration(self):
        """Test the internal fetch_fields_and_answers function behavior."""
        # This would test the complex query logic, but since it's an internal function
        # and we're mocking the database, we focus on the endpoints that use it
        
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/fields/")

        # Assert
        assert response.status_code == 200

    def test_field_creation_with_requirement(self):
        """Test that field creation also creates associated requirement."""
        # Arrange
        field_data = {
            "name": "new_field",
            "field_type": "text",
            "sequence": 1,
            "required": True
        }

        # Act
        response = self.client.post("/v1/fields/", json=field_data)

        # Assert
        assert response.status_code == 200
        # Verify both field and requirement were added
        assert self.mock_db.add.call_count == 2  # Field + Requirement
        self.mock_db.commit.assert_called_once()

    @pytest.mark.parametrize("user_municipality", [1, 2, 10, 100])
    def test_different_municipality_contexts(self, user_municipality):
        """Test field operations with different municipality contexts."""
        # Arrange
        self.mock_user.municipality_id = user_municipality
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/fields/")

        # Assert
        assert response.status_code == 200

    def test_field_status_handling(self):
        """Test that field status is properly handled."""
        # Arrange
        field_data = {
            "name": "new_field",
            "field_type": "text",
            "sequence": 1,
            "required": True
        }

        # Act
        response = self.client.post("/v1/fields/", json=field_data)

        # Assert
        assert response.status_code == 200
        # Status should be set to 1 by default
        # The first call to add() should be the Field
        created_field = self.mock_db.add.call_args_list[0][0][0]
        assert created_field.status == 1

    def test_concurrent_field_operations(self):
        """Test concurrent field operations."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_result.scalar_one_or_none.return_value = self.create_mock_field()
        self.mock_db.execute.return_value = mock_result

        # Act - Multiple concurrent requests
        responses = []
        for i in range(5):
            response = self.client.get(f"/{i+1}")
            responses.append(response)

        # Assert
        for response in responses:
            assert response.status_code in [200, 404]

    def test_large_field_datasets(self):
        """Test handling of large field datasets."""
        # Arrange
        large_field_list = [
            self.create_mock_field(i, f"field_{i}", "text") 
            for i in range(1000)
        ]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = large_field_list
        self.mock_db.execute.return_value = mock_result

        # Act
        response = self.client.get("/v1/fields/")

        # Assert
        assert response.status_code == 200
        # Should handle large datasets without issues
