from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class BusinessSectorBase(BaseModel):
    """Base schema for business sectors"""
    code: Optional[str] = Field(None, description="Business sector code")
    industry_classification_code: Optional[str] = Field(None, alias="SCIAN", description="SCIAN industry classification code")
    related_words: Optional[str] = Field(None, description="Related keywords")

class BusinessSectorResponse(BusinessSectorBase):
    """Response schema for business sectors"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class BusinessSectorConfigurationResponse(BaseModel):
    """Response schema for business sector configurations"""
    id: int
    business_sector_id: int = Field(alias="giros_id")
    municipality_id: int = Field(alias="municipios_id")
    inactive_business_flag: int = Field(alias="giro_apagado")
    business_impact_flag: int = Field(alias="giro_impacto")
    business_sector_certificate_flag: int = Field(alias="giro_cedula")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Include business sector information
    code: Optional[str] = None
    industry_classification_code: Optional[str] = Field(None, alias="SCIAN")
    related_words: Optional[str] = Field(None, alias="palabras_relacion")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class BusinessSectorEnabledResponse(BaseModel):
    """Response schema for enabled business sectors (matching legacy getEncendidos)"""
    id: int
    code: Optional[str] = Field(None, alias="codigo")
    industry_classification_code: Optional[str] = Field(None, alias="SCIAN")
    related_words: Optional[str] = Field(None, alias="palabras_relacion")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
