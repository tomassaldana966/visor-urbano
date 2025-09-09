from sqlalchemy import Column, Integer, String, func
from geoalchemy2 import Geometry #type: ignore
from config.settings import Base

class BaseAdministrativeDivision(Base):
    __tablename__ = 'base_administrative_division'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(5), nullable=False)
    division_type = Column(String(50), nullable=True)    
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)
