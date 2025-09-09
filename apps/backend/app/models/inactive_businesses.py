from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class InactiveBusiness(Base):
    __tablename__ = 'inactive_businesses'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    business_line_id = Column(Integer, ForeignKey('business_lines.id'), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    
    business_line = relationship("BusinessLine", back_populates="inactive_businesses")
    municipality = relationship("Municipality", back_populates="inactive_businesses")
