from pydantic import BaseModel, ConfigDict
from typing import Optional
from geojson_pydantic import Polygon # type: ignore

class ProcedureRegistrationBase(BaseModel):
    reference: Optional[str] = None
    area: float  # Only required field
    business_sector: Optional[str] = None
    procedure_type: Optional[str] = None
    procedure_origin: Optional[str] = None
    historical_id: Optional[int] = None
    bbox: Optional[str] = None
    municipality_id: Optional[int] = None

class ProcedureRegistrationCreate(BaseModel):
    reference: Optional[str] = None
    area: float  # Only required field
    business_sector: Optional[str] = None
    procedure_type: Optional[str] = None
    procedure_origin: Optional[str] = None
    historical_id: Optional[int] = None
    bbox: Optional[str] = None
    municipality_id: Optional[int] = None
    geom: Optional[Polygon] = None

class ProcedureRegistrationUpdate(BaseModel):
    reference: Optional[str] = None
    area: Optional[float] = None
    business_sector: Optional[str] = None
    procedure_type: Optional[str] = None
    procedure_origin: Optional[str] = None
    historical_id: Optional[int] = None
    bbox: Optional[str] = None
    municipality_id: Optional[int] = None
    geom: Optional[Polygon] = None

class ProcedureRegistrationResponse(ProcedureRegistrationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ProcedureRegistrationGeoResponse(ProcedureRegistrationResponse):
    geom: Optional[Polygon] = None
