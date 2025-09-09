from sqlalchemy import Column, BigInteger, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.settings import Base

class BusinessSignature(Base):
    __tablename__ = 'business_signatures'
     
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    procedure_id = Column("procedure_id", Integer, ForeignKey('procedures.id'), nullable=False)
    user_id = Column("user_id", Integer, ForeignKey('users.id'), nullable=False)
    role = Column("role", Integer, nullable=False)
    hash_to_sign = Column("hash_to_sign", Text, nullable=True)
    signed_hash = Column("signed_hash", Text, nullable=True)
    response = Column(JSON, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    procedure = relationship("Procedure", back_populates="business_signatures")
    user = relationship("UserModel", back_populates="business_signatures")
