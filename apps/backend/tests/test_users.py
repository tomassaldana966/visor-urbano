import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
import sys
import os
from uuid import uuid4

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.routers.users import users
from app.schemas.users import UserCreateSchema, UserUpdateSchema, UserOutSchema, MessageSchema
from app.schemas.user_roles import AssignRoleRequestSchema, RoleValidationResponse
from app.models.user import UserModel
from app.models.user_roles import UserRoleModel
from app.models.user_roles_assignments import UserRoleAssignment
from app.models.municipality import Municipality
from config.settings import get_db, get_session
from config.security import get_current_user

# Create test app
app = FastAPI()
app.include_router(users, prefix="/v1/users")

# --- Mock Data ---
FAKE_USERS = [
    {
        "id": 1,
        "name": "John",
        "paternal_last_name": "Doe",
        "maternal_last_name": "Smith",
        "cellphone": "1234567890",
        "email": "john.doe@test.com",
        "municipality_id": 1,
        "role_id": 1,
        "is_active": True,
        "api_token": None,
        "role_name": "User",
        "municipality_data": None,
        "municipality_geospatial": None
    },
    {
        "id": 2,
        "name": "Jane",
        "paternal_last_name": "Smith",
        "maternal_last_name": "Johnson",
        "cellphone": "0987654321",
        "email": "jane.smith@test.com",
        "municipality_id": 2,
        "role_id": 2,
        "is_active": True,
        "api_token": None,
        "role_name": "Admin",
        "municipality_data": None,
        "municipality_geospatial": None
    }
]

FAKE_ROLES = [
    {
        "id": 1,
        "name": "admin",
        "description": "Administrator role",
        "municipality_id": None
    },
    {
        "id": 2,
        "name": "director",
        "description": "Director role",
        "municipality_id": 1
    }
]

FAKE_MUNICIPALITIES = [
    {
        "id": 1,
        "name": "Test Municipality 1",
        "director": "John Director",
        "address": "123 Main St, Test City",
        "phone": "555-0001"
    },
    {
        "id": 2,
        "name": "Test Municipality 2",
        "director": "Jane Director",
        "address": "456 Oak Ave, Test City",
        "phone": "555-0002"
    }
]

FAKE_ROLE_ASSIGNMENTS = [
    {
        "id": 1,
        "user_id": 1,
        "role_id": 1,
        "pending_role_id": None,
        "token": None,
        "role_status": "active"
    }
]

# --- Mock Database Sessions ---
class FakeSession:
    def __init__(self, data=None):
        self.data = data if data is not None else FAKE_USERS
        self.roles_data = FAKE_ROLES
        self.municipalities_data = FAKE_MUNICIPALITIES
        self.assignments_data = FAKE_ROLE_ASSIGNMENTS
        self._committed = False
        self._refreshed_objects = []

    def get(self, model, id):
        if model == UserModel:
            user_data = next((user for user in self.data if user["id"] == id), None)
            if user_data:
                # Create a proper mock object with actual attribute values
                mock_user = Mock()
                for key, value in user_data.items():
                    setattr(mock_user, key, value)
                return mock_user
        return None

    def query(self, model):
        if model == UserModel:
            return FakeQuery(self.data)
        return FakeQuery([])

    def add(self, obj):
        # Mock adding object to session
        pass

    def delete(self, obj):
        # Mock deleting object from session
        pass

    def commit(self):
        self._committed = True

    def refresh(self, obj):
        self._refreshed_objects.append(obj)

