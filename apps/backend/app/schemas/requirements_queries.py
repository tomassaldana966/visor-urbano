from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal

class RequirementsQueryBaseSchema(BaseModel):
    folio: Optional[str] = None
    street: Optional[str] = Field(None, max_length=100)
    neighborhood: Optional[str] = Field(None, max_length=100)
    municipality_name: Optional[str] = Field(None, max_length=50)
    municipality_id: int = Field(...)
    scian_code: Optional[str] = Field(None, max_length=100)
    scian_name: Optional[str] = Field(None, max_length=100)
    property_area: Optional[Decimal] = Field(None, ge=0)
    activity_area: Optional[Decimal] = Field(None, ge=0)
    applicant_name: Optional[str] = Field(None, max_length=100)
    applicant_character: Optional[str] = Field(None, max_length=100)
    person_type: Optional[str] = Field(None, max_length=100)
    minimap_url: Optional[str] = None
    restrictions: Optional[Dict[str, Any]] = None
    alcohol_sales: Optional[int] = Field(default=0)
    primary_folio: Optional[str] = Field(None, max_length=255)
    issue_license: Optional[int] = Field(default=0)
    
    # New fields for license type and specific information
    license_type: Optional[str] = Field(None, max_length=50)  # 'commercial' or 'construction'
    scian: Optional[str] = Field(None, max_length=100)  # For commercial licenses
    entry_date: Optional[date] = None  # Common field for both types
    interested_party: Optional[str] = Field(None, max_length=255)  # For construction licenses
    last_resolution: Optional[str] = None  # For construction licenses
    resolution_sense: Optional[str] = Field(None, max_length=50)  # For construction licenses

class RequirementsQueryCreateWithDynamicFieldsSchema(RequirementsQueryBaseSchema):
    locality: Optional[str] = Field(None)
    activity_description: Optional[str] = Field(None)
    minimap_sketch_url: Optional[str] = Field(None)
    dynamic_fields: Optional[Dict[str, Any]] = Field(None)

    @field_validator('alcohol_sales', mode='before')
    @classmethod
    def validate_alcohol_sales(cls, v, info):        
        if hasattr(info, 'data') and info.data.get('dynamic_fields'):
            dynamic_fields = info.data.get('dynamic_fields')
            if isinstance(dynamic_fields, dict):
                # Support both English and Spanish field names
                alcohol_field = dynamic_fields.get('alcohol_sales') or dynamic_fields.get('venta_alcohol')
                if alcohol_field is not None:
                    if isinstance(alcohol_field, bool):
                        return 1 if alcohol_field else 0                
                    elif isinstance(alcohol_field, str):
                        return 1 if alcohol_field.lower() in ['true', 'si', '1', 'yes'] else 0
                
        if isinstance(v, bool):
            return 1 if v else 0
                    
        if isinstance(v, str):
            if v.lower() in ['true', 'false']:
                return 1 if v.lower() == 'true' else 0            
            try:
                return int(v)
            except ValueError:
                return 0
        return v or 0

    @field_validator('property_area', 'activity_area', mode='before')
    @classmethod
    def validate_area_fields(cls, v):
        if v is None:
            return Decimal('0')
        try:
            return Decimal(str(v))
        except (ValueError, TypeError):
            return Decimal('0')

class RequirementsQueryCreateSchema(RequirementsQueryBaseSchema):
    pass

class RequirementsQueryUpdateSchema(BaseModel):
    street: Optional[str] = Field(None, max_length=100)
    neighborhood: Optional[str] = Field(None, max_length=100)
    municipality_name: Optional[str] = Field(None, max_length=50)
    municipality_id: Optional[int] = None
    scian_code: Optional[str] = Field(None, max_length=100)
    scian_name: Optional[str] = Field(None, max_length=100)
    property_area: Optional[Decimal] = Field(None, ge=0)
    activity_area: Optional[Decimal] = Field(None, ge=0)
    applicant_name: Optional[str] = Field(None, max_length=100)
    applicant_character: Optional[str] = Field(None, max_length=100)
    person_type: Optional[str] = Field(None, max_length=100)
    minimap_url: Optional[str] = None
    restrictions: Optional[Dict[str, Any]] = None
    status: Optional[int] = None
    alcohol_sales: Optional[int] = Field(None)
    primary_folio: Optional[str] = Field(None, max_length=255)

class RequirementsQueryOutSchema(RequirementsQueryBaseSchema):
    id: int
    status: int = Field()
    user_id: int = Field()
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    year_folio: int = Field()
    model_config = ConfigDict(from_attributes=True)

class ProcedureInfoSchema(BaseModel):
    folio: str
    procedure_data: Dict[str, Any]
    requirements: List[Dict[str, Any]]
    status: str
    model_config = ConfigDict(from_attributes=True)

class ProcedureTypeInfoSchema(BaseModel):
    folio: str
    procedure_type: str
    type_data: Dict[str, Any]
    model_config = ConfigDict(from_attributes=True)

class ProcedureRenewalInfoSchema(BaseModel):
    folio: str
    renewal_data: Dict[str, Any]
    renewal_requirements: List[Dict[str, Any]]
    model_config = ConfigDict(from_attributes=True)

class RequirementsPdfSchema(BaseModel):
    folio: str
    requirement_id: int
    pdf_data: str
    filename: str
    model_config = ConfigDict(from_attributes=True)
