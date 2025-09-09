from sqlalchemy import Column, Integer, String, Float, ForeignKey
from geoalchemy2 import Geometry #type: ignore
from sqlalchemy.orm import relationship
from config.settings import Base

class BuildingFootprint(Base):
    __tablename__ = 'building_footprints'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    building_code = Column(String(10), nullable=False)
    area_m2 = Column(Float, nullable=True)
    time = Column(Integer, nullable=False)
    source = Column(String(200), nullable=False)
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)
    neighborhood_id = Column(Integer, ForeignKey('base_neighborhood.id'), nullable=True)
    locality_id = Column(Integer, ForeignKey('base_locality.id'), nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)

    neighborhood = relationship("BaseNeighborhood", back_populates="building_footprints")
    locality = relationship("BaseLocality", back_populates="building_footprints")
    municipality = relationship("Municipality", back_populates="building_footprints")
