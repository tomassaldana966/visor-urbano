from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class RequirementBase(BaseModel):
    municipality_id: int
    field_id: int
    requirement_code: Optional[str] = Field(None, max_length=300)

class RequirementCreate(RequirementBase):
    model_config = ConfigDict(from_attributes=True)

class RequirementUpdate(RequirementBase):
    municipality_id: Optional[int] = None
    field_id: Optional[int] = None

class RequirementResponse(RequirementBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class RequirementValidationUpdate(BaseModel):
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)

class FolioValidationResponse(BaseModel):
    id: int
    folio: str
    municipality_id: int
    municipality_name: str
    street: str
    neighborhood: str
    scian_code: str
    scian_name: str
    property_area: float
    activity_area: float
    applicant_name: Optional[str] = None
    applicant_character: Optional[str] = None
    person_type: Optional[str] = None
    status: int
    user_id: int
    alcohol_sales: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
