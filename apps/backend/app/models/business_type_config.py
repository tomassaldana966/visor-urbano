from sqlalchemy import Column, Integer, Boolean, ForeignKey
from config.settings import Base
from sqlalchemy.orm import relationship

class BusinessTypeConfig(Base):
    __tablename__ = "business_type_configurations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_type_id = Column(Integer, ForeignKey("business_types.id"), nullable=False)
    municipality_id = Column(Integer, ForeignKey("municipalities.id"), nullable=False)
    is_disabled = Column(Boolean, default=False)
    has_certificate = Column(Boolean, default=False)
    impact_level = Column(Integer, nullable=True)
    
    business_type = relationship("BusinessType", back_populates="configurations") 
