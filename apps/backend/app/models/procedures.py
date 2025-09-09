from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class Procedure(Base):
    __tablename__ = 'procedures'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    folio = Column(String(255), nullable=True)
    current_step = Column("current_step", Integer, nullable=True)
    user_signature = Column("user_signature", String(255), nullable=True)
    user_id = Column("user_id", Integer, ForeignKey('users.id'), nullable=True)
    window_user_id = Column("window_user_id", Integer, ForeignKey('users.id'), nullable=True)
    entry_role = Column("entry_role", Integer, nullable=True)
    documents_submission_date = Column("documents_submission_date", DateTime, nullable=True)
    procedure_start_date = Column("procedure_start_date", DateTime, nullable=True)
    window_seen_date = Column("window_seen_date", DateTime, nullable=True)
    license_delivered_date = Column("license_delivered_date", DateTime, nullable=True)
    has_signature = Column("has_signature", Integer, nullable=True)
    no_signature_date = Column("no_signature_date", DateTime, nullable=True)
    official_applicant_name = Column("official_applicant_name", String(255), nullable=True)
    responsibility_letter = Column("responsibility_letter", String(255), nullable=True)
    sent_to_reviewers = Column("sent_to_reviewers", Integer, nullable=True)
    sent_to_reviewers_date = Column("sent_to_reviewers_date", DateTime, nullable=True)
    license_pdf = Column("license_pdf", String(255), nullable=True)
    payment_order = Column("payment_order", String(255), nullable=True)
    status = Column(Integer, nullable=False, default=0)  # Status should start at 0 for new procedures
    step_one = Column("step_one", Integer, nullable=True)
    step_two = Column("step_two", Integer, nullable=True)
    step_three = Column("step_three", Integer, nullable=True)
    step_four = Column("step_four", Integer, nullable=True)
    director_approval = Column("director_approval", Integer, nullable=True, default=0)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    window_license_generated = Column("window_license_generated", Integer, nullable=True, default=0)
    procedure_type = Column("procedure_type", String(255), nullable=True)
    license_status = Column("license_status", String(255), nullable=True)
    reason = Column(String(255), nullable=True)  # reason
    renewed_folio = Column("renewed_folio", String(255), nullable=True)
    requirements_query_id = Column("requirements_query_id", Integer, ForeignKey('requirements_querys.id'), nullable=True)
    
    # Address fields for construction procedures
    street = Column(String(255), nullable=True)
    exterior_number = Column(String(100), nullable=True)
    interior_number = Column(String(100), nullable=True)
    neighborhood = Column(String(255), nullable=True)
    reference = Column(String(500), nullable=True)
    project_municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    
    # General municipality for all procedures
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    
    # Business establishment fields for commercial procedures
    establishment_name = Column("establishment_name", String(255), nullable=True)
    establishment_address = Column("establishment_address", String(500), nullable=True)
    establishment_phone = Column("establishment_phone", String(50), nullable=True)
    establishment_area = Column("establishment_area", String(50), nullable=True)  # Surface area in m²
    
    # SCIAN fields for business classification
    scian_code = Column("scian_code", String(100), nullable=True)
    scian_name = Column("scian_name", String(100), nullable=True)
    
    answers = relationship("Answer", back_populates="procedure")
    requirements_query = relationship("RequirementsQuery", back_populates="procedures") 
    renewals = relationship("PermitRenewal", back_populates="procedure", cascade="all, delete-orphan")   
    user = relationship("UserModel", foreign_keys=[user_id], back_populates="procedures")
    window_user = relationship("UserModel", foreign_keys=[window_user_id], back_populates="window_procedures")
    project_municipality = relationship("Municipality", foreign_keys=[project_municipality_id])
    municipality = relationship("Municipality", foreign_keys=[municipality_id])
            
    provisional_openings = relationship("ProvisionalOpening", back_populates="procedure")
    dependency_reviews = relationship("DependencyReview", back_populates="procedure", lazy="select")
    dependency_resolutions = relationship("DependencyResolution", back_populates="procedure", cascade="all, delete-orphan")
    business_signatures = relationship("BusinessSignature", back_populates="procedure", cascade="all, delete-orphan")
    business_logs = relationship("BusinessLog", back_populates="procedure", cascade="all, delete-orphan")
    issue_resolutions = relationship("IssueResolution", back_populates="procedure", cascade="all, delete-orphan")
    chat_reviewers = relationship("ChatReviewer", back_populates="procedure", cascade="all, delete-orphan")
    answers_json = relationship("AnswerJSON", back_populates="procedure", cascade="all, delete-orphan")

class HistoricalProcedure(Base):
    __tablename__ = 'historical_procedures'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    folio = Column(String(255), nullable=True)
    current_step = Column("current_step", Integer, nullable=True)
    user_signature = Column("user_signature", String(255), nullable=True)
    user_id = Column("user_id", Integer, nullable=True)
    window_user_id = Column("window_user_id", Integer, nullable=True)
    entry_role = Column("entry_role", Integer, nullable=True)
    documents_submission_date = Column("documents_submission_date", DateTime, nullable=True)
    procedure_start_date = Column("procedure_start_date", DateTime, nullable=True)
    window_seen_date = Column("window_seen_date", DateTime, nullable=True)
    license_delivered_date = Column("license_delivered_date", DateTime, nullable=True)
    has_signature = Column("has_signature", Integer, nullable=True)
    no_signature_date = Column("no_signature_date", DateTime, nullable=True)
    official_applicant_name = Column("official_applicant_name", String(255), nullable=True)
    responsibility_letter = Column("responsibility_letter", String(255), nullable=True)
    sent_to_reviewers = Column("sent_to_reviewers", Integer, nullable=True)
    sent_to_reviewers_date = Column("sent_to_reviewers_date", DateTime, nullable=True)
    license_pdf = Column("license_pdf", String(255), nullable=True)
    payment_order = Column("payment_order", String(255), nullable=True)
    status = Column(Integer, nullable=False)
    step_one = Column("step_one", Integer, nullable=True)
    step_two = Column("step_two", Integer, nullable=True)
    step_three = Column("step_three", Integer, nullable=True)
    step_four = Column("step_four", Integer, nullable=True)
    director_approval = Column("director_approval", Integer, nullable=True, default=0)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    window_license_generated = Column("window_license_generated", Integer, nullable=True, default=0)
    procedure_type = Column("procedure_type", String(255), nullable=True)
    license_status = Column("license_status", String(255), nullable=True)
    reason = Column(String(255), nullable=True)
    renewed_folio = Column("renewed_folio", String(255), nullable=True)
    requirements_query_id = Column("requirements_query_id", Integer, nullable=True)
    
    # Business establishment fields for commercial procedures (historical)
    establishment_name = Column("establishment_name", String(255), nullable=True)
    establishment_address = Column("establishment_address", String(500), nullable=True)
    establishment_phone = Column("establishment_phone", String(50), nullable=True)
    establishment_area = Column("establishment_area", String(50), nullable=True)  # Surface area in m²
    
    # SCIAN fields for business classification (historical)
    scian_code = Column("scian_code", String(100), nullable=True)
    scian_name = Column("scian_name", String(100), nullable=True)

