from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class DependencyResolution(Base):
    __tablename__ = 'dependency_resolutions'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    review_id = Column("review_id", BigInteger, ForeignKey('dependency_reviews.id'), nullable=True)
    procedure_id = Column("procedure_id", Integer, ForeignKey('procedures.id'), nullable=False)
    role = Column("role", Integer, nullable=True)
    user_id = Column("user_id", Integer, ForeignKey('users.id'), nullable=True)
    resolution_status = Column("resolution_status", Integer, nullable=True)
    resolution_text = Column("resolution_text", Text, nullable=True)
    resolution_file = Column("resolution_file", Text, nullable=True)
    additional_files = Column("additional_files", Text, nullable=True)
    is_final_resolution = Column("is_final_resolution", Boolean, default=False)
    signature = Column(String(255), nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    review = relationship("DependencyReview", back_populates="resolutions")
    procedure = relationship("Procedure", back_populates="dependency_resolutions")
    user = relationship("UserModel", back_populates="dependency_resolutions")
