from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class UserBaseSchema(BaseModel):
    name: str
    paternal_last_name: str
    maternal_last_name: Optional[str] = None
    cellphone: str
    email: str
    municipality_id: int

class UserCreateSchema(UserBaseSchema):
    password: str
    municipality_id: int = Field(..., gt=0)
    role_id: int = Field(..., gt=0)  


class UserOutSchema(BaseModel):
    id: int
    name: str
    paternal_last_name: str
    maternal_last_name: Optional[str] = None
    cellphone: str
    email: str
    municipality_id: int
    role_id: int
    is_active: bool
    role_name: Optional[str] = "User"  # Default to "User" if no role assigned
    
    municipality_data: Optional[Dict[str, Any]] = None
    municipality_geospatial: Optional[Dict[str, Any]] = None
    
    model_config = {
        "from_attributes": True  
    }

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    paternal_last_name: Optional[str] = None
    maternal_last_name: Optional[str] = None
    cellphone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    municipality_id: Optional[int] = None
    role_id: Optional[int] = None

class MessageSchema(BaseModel):
    message: str
