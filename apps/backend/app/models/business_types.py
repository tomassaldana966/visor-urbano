from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from config.settings import Base
from sqlalchemy.orm import relationship

class BusinessType(Base):
    __tablename__ = 'business_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    code = Column(String(50), nullable=True)  # SCIAN code
    related_words = Column(String(500), nullable=True)  
    
    configurations = relationship("BusinessTypeConfig", back_populates="business_type")

    def __repr__(self):
        return f"<BusinessType(id={self.id}, name='{self.name}')>"

