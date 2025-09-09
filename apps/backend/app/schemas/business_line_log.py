from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List

class BusinessLineLogBase(BaseModel):
    action: str = Field(..., min_length=1, max_length=255, description="Action performed")
    previous: Optional[str] = Field(None, max_length=65535, description="Previous state/value")
    log_type: int = Field(..., ge=0, description="Type of log entry")
    procedure_id: Optional[int] = Field(None, ge=1, description="Associated procedure ID")
    host: Optional[str] = Field(None, max_length=255, description="Host information")
    user_ip: Optional[str] = Field(None, max_length=45, description="User's IP address")
    role_id: Optional[int] = Field(None, ge=1, description="User's role ID")
    user_agent: Optional[str] = Field(None, max_length=65535, description="User agent information")
    post_request: Optional[str] = Field(None, max_length=65535, description="POST request data")

class BusinessLineLogCreate(BaseModel):
    action: str = Field(..., min_length=1, max_length=255, description="Action performed")
    previous: Optional[str] = Field(None, max_length=65535, description="Previous state/value")
    log_type: int = Field(..., ge=0, description="Type of log entry")
    procedure_id: Optional[int] = Field(None, ge=1, description="Associated procedure ID")
    post_request: Optional[str] = Field(None, max_length=65535, description="POST request data")

class BusinessLineLogResponse(BusinessLineLogBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BusinessLineLogUpdate(BaseModel):
    action: Optional[str] = Field(None, min_length=1, max_length=255)
    previous: Optional[str] = Field(None, max_length=65535)
    log_type: Optional[int] = Field(None, ge=0)
    procedure_id: Optional[int] = Field(None, ge=1)
    host: Optional[str] = Field(None, max_length=255)
    user_ip: Optional[str] = Field(None, max_length=45)
    role_id: Optional[int] = Field(None, ge=1)
    user_agent: Optional[str] = Field(None, max_length=65535)
    post_request: Optional[str] = Field(None, max_length=65535)

class BusinessLineLogListResponse(BaseModel):
    logs: List[BusinessLineLogResponse]
    total_count: int = Field(..., ge=0, description="Total number of logs matching the criteria")
    skip: int = Field(..., ge=0, description="Number of records skipped")
    limit: int = Field(..., ge=1, description="Maximum number of records returned")
    
    model_config = ConfigDict(from_attributes=True)