from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class Requirement(Base):
    __tablename__ = 'requirements'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    municipality_id = Column("municipality_id", Integer, ForeignKey('municipalities.id'), nullable=False)
    field_id = Column("field_id", Integer, ForeignKey('fields.id'), nullable=False)
    requirement_code = Column("requirement_code", String(300), nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    municipality = relationship("Municipality", back_populates="requirements")
    field = relationship("Field", back_populates="requirements")
