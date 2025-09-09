from sqlalchemy import Column, BigInteger, Integer, String, Text, Date, DateTime, Numeric, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class RequirementsQuery(Base):
    __tablename__ = 'requirements_querys'  # Temporarily use old name until migration
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    folio = Column(String(255), nullable=True)
    street = Column(String(100), nullable=False)
    neighborhood = Column(String(100), nullable=False)
    municipality_name = Column(String(50), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    scian_code = Column(String(100), nullable=False)
    scian_name = Column(String(100), nullable=False)
    property_area = Column(Numeric(12, 2), nullable=False, default=0)
    activity_area = Column(Numeric(12, 2), nullable=False, default=0)
    applicant_name = Column(String(100), nullable=True)
    applicant_character = Column(String(100), nullable=True)
    person_type = Column(String(100), nullable=True)
    minimap_url = Column(Text, nullable=True)
    restrictions = Column(JSON, nullable=True)
    status = Column(Integer, nullable=False, default=1)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, default=0)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    year_folio = Column(Integer, nullable=False, default=1)
    alcohol_sales = Column(Integer, nullable=False, default=0)
    primary_folio = Column(String(255), nullable=True)
    issue_license = Column(Integer, nullable=False, default=0)
    
    # New fields for license type and specific information
    license_type = Column(String(50), nullable=True)  # 'commercial' or 'construction'
    scian = Column(String(100), nullable=True)  # For commercial licenses
    entry_date = Column(Date, nullable=True)  # Common field for both types
    interested_party = Column(String(255), nullable=True)  # For construction licenses
    last_resolution = Column(Text, nullable=True)  # For construction licenses
    resolution_sense = Column(String(50), nullable=True)  # For construction licenses ('approved', 'denied', 'pending')

    municipality = relationship("Municipality", back_populates="requirements_queries")    
    renewals = relationship("PermitRenewal", back_populates="requirements_query", cascade="all, delete-orphan")
    procedures = relationship("Procedure", back_populates="requirements_query")
    user = relationship("UserModel", back_populates="requirements_queries")
    answers = relationship("Answer", back_populates="requirements_query")