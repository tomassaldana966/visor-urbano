from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.settings import Base

class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    content_type_id = Column(Integer, nullable=False)
    codename = Column(String(100), nullable=False)
    
    group_permissions = relationship("AuthGroupPermission", back_populates="permission", cascade="all, delete-orphan")
    user_permissions = relationship("AuthUserUserPermission", back_populates="permission", cascade="all, delete-orphan")
