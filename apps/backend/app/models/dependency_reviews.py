from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class DependencyReview(Base):
    __tablename__ = 'dependency_reviews'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    procedure_id = Column("procedure_id", Integer, ForeignKey('procedures.id'), nullable=False)
    municipality_id = Column("municipality_id", Integer, ForeignKey('municipalities.id'), nullable=False)
    folio = Column(String(255), nullable=False, unique=True)
    role = Column("role", Integer, nullable=False)  # Mantener para compatibilidad
    department_id = Column("department_id", Integer, ForeignKey('departments.id'), nullable=True)  # Nuevo sistema basado en departamentos
    start_date = Column("start_date", DateTime, nullable=True)
    update_date = Column("update_date", DateTime, nullable=True)
    current_status = Column("current_status", Integer, nullable=True)
    current_file = Column("current_file", Text, nullable=True)
    signature = Column(String(255), nullable=True)
    user_id = Column("user_id", Integer, ForeignKey('users.id'), nullable=True)
    director_approved = Column("director_approved", Integer, default=0)
    sent_to_reviewers = Column("sent_to_reviewers", DateTime, nullable=True)
    license_pdf = Column("license_pdf", Text, nullable=True)
    license_issued = Column("license_issued", Boolean, default=False)
    payment_order_file = Column("payment_order_file", Text, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    procedure = relationship("Procedure", back_populates="dependency_reviews")
    municipality = relationship("Municipality", back_populates="dependency_reviews")
    user = relationship("UserModel", back_populates="dependency_reviews")
    department = relationship("Department", back_populates="dependency_reviews")
    resolutions = relationship("DependencyResolution", back_populates="review")
    prevention_requests = relationship("PreventionRequest", back_populates="review")
    notifications = relationship("Notification", back_populates="review")

class PreventionRequest(Base):
    __tablename__ = 'prevention_requests'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column("review_id", BigInteger, ForeignKey('dependency_reviews.id'), nullable=False)
    procedure_id = Column("procedure_id", Integer, ForeignKey('procedures.id'), nullable=False)
    role = Column("role", Integer, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey('users.id'), nullable=False)
    comments = Column("comments", Text, nullable=True)
    max_resolution_date = Column("max_resolution_date", DateTime, nullable=True)
    business_days = Column("business_days", Integer, default=15)
    status = Column("status", Integer, default=0)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    review = relationship("DependencyReview")
    procedure = relationship("Procedure")
    user = relationship("UserModel")

class DirectorApproval(Base):
    __tablename__ = 'director_approvals'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column("review_id", BigInteger, ForeignKey('dependency_reviews.id'), nullable=False)
    procedure_id = Column("procedure_id", Integer, ForeignKey('procedures.id'), nullable=False)
    municipality_id = Column("municipality_id", Integer, ForeignKey('municipalities.id'), nullable=False)
    folio = Column("folio", String(255), nullable=False)
    director_id = Column("director_id", Integer, ForeignKey('users.id'), nullable=False)
    approval_status = Column("approval_status", Integer, default=0)
    approval_comments = Column("approval_comments", Text, nullable=True)
    approved_at = Column("approved_at", DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    review = relationship("DependencyReview")
    procedure = relationship("Procedure")
    municipality = relationship("Municipality")
    director = relationship("UserModel")
