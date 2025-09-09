from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class BusinessTypeBase(BaseModel):
    """Base schema for business types"""
    name: str = Field(..., max_length=255, description="Business type name")
    description: Optional[str] = Field(None, max_length=500, description="Business type description")
    is_active: Optional[bool] = Field(True, description="Whether the business type is active")
    code: Optional[str] = Field(None, max_length=50, description="SCIAN code")
    related_words: Optional[str] = Field(None, max_length=500, description="Related keywords")

class BusinessTypeCreate(BusinessTypeBase):
    """Schema for creating a business type"""
    model_config = ConfigDict(from_attributes=True)

class BusinessTypeUpdate(BusinessTypeBase):
    """Schema for updating a business type"""
    name: Optional[str] = Field(None, max_length=255, description="Business type name")
    
    model_config = ConfigDict(from_attributes=True)

class BusinessTypeResponse(BusinessTypeBase):
    """Response schema for business types"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class BusinessTypeDisable(BaseModel):
    """Schema for disabling a business type"""
    business_type_id: int
    municipality_id: int
    
    model_config = ConfigDict(from_attributes=True)
