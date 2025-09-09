from sqlalchemy import Column, Integer, String, Boolean
from geoalchemy2 import Geometry #type: ignore
from config.settings import Base

class BaseMunicipality(Base):
    __tablename__ = 'base_municipality'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    municipality_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    entity_code = Column(String(5), nullable=False)
    municipality_code = Column(String(5), nullable=False)
    geocode = Column(String(10), nullable=False)    
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)
    has_zoning = Column(Boolean, nullable=False)
