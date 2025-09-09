#TODO Review is still necessary
from sqlalchemy import Column, Integer, String
from config.settings import Base

class Migration(Base):
    __tablename__ = 'migrations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    migration = Column(String(255), nullable=False)
    batch = Column(Integer, nullable=False)
