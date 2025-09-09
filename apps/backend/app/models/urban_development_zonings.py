from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from geoalchemy2 import Geometry #type: ignore
from sqlalchemy.orm import relationship
from config.settings import Base

class UrbanDevelopmentZoning(Base):
    __tablename__ = 'urban_development_zonings' #zonificacion_zonadesarrollourbanodev
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    district = Column(String(120), nullable=False)  # distrito
    sub_district = Column(String(18), nullable=True)  # sub_distrito
    publication_date = Column(Date, nullable=True)    # fecha_de_publicacion
    primary_area_classification_key = Column(String(50), nullable=True)  # clave_de_clasificacion_de_area_primaria
    primary_area_classification_description = Column(String(255), nullable=True)  # descripcion_de_clasificacion_de_area_primaria
    secondary_area_classification_key = Column(String(50), nullable=True)  # clave_de_clasificacion_de_area_secundaria
    secondary_area_classification_description = Column(String(255), nullable=True)  # descripcion_de_clasificacion_de_area_secundaria
    land_use_key = Column(String(50), nullable=True)  # clave_de_uso_de_suelo
    primary_zone_classification_key = Column(String(255), nullable=True)  # clave_de_clasificacion_de_zona_primaria
    primary_zone_classification_description = Column(String(255), nullable=True)  # descripcion_de_clasificacion_de_zona_primaria
    secondary_zone_classification_key = Column(String(255), nullable=True)  # clave_de_clasificacion_de_zona_secundaria
    secondary_zone_classification_description = Column(String(255), nullable=True)  # descripcion_de_clasificacion_de_zona_secundaria
    area_classification_number = Column(String(50), nullable=True)  # numero_de_clasificacion_de_area
    zone_classification_number = Column(String(50), nullable=True)  # numero_de_clasificacion_de_zona
    zoning_key = Column(String(160), nullable=True)  # clave_de_zonificacion
    restriction = Column(String(250), nullable=True)  # restriccion
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)  # geom
    user = Column(String(60), nullable=True)  # usuario
    record_timestamp = Column('timestamp', DateTime(timezone=True), nullable=True)  # "timestamp"
    aux = Column(String(50), nullable=True)  # aux
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)  # municipio_id
    
    municipality = relationship("Municipality", back_populates="urban_development_zonings")
