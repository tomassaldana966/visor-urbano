from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class BusinessSectorCertificate(Base):
    __tablename__ = 'business_sector_certificates'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    business_sector_id = Column(Integer, ForeignKey('business_sectors.id'), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    business_sector = relationship("BusinessSector", back_populates="certificates")
    municipality = relationship("Municipality", back_populates="business_sector_certificates")
