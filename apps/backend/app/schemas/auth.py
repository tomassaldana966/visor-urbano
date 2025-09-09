from pydantic import BaseModel, EmailStr
from .users import UserOutSchema
from typing import Optional
from fastapi import Form
from typing import Annotated

class AuthLoginSchema(BaseModel):
    email: EmailStr
    password: str

class AuthResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional[UserOutSchema] = None
            
    model_config = {
        "from_attributes": True  
    }

class OAuth2PasswordRequestFormEmail:
    """
    Custom OAuth2 form that uses 'email' instead of 'username' for better UX in Swagger UI.
    
    This class maintains OAuth2 compatibility by internally mapping the email field 
    to the standard 'username' field expected by FastAPI's authentication system.
    
    Fields:
    - email: User's email address (mapped to username for OAuth2 compatibility)
    - password: User's password
    - grant_type: OAuth2 grant type (must be "password")
    - scope: OAuth2 scopes (space-separated string)
    - client_id: Optional OAuth2 client ID
    - client_secret: Optional OAuth2 client secret
    """
    def __init__(
        self,
        email: Annotated[str, Form(description="Email address")],
        password: Annotated[str, Form(description="Password")],
        grant_type: Annotated[str, Form(pattern="^password$")] = "password",
        scope: Annotated[str, Form()] = "",
        client_id: Annotated[str, Form()] = None,
        client_secret: Annotated[str, Form()] = None,
    ):
        # OAuth2 standard requires 'username' field for compatibility with FastAPI's authenticate_user()
        # and other OAuth2-related functions that expect this specific field name
        self.username = email  
        
        # Also store as 'email' for:
        # 1. Code clarity - makes it obvious we're working with email addresses
        # 2. Future compatibility - if we need to access the email field directly
        # 3. Debugging - easier to identify the field type in logs/error messages
        self.email = email
        self.password = password
        self.grant_type = grant_type
        self.scopes = scope.split() if scope else []
        self.client_id = client_id
        self.client_secret = client_secret
