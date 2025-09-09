from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey('auth_group.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('auth_permission.id'), nullable=False)
    
    group = relationship("AuthGroup", back_populates="group_permissions")
    permission = relationship("AuthPermission", back_populates="group_permissions")
