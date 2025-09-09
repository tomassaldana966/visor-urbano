from sqlalchemy import Column, String, Boolean, Integer, DECIMAL, ForeignKey, Table
from sqlalchemy.orm import relationship
from config.settings import Base

maplayer_municipality = Table(
    "maplayer_municipality",
    Base.metadata,
    Column("maplayer_id", ForeignKey("map_layers.id"), primary_key=True),
    Column("municipality_id", ForeignKey("municipalities.id"), primary_key=True),
)

class MapLayer(Base):
    __tablename__ = 'map_layers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(100), nullable=False)
    label = Column(String(180), nullable=False)
    type = Column(String(20), nullable=False)
    url = Column(String(255), nullable=False)
    layers = Column(String(60), nullable=False)
    visible = Column(Boolean, default=True)
    active = Column(Boolean, default=True)
    attribution = Column(String(100), nullable=True)
    opacity = Column(DECIMAL(3, 2))
    server_type = Column(String(60), nullable=True)
    projection = Column(String(20), default='EPSG:4326')
    version = Column(String(10), default='1.3.0')
    format = Column(String(60), nullable=False)
    order = Column(Integer, default=0)
    editable = Column(Boolean, default=True)
    type_geom = Column(String(20), nullable=True)
    cql_filter = Column(String(255), nullable=True)

    municipalities = relationship("Municipality", secondary=maplayer_municipality, back_populates="map_layers")
