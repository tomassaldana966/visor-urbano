from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry #type: ignore
from config.settings import Base

class EconomicUnitsDirectory(Base):
    __tablename__ = 'economic_units_directory'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    directory_type = Column(String(50), nullable=False, default='denue')
    
    commercial_name = Column(String(150), nullable=False)
    legal_name = Column(String(150), nullable=True)
    economic_activity_name = Column(String(250), nullable=True)
    employed_people = Column(String(20), nullable=True)
    
    road_type = Column(String(40), nullable=True)
    road_name = Column(String(150), nullable=True)
    road_type_ext_1 = Column(String(40), nullable=True)
    road_name_ext_1 = Column(String(150), nullable=True)
    road_type_ext_2 = Column(String(40), nullable=True)
    road_name_ext_2 = Column(String(150), nullable=True)
    road_type_ext_3 = Column(String(40), nullable=True)
    road_name_ext_3 = Column(String(150), nullable=True)
    
    exterior_number = Column(Integer, nullable=True)
    exterior_letter = Column(String(35), nullable=True)
    building = Column(String(35), nullable=True)
    building_level = Column(String(35), nullable=True)
    interior_number = Column(Integer, nullable=True)
    interior_letter = Column(String(35), nullable=True)
    
    settlement_type = Column(String(35), nullable=True)
    settlement_name = Column(String(100), nullable=True)
    mall_type = Column(String(30), nullable=True)
    mall_name = Column(String(100), nullable=True)
    local_number = Column(String(35), nullable=True)
    postal_code = Column(String(5), nullable=True)
    municipality_name = Column(String(150), nullable=True)
    
    ageb = Column(String(4), nullable=True)
    block = Column(String(4), nullable=True)
    
    phone = Column(String(20), nullable=True)
    email = Column(String(80), nullable=True)
    website = Column(String(70), nullable=True)
    registration_date = Column(String(15), nullable=True)
    edited = Column(Boolean, nullable=False)
    
    geom = Column(Geometry('POINT', srid=32613, use_typmod=False, spatial_index=False), nullable=True)
    
    economic_activity_id = Column(Integer, ForeignKey('economic_activity_base.id'), nullable=False)
    locality_id = Column(Integer, ForeignKey('base_locality.id'), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    
    economic_activity = relationship("EconomicActivityBase", back_populates="denue_records")
    locality = relationship("BaseLocality", back_populates="denue_records")
    municipality = relationship("Municipality", back_populates="denue_records")
