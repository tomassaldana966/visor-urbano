from sqlalchemy import Column, Integer, Float
from geoalchemy2 import Geometry #type: ignore
from config.settings import Base

class WaterBodyFootprint(Base):
    __tablename__ = 'water_body_footprints'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    area_m2 = Column(Float, nullable=True)  
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)
