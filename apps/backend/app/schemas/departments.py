from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

# === Department Schemas ===

class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    code: str = Field(..., max_length=20)
    municipality_id: int
    is_active: bool = True
    can_approve_procedures: bool = True
    can_reject_procedures: bool = True
    requires_all_requirements: bool = False

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    can_approve_procedures: Optional[bool] = None
    can_reject_procedures: Optional[bool] = None
    requires_all_requirements: Optional[bool] = None

class DepartmentSchema(DepartmentBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

# === Department Role Schemas ===

class DepartmentRoleBase(BaseModel):
    department_id: int
    role_id: int
    municipality_id: int
    can_review_requirements: bool = True
    can_approve_department_review: bool = False
    can_reject_department_review: bool = False
    is_department_lead: bool = False

class DepartmentRoleCreate(DepartmentRoleBase):
    pass

class DepartmentRoleUpdate(BaseModel):
    can_review_requirements: Optional[bool] = None
    can_approve_department_review: Optional[bool] = None
    can_reject_department_review: Optional[bool] = None
    is_department_lead: Optional[bool] = None

class DepartmentRoleSchema(DepartmentRoleBase):
    id: int
    created_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

# === Requirement Department Assignment Schemas ===

class RequirementDepartmentAssignmentBase(BaseModel):
    field_id: int
    department_id: int
    municipality_id: int
    procedure_type: str = Field(..., max_length=100)
    is_required_for_approval: bool = True
    can_be_reviewed_in_parallel: bool = True
    depends_on_department_id: Optional[int] = None
    review_priority: int = Field(default=1, ge=1, le=5)
    requires_all_users_approval: bool = False
    auto_approve_if_no_issues: bool = False

class RequirementDepartmentAssignmentCreate(RequirementDepartmentAssignmentBase):
    pass

class RequirementDepartmentAssignmentUpdate(BaseModel):
    is_required_for_approval: Optional[bool] = None
    can_be_reviewed_in_parallel: Optional[bool] = None
    depends_on_department_id: Optional[int] = None
    review_priority: Optional[int] = Field(None, ge=1, le=5)
    requires_all_users_approval: Optional[bool] = None
    auto_approve_if_no_issues: Optional[bool] = None

class RequirementDepartmentAssignmentSchema(RequirementDepartmentAssignmentBase):
    id: int
    created_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

# === Procedure Department Flow Schemas ===

class ProcedureDepartmentFlowBase(BaseModel):
    procedure_type: str = Field(..., max_length=100)
    department_id: int
    municipality_id: int
    step_order: int = 1
    is_required_step: bool = True
    is_parallel_with_previous: bool = False
    activation_conditions: Optional[Dict[str, Any]] = None
    estimated_review_days: int = 5
    max_review_days: int = 15
    is_active: bool = True

class ProcedureDepartmentFlowCreate(ProcedureDepartmentFlowBase):
    pass

class ProcedureDepartmentFlowUpdate(BaseModel):
    step_order: Optional[int] = None
    is_required_step: Optional[bool] = None
    is_parallel_with_previous: Optional[bool] = None
    activation_conditions: Optional[Dict[str, Any]] = None
    estimated_review_days: Optional[int] = None
    max_review_days: Optional[int] = None
    is_active: Optional[bool] = None

class ProcedureDepartmentFlowSchema(ProcedureDepartmentFlowBase):
    id: int
    created_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

# === Dependency Review Workflow Schemas ===

class DependencyReviewWorkflowBase(BaseModel):
    procedure_id: int
    department_id: int
    dependency_review_id: Optional[int] = None
    status: str = "pending"
    assigned_user_id: Optional[int] = None
    can_start_review: bool = False
    blocking_department_ids: Optional[List[int]] = None
    dependency_completion_percentage: int = 0
    reviewed_requirements: Optional[List[int]] = None
    pending_requirements: Optional[List[int]] = None
    issues_found: Optional[List[Dict[str, Any]]] = None
    review_comments: Optional[str] = None
    uploaded_files: Optional[List[str]] = None

class DependencyReviewWorkflowCreate(DependencyReviewWorkflowBase):
    pass

class DependencyReviewWorkflowUpdate(BaseModel):
    status: Optional[str] = None
    assigned_user_id: Optional[int] = None
    can_start_review: Optional[bool] = None
    blocking_department_ids: Optional[List[int]] = None
    dependency_completion_percentage: Optional[int] = None
    reviewed_requirements: Optional[List[int]] = None
    pending_requirements: Optional[List[int]] = None
    issues_found: Optional[List[Dict[str, Any]]] = None
    review_comments: Optional[str] = None
    uploaded_files: Optional[List[str]] = None

class DependencyReviewWorkflowSchema(DependencyReviewWorkflowBase):
    id: int
    assigned_at: Optional[datetime]
    ready_at: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

# === Combined/Extended Schemas ===

class DepartmentWithRolesSchema(DepartmentSchema):
    """Department with its assigned roles and users"""
    roles: List[DepartmentRoleSchema] = []
    user_count: int = 0
    active_user_count: int = 0

class DepartmentWithRequirementsSchema(DepartmentSchema):
    """Department with its assigned requirements"""
    requirements: List[RequirementDepartmentAssignmentSchema] = []
    requirement_count: int = 0

class DepartmentFullInfoSchema(DepartmentSchema):
    """Complete department information for director dashboard"""
    roles: List[Dict[str, Any]] = []
    requirements: List[Dict[str, Any]] = []
    user_count: int = 0
    active_user_count: int = 0
    requirement_count: int = 0
    pending_procedures: int = 0
    completed_procedures: int = 0

# === Director Quick Actions Schemas ===

class DepartmentQuickActionRequest(BaseModel):
    """Request for department quick actions"""
    action: str = Field(..., description="Action to perform: add_field, remove_field, add_role, remove_role")
    department_id: int
    field_id: Optional[int] = None
    role_id: Optional[int] = None
    procedure_type: Optional[str] = None

class DepartmentQuickActionResponse(BaseModel):
    """Response for department quick actions"""
    success: bool
    message: str
    department_id: int
    action_performed: str
    affected_item_id: Optional[int] = None

# === Enhanced User Response Schema ===

class DepartmentUserInfo(BaseModel):
    """Enhanced user info with department assignment status"""
    id: int
    name: str
    email: str
    role_name: Optional[str] = None
    is_active: bool = True
    is_active_for_reviews: bool = True  # New field for department-specific activation
    can_receive_assignments: bool = True
    can_review_requirements: bool = True
    can_approve_department_review: bool = False
    can_reject_department_review: bool = False
    is_backup_reviewer: bool = False
    last_activity_at: Optional[datetime] = None
    assigned_at: Optional[datetime] = None

class DepartmentUsersResponse(BaseModel):
    """Response with department users including activation status"""
    department_id: int
    department_name: str
    users: List[DepartmentUserInfo]
    total_users: int
    active_users: int
    active_for_reviews: int  # New field for users active for reviews

class DepartmentRequirementsResponse(BaseModel):
    """Response with department requirements"""
    department_id: int
    department_name: str
    procedure_type: Optional[str]
    requirements: List[Dict[str, Any]]
    total_requirements: int

# === Department User Assignment Schemas ===

class DepartmentUserAssignmentBase(BaseModel):
    department_id: int
    user_id: int
    municipality_id: int
    is_active_for_reviews: bool = True
    can_receive_assignments: bool = True
    can_review_requirements: bool = True
    can_approve_department_review: bool = False
    can_reject_department_review: bool = False
    is_backup_reviewer: bool = False
    receive_email_notifications: bool = True
    receive_urgent_notifications: bool = True

class DepartmentUserAssignmentCreate(DepartmentUserAssignmentBase):
    pass

class DepartmentUserAssignmentUpdate(BaseModel):
    is_active_for_reviews: Optional[bool] = None
    can_receive_assignments: Optional[bool] = None
    can_review_requirements: Optional[bool] = None
    can_approve_department_review: Optional[bool] = None
    can_reject_department_review: Optional[bool] = None
    is_backup_reviewer: Optional[bool] = None
    receive_email_notifications: Optional[bool] = None
    receive_urgent_notifications: Optional[bool] = None

class DepartmentUserAssignmentSchema(DepartmentUserAssignmentBase):
    id: int
    assigned_at: datetime
    last_activity_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deactivated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)
