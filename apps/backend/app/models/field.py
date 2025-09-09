from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class Field(Base):
    __tablename__ = 'fields'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    field_type = Column("type", String(100), nullable=False)
    description = Column(Text, nullable=True)
    description_rec = Column(Text, nullable=True)
    rationale = Column(String(255), nullable=True)
    options = Column(String(255), nullable=True)
    options_description = Column(String(255), nullable=True)
    step = Column(Integer, nullable=True)
    sequence = Column(Integer, nullable=True)
    required = Column(Integer, nullable=True)
    visible_condition = Column(String(255), nullable=True)
    affected_field = Column(String(100), nullable=True)
    procedure_type = Column(String(100), nullable=True)
    dependency_condition = Column(String(255), nullable=True)
    trade_condition = Column(String(255), nullable=True)
    status = Column(Integer, nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    editable = Column(Integer, default=0)
    static_field = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    required_official = Column(Integer, default=1)
    
    municipality = relationship("Municipality", back_populates="fields")
    requirements = relationship("Requirement", back_populates="field")    
    department_assignments = relationship("RequirementDepartmentAssignment", back_populates="field", cascade="all, delete-orphan")
