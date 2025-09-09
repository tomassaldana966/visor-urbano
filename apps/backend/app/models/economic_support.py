from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime
from config.settings import Base

class EconomicSupport(Base):
    __tablename__ = 'economic_supports'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dependency = Column(String(200), default='0')
    scian = Column(Integer, default=0)
    program_name = Column(String(200), default='')
    url = Column(String(255), default='')
    program_description = Column(Text, nullable=False)
    
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
