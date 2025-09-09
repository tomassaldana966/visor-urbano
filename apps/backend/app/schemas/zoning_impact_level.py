from pydantic import BaseModel, ConfigDict
from typing import Optional
from geojson_pydantic import Polygon # type: ignore

class ZoningImpactLevelBase(BaseModel):
    impact_level: int
    municipality_id: int

class ZoningImpactLevelCreate(ZoningImpactLevelBase):
    geom: Optional[Polygon] = None

class ZoningImpactLevelUpdate(BaseModel):
    impact_level: Optional[int] = None
    municipality_id: Optional[int] = None
    geom: Optional[Polygon] = None

class ZoningImpactLevelResponse(ZoningImpactLevelBase):
    id: int
    geom: Optional[Polygon]

    model_config = ConfigDict(from_attributes=True)
