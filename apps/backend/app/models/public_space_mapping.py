from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry #type: ignore
from config.settings import Base

class PublicSpace(Base):
    __tablename__ = 'public_space_mapping'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)      
    space_type = Column(String(40), nullable=True) 
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)
