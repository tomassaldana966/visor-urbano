from sqlalchemy import Column, BigInteger, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class RenewalFile(Base):
    __tablename__ = 'renewal_files'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    file = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    renewal_id = Column("renewal_id", Integer, ForeignKey('renewals.id'), nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    renewal = relationship("Renewal", back_populates="files")