class FakeAsyncSession:
    def __init__(self, data=None):
        self.data = data if data is not None else FAKE_USERS
        self.roles_data = FAKE_ROLES
        self.municipalities_data = FAKE_MUNICIPALITIES
        self.assignments_data = FAKE_ROLE_ASSIGNMENTS
        self._committed = False
        self._refreshed_objects = []
        self._new_user_id = 100  # For creating new users

    async def execute(self, statement):
        query_str = str(statement).lower()
        
        # Handle SQLAlchemy select statements - ORDER MATTERS: more specific checks first
        if "select" in query_str:
            # Handle user selection by email (existence check) - should return empty by default
            # Look for WHERE email = pattern, not just presence of "email" field
            if ("usermodel" in query_str or "from users" in query_str) and "where" in query_str and "email =" in query_str:
                return FakeResult([])  # No existing user by default
            # Handle user selection by ID - MUST come before municipality check
            elif ("usermodel" in query_str or "from users" in query_str) and "where" in query_str and ("id =" in query_str or "id_1" in query_str):
                return FakeResult(self.data)
            # Handle role selection by ID
            elif ("userrolemodel" in query_str or "user_roles" in query_str) and "id" in query_str and "=" in query_str:
                return FakeResult(self.roles_data)
            # Handle role assignment selection by user_id
            elif "userroleassignment" in query_str and "user_id" in query_str and "=" in query_str:
                return FakeResult(self.assignments_data)
            # Handle role assignment selection by token
            elif "userroleassignment" in query_str and "token" in query_str and "=" in query_str:
                return FakeResult(self.assignments_data)
            # Handle municipality selection by ID - MUST come after usermodel check
            elif "municipalities" in query_str and "id" in query_str and "=" in query_str:
                return FakeResult(self.municipalities_data)
        
        # Handle table-based queries (backwards compatibility)
        elif "user_model" in query_str or "users" in query_str:
            if "email" in query_str and "=" in query_str:
                return FakeResult([])  # No existing user found
            elif "id" in query_str and "=" in query_str:
                return FakeResult(self.data)
            else:
                return FakeResult(self.data)
        elif "userrolemodel" in query_str or "user_role" in query_str:
            return FakeResult(self.roles_data)
        elif "municipality" in query_str:
            return FakeResult(self.municipalities_data)
        elif "userroleassignment" in query_str or "assignment" in query_str:
            return FakeResult(self.assignments_data)
        
        return FakeResult([])

    def add(self, obj):
        # Mock adding object to session - create a proper mock user with ID
        if hasattr(obj, 'name'):  # This is likely a user
            obj.id = self._new_user_id
            self._new_user_id += 1
            # Set all the required attributes for response validation
            for key, value in FAKE_USERS[0].items():
                if not hasattr(obj, key):
                    setattr(obj, key, value)

    async def delete(self, obj):
        # Mock delete operation
        pass

    async def commit(self):
        self._committed = True

    async def refresh(self, obj):
        self._refreshed_objects.append(obj)
        # Ensure the object has all required attributes
        if hasattr(obj, 'name'):  # This is likely a user
            for key, value in FAKE_USERS[0].items():
                if not hasattr(obj, key):
                    setattr(obj, key, value)

class FakeQuery:
    def __init__(self, data):
        self.data = data

    def filter(self, *args):
        return self

    def first(self):
        if self.data:
            # Create a proper mock object with actual attribute values
            mock_user = Mock()
            for key, value in self.data[0].items():
                setattr(mock_user, key, value)
            return mock_user
        return None

class FakeResult:
    def __init__(self, data):
        self.data = data

    def scalars(self):
        return FakeScalars(self.data)

    def scalar_one_or_none(self):
        if self.data:
            # Return a simple object that acts like a model but with real values
            class SimpleUser:
                def __init__(self, data):
                    for key, value in data.items():
                        setattr(self, key, value)
            
            return SimpleUser(self.data[0])
        return None

class FakeScalars:
    def __init__(self, data):
        self.data = data

    def first(self):
        if self.data:
            # Return a simple object that acts like a model but with real values
            class SimpleObject:
                def __init__(self, data):
                    for key, value in data.items():
                        setattr(self, key, value)
            
            return SimpleObject(self.data[0])
        return None

    def all(self):
        # Return all objects as simple objects
        result = []
        for item_data in self.data:
            class SimpleObject:
                def __init__(self, data):
                    for key, value in data.items():
                        setattr(self, key, value)
            
            result.append(SimpleObject(item_data))
        return result

# --- Mock Dependency Functions ---
def get_fake_db():
    return FakeSession()

def get_fake_session():
    return FakeAsyncSession()

# --- Fake current user for authentication ---
FAKE_CURRENT_USER = {
    "id": 1,
    "name": "Test Admin",
    "email": "admin@test.com",
    "role_id": 1,
    "municipality_id": 1,
    "municipality_data": {"id": 1, "name": "Test Municipality"},
    "is_active": True
}

