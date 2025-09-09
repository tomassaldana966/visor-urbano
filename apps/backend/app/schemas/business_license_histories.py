from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class BusinessLicenseHistoryBase(BaseModel):
    license_folio: Optional[str] = None
    issue_date: Optional[str] = None
    business_line: Optional[str] = None
    detailed_description: Optional[str] = None
    business_line_code: Optional[str] = None
    business_area: Optional[str] = None
    street: Optional[str] = None
    exterior_number: Optional[str] = None
    interior_number: Optional[str] = None
    neighborhood: Optional[str] = None
    cadastral_key: Optional[str] = None
    reference: Optional[str] = None
    coordinate_x: Optional[str] = None
    coordinate_y: Optional[str] = None
    owner_first_name: Optional[str] = None
    owner_last_name_p: Optional[str] = None
    owner_last_name_m: Optional[str] = None
    user_tax_id: Optional[str] = None
    national_id: Optional[str] = None
    owner_phone: Optional[str] = None
    business_name: Optional[str] = None
    owner_email: Optional[EmailStr] = None
    owner_street: Optional[str] = None
    owner_exterior_number: Optional[str] = None
    owner_interior_number: Optional[str] = None
    owner_neighborhood: Optional[str] = None
    alcohol_sales: Optional[str] = None
    schedule: Optional[str] = None
    municipality_id: Optional[int] = None
    status: Optional[int] = None
    applicant_first_name: Optional[str] = None
    applicant_last_name_p: Optional[str] = None
    applicant_last_name_m: Optional[str] = None
    applicant_user_tax_id: Optional[str] = None
    applicant_national_id: Optional[str] = None
    applicant_phone: Optional[str] = None
    applicant_street: Optional[str] = None
    applicant_email: Optional[EmailStr] = None
    applicant_postal_code: Optional[str] = None
    owner_postal_code: Optional[str] = None
    property_street: Optional[str] = None
    property_neighborhood: Optional[str] = None
    property_interior_number: Optional[str] = None
    property_exterior_number: Optional[str] = None
    property_postal_code: Optional[str] = None
    property_type: Optional[str] = None
    business_trade_name: Optional[str] = None
    investment: Optional[str] = None
    number_of_employees: Optional[str] = None
    number_of_parking_spaces: Optional[str] = None
    license_year: Optional[str] = None
    license_type: Optional[str] = None
    license_status: Optional[str] = None
    reason: Optional[str] = None
    deactivation_status: Optional[str] = None
    payment_status: Optional[str] = None
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None
    alternate_license_year: Optional[str] = None
    payment_user_id: Optional[int] = None
    payment_date: Optional[datetime] = None
    scanned_pdf: Optional[str] = None
    step_1: Optional[int] = None
    step_2: Optional[int] = None
    step_3: Optional[int] = None
    step_4: Optional[int] = None
    minimap_url: Optional[str] = None
    reason_file: Optional[str] = None
    status_change_date: Optional[datetime] = None

class BusinessLicenseHistoryCreate(BusinessLicenseHistoryBase):
    pass

class BusinessLicenseHistoryUpdate(BusinessLicenseHistoryBase):
    pass

class BusinessLicenseHistoryRead(BusinessLicenseHistoryBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class BusinessLicenseHistoryStatusUpdate(BaseModel):
    license_status: str = Field(..., description="New license status")
    reason: Optional[str] = Field(None, description="Reason for status change")
    reason_file: Optional[str] = Field(None, description="File path or URL for reason documentation")
    status_change_date: Optional[datetime] = Field(None, description="Date of status change")

class BusinessLicenseHistoryPaymentUpdate(BaseModel):
    payment_status: str = Field(..., description="Payment status (e.g., 'paid', 'pending')")
    payment_user_id: Optional[int] = Field(None, description="ID of user who processed payment")
    payment_date: Optional[datetime] = Field(None, description="Date payment was made")

class BusinessLicenseHistoryRenewalRequest(BaseModel):
    license_year: str = Field(..., description="Year for the renewal license")
    license_type: Optional[str] = Field(None, description="Type of license for renewal")

class FileInfo(BaseModel):
    filename: str
    url: str
    uploaded_at: datetime

class FileListResponse(BaseModel):
    files: List[FileInfo]
    total_count: int
