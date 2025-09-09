from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class BusinessLog(Base):
    __tablename__ = 'business_logs'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    action = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    previous_value = Column(String(1000), nullable=True)
    procedure_id = Column(Integer, ForeignKey('procedures.id'), nullable=True)
    host = Column(String(255), nullable=True)
    user_ip = Column(String(255), nullable=True)
    post_request = Column(String(1000), nullable=True)
    device = Column(String(255), nullable=True)
    log_type = Column(Integer, nullable=True)
    role_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    user = relationship("UserModel", back_populates="business_logs", foreign_keys=[user_id])
    procedure = relationship("Procedure", back_populates="business_logs", foreign_keys=[procedure_id])
