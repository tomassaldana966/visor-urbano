from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.settings import Base

class AuthGroup(Base):
    __tablename__ = 'auth_group'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)

    user_groups = relationship("AuthUserGroup", back_populates="group", cascade="all, delete-orphan")
    group_permissions = relationship("AuthGroupPermission", back_populates="group", cascade="all, delete-orphan")        
    