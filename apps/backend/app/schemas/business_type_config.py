from pydantic import BaseModel, ConfigDict
from typing import Optional

class BusinessTypeStatusBase(BaseModel):
    business_type_id: int

class BusinessTypeDisableRequest(BusinessTypeStatusBase):
    pass

class BusinessTypeCertificateStatusRequest(BusinessTypeStatusBase):
    status: bool

class BusinessTypeImpactRequest(BaseModel):
    business_type_id: int
    impact_level: int

class BusinessTypeConfigResponse(BaseModel):
    id: int
    business_type_id: int
    municipality_id: int
    is_disabled: bool
    has_certificate: bool
    impact_level: Optional[int]
    name: Optional[str]
    description: Optional[str]
    code: Optional[str]  # SCIAN code
    related_words: Optional[str]  # Related words

    model_config = ConfigDict(from_attributes=True)
