from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from config.settings import Base

class BusinessLine(Base):
    __tablename__ = 'business_lines'  
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    inactive_businesses = relationship("InactiveBusiness", back_populates="business_line", cascade="all, delete-orphan")
