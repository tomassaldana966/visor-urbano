from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class Department(Base):
    """
    Departments that can review procedures.
    Separated from user roles for greater flexibility.
    """
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    code = Column(String(20), nullable=False, unique=True)  # Unique code for identification
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Department configuration
    can_approve_procedures = Column(Boolean, default=True)
    can_reject_procedures = Column(Boolean, default=True)
    requires_all_requirements = Column(Boolean, default=False)  # If requires ALL fields or just some
    
    # Metadata
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    municipality = relationship("Municipality", back_populates="departments")
    department_roles = relationship("DepartmentRole", back_populates="department", cascade="all, delete-orphan")
    user_assignments = relationship("DepartmentUserAssignment", back_populates="department", cascade="all, delete-orphan")
    dependency_reviews = relationship("DependencyReview", back_populates="department")
    requirement_assignments = relationship(
        "RequirementDepartmentAssignment", 
        back_populates="department", 
        cascade="all, delete-orphan",
        foreign_keys="RequirementDepartmentAssignment.department_id"
    )
    workflow_steps = relationship("DependencyReviewWorkflow", back_populates="department", cascade="all, delete-orphan")
    procedure_flows = relationship("ProcedureDepartmentFlow", back_populates="department", cascade="all, delete-orphan")


class DepartmentRole(Base):
    """
    Mapping of user roles to departments.
    A department can have multiple roles, a role can be in multiple departments.
    """
    __tablename__ = 'department_roles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    
    # Role-specific permissions in the department
    can_review_requirements = Column(Boolean, default=True)
    can_approve_department_review = Column(Boolean, default=False)
    can_reject_department_review = Column(Boolean, default=False)
    is_department_lead = Column(Boolean, default=False)  # Department leader
    
    # Metadata
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    # Relationships
    department = relationship("Department", back_populates="department_roles")
    role = relationship("UserRoleModel", back_populates="department_assignments")
    municipality = relationship("Municipality")
    
    # Unique constraint to avoid duplicates
    __table_args__ = (
        {'mysql_charset': 'utf8mb4'},
    )


class RequirementDepartmentAssignment(Base):
    """
    Assignment of specific requirements to departments.
    Defines which department must review which field/requirement.
    """
    __tablename__ = 'requirement_department_assignments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    field_id = Column(Integer, ForeignKey('fields.id'), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    procedure_type = Column(String(100), nullable=False)
    
    # Workflow control
    is_required_for_approval = Column(Boolean, default=True)
    can_be_reviewed_in_parallel = Column(Boolean, default=True)
    depends_on_department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    review_priority = Column(Integer, default=1)  # 1=high, 5=low
    
    # Specific configuration
    requires_all_users_approval = Column(Boolean, default=False)  # If approval from all department users is required
    auto_approve_if_no_issues = Column(Boolean, default=False)   # Auto-approve if no issues detected
    
    # Metadata
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    # Relationships
    field = relationship("Field", back_populates="department_assignments")
    department = relationship(
        "Department", 
        back_populates="requirement_assignments", 
        foreign_keys=[department_id]
    )
    depends_on_department = relationship(
        "Department", 
        foreign_keys=[depends_on_department_id]
    )
    municipality = relationship("Municipality")


class ProcedureDepartmentFlow(Base):
    """
    Department flow configuration by procedure type.
    Defines which departments participate in which types of procedures.
    """
    __tablename__ = 'procedure_department_flows'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    procedure_type = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    
    # Flow configuration
    step_order = Column(Integer, default=1)  # Order in the flow (1, 2, 3...)
    is_required_step = Column(Boolean, default=True)
    is_parallel_with_previous = Column(Boolean, default=False)  # If executed in parallel with previous step
    
    # Conditions to activate this step
    activation_conditions = Column(JSON, nullable=True)  # JSON conditions to activate this department
    
    # Timing configuration
    estimated_review_days = Column(Integer, default=5)
    max_review_days = Column(Integer, default=15)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    # Relationships
    department = relationship("Department", back_populates="procedure_flows")
    municipality = relationship("Municipality")


class DependencyReviewWorkflow(Base):
    """
    Workflow control for dependency reviews.
    Replaces the simple dependency_reviews logic with a state system.
    """
    __tablename__ = 'dependency_review_workflows'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    procedure_id = Column(Integer, ForeignKey('procedures.id'), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    dependency_review_id = Column(Integer, ForeignKey('dependency_reviews.id'), nullable=True)  # Link to original review
    
    # Workflow states
    status = Column(String(20), default='pending')  # pending, ready, in_review, approved, rejected, on_hold, skipped
    assigned_at = Column(DateTime, default=func.now())
    ready_at = Column(DateTime, nullable=True)      # When it was ready for review
    started_at = Column(DateTime, nullable=True)    # When review started
    completed_at = Column(DateTime, nullable=True)  # When review finished
    
    # Dependency control
    can_start_review = Column(Boolean, default=False)  # Calculated based on dependencies
    blocking_department_ids = Column(JSON, nullable=True)  # Departments blocking this one
    dependency_completion_percentage = Column(Integer, default=0)  # % of dependencies completed
    
    # Assignment and review
    assigned_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    reviewed_requirements = Column(JSON, nullable=True)  # field_ids reviewed
    pending_requirements = Column(JSON, nullable=True)   # field_ids pending
    issues_found = Column(JSON, nullable=True)           # Issues found
    
    # Comments and files
    review_comments = Column(Text, nullable=True)
    uploaded_files = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    
    # Relationships
    procedure = relationship("Procedure")
    department = relationship("Department", back_populates="workflow_steps")
    assigned_user = relationship("UserModel")
    dependency_review = relationship("DependencyReview")


class DepartmentUserAssignment(Base):
    """
    Direct assignment of users to departments with activation control.
    Allows activating/deactivating specific users for reviews in a department.
    """
    __tablename__ = 'department_user_assignments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=False)
    
    # Activation control for reviews
    is_active_for_reviews = Column(Boolean, default=True)  # Main switch to activate/deactivate
    can_receive_assignments = Column(Boolean, default=True)  # If can receive new assignments
    
    # User-specific permissions in the department
    can_review_requirements = Column(Boolean, default=True)
    can_approve_department_review = Column(Boolean, default=False)
    can_reject_department_review = Column(Boolean, default=False)
    is_backup_reviewer = Column(Boolean, default=False)  # Backup reviewer
    
    # Notification configuration
    receive_email_notifications = Column(Boolean, default=True)
    receive_urgent_notifications = Column(Boolean, default=True)
    
    # Metadata
    assigned_at = Column(DateTime, nullable=False, default=func.now())
    last_activity_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    deactivated_at = Column(DateTime, nullable=True)  # When was deactivated
    
    # Relationships
    department = relationship("Department", back_populates="user_assignments")
    user = relationship("UserModel", back_populates="department_assignments")
    municipality = relationship("Municipality")
