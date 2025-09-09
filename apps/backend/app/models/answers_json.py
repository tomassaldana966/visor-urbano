from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class AnswerJSON(Base):
    __tablename__ = 'answers_json'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    procedure_id = Column("procedure_id", Integer, ForeignKey('procedures.id'), nullable=False)
    user_id = Column("user_id", Integer, ForeignKey('users.id'), nullable=False)
    answers = Column("answers", JSON, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    procedure = relationship("Procedure", back_populates="answers_json")
    user = relationship("UserModel", back_populates="answers_json")
