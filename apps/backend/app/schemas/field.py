from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, ConfigDict, Field, validator

class FieldBase(BaseModel):
    name: str = Field(..., min_length=1, description="Field name cannot be empty")
    field_type: str = Field(..., min_length=1, description="Field type cannot be empty")
    description: Optional[str] = None
    description_rec: Optional[str] = None
    rationale: Optional[str] = None
    options: Optional[str] = None
    options_description: Optional[str] = None
    step: Optional[int] = None
    sequence: Optional[int] = Field(None, ge=0, description="Sequence must be non-negative")
    required: Optional[Union[int, bool]] = None  # Allow both int and bool for compatibility
    visible_condition: Optional[str] = None
    affected_field: Optional[str] = None
    procedure_type: Optional[str] = None
    dependency_condition: Optional[str] = None
    trade_condition: Optional[str] = None
    status: Optional[int] = 1

class FieldCreate(FieldBase):
    pass

class FieldUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Field name cannot be empty")
    field_type: Optional[str] = Field(None, min_length=1, description="Field type cannot be empty")
    description: Optional[str] = None
    description_rec: Optional[str] = None
    rationale: Optional[str] = None
    options: Optional[str] = None
    options_description: Optional[str] = None
    step: Optional[int] = None
    sequence: Optional[int] = Field(None, ge=0, description="Sequence must be non-negative")
    required: Optional[Union[int, bool]] = None  # Allow both int and bool for compatibility
    visible_condition: Optional[str] = None
    affected_field: Optional[str] = None
    procedure_type: Optional[str] = None
    dependency_condition: Optional[str] = None
    trade_condition: Optional[str] = None
    status: Optional[int] = None

class FieldResponse(FieldBase):
    id: int
    municipality_id: int
    value: Optional[str] = None  # Add value field for storing answers
    editable: Optional[bool] = None  # Add editable field
    static_field: Optional[bool] = None  # Add static_field field
    required_official: Optional[bool] = None  # Add required_official field

    model_config = ConfigDict(from_attributes=True)

class RequirementToggle(BaseModel):
    field_id: int
    requirement_id: int
    status: Optional[str] = None 

class FieldsAndAnswersResponse(BaseModel):
    dynamic_fields: List[FieldResponse]
    static_fields: List[Dict[str, Any]]
    
    model_config = ConfigDict(from_attributes=True)
