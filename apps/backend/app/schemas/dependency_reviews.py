from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Literal, Dict, Any
from datetime import datetime

class DependencyReviewBase(BaseModel):
    procedure_id: int
    municipality_id: int
    folio: str
    role: int
    start_date: Optional[datetime] = None
    update_date: Optional[datetime] = None
    current_status: Optional[int] = None
    current_file: Optional[str] = None
    signature: Optional[str] = None
    user_id: Optional[int] = None
    director_approved: int = 0
    sent_to_reviewers: Optional[datetime] = None
    license_pdf: Optional[str] = None
    license_issued: bool = False
    payment_order_file: Optional[str] = None

class DependencyReviewCreate(DependencyReviewBase):
    pass

class DependencyReviewFilter(BaseModel):
    procedure_id: Optional[int] = None
    municipality_id: Optional[int] = None
    folio: Optional[str] = None
    role: Optional[int] = None
    start_date: Optional[datetime] = None
    update_date: Optional[datetime] = None
    current_status: Optional[int] = None
    current_file: Optional[str] = None
    signature: Optional[str] = None
    user_id: Optional[int] = None

class DependencyReviewUpdate(BaseModel):
    resolution_text: Optional[str] = Field(None, description="Resolution comments")
    resolution_file: Optional[str] = Field(None, description="Resolution file URL")
    resolution_status: int = Field(..., description="Resolution status (0=pending, 1=approved, 2=rejected, 3=prevention, 4=license_issued)")
    additional_files: Optional[List[str]] = Field(None, description="Additional supporting files")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "resolution_text": "Approved according to current regulations",
                "resolution_file": "https://storage.example.com/file.pdf",
                "resolution_status": 1,
                "additional_files": ["https://storage.example.com/support1.pdf"]
            }
        }
    )

class DependencyReviewResponse(DependencyReviewBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    resolutions: Optional[List["DependencyResolutionResponse"]] = []
    prevention_requests: Optional[List["PreventionRequestResponse"]] = []

    model_config = ConfigDict(from_attributes=True)

class DependencyResolutionBase(BaseModel):
    review_id: Optional[int] = None
    procedure_id: int
    role: Optional[int] = None
    user_id: Optional[int] = None
    resolution_status: Optional[int] = None
    resolution_text: Optional[str] = None
    resolution_file: Optional[str] = None
    additional_files: Optional[str] = None
    is_final_resolution: bool = False
    signature: Optional[str] = None

class DependencyResolutionCreate(DependencyResolutionBase):
    pass

class DependencyResolutionUpdate(BaseModel):
    resolution_status: Optional[int] = None
    resolution_text: Optional[str] = None
    resolution_file: Optional[str] = None
    additional_files: Optional[str] = None
    is_final_resolution: Optional[bool] = None

class DependencyResolutionResponse(DependencyResolutionBase):
    id: int
    deleted_at: Optional[datetime] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    user_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PreventionRequestBase(BaseModel):
    review_id: int
    procedure_id: int
    role: int
    user_id: int
    comments: Optional[str] = None
    max_resolution_date: Optional[datetime] = None
    business_days: int = 15
    status: int = 0

class PreventionRequestCreate(BaseModel):
    review_id: int
    procedure_id: int
    role: int
    comments: str
    business_days: int = 15

class PreventionRequestResponse(PreventionRequestBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class NotificationBase(BaseModel):
    user_id: Optional[int] = None
    review_id: Optional[int] = None
    prevention_request_id: Optional[int] = None
    folio: str
    applicant_email: str
    comment: Optional[str] = None
    comments: Optional[str] = None
    file: Optional[str] = None
    creation_date: datetime
    seen_date: Optional[datetime] = None
    dependency_file: Optional[str] = None
    notified: Optional[int] = None
    is_notified: int = 0
    notifying_department: Optional[int] = None
    notification_type: Optional[int] = None
    resolution_id: Optional[int] = 0
    email_sent: bool = False
    email_sent_at: Optional[datetime] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class DirectorApprovalBase(BaseModel):
    review_id: int
    procedure_id: int
    municipality_id: int
    folio: str
    director_id: int
    approval_status: int = 0
    approval_comments: Optional[str] = None
    approved_at: Optional[datetime] = None

class DirectorApprovalCreate(DirectorApprovalBase):
    pass

class DirectorApprovalResponse(DirectorApprovalBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class DirectorInsertRequest(BaseModel):
    procedure_id: int
    municipality_id: int
    folio: str

class ResolutionFlowStatus(BaseModel):
    review_id: int
    status: Literal["pending", "approved", "rejected", "prevention", "director_review", "license_issued"]
    role: int
    user_id: int
    resolution_text: Optional[str] = None
    resolution_file: Optional[str] = None
    created_at: datetime

class BulkResolutionUpdate(BaseModel):
    review_ids: List[int]
    resolution_status: int
    resolution_text: Optional[str] = None
    resolution_file: Optional[str] = None

class LicenseEmissionRequest(BaseModel):
    folio: str
    license_file: str
    additional_instructions: Optional[str] = None

class ResolutionStatistics(BaseModel):
    total_reviews: int
    pending_reviews: int
    approved_reviews: int
    rejected_reviews: int
    prevention_reviews: int
    average_resolution_time: float

class FileUploadRequest(BaseModel):
    folio: str
    file_type: Literal["resolution", "payment_order", "license", "support"]
    file_url: str
    comments: Optional[str] = None

class ResolutionInfoResponse(BaseModel):
    review: Optional[DependencyReviewResponse] = None
    resolutions: List[DependencyResolutionResponse] = []
    prevention_requests: List[PreventionRequestResponse] = []
    director_approval: Optional[DirectorApprovalResponse] = None
    procedure_info: Optional[Dict[str, Any]] = None

class BusinessDaysCalculation(BaseModel):
    start_date: datetime
    business_days: int
    calculated_end_date: datetime

class NotificationEmailRequest(BaseModel):
    folio: str
    recipient_email: str
    notification_type: Literal["approval", "rejection", "prevention", "license_issued"]
    additional_message: Optional[str] = None

class AnalyticsRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    municipality_id: Optional[int] = None
    role: Optional[int] = None
    status: Optional[int] = None

class AnalyticsResponse(BaseModel):
    total_count: int
    approved_count: int
    rejected_count: int
    pending_count: int
    prevention_count: int
    average_processing_time: float
    data_points: List[Dict[str, Any]] = []
