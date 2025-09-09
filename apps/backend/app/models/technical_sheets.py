from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base
from sqlalchemy.sql import func

class TechnicalSheet(Base):
    __tablename__ = 'technical_sheets'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    square_meters = Column(Text, nullable=False)
    coordinates = Column(Text, nullable=False)
    image = Column(Text, nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    technical_sheet_download_id = Column(Integer, ForeignKey('technical_sheet_downloads.id'), nullable=True)
    
    municipality = relationship("Municipality", back_populates="technical_sheets")
    technical_sheet_download = relationship("TechnicalSheetDownload", back_populates="technical_sheet")
