from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('auth_permission.id'), nullable=False)
    
    user = relationship("UserModel", back_populates="user_permissions")
    permission = relationship("AuthPermission", back_populates="user_permissions")
