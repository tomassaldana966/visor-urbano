from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.settings import Base

class EconomicActivityBase(Base):
    __tablename__ = 'economic_activity_base'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)

    denue_records = relationship("EconomicUnitsDirectory", back_populates="economic_activity", cascade="all, delete-orphan")