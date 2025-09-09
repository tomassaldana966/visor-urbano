from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base
from app.models.national_id import UserNationalID 
from app.models.user_tax_id import ClientTaxID
from app.models.municipality import Municipality

class UserModel(Base):
    __tablename__ = 'users'
    
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # Core user information (keeping Spanish naming convention for legacy compatibility)
    name = Column(String(50), nullable=False)  # first_name equivalent
    paternal_last_name = Column(String(50), nullable=False)  # last_name equivalent  
    maternal_last_name = Column(String(50), nullable=True)  # Additional Spanish convention
    user_tax_id = Column(String(50), nullable=True)
    national_id = Column(String(50), nullable=True)
    cellphone = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    
    # API and tokens
    api_token = Column(String(100), nullable=True)
    api_token_expiration = Column(DateTime, nullable=True)
    
    # Role and municipality relationships
    subrole_id = Column(Integer, ForeignKey('sub_roles.id'), nullable=True)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    role_id = Column(BigInteger, ForeignKey('user_roles.id'), nullable=True)
    
    # Django/AuthUser compatibility fields (consolidated)
    username = Column(String(150), nullable=True)  # Django username field
    is_active = Column(Boolean, nullable=False, default=True)  # Active status
    is_staff = Column(Boolean, nullable=False, default=False)  # Django staff status
    is_superuser = Column(Boolean, nullable=False, default=False)  # Django superuser status
    
    # Timestamps
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)  # Django last login
    date_joined = Column(DateTime(timezone=True), nullable=True, default=func.now())  # Django date joined
    
     
    tax_id_relation = relationship(lambda: ClientTaxID, back_populates="user", uselist=False)
    national_id_relation = relationship(lambda: UserNationalID, back_populates="user", uselist=False)
    municipality = relationship("Municipality", back_populates="users")
    answers = relationship("Answer", back_populates="users")    
    role_assignment = relationship(
        "UserRoleAssignment",
        back_populates="user",
        uselist=False, 
        primaryjoin="UserModel.id == UserRoleAssignment.user_id",
        cascade="all, delete-orphan"
    )
    user_roles = relationship("UserRoleModel", back_populates="users", uselist=False)
    sub_role = relationship("SubRoleModel", back_populates="users")
    
    business_license_histories = relationship("BusinessLicenseHistory", back_populates="payment_user")    
    provisional_openings_granted = relationship("ProvisionalOpening", back_populates="granted_by_user", foreign_keys="ProvisionalOpening.granted_by_user_id")
    
    # Relationships that were in AuthUser
    procedures = relationship("Procedure", back_populates="user", 
                             foreign_keys="Procedure.user_id")
    
    window_procedures = relationship("Procedure", back_populates="window_user", 
                                   foreign_keys="Procedure.window_user_id")
    
    requirements_queries = relationship("RequirementsQuery", back_populates="user", cascade="all, delete-orphan")
    business_signatures = relationship("BusinessSignature", back_populates="user", cascade="all, delete-orphan")
    business_logs = relationship("BusinessLog", back_populates="user", cascade="all, delete-orphan")
    business_line_logs = relationship("BusinessLineLog", back_populates="user", cascade="all, delete-orphan")
    dependency_resolutions = relationship("DependencyResolution", back_populates="user", cascade="all, delete-orphan")
    dependency_reviews = relationship("DependencyReview", back_populates="user", cascade="all, delete-orphan")
    issue_resolutions = relationship("IssueResolution", back_populates="user", cascade="all, delete-orphan")
    auth_tokens = relationship("AuthToken", back_populates="user", cascade="all, delete-orphan")
    user_groups = relationship("AuthUserGroup", back_populates="user", cascade="all, delete-orphan")
    user_permissions = relationship("AuthUserUserPermission", back_populates="user", cascade="all, delete-orphan")
    
    # Additional relationships migrated from AuthUser
    chat_reviewers = relationship("ChatReviewer", back_populates="reviewer", cascade="all, delete-orphan")
    answers_json = relationship("AnswerJSON", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    department_assignments = relationship("DepartmentUserAssignment", back_populates="user", cascade="all, delete-orphan")
    
    # Django compatibility properties for seamless migration
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
    
    def __repr__(self):
        return f"<UserModel(id={self.id}, email='{self.email}', name='{self.full_name}'>"