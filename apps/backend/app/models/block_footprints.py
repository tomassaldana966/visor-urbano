from sqlalchemy import Column, Integer, Float, String, ForeignKey
from geoalchemy2 import Geometry #type: ignore
from sqlalchemy.orm import relationship
from config.settings import Base

class BlockFootprint(Base):
    __tablename__ = 'block_footprints'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    area_m2 = Column(Float, nullable=True)
    time = Column(Integer, nullable=False)
    source = Column(String(200), nullable=False)
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)
    
    colony_id = Column(Integer, ForeignKey('base_neighborhood.id'), nullable=True)
    locality_id = Column(Integer, ForeignKey('base_locality.id'), nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    
    colony = relationship("BaseNeighborhood", back_populates="block_footprints")
    locality = relationship("BaseLocality", back_populates="block_footprints")
    municipality = relationship("Municipality", back_populates="block_footprints")
