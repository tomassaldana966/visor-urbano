from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class BusinessSectorImpact(Base):
    __tablename__ = 'business_sector_impacts'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    business_sector_id = Column(Integer, ForeignKey('business_sectors.id'), nullable=False)
    impact = Column(Integer, nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    business_sector = relationship("BusinessSector", back_populates="impacts")
    municipality = relationship("Municipality", back_populates="business_sector_impacts")
