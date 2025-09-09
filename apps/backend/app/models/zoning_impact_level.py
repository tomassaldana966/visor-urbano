from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry # type: ignore
from config.settings import Base

class ZoningImpactLevel(Base):
    __tablename__ = 'zoning_impact_level'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    impact_level = Column(Integer, nullable=False)
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    municipality = relationship("Municipality", back_populates="zoning_impact_levels")
