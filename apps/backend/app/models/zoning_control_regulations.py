from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class ZoningControlRegulation(Base):
    __tablename__ = 'zoning_control_regulations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    district = Column(String(2), nullable=False)
    regulation_key = Column(String(160), nullable=False)
    land_use = Column(String(200), nullable=False)
    density = Column(String(190), nullable=True)
    intensity = Column(String(190), nullable=True)
    business_sector = Column(String(255), nullable=True)
    minimum_area = Column(String(190), nullable=True)
    minimum_frontage = Column(String(190), nullable=True)
    building_index = Column(String(190), nullable=True)
    land_occupation_coefficient = Column(String(190), nullable=True)
    land_utilization_coefficient = Column(String(190), nullable=True)
    max_building_height = Column(String(190), nullable=True)
    parking_spaces = Column(String(190), nullable=True)
    front_gardening_percentage = Column(String(190), nullable=True)
    front_restriction = Column(String(190), nullable=True)
    lateral_restrictions = Column(String(190), nullable=True)
    rear_restriction = Column(String(190), nullable=True)
    building_mode = Column(String(190), nullable=True)
    observations = Column(Text, nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    
    urban_environmental_value_areas = Column(Boolean, nullable=False)
    planned_public_space = Column(Boolean, nullable=False)
    increase_land_utilization_coefficient = Column(String(190), nullable=True)
    hotel_occupation_index = Column(String(160), nullable=True)
    
    municipality = relationship("Municipality", back_populates="zoning_control_regulations")    