from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class NotificationBase(BaseModel):
    user_id: Optional[int] = None
    applicant_email: str = Field(..., max_length=100)
    comment: Optional[str] = Field(None, max_length=300)
    file: Optional[str] = None
    dependency_file: Optional[str] = None
    notified: Optional[int] = None
    notifying_department: Optional[int] = None
    notification_type: Optional[int] = None
    resolution_id: Optional[int] = Field(default=0)
    folio: str = Field(..., max_length=255)

class NotificationCreate(NotificationBase):
    creation_date: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(from_attributes=True)

class NotificationUpdate(BaseModel):
    notified: Optional[int] = None
    seen_date: Optional[datetime] = None
    user_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class NotificationRead(NotificationBase):
    id: int
    creation_date: datetime
    seen_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class NotificationListResponse(BaseModel):
    """Response for paginated notification list"""
    notifications: List[NotificationRead]
    total_count: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool
    model_config = ConfigDict(from_attributes=True)

class FileTypeResponse(BaseModel):
    """Response for file type information"""
    id: int
    procedure_id: int
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
