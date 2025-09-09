from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class DependencyResolutionBase(BaseModel):
    procedure_id: int
    role: Optional[int] = None
    user_id: Optional[int] = None
    resolution_status: Optional[int] = None
    resolution_text: Optional[str] = None
    resolution_file: Optional[str] = None
    signature: Optional[str] = None


class DependencyResolutionCreate(DependencyResolutionBase):
    pass


class DependencyResolutionUpdate(BaseModel):
    resolution_status: Optional[int] = None
    resolution_text: Optional[str] = None
    resolution_file: Optional[str] = None
    signature: Optional[str] = None


class DependencyResolutionResponse(DependencyResolutionBase):
    id: int
    procedure_id: int
    role: int
    user_id: int
    resolution_status: int
    resolution_text: Optional[str]
    resolution_file: Optional[str]
    signature: Optional[str]
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    review_id: int
    additional_files: Optional[str]
    is_final_resolution: bool
    user_name: Optional[str] = None  # Agregado para exponer el nombre completo del usuario

    model_config = ConfigDict(from_attributes=True)
