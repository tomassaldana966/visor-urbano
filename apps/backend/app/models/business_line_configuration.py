from sqlalchemy import Column, Integer, String, Text, DateTime, func
from config.settings import Base

class BusinessLineConfiguration(Base):
    __tablename__ = 'business_line_configurations'  

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_line_id = Column(Integer, nullable=False)  
    setting_key = Column(String(255), nullable=False)     
    setting_value = Column(Text, nullable=True)           

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
