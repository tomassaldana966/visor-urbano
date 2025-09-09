from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base
from sqlalchemy.sql import func

class TechnicalSheetDownload(Base):
    __tablename__ = 'technical_sheet_downloads'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    city = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    age = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    sector = Column(String(255), nullable=True)
    uses = Column(Text, nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    technical_sheet = relationship("TechnicalSheet", back_populates="technical_sheet_download", uselist=False)
    municipality = relationship("Municipality")