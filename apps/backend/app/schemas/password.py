from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class PasswordResetRequestSchema(BaseModel):
    """
    Used to request a password reset link via email.
    """
    email: EmailStr = Field(..., description="User's email address")


class PasswordResetResponseSchema(BaseModel):
    """
    Response schema for password reset requests.
    """
    detail: str = Field(..., description="Response message")
    success: bool = Field(..., description="Whether the operation was successful")


class PasswordResetSchema(BaseModel):
    """
    Used to reset the password using a token.
    """
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="New password")
    token: str = Field(..., description="Password recovery token")


class AuthenticatedPasswordChangeSchema(BaseModel):
    """
    Used to change password by a logged-in user.
    """
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
