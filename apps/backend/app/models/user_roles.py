from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class UserRoleModel(Base):
    __tablename__ = 'user_roles'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    description = Column(String(200), nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    municipality = relationship("Municipality", back_populates="user_roles")
    users = relationship("UserModel", back_populates="user_roles", cascade="all, delete-orphan")
    user_assignments = relationship(
        "UserRoleAssignment", 
        back_populates="role",
        foreign_keys="UserRoleAssignment.role_id",
        primaryjoin="UserRoleModel.id == UserRoleAssignment.role_id"
    )
    
    pending_role_assignments = relationship(
        "UserRoleAssignment", 
        back_populates="pending_role",
        foreign_keys="UserRoleAssignment.pending_role_id",
        primaryjoin="UserRoleModel.id == UserRoleAssignment.pending_role_id"
    )
        
    department_assignments = relationship("DepartmentRole", back_populates="role", cascade="all, delete-orphan")