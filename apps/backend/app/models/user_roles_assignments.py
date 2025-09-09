from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class UserRoleAssignment(Base):        
    __tablename__ = 'user_roles_assignments'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())    
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    role_id = Column(BigInteger, ForeignKey('user_roles.id'), nullable=True)
    pending_role_id = Column(Integer, ForeignKey('user_roles.id'), nullable=True)        
    role_status = Column(String(20), nullable=True)
    
    token = Column(String(36), nullable=True)
                
    user = relationship("UserModel", back_populates="role_assignment", foreign_keys=[user_id])
        
    role = relationship(
        "UserRoleModel", 
        back_populates="user_assignments",
        foreign_keys=[role_id],
        primaryjoin="UserRoleAssignment.role_id == UserRoleModel.id"
    )
    
    pending_role = relationship(
        "UserRoleModel", 
        back_populates="pending_role_assignments",
        foreign_keys=[pending_role_id],
        primaryjoin="UserRoleAssignment.pending_role_id == UserRoleModel.id"
    )