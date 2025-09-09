from sqlalchemy import Column, Integer, String, ForeignKey
from geoalchemy2 import Geometry #type: ignore
from sqlalchemy.orm import relationship
from config.settings import Base

class BaseNeighborhood(Base):
    __tablename__ = 'base_neighborhood'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    postal_code = Column(String(20), nullable=True)
    geom = Column(Geometry('MULTIPOLYGON', srid=4326, use_typmod=False, spatial_index=False), nullable=True)
    locality_id = Column(Integer, nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)

    municipality = relationship("Municipality", back_populates="neighborhoods")
    building_footprints = relationship("BuildingFootprint", back_populates="neighborhood", cascade="all, delete-orphan")
    land_parcel_mappings = relationship("LandParcelMapping", back_populates="neighborhood", cascade="all, delete-orphan")
