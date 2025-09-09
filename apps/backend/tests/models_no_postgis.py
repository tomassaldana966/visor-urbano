"""
Test models that mirror the production models but without PostGIS dependencies.
These models are used during testing to avoid SQLite/PostGIS compatibility issues.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
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
    role_id = Column(Integer, nullable=True)
    
    # Django/AuthUser compatibility fields
    username = Column(String(150), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_staff = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_login = Column(DateTime, nullable=True)
    date_joined = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    
    # Django compatibility properties
    @property
    def first_name(self):
        return self.name
    
    @first_name.setter
    def first_name(self, value):
        self.name = value
    
    @property
    def last_name(self):
        return self.paternal_last_name
    
    @last_name.setter  
    def last_name(self, value):
        self.paternal_last_name = value
    
    @property
    def full_name(self):
        parts = [self.name, self.paternal_last_name]
        if self.maternal_last_name:
            parts.append(self.maternal_last_name)
        return " ".join(parts)

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
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    responsible_area = Column(String(250), nullable=True)
    allow_online_procedures = Column(Boolean, default=False, nullable=True)
    allow_window_reviewer_licenses = Column(Boolean, default=False, nullable=True)
    low_impact_license_cost = Column(String(255), nullable=True)
    license_additional_text = Column(Text, nullable=True)
    theme_color = Column(String(7), nullable=True)
    code = Column(String(10), nullable=True)
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

class BusinessLineLog(Base):
    """Test model for BusinessLineLog without PostGIS dependencies."""
    __tablename__ = 'business_line_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(255), nullable=False)
    previous = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    log_type = Column(Integer, nullable=False)
    procedure_id = Column(Integer, nullable=True)
    host = Column(String(255), nullable=True)
    user_ip = Column(String(45), nullable=True)
    role_id = Column(Integer, nullable=True)
    user_agent = Column(Text, nullable=True)
    post_request = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    
    user = relationship("AuthUser", back_populates="business_line_logs")

class AuthUser(Base):
    """Test model for AuthUser without PostGIS dependencies."""
    __tablename__ = 'auth_user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime, nullable=False)
    
    business_line_logs = relationship("BusinessLineLog", back_populates="user")

class RequirementsQuery(Base):
    """Test model for RequirementsQuery without PostGIS dependencies."""
    __tablename__ = 'requirements_querys'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

class UserRole(Base):
    """Test model for UserRole without PostGIS dependencies."""
    __tablename__ = 'user_roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    description = Column(String(200), nullable=True)
    municipality_id = Column(Integer, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
