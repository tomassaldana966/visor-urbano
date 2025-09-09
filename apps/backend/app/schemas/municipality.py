from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from .municipality_signature import MunicipalitySignatureResponse

class MunicipalityBase(BaseModel):
    name: str = Field(..., max_length=250)
    image: Optional[str] = Field(None, max_length=250)
    director: Optional[str] = Field(None, max_length=250)
    director_signature: Optional[str] = Field(None, max_length=250)
    process_sheet: Optional[int] = Field(1)
    solving_days: Optional[int] = None
    issue_license: Optional[int] = Field(0)
    address: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=255)
    responsible_area: Optional[str] = Field(None, max_length=250)
    window_license_generation: Optional[int] = Field(0)
    license_restrictions: Optional[str] = Field("", max_length=500)
    license_price: Optional[str] = Field(None, max_length=255)
    initial_folio: Optional[int] = None
    has_zoning: Optional[bool] = Field(None, description="Indicates if zoning is available")
    
    # License configuration fields
    allow_online_procedures: Optional[bool] = Field(None, description="Allow online procedures and license issuance")
    allow_window_reviewer_licenses: Optional[bool] = Field(None, description="Allow window and reviewer users to issue licenses with opening certificate")
    low_impact_license_cost: Optional[str] = Field(None, max_length=255, description="Cost for low impact licenses")
    license_additional_text: Optional[str] = Field(None, description="Additional text to appear on licenses")
    theme_color: Optional[str] = Field(None, max_length=7, description="Hexadecimal theme color (#FFFFFF)")

class MunicipalityCreate(MunicipalityBase):
    model_config = ConfigDict(
        from_attributes=True  
    )

class MunicipalityUpdate(MunicipalityBase):
    name: Optional[str] = None

class MunicipalityResponse(MunicipalityBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    signatures: List[MunicipalitySignatureResponse] = Field(default_factory=list, description="Municipality signatures for licenses")
    
    model_config = ConfigDict(
        from_attributes=True  
    )

class MunicipalityLegacyResponse(BaseModel):
    """
    Legacy-compatible response schema for municipalities endpoint.
    Matches the format expected by legacy /municipios GET endpoint.
    """
    id: int
    nombre: str
    cve_ent: Optional[str] = Field(None, description="State code")
    cve_mun: Optional[str] = Field(None, description="Municipality code") 
    cvegeo: Optional[str] = Field(None, description="Geographic code")
    tiene_zonificacion: Optional[bool]
    
    model_config = ConfigDict(
        from_attributes=True
    )

class MunicipalityGeomLegacyResponse(BaseModel):
    """
    Legacy-compatible response schema for municipality geometry endpoint.
    Matches the format expected by legacy /rest/v1/municipios-geom/{id} GET endpoint.
    """
    id: int
    type: str = Field(default="Feature")
    geometry: dict = Field(description="GeoJSON geometry object")
    properties: dict = Field(description="Municipality properties")
    
    model_config = ConfigDict(
        from_attributes=True
    )

class MunicipalityDataSchema(BaseModel):
    """Schema for municipality basic data extraction"""
    id: int
    name: str
    director: str
    address: str
    phone: str

class MunicipalityGeospatialSchema(BaseModel):
    """Schema for municipality geospatial data extraction"""
    entity_code: str
    municipality_code: str
    geocode: str
    has_zoning: bool
