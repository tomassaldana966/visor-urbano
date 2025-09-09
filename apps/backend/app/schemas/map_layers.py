from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class MapLayerBase(BaseModel):
    value: str
    label: str
    type: str
    url: str
    layers: str
    visible: bool
    active: bool
    attribution: Optional[str] = None # Added default None
    opacity: float
    server_type: Optional[str] = None # Added default None
    projection: Optional[str] = 'EPSG:4326'
    version: Optional[str] = '1.3.0'
    format: str
    order: Optional[int] = 0
    editable: Optional[bool] = True
    type_geom: Optional[str] = None # Added default None
    cql_filter: Optional[str] = None # Added default None
    municipality_ids: List[int] = []

class MapLayerCreate(MapLayerBase):
    pass

class MapLayerUpdate(BaseModel): # Changed from MapLayerBase
    value: Optional[str] = None
    label: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    layers: Optional[str] = None
    visible: Optional[bool] = None
    active: Optional[bool] = None
    attribution: Optional[str] = None
    opacity: Optional[float] = None
    server_type: Optional[str] = None
    projection: Optional[str] = None
    version: Optional[str] = None
    format: Optional[str] = None
    order: Optional[int] = None
    editable: Optional[bool] = None
    type_geom: Optional[str] = None
    cql_filter: Optional[str] = None
    municipality_ids: Optional[List[int]] = None

class MapLayerResponse(MapLayerBase):
    id: int
    municipality_ids: List[int] = []
    model_config = ConfigDict(from_attributes=True)
            
    @classmethod
    def from_orm(cls, layer):        
        obj = super().from_orm(layer)
                
        if hasattr(layer, 'municipalities') and layer.municipalities:
            obj.municipality_ids = [m.id for m in layer.municipalities]
        
        return obj
