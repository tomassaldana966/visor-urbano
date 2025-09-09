from sqlalchemy import Column, BigInteger, Integer, Text, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class ChatReviewer(Base):
    __tablename__ = 'reviewers_chat'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    procedure_id = Column('id_tramite', Integer, ForeignKey('procedures.id'), nullable=False)
    reviewer_id = Column('ir_usuario', Integer, ForeignKey('users.id'), nullable=False)
    role = Column("rol", Integer, nullable=True)
    comment = Column("comentario", Text, nullable=True)
    image = Column("imagen", Text, nullable=True)
    attached_file = Column("archivo_adjunto", String(255), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    
    procedure = relationship("Procedure", back_populates="chat_reviewers")
    reviewer = relationship("UserModel", back_populates="chat_reviewers")
