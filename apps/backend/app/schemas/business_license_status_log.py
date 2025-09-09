from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class BusinessLicenseStatusLogBase(BaseModel):
    license_id: int
    previous_status: Optional[str] = None
    new_status: str
    reason: Optional[str] = None
    reason_file: Optional[str] = None
    changed_by_user_id: Optional[int] = None

class BusinessLicenseStatusLogCreate(BusinessLicenseStatusLogBase):
    pass

class UserRoleInfo(BaseModel):
    id: int
    name: str
    role_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class BusinessLicenseStatusLogRead(BusinessLicenseStatusLogBase):
    id: int
    changed_at: datetime
    created_at: datetime
    updated_at: datetime
    changed_by_user: Optional[UserRoleInfo] = None
    
    model_config = ConfigDict(from_attributes=True)
