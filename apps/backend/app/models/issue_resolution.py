from sqlalchemy import Column, BigInteger, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class IssueResolution(Base):
    __tablename__ = 'issue_resolutions'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    procedure_id = Column("id_tramite", Integer, ForeignKey('procedures.id'), nullable=False)
    role = Column("rol", Integer, nullable=True)
    user_id = Column("id_usuario", Integer, ForeignKey('users.id'), nullable=True)
    comment = Column("comentario", Text, nullable=True)
    user_comment = Column("comentario_usuario", Text, nullable=True)
    files = Column("archivos", Text, nullable=True)
    maximum_resolution_date = Column("fecha_maxima_solventacion", DateTime, nullable=True)
    documents_submission_date = Column("fecha_ingreso_documentos", DateTime, nullable=True)
    seen_date = Column("fecha_visto", DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    procedure = relationship("Procedure", back_populates="issue_resolutions")
    user = relationship("UserModel", back_populates="issue_resolutions")
