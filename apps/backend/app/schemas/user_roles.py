from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserRoleBaseSchema(ConfiguredBaseModel):
    name: str = Field(..., min_length=1, max_length=20, json_schema_extra={"example": "admin"})
    description: Optional[str] = Field(None, max_length=200, json_schema_extra={"example": "Administrator role"})
    municipality_id: Optional[int] = Field(None, json_schema_extra={"example": 1})

class UserRoleCreateSchema(ConfiguredBaseModel):
    name: str = Field(..., min_length=1, max_length=20, json_schema_extra={"example": "admin"})
    description: Optional[str] = Field(None, max_length=200, json_schema_extra={"example": "Administrator role"})
    # municipality_id is automatically set from current user, not included in create schema
    
class UserRoleUpdateSchema(ConfiguredBaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=20, json_schema_extra={"example": "admin"})
    description: Optional[str] = Field(None, max_length=200, json_schema_extra={"example": "Administrator role"})
    # municipality_id should not be updated after creation

class UserRoleResponseSchema(ConfiguredBaseModel):
    id: int
    deleted_at: Optional[datetime] = Field(None, json_schema_extra={"example": "2025-03-10T12:00:00"})
    created_at: Optional[datetime] = Field(None, json_schema_extra={"example": "2025-03-10T12:00:00"})
    updated_at: Optional[datetime] = Field(None, json_schema_extra={"example": "2025-03-10T12:00:00"})

class UserRoleOutSchema(UserRoleBaseSchema):
    id: int
    deleted_at: Optional[datetime] = Field(None, json_schema_extra={"example": "2025-03-10T12:00:00"})
    created_at: Optional[datetime] = Field(None, json_schema_extra={"example": "2025-03-10T12:00:00"})
    updated_at: Optional[datetime] = Field(None, json_schema_extra={"example": "2025-03-10T12:00:00"})

class MessageSchema(ConfiguredBaseModel):
    message: str

class AssignRoleRequestSchema(BaseModel):
    role_id: int
    
class RoleValidationResponse(ConfiguredBaseModel):
    detail: str = Field(..., json_schema_extra={"example": "Role successfully validated and assigned."})
