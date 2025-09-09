from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.user_roles import user_roles
import copy
from config.security import get_current_user
from config.settings import get_db

# --- Fake database session and query implementations ---
class FakeQuery:
    def __init__(self, roles):
        self.roles = roles

    def limit(self, _n):    
        return self
    def all(self):
        return self.roles

    def filter_by(self, **kwargs):
        filtered = [role for role in self.roles if all(role.get(k) == v for k, v in kwargs.items())]
        return FakeQuery(filtered)

    def first(self):
        return self.roles[0] if self.roles else None

class FakeSession:
    def __init__(self, roles):
        self.roles = roles

    def query(self, _model):    
        return FakeQuery(self.roles)
    def get(self, _model, role_id):    
        for role in self.roles:
            if role.get("id") == role_id:
                return role
        return None
    async def execute(self, _statement):
        # For our tests, we need to handle different types of queries
        statement_str = str(_statement).lower()
        
        if "filter" in statement_str and "role_id" in statement_str:
            # This is for /role_user endpoint - filter by current_user.role_id
            filtered = [role for role in self.roles if role.get("id") == FAKE_CURRENT_USER.get("role_id")]
        else:
            # This is for the simple list endpoint - return all roles
            filtered = self.roles
            
        class FakeScalars:
            def __init__(self, items):
                self.items = items

            def first(self):
                return self.items[0] if self.items else None

            def all(self):
                return self.items

        class FakeResult:
            def __init__(self, items):
                self._scalars = FakeScalars(items)

            def scalars(self):
                return self._scalars

        return FakeResult(filtered)

    def add(self, obj):
        self.roles.append(obj)

    def commit(self):
        pass

    def refresh(self, _obj):    
        pass
    def delete(self, obj):
        self.roles[:] = [role for role in self.roles if role.get("id") != obj.get("id")]

# --- Global fake data for tests ---
# A starting fake role list
FAKE_ROLES = [
    {"id": 1, "name": "Test Role", "municipality_id": 100, "user_id": 10},
    {"id": 2, "name": "Another Role", "municipality_id": 200, "user_id": 20},
]
# A valid fake current user used in many tests.
FAKE_CURRENT_USER = {
    "id": 10,
    "role_id": 1,
    "municipality_id": 100,
    "municipality_data": {"id": 100},
}

# --- Dependency override functions ---
def override_get_db():
    # Return a new FakeSession with a copy of FAKE_ROLES for each test.
    return FakeSession(copy.deepcopy(FAKE_ROLES))

def override_get_current_user():
    return FAKE_CURRENT_USER

# Create FastAPI app and include router with dependency overrides.
app = FastAPI()
app.include_router(user_roles, prefix="/user_roles")
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

# --- Tests ---

def test_list_roles():
    response = client.get("/user_roles/")
    assert response.status_code == 200
    data = response.json()
    # We expect 2 roles as configured in FAKE_ROLES limited to 20.
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == 1

