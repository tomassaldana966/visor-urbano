from sqlalchemy import Column, Integer, String, Boolean, Numeric
from sqlalchemy.orm import relationship
from config.settings import Base

class BaseMapLayer(Base):
    __tablename__ = 'base_map_layer'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(100), nullable=False)
    label = Column(String(180), nullable=False)
    layer_type = Column("type", String(20), nullable=False)
    url = Column(String(255), nullable=False)
    layers = Column(String(60), nullable=False)
    visible = Column(Boolean, nullable=False)
    active = Column(Boolean, nullable=False)
    attribution = Column(String(100), nullable=True)
    opacity = Column(Numeric(3, 2), nullable=False)
    server_type = Column(String(60), nullable=True)
    projection = Column(String(20), nullable=False)
    version = Column(String(10), nullable=False)
    format = Column(String(60), nullable=False)
    order_index = Column("order", Integer, nullable=False)
    editable = Column(Boolean, nullable=False)
    geometry_type = Column("type_geom", String(20), nullable=True)
    cql_filter = Column(String(255), nullable=True)

    municipality_associations = relationship("MunicipalityMapLayerBase", back_populates="base_map_layer", cascade="all, delete-orphan")
