from sqlalchemy import Column, Integer, String, Text, DateTime, func
from config.settings import Base

class RenewalFileHistory(Base):
    __tablename__ = 'renewal_file_histories'  
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    renewal_id = Column(Integer, nullable=False)  
    file_name = Column(String(255), nullable=False)  
    description = Column(Text, nullable=True)       
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
