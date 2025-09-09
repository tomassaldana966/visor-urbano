from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.settings import Base

class BusinessSectorConfiguration(Base):
    __tablename__ = 'business_sector_configurations'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    business_sector_id = Column(Integer, ForeignKey('business_sectors.id'), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    inactive_business_flag = Column(Integer, nullable=False)
    business_impact_flag = Column(Integer, nullable=False)
    business_sector_certificate_flag = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    business_sector = relationship("BusinessSector", back_populates="configuration")
    municipality = relationship("Municipality", back_populates="business_sector_configurations")
