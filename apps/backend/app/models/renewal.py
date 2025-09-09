from sqlalchemy import Column, Integer, String, Text, DateTime, func
from config.settings import Base

class Renewal(Base):
    __tablename__ = 'renewals'  
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    license_id = Column(Integer, nullable=False)       
    renewal_date = Column(DateTime, nullable=False)      
    status = Column(String(50), nullable=True)           
    observations = Column(Text, nullable=True)          
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
