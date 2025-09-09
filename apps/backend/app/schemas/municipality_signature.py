from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class MunicipalitySignatureBase(BaseModel):
    position_title: str = Field(..., description="Cargo del servidor público")
    signer_name: str = Field(..., description="Nombre del firmante")
    order_index: int = Field(..., description="Orden de aparición", ge=1, le=4)
    is_active: str = Field(default="Y", description="Estado activo (Y/N)")

class MunicipalitySignatureCreate(BaseModel):
    position_title: str = Field(..., description="Cargo del servidor público")
    signer_name: str = Field(..., description="Nombre del firmante")
    order_index: int = Field(..., description="Orden de aparición", ge=1, le=4)
    is_active: str = Field(default="Y", description="Estado activo (Y/N)")

class MunicipalitySignatureUpdate(BaseModel):
    position_title: Optional[str] = None
    signer_name: Optional[str] = None
    order_index: Optional[int] = Field(None, ge=1, le=4)
    is_active: Optional[str] = None

class MunicipalitySignatureResponse(BaseModel):
    id: int
    municipality_id: int
    signer_name: str = Field(..., description="Nombre del firmante")
    position_title: str = Field(..., description="Cargo del servidor público")
    order_index: int = Field(..., description="Orden de aparición", ge=1, le=4)
    signature_image: Optional[str] = Field(None, description="Ruta de la imagen de firma")
    is_active: str = Field(default="Y", description="Estado activo (Y/N)")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_db_model(cls, db_obj):
        """Create response object from database model with field mapping"""
        return cls(
            id=db_obj.id,
            municipality_id=db_obj.municipality_id,
            signer_name=db_obj.signer_name,
            position_title=db_obj.department,  # Map department to position_title
            order_index=db_obj.orden,  # Map orden to order_index
            signature_image=db_obj.signature,  # Map signature to signature_image
            is_active='Y',  # Default to active
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
        )
