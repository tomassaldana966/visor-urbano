from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class MunicipalityMapLayerBase(Base):
    __tablename__ = 'municipality_map_layer_base'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    map_layer_id = Column(Integer, ForeignKey('base_map_layer.id'), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    
    base_map_layer = relationship("BaseMapLayer", back_populates="municipality_associations")
    municipality = relationship("Municipality", back_populates="base_map_layer_associations")
