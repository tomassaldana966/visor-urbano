from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.settings import Base

class BusinessSector(Base):
    __tablename__ = 'business_sectors'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String(255), nullable=True)
    industry_classification_code = Column("SCIAN", String(255), nullable=True)
    related_words = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    certificates = relationship("BusinessSectorCertificate", back_populates="business_sector", cascade="all, delete-orphan")
    configuration = relationship("BusinessSectorConfiguration", back_populates="business_sector", uselist=False, cascade="all, delete-orphan")
    impacts = relationship("BusinessSectorImpact", back_populates="business_sector", cascade="all, delete-orphan", lazy="select")
