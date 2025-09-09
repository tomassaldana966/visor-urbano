from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from config.settings import Base

class Answer(Base):
    __tablename__ = 'answers'  
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    procedure_id = Column(Integer, ForeignKey('procedures.id'), nullable=True)  
    requirements_query_id = Column(Integer, ForeignKey('requirements_querys.id'), nullable=True)
    name = Column(String(255), nullable=True)
    value = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  
    status = Column(Integer, default=1, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
        
    procedure = relationship("Procedure", back_populates="answers")
    requirements_query = relationship("RequirementsQuery", back_populates="answers")
    users = relationship("UserModel", back_populates="answers")
