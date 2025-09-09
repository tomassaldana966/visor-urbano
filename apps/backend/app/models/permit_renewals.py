from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class PermitRenewal(Base):
    __tablename__ = 'permit_renewals'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    requirements_query_id = Column("id_consulta_requisitos", Integer, ForeignKey('requirements_querys.id'), nullable=True)
    procedure_id = Column("id_tramite", Integer, ForeignKey('procedures.id'), nullable=True)
        
    requirements_query = relationship("RequirementsQuery", back_populates="renewals")
    procedure = relationship("Procedure", back_populates="renewals")
