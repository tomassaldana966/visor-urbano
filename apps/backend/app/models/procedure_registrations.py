from sqlalchemy import Column, Integer, String, Float, ForeignKey
from geoalchemy2 import Geometry  # type: ignore
from sqlalchemy.orm import relationship
from config.settings import Base

class ProcedureRegistration(Base):
    __tablename__ = 'procedure_registrations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    reference = Column(String(100), nullable=True)
    area = Column(Float, nullable=False, default=0)
    business_sector = Column("business_sector", String(150), nullable=True)
    procedure_type = Column(String(30), nullable=True)
    procedure_origin = Column(String(30), nullable=True)
    historical_id = Column('historical_id', Integer, nullable=True)
    bbox = Column(String(200), nullable=True)
    geom = Column(Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False), nullable=True)

    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    municipality = relationship("Municipality", back_populates="procedure_registrations")