def get_fake_current_user():
    """Mock current user for authentication"""
    return FAKE_CURRENT_USER

def reset_dependency_overrides():
    """Reset all dependency overrides to their default fake implementations"""
    app.dependency_overrides[get_db] = get_fake_db
    app.dependency_overrides[get_session] = get_fake_session
    app.dependency_overrides[get_current_user] = get_fake_current_user

# Override dependencies
app.dependency_overrides[get_db] = get_fake_db
app.dependency_overrides[get_session] = get_fake_session
app.dependency_overrides[get_current_user] = get_fake_current_user

client = TestClient(app)

# --- Test Functions ---

def test_get_users_endpoint():
    """Test the basic users endpoint (for testing purposes only)"""
    response = client.get("/v1/users/test")
    assert response.status_code == 200
    assert response.json() == {"users": "test user"}

def test_send_email_endpoint():
    """Test the send email endpoint"""
    with patch("app.routers.users.send_email") as mock_send_email, \
         patch("app.routers.users.render_email_template") as mock_render:
        
        mock_render.return_value = "<html>Test Email</html>"
        mock_send_email.return_value = True
        
        response = client.get("/v1/users/send_email?email=test@example.com")
        assert response.status_code == 200
        assert response.json() == {"message": "Email sent successfully"}
        
        mock_render.assert_called_once()
        mock_send_email.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_success():
    """Test successful user creation"""
    with patch("config.security.get_password_hash") as mock_hash:
        mock_hash.return_value = "hashed_password_123"
        
        # Create a custom session that returns empty for email check
        def get_fake_session_for_create():
            session = FakeAsyncSession()
            original_execute = session.execute
            
            async def mock_execute(statement):
                # Always return empty for any query (no existing email)
                return FakeResult([])
            
            session.execute = mock_execute
            return session
        
        app.dependency_overrides[get_session] = get_fake_session_for_create
        
        user_data = {
            "name": "Test User",
            "paternal_last_name": "Doe",
            "maternal_last_name": "Smith",
            "cellphone": "1234567890",
            "email": "test.user@example.com",
            "municipality_id": 1,
            "role_id": 1,
            "password": "secret123"
        }
        
    response = client.post("/v1/users/", json=user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test User"
    assert data["email"] == "test.user@example.com"
    assert data["cellphone"] == "1234567890"
    
    # Reset dependency overrides
    reset_dependency_overrides()

@pytest.mark.asyncio
async def test_create_user_email_exists():
    """Test user creation with existing email"""
    # Override session to return existing user
    def get_fake_session_with_existing_user():
        session = FakeAsyncSession()
        # Override the execute method to return existing user for email check
        original_execute = session.execute

        async def mock_execute(statement):
            query_str = str(statement).lower()
            # ONLY return existing user for email existence checks
            if "email =" in query_str and "where" in query_str:
                # Return existing user for email check
                return FakeResult([{"id": 999, "email": "existing@example.com", "name": "Existing User"}])
            # For all other queries, use the original behavior
            return await original_execute(statement)

        session.execute = mock_execute
        return session

    app.dependency_overrides[get_session] = get_fake_session_with_existing_user

    user_data = {
        "name": "Test User",
        "paternal_last_name": "Doe",
        "maternal_last_name": "Smith",
        "cellphone": "1234567890",
        "email": "existing@example.com",
        "municipality_id": 1,
        "role_id": 1,
        "password": "secret123"
    }

    response = client.post("/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "User with this email already exists" in response.json()["detail"]

    # Reset dependency overrides
    reset_dependency_overrides()

def test_get_user_success():
    """Test successful user retrieval by ID"""
    response = client.get("/v1/users/1")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "John"
    assert data["email"] == "john.doe@test.com"

def test_get_user_not_found():
    """Test user retrieval with non-existent ID"""
    def get_fake_session_empty():
        session = FakeAsyncSession()
        async def mock_execute(statement):
            # Return empty for any query (no user found)
            return FakeResult([])
        session.execute = mock_execute
        return session
    
    app.dependency_overrides[get_session] = get_fake_session_empty
    
    response = client.get("/v1/users/999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
    
    # Reset dependency overrides
    reset_dependency_overrides()

def test_update_user_success():
    """Test successful user update"""
    with patch("config.security.get_password_hash") as mock_hash:
        mock_hash.return_value = "new_hashed_password"
        
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "password": "newpassword123"
        }
        
        response = client.put("/v1/users/1", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == 1

def test_update_user_not_found():
    """Test user update with non-existent ID"""
    def get_fake_session_empty():
        session = FakeAsyncSession()
        async def mock_execute(statement):
            # Return empty for any query (no user found)
            return FakeResult([])
        session.execute = mock_execute
        return session
    
    app.dependency_overrides[get_session] = get_fake_session_empty
    
    update_data = {"name": "Updated Name"}
    response = client.put("/v1/users/999", json=update_data)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
    
    # Reset dependency overrides
    reset_dependency_overrides()

def test_delete_user_success():
    """Test successful user deletion"""
    response = client.delete("/v1/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

def test_delete_user_not_found():
    """Test user deletion with non-existent ID"""
    def get_fake_session_empty():
        session = FakeAsyncSession()
        async def mock_execute(statement):
            # Return empty for any query (no user found)
            return FakeResult([])
        session.execute = mock_execute
        return session
    
    app.dependency_overrides[get_session] = get_fake_session_empty
    
    response = client.delete("/v1/users/999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
    
    # Reset dependency overrides
    reset_dependency_overrides()

@pytest.mark.asyncio
async def test_assign_role_success():
    """Test successful role assignment"""
    with patch("app.routers.users.send_email") as mock_send_email, \
         patch("app.routers.users.render_email_template") as mock_render, \
         patch("os.getenv") as mock_getenv:
        
        mock_render.return_value = "<html>Role Assignment Email</html>"
        mock_send_email.return_value = True
        mock_getenv.side_effect = lambda key, default=None: {
            "APP_FRONT": "https://test.app.com",
            "MAIL_FROM_ADDRESS": "admin@test.com"
        }.get(key, default)
        
        # Create a custom session that returns appropriate data for each query
        def get_fake_session_for_assign_role():
            session = FakeAsyncSession()
            original_execute = session.execute
            
            call_count = [0]  # Use list to modify from inner function
            
            async def mock_execute(statement):
                call_count[0] += 1
                
                if call_count[0] == 1:
                    # First call: User lookup - return user
                    return FakeResult(FAKE_USERS)
                elif call_count[0] == 2:
                    # Second call: Role lookup - return role
                    return FakeResult(FAKE_ROLES)
                elif call_count[0] == 3:
                    # Third call: Municipality lookup - return municipality
                    return FakeResult(FAKE_MUNICIPALITIES)
                elif call_count[0] == 4:
                    # Fourth call: Role assignment lookup - return empty (no existing assignment)
                    return FakeResult([])
                else:
                    # Any additional calls
                    return FakeResult([])
            
            session.execute = mock_execute
            return session
        
        app.dependency_overrides[get_session] = get_fake_session_for_assign_role
        
        role_data = {"role_id": 1}
        response = client.post("/v1/users/1/assign-role", json=role_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "detail" in data
        assert "token" in data
        assert data["detail"] == "Role assignment email sent"
        
        # Reset dependency overrides
        reset_dependency_overrides()

@pytest.mark.asyncio
async def test_assign_role_user_not_found():
    """Test role assignment with non-existent user"""
    def get_fake_session_empty():
        session = FakeAsyncSession()
        
        async def mock_execute(statement):
            # Return empty for any query (no user found)
            return FakeResult([])
        
        session.execute = mock_execute
        return session
    
    app.dependency_overrides[get_session] = get_fake_session_empty
    
    role_data = {"role_id": 1}
    response = client.post("/v1/users/999/assign-role", json=role_data)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
    
    # Reset dependency overrides
    reset_dependency_overrides()

@pytest.mark.asyncio
async def test_assign_role_role_not_found():
    """Test role assignment with non-existent role"""
    def get_fake_session_no_roles():
        session = FakeAsyncSession()
        original_execute = session.execute
        
        async def mock_execute(statement):
            query_str = str(statement).lower()
            if "userrolemodel" in query_str or "user_role" in query_str:
                # Return empty for role lookup
                return FakeResult([])
            return await original_execute(statement)
        
        session.execute = mock_execute
        return session
    
    app.dependency_overrides[get_session] = get_fake_session_no_roles
    
    role_data = {"role_id": 999}
    response = client.post("/v1/users/1/assign-role", json=role_data)
    assert response.status_code == 404
    assert "Role not found" in response.json()["detail"]
    
    # Reset dependency overrides
    reset_dependency_overrides()

@pytest.mark.asyncio
async def test_validate_user_role_success():
    """Test successful role validation"""
    with patch("app.routers.users.send_email") as mock_send_email, \
         patch("app.routers.users.render_email_template") as mock_render, \
         patch("os.getenv") as mock_getenv:
        
        mock_render.return_value = "<html>Role Confirmation Email</html>"
        mock_send_email.return_value = True
        mock_getenv.side_effect = lambda key, default=None: {
            "APP_FRONT": "https://test.app.com",
            "MAIL_FROM_ADDRESS": "admin@test.com"
        }.get(key, default)
        
        def get_fake_session_for_validate_role():
            session = FakeAsyncSession()
            original_execute = session.execute
            
            call_count = [0]  # Use list to modify from inner function
            
            async def mock_execute(statement):
                call_count[0] += 1
                
                if call_count[0] == 1:
                    # First call: Role assignment lookup by token - return pending assignment
                    return FakeResult([{
                        "id": 1,
                        "user_id": 1,
                        "role_id": None,
                        "pending_role_id": 1,
                        "token": "test-token-123",
                        "role_status": "pending"
                    }])
                elif call_count[0] == 2:
                    # Second call: User lookup - return user
                    return FakeResult(FAKE_USERS)
                elif call_count[0] == 3:
                    # Third call: Role lookup - return role
                    return FakeResult(FAKE_ROLES)
                else:
                    # Any additional calls
                    return FakeResult([])
            
            session.execute = mock_execute
            return session
        
        app.dependency_overrides[get_session] = get_fake_session_for_validate_role
        
        response = client.get("/v1/users/validate-role/test-token-123")
        assert response.status_code == 200
        
        data = response.json()
        assert data["detail"] == "Role successfully validated and assigned."
        
        # Reset dependency overrides
        reset_dependency_overrides()

@pytest.mark.asyncio
async def test_validate_user_role_token_not_found():
    """Test role validation with invalid token"""
    def get_fake_session_no_assignments():
        session = FakeAsyncSession()
        
        async def mock_execute(statement):
            query_str = str(statement).lower()
            # For assignment token queries, return empty result
            if "userroleassignment" in query_str and "token" in query_str:
                return FakeResult([])
            # For any other query, return empty as well (no users, roles, etc.)
            return FakeResult([])
        
        session.execute = mock_execute
        return session
    
    app.dependency_overrides[get_session] = get_fake_session_no_assignments
    
    response = client.get("/v1/users/validate-role/invalid-token")
    assert response.status_code == 404
    assert "Role assignment not found" in response.json()["detail"]
    
    # Reset dependency overrides
    reset_dependency_overrides()

@pytest.mark.asyncio
async def test_validate_user_role_already_validated():
    """Test role validation with already validated token"""
    def get_fake_session_with_active_assignment():
        session = FakeAsyncSession()
        
        async def mock_execute(statement):
            # Return active assignment for token lookup
            return FakeResult([{
                "id": 1,
                "user_id": 1,
                "role_id": 1,
                "pending_role_id": None,
                "token": "already-used-token",
                "role_status": "active"
            }])
        
        session.execute = mock_execute
        return session
    
    app.dependency_overrides[get_session] = get_fake_session_with_active_assignment
    
    response = client.get("/v1/users/validate-role/already-used-token")
    assert response.status_code == 400
    assert "already been validated" in response.json()["detail"]
    
    # Reset dependency override
    app.dependency_overrides[get_session] = get_fake_session

@pytest.mark.asyncio
async def test_validate_role_redirect():
    """Test role validation redirect endpoint"""
    with patch("os.getenv") as mock_getenv:
        mock_getenv.return_value = "https://test.app.com"
        
        response = client.get("/v1/users/validate-role-redirect/test-token", follow_redirects=False)
        assert response.status_code == 307  # Redirect status code
        assert "https://test.app.com/validate-role?token=test-token" in response.headers["location"]
    
