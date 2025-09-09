from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class SubRoleModel(Base):
    __tablename__ = 'sub_roles'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)

    municipality = relationship("Municipality", back_populates="sub_roles")
    users = relationship("UserModel", back_populates="sub_role")