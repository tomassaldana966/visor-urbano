from sqlalchemy import Column, Integer, String
from config.settings import Base

class EconomicActivitySector(Base):
    __tablename__ = 'economic_activity_sector'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
