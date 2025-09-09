from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class ProvisionalOpening(Base):
    __tablename__ = 'provisional_openings'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    folio = Column(String(255), nullable=False)
    procedure_id = Column(Integer, ForeignKey('procedures.id'), nullable=True)
    counter = Column(Integer, nullable=True)
    granted_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    granted_role = Column(Integer, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    procedure = relationship("Procedure", back_populates="provisional_openings")
    granted_by_user = relationship("UserModel", back_populates="provisional_openings_granted", foreign_keys=[granted_by_user_id])
    municipality = relationship("Municipality", back_populates="provisional_openings")
    created_by_user = relationship("UserModel", foreign_keys=[created_by])
