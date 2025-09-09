"""
Test models that mirror the production models but without PostGIS dependencies.
These models are used during testing to avoid SQLite/PostGIS compatibility issues.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Procedure(Base):
    """Test model for Procedure without PostGIS dependencies."""
    __tablename__ = 'procedures'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    folio = Column(String(255), unique=True, nullable=False)
    status = Column(String(50), nullable=False, default='active')
    title = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    priority = Column(String(20), nullable=True)
    assigned_to = Column(String(255), nullable=True)
    procedure_type = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    payment_order = Column(String(500), nullable=True)
    renewed_folio = Column(String(255), nullable=True)
    requirements_query_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    window_user_id = Column(Integer, nullable=True)
    documents_submission_date = Column(DateTime, nullable=True)
    procedure_start_date = Column(DateTime, nullable=True)
    window_seen_date = Column(DateTime, nullable=True)
    license_delivered_date = Column(DateTime, nullable=True)
    no_signature_date = Column(DateTime, nullable=True)
    sent_to_reviewers_date = Column(DateTime, nullable=True)

class User(Base):
    """Test model for User without PostGIS dependencies."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    paternal_last_name = Column(String(50), nullable=False)
    maternal_last_name = Column(String(50), nullable=True)
    user_tax_id = Column(String(50), nullable=True)
    national_id = Column(String(50), nullable=True)
    cellphone = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    api_token = Column(String(100), nullable=True)
    api_token_expiration = Column(DateTime, nullable=True)
    subrole_id = Column(Integer, nullable=True)
    municipality_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    role_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=True)

class PasswordRecovery(Base):
    """Test model for PasswordRecovery without PostGIS dependencies."""
    __tablename__ = 'password_recoveries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    expiration_date = Column(DateTime, nullable=False)
    used = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    def is_expired(self):
        """Check if the token has expired"""
        current_time = datetime.now()
        return current_time > self.expiration_date
    
    def is_valid(self):
        """Check if the token is valid (not expired and not used)"""
        return not self.is_expired() and self.used == 0

class Municipality(Base):
    """Test model for Municipality without PostGIS dependencies."""
    __tablename__ = 'municipalities'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    image = Column(String(250), nullable=True)
    director = Column(String(250), nullable=True)
    director_signature = Column(String(250), nullable=True)
    process_sheet = Column(Integer, nullable=True, default=1)
    solving_days = Column(Integer, nullable=True)
    issue_license = Column(Integer, nullable=True, default=0)
    address = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    responsible_area = Column(String(250), nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    window_license_generation = Column(Integer, nullable=True, default=0)
    license_restrictions = Column(Text, nullable=True, default='')
    license_price = Column(String(255), nullable=True)
    initial_folio = Column(Integer, nullable=True)
    has_zoning = Column(Boolean, default=False, nullable=True)

class BusinessSignature(Base):
    """Test model for BusinessSignature without PostGIS dependencies."""
    __tablename__ = 'business_signatures'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    signature_data = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
