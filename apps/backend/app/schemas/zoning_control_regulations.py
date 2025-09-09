from pydantic import BaseModel, ConfigDict
from typing import Optional

class ZoningControlRegulationBase(BaseModel):
    municipality_id: int
    district: str
    regulation_key: str
    land_use: str
    density: Optional[str]
    intensity: Optional[str]
    business_sector: Optional[str]
    minimum_area: Optional[str]
    minimum_frontage: Optional[str]
    building_index: Optional[str]
    land_occupation_coefficient: Optional[str]
    land_utilization_coefficient: Optional[str]
    max_building_height: Optional[str]
    parking_spaces: Optional[str]
    front_gardening_percentage: Optional[str]
    front_restriction: Optional[str]
    lateral_restrictions: Optional[str]
    rear_restriction: Optional[str]
    building_mode: Optional[str]
    observations: Optional[str]
    hotel_occupation_index: Optional[str]
    increase_land_utilization_coefficient: Optional[str]
    urban_environmental_value_areas: bool
    planned_public_space: bool

class ZoningControlRegulationResponse(ZoningControlRegulationBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True  
    )
