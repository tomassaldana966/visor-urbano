from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProcedureBase(BaseModel):
    folio: Optional[str] = None
    current_step: Optional[int] = None
    user_signature: Optional[str] = None
    user_id: Optional[int] = None
    window_user_id: Optional[int] = None
    entry_role: Optional[int] = None
    documents_submission_date: Optional[datetime] = None
    procedure_start_date: Optional[datetime] = None
    window_seen_date: Optional[datetime] = None
    license_delivered_date: Optional[datetime] = None
    has_signature: Optional[int] = None
    no_signature_date: Optional[datetime] = None
    official_applicant_name: Optional[str] = None
    responsibility_letter: Optional[str] = None
    sent_to_reviewers: Optional[int] = None
    sent_to_reviewers_date: Optional[datetime] = None
    license_pdf: Optional[str] = None
    payment_order: Optional[str] = None
    status: int
    step_one: Optional[int] = None
    step_two: Optional[int] = None
    step_three: Optional[int] = None
    step_four: Optional[int] = None
    director_approval: Optional[int] = 0
    window_license_generated: Optional[int] = 0
    procedure_type: Optional[str] = None
    license_status: Optional[str] = None
    reason: Optional[str] = None
    renewed_folio: Optional[str] = None
    requirements_query_id: Optional[int] = None
    business_type_id: Optional[int] = None  # Add business type field
    
    # Address fields
    street: Optional[str] = None
    exterior_number: Optional[str] = None
    interior_number: Optional[str] = None
    neighborhood: Optional[str] = None
    reference: Optional[str] = None
    project_municipality_id: Optional[int] = None
    municipality_id: Optional[int] = None
    
    # Business establishment fields
    establishment_name: Optional[str] = None
    establishment_address: Optional[str] = None
    establishment_phone: Optional[str] = None
    establishment_area: Optional[str] = None
    
    # SCIAN fields for business classification
    scian_code: Optional[str] = None
    scian_name: Optional[str] = None

class ProcedureCreate(ProcedureBase):
    pass

class ProcedureUpdate(ProcedureBase):
    status: Optional[int] = None

class ProcedureRead(ProcedureBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    municipality_name: Optional[str] = None
    business_line: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Schema specifically for Business Commercial Procedures (Trámites de Giro Comercial)
class BusinessCommercialProcedureBase(BaseModel):
    """Base schema for business commercial procedures with additional address and business information"""
    # Procedure fields
    folio: Optional[str] = None
    current_step: Optional[int] = None
    procedure_type: Optional[str] = None
    license_status: Optional[str] = None
    status: Optional[int] = None
    procedure_start_date: Optional[datetime] = None
    official_applicant_name: Optional[str] = None
    
    # Address information from business_license_histories
    street: Optional[str] = None
    exterior_number: Optional[str] = None
    interior_number: Optional[str] = None
    neighborhood: Optional[str] = None
    
    # Municipality information
    municipality_id: Optional[int] = None
    municipality_name: Optional[str] = None
    
    # Business sector information (SCIAN)
    industry_classification_code: Optional[str] = None
    business_line: Optional[str] = None
    business_line_code: Optional[str] = None
    
    # Business details
    business_name: Optional[str] = None
    detailed_description: Optional[str] = None

class BusinessCommercialProcedureRead(BusinessCommercialProcedureBase):
    """Response schema for business commercial procedures"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Full address computed field
    full_address: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class BusinessCommercialProcedureList(BaseModel):
    """Schema for listing business commercial procedures with pagination"""
    procedures: list[BusinessCommercialProcedureRead]
    total_count: int
    skip: int
    limit: int

# Schema specifically for Construction Procedures (Trámites de Construcción)
class ConstructionProcedureBase(BaseModel):
    """Base schema for construction procedures with address information"""
    # Procedure fields
    folio: Optional[str] = None
    current_step: Optional[int] = None
    procedure_type: Optional[str] = None
    license_status: Optional[str] = None
    status: Optional[int] = None
    procedure_start_date: Optional[datetime] = None
    official_applicant_name: Optional[str] = None
    
    # Address information from procedures table
    street: Optional[str] = None
    exterior_number: Optional[str] = None
    interior_number: Optional[str] = None
    neighborhood: Optional[str] = None
    reference: Optional[str] = None
    
    # Municipality information
    municipality_id: Optional[int] = None
    municipality_name: Optional[str] = None

class ConstructionProcedureRead(ConstructionProcedureBase):
    """Response schema for construction procedures"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Full address computed field
    full_address: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class ConstructionProcedureList(BaseModel):
    """Schema for listing construction procedures with pagination"""
    procedures: list[ConstructionProcedureRead]
    total_count: int
    skip: int
    limit: int
