"""Test models for password testing without GeoAlchemy2 dependencies."""
from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta, timezone

ModelBase = declarative_base()

class UserTestModel(ModelBase):
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
    
    # Django/AuthUser compatibility fields
    username = Column(String(150), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    is_staff = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_login = Column(DateTime, nullable=True)
    date_joined = Column(DateTime, nullable=True, default=func.now())
    
    # Timestamps
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    role_id = Column(Integer, nullable=True)  # Changed from BigInteger
    
    # Django compatibility properties
    @property
    def first_name(self):
        """Django-style first_name property mapped to name field"""
        return self.name
    
    @first_name.setter
    def first_name(self, value):
        self.name = value
    
    @property
    def last_name(self):
        """Django-style last_name property mapped to paternal_last_name field"""
        return self.paternal_last_name
    
    @last_name.setter
    def last_name(self, value):
        self.paternal_last_name = value
    
    @property
    def full_name(self):
        """Full name combining name and last names"""
        parts = [self.name, self.paternal_last_name]
        if self.maternal_last_name:
            parts.append(self.maternal_last_name)
        return " ".join(parts)

class PasswordRecoveryTestModel(ModelBase):
    __tablename__ = 'password_recoveries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False, unique=True)
    expiration_date = Column(DateTime, nullable=False)
    used = Column(Integer, default=0, nullable=False)  # 0 = unused, 1 = used
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    def is_expired(self):
        """Check if the token has expired"""
        # Convert both to naive datetimes for comparison since SQLAlchemy stores as naive
        current_time = datetime.now(timezone.utc).replace(tzinfo=None)
        expiration_time = self.expiration_date
        if hasattr(expiration_time, 'tzinfo') and expiration_time.tzinfo is not None:
            expiration_time = expiration_time.replace(tzinfo=None)
        return current_time > expiration_time
    
    def is_valid(self):
        """Check if the token is valid (not expired and not used)"""
        return not self.is_expired() and self.used == 0
    
    @classmethod
    def get_expiration_time(cls, hours=24):
        """Get expiration time (default 24 hours from now) as naive datetime"""
        return (datetime.now(timezone.utc) + timedelta(hours=hours)).replace(tzinfo=None)

# Aliases for backward compatibility
TestUser = UserTestModel
TestPasswordRecovery = PasswordRecoveryTestModel

def get_expiration_time(hours=24):
    """Get expiration time (default 24 hours from now) as naive datetime"""
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).replace(tzinfo=None)
