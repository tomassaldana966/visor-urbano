from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict
from datetime import datetime


class BusinessSignatureBaseSchema(BaseModel):
    procedure_id: int = Field(..., description="ID of the related procedure", gt=0)
    user_id: int = Field(..., description="ID of the user signing the document", gt=0)
    role: int = Field(..., description="Role of the user", gt=0)
    hash_to_sign: Optional[str] = Field(None, description="Original hash that was to be signed", max_length=10000)
    signed_hash: Optional[str] = Field(None, description="Base64 signed hash", max_length=10000)
    response: Optional[Dict[str, Any]] = Field(None, description="JSON containing metadata from the signing process")


class BusinessSignatureCreateSchema(BaseModel):
    """Schema for creating business signatures via form data"""
    password: str = Field(..., description="Private key password", min_length=8, max_length=100)
    chain: str = Field(..., description="Chain to sign", min_length=1, max_length=10000)
    curp: str = Field(..., description="CURP of the signer", min_length=18, max_length=18)
    procedure_id: int = Field(..., description="ID of the related procedure", gt=0)
    procedure_part: str = Field(..., description="Part of the procedure", min_length=1, max_length=100)
    
    @field_validator('curp')
    @classmethod
    def validate_curp_format(cls, v):
        import re
        curp_pattern = re.compile(r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$')
        if not curp_pattern.match(v.upper()):
            raise ValueError('Invalid CURP format')
        return v.upper()


class BusinessSignatureResponseSchema(BusinessSignatureBaseSchema):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}



