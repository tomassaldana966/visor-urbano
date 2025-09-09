from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ProvisionalOpeningBase(BaseModel):
    folio: str = Field(..., max_length=255, description="Unique folio for the provisional opening")
    procedure_id: Optional[int] = Field(None, description="Associated procedure ID")
    counter: Optional[int] = Field(None, description="Counter")
    granted_by_user_id: Optional[int] = Field(None, description="ID of the user who granted the opening")
    granted_role: Optional[int] = Field(None, description="Role of the granting user")
    start_date: datetime = Field(..., description="Start date of the provisional opening")
    end_date: datetime = Field(..., description="End date of the provisional opening")
    status: int = Field(default=1, description="Status: 1=active, 0=inactive")


class ProvisionalOpeningCreate(ProvisionalOpeningBase):
    municipality_id: int = Field(..., description="Municipality ID")
    created_by: Optional[int] = Field(None, description="Creator user ID")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "folio": "PROV-2024-001",
                "procedure_id": 123,
                "municipality_id": 1,
                "start_date": "2024-01-15T08:00:00",
                "end_date": "2024-02-14T17:00:00",
                "status": 1,
                "granted_by_user_id": 456,
                "granted_role": 2,
                "created_by": 456
            }
        }
    )


class ProvisionalOpeningUpdate(BaseModel):
    folio: Optional[str] = Field(None, max_length=255)
    procedure_id: Optional[int] = None
    counter: Optional[int] = None
    granted_by_user_id: Optional[int] = None
    granted_role: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[int] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "end_date": "2024-03-15T17:00:00",
                "status": 1
            }
        }
    )


class ProvisionalOpeningRead(ProvisionalOpeningBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Campos calculados/adicionales para la respuesta
    municipality_name: Optional[str] = Field(None, description="Municipality name")
    granted_by_user_name: Optional[str] = Field(None, description="Name of the granting user")
    procedure_folio: Optional[str] = Field(None, description="Procedure folio")
    days_remaining: Optional[int] = Field(None, description="Days remaining until expiration")
    is_expired: Optional[bool] = Field(None, description="Whether the provisional opening has expired")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "folio": "PROV-2024-001",
                "procedure_id": 123,
                "start_date": "2024-01-15T08:00:00",
                "end_date": "2024-02-14T17:00:00",
                "status": 1,
                "granted_by_user_id": 456,
                "granted_role": 2,
                "created_at": "2024-01-15T08:00:00",
                "updated_at": "2024-01-15T08:00:00",
                "municipality_name": "Tijuana",
                "granted_by_user_name": "John Doe",
                "procedure_folio": "PROC-2024-123",
                "days_remaining": 30,
                "is_expired": False
            }
        }
    )


class ProvisionalOpeningList(BaseModel):
    total: int
    items: list[ProvisionalOpeningRead]
    page: int = Field(default=1)
    size: int = Field(default=10)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 25,
                "items": [],
                "page": 1,
                "size": 10
            }
        }
    )


class PDFResponse(BaseModel):
    pdf_content: str = Field(..., description="PDF content in base64")
    filename: str = Field(..., description="PDF filename")
    qr_code: str = Field(..., description="QR code in base64")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pdf_content": "JVBERi0xLjQKMSAwIG9iago...",
                "filename": "provisional_opening_PROV-2024-001.pdf",
                "qr_code": "iVBORw0KGgoAAAANSUhEUgAA..."
            }
        }
    )