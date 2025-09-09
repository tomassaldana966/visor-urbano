from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class BusinessLicenseBase(BaseModel):
    owner: str
    license_folio: str
    commercial_activity: str
    industry_classification_code: str
    authorized_area: str
    opening_time: str
    closing_time: str
    owner_last_name_p: Optional[str] = None
    owner_last_name_m: Optional[str] = None
    national_id: Optional[str] = None
    owner_profile: Optional[str] = None
    logo_image: Optional[str] = None
    signature: Optional[str] = None
    minimap_url: Optional[str] = None
    scanned_pdf: Optional[str] = None
    license_year: int = 1
    license_category: Optional[int] = 1
    generated_by_user_id: int = 1
    payment_status: Optional[int] = 0
    payment_user_id: Optional[int] = 0
    deactivation_status: Optional[int] = 0
    payment_date: Optional[datetime] = None
    deactivation_date: Optional[datetime] = None
    secondary_folio: Optional[str] = ''
    deactivation_reason: Optional[str] = None
    deactivated_by_user_id: Optional[int] = 0
    signer_name_1: Optional[str] = None
    department_1: Optional[str] = None
    signature_1: Optional[str] = None
    signer_name_2: Optional[str] = None
    department_2: Optional[str] = None
    signature_2: Optional[str] = None
    signer_name_3: Optional[str] = None
    department_3: Optional[str] = None
    signature_3: Optional[str] = None
    signer_name_4: Optional[str] = None
    department_4: Optional[str] = None
    signature_4: Optional[str] = None
    license_number: Optional[int] = None
    municipality_id: Optional[int] = None
    license_type: Optional[str] = None
    license_status: Optional[str] = None
    reason: Optional[str] = None
    reason_file: Optional[str] = None
    status_change_date: Optional[datetime] = None
    observations: Optional[str] = None
    
    # Connection to procedure and requirements query
    procedure_id: Optional[int] = None
    requirements_query_id: Optional[int] = None
    
    # Establishment data copied from procedure
    establishment_name: Optional[str] = None
    establishment_address: Optional[str] = None
    establishment_phone: Optional[str] = None
    establishment_email: Optional[str] = None

class BusinessLicenseCreate(BusinessLicenseBase):
    pass

class BusinessLicenseUpdate(BusinessLicenseBase):
    pass

class BusinessLicenseRead(BusinessLicenseBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    # Additional fields from procedure joins
    procedure_applicant_name: Optional[str] = None
    procedure_street: Optional[str] = None
    procedure_neighborhood: Optional[str] = None
    procedure_scian_name: Optional[str] = None
    procedure_establishment_name: Optional[str] = None
    procedure_establishment_address: Optional[str] = None
    procedure_establishment_phone: Optional[str] = None
    user_email: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# Public schema for listing (without sensitive data)
class BusinessLicensePublic(BaseModel):
    license_folio: str
    commercial_activity: str
    industry_classification_code: str
    municipality_id: Optional[int] = None  
    municipality_name: Optional[str] = None  # Added municipality name
    license_status: Optional[str] = None
    license_type: Optional[str] = None
    payment_status: Optional[int] = 0  # Added payment status
    scanned_pdf: Optional[str] = None  # Added license file path
    establishment_phone: Optional[str] = None  # Establishment phone
    establishment_name: Optional[str] = None  # Establishment name
    establishment_address: Optional[str] = None  # Establishment address
    applicant_name: Optional[str] = None  # Applicant name
    rq_street: Optional[str] = None  # Street from RequirementsQuery
    rq_neighborhood: Optional[str] = None  # Neighborhood from RequirementsQuery
    user_email: Optional[str] = None  # User email as fallback
    
    model_config = ConfigDict(from_attributes=True)

# Response model with pagination information
class BusinessLicenseResponse(BaseModel):
    items: List[dict]  # List of business license dictionaries
    page: int
    per_page: int
    total: int
    total_pages: int  # Changed from 'pages' to 'total_pages' for consistency
