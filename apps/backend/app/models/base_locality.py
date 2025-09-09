from sqlalchemy import Column, Integer, String, ForeignKey
from geoalchemy2 import Geometry #type: ignore
from sqlalchemy.orm import relationship
from config.settings import Base

class BaseLocality(Base):
    __tablename__ = 'base_locality'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    scope = Column(String(15), nullable=False)
    municipality_code = Column(String(5), nullable=False)
    locality_code = Column(String(8), nullable=False)
    geocode = Column(String(12), nullable=False)
    geom = Column(Geometry('MULTIPOLYGON', srid=4326, use_typmod=False, spatial_index=False), nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    
    municipality = relationship("Municipality", back_populates="localities")
    denue_records = relationship("EconomicUnitsDirectory", back_populates="locality", cascade="all, delete-orphan")
    building_footprints = relationship("BuildingFootprint", back_populates="locality", cascade="all, delete-orphan")
    land_parcel_mappings = relationship("LandParcelMapping", back_populates="locality", cascade="all, delete-orphan")
