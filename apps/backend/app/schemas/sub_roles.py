from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class SubRoleBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=250, json_schema_extra={"example": "Supervisor"})
    description: str = Field(..., min_length=1, max_length=250, json_schema_extra={"example": "Oversees regional operations"})
    municipality_id: Optional[int] = Field(None, json_schema_extra={"example": 1})

class SubRoleCreateSchema(SubRoleBaseSchema):
    model_config = ConfigDict(from_attributes=True)

class SubRoleUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=250, json_schema_extra={"example": "Supervisor"})
    description: Optional[str] = Field(None, min_length=1, max_length=250, json_schema_extra={"example": "Updated description"})
    municipality_id: Optional[int] = Field(None, json_schema_extra={"example": 1})

class SubRoleOutSchema(SubRoleBaseSchema):
    id: int
    deleted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class MessageSchema(BaseModel):
    message: str

    model_config = ConfigDict(
        from_attributes=True  
    )

