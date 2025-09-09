from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('auth_group.id'), nullable=False)
    
    user = relationship("UserModel", back_populates="user_groups")
    group = relationship("AuthGroup", back_populates="user_groups")
