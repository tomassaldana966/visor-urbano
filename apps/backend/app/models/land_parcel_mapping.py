from sqlalchemy import Column, Integer, Float, String, ForeignKey
from geoalchemy2 import Geometry #type: ignore
from sqlalchemy.orm import relationship
from config.settings import Base

class LandParcelMapping(Base):
    __tablename__ = 'land_parcel_mapping'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    area_m2 = Column(Float, nullable=True)
    time = Column(Integer, nullable=False)
    source = Column(String(200), nullable=False)
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)
    
    neighborhood_id = Column(Integer, ForeignKey('base_neighborhood.id'), nullable=True)
    locality_id = Column(Integer, ForeignKey('base_locality.id'), nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    
    neighborhood = relationship("BaseNeighborhood", back_populates="land_parcel_mappings")
    locality = relationship("BaseLocality", back_populates="land_parcel_mappings")
    municipality = relationship("Municipality", back_populates="land_parcel_mappings")
