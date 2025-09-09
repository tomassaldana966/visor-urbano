"""
Department Management Service

Handles department creation, role assignment, requirement mapping,
and intelligent workflow management for dependency reviews.
"""

import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, or_, func, literal, exists

from app.models.departments import (
    Department, DepartmentRole, RequirementDepartmentAssignment,
    ProcedureDepartmentFlow, DependencyReviewWorkflow, DepartmentUserAssignment
)
from app.models.user_roles import UserRoleModel
from app.models.user import UserModel
from app.models.field import Field
from app.models.procedures import Procedure
from app.models.dependency_reviews import DependencyReview
from app.schemas.departments import (
    DepartmentCreate, DepartmentUpdate, DepartmentFullInfoSchema,
    DepartmentUsersResponse, DepartmentRequirementsResponse,
    DepartmentUserInfo
)

logger = logging.getLogger(__name__)


class DepartmentService:
    """Service for managing departments and their workflows"""
    
    # Allowed roles in departments
    ALLOWED_DEPARTMENT_ROLES = {
        "reviewer": "Reviewer role for checking submissions",
        "counter": "Counter staff role for basic operations", 
        "technician": "Technical role for system maintenance"
    }

    @classmethod
    async def create_department(
        cls,
        db: AsyncSession,
        department_data: DepartmentCreate
    ) -> Department:
        """Create a new department"""
        try:
            # Ensure the code is unique within the municipality
            existing = await db.execute(
                select(Department).where(
                    and_(
                        Department.code == department_data.code,
                        Department.municipality_id == department_data.municipality_id,
                        Department.deleted_at.is_(None)
                    )
                )
            )
            if existing.scalar_one_or_none():
                raise ValueError(f"Department code '{department_data.code}' already exists in this municipality")

            department = Department(**department_data.dict())
            db.add(department)
            await db.commit()
            await db.refresh(department)
            
            logger.info(f"Created department {department.name} (ID: {department.id}) in municipality {department.municipality_id}")
            return department
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating department: {str(e)}")
            raise

    @classmethod
    async def get_department_full_info(
        cls,
        db: AsyncSession,
        department_id: int
    ) -> Optional[DepartmentFullInfoSchema]:
        """Get complete department information for director dashboard"""
        try:
            stmt = select(Department).options(
                selectinload(Department.department_roles).selectinload(DepartmentRole.role),
                selectinload(Department.requirement_assignments).selectinload(RequirementDepartmentAssignment.field)
            ).where(Department.id == department_id)
            
            result = await db.execute(stmt)
            department = result.scalar_one_or_none()
            
            if not department:
                return None

            # Count department users
            user_count_stmt = select(func.count(UserModel.id.distinct())).select_from(
                UserModel
            ).join(
                DepartmentRole, UserModel.role_id == DepartmentRole.role_id
            ).where(
                and_(
                    DepartmentRole.department_id == department_id,
                    UserModel.municipality_id == department.municipality_id,
                    UserModel.deleted_at.is_(None)
                )
            )
            user_count = await db.execute(user_count_stmt)
            total_users = user_count.scalar() or 0
            
            # Count active users
            active_user_count_stmt = select(func.count(UserModel.id.distinct())).select_from(
                UserModel
            ).join(
                DepartmentRole, UserModel.role_id == DepartmentRole.role_id
            ).where(
                and_(
                    DepartmentRole.department_id == department_id,
                    UserModel.municipality_id == department.municipality_id,
                    UserModel.is_active == True,
                    UserModel.deleted_at.is_(None)
                )
            )
            active_user_count = await db.execute(active_user_count_stmt)
            active_users = active_user_count.scalar() or 0
            
            # Count pending and completed procedures
            pending_procs_stmt = select(func.count(DependencyReviewWorkflow.id)).where(
                and_(
                    DependencyReviewWorkflow.department_id == department_id,
                    DependencyReviewWorkflow.status.in_(['pending', 'ready', 'in_review'])
                )
            )
            pending_count = await db.execute(pending_procs_stmt)
            pending_procedures = pending_count.scalar() or 0
            
            completed_procs_stmt = select(func.count(DependencyReviewWorkflow.id)).where(
                and_(
                    DependencyReviewWorkflow.department_id == department_id,
                    DependencyReviewWorkflow.status.in_(['approved', 'rejected'])
                )
            )
            completed_count = await db.execute(completed_procs_stmt)
            completed_procedures = completed_count.scalar() or 0

            # Build list of roles with full info
            roles_data = []
            for dept_role in department.department_roles:
                if dept_role.role:  # Ensure the role exists
                    roles_data.append({
                        "id": dept_role.id,
                        "role_id": dept_role.role_id,
                        "role_name": dept_role.role.name,
                        "role_description": dept_role.role.description,
                        "department_id": dept_role.department_id,
                        "can_review_requirements": dept_role.can_review_requirements,
                        "can_approve_department_review": dept_role.can_approve_department_review,
                        "can_reject_department_review": dept_role.can_reject_department_review,
                        "is_department_lead": dept_role.is_department_lead,
                        "created_at": dept_role.created_at.isoformat() if dept_role.created_at else None
                    })

            # Build list of requirements with full info
            requirements_data = []
            for req_assignment in department.requirement_assignments:
                if req_assignment.field:  # Ensure the field exists
                    requirements_data.append({
                        "id": req_assignment.id,
                        "field_id": req_assignment.field_id,
                        "field_name": req_assignment.field.name,
                        "field_label": req_assignment.field.description or req_assignment.field.name,
                        "field_type": req_assignment.field.field_type,
                        "procedure_type": req_assignment.procedure_type,
                        "is_required_for_approval": req_assignment.is_required_for_approval,
                        "can_be_reviewed_in_parallel": req_assignment.can_be_reviewed_in_parallel,
                        "review_priority": req_assignment.review_priority,
                        "depends_on_department_id": req_assignment.depends_on_department_id,
                        "requires_all_users_approval": req_assignment.requires_all_users_approval,
                        "auto_approve_if_no_issues": req_assignment.auto_approve_if_no_issues,
                        "created_at": req_assignment.created_at.isoformat() if req_assignment.created_at else None
                    })

            return DepartmentFullInfoSchema(
                id=department.id,
                name=department.name,
                description=department.description,
                code=department.code,
                municipality_id=department.municipality_id,
                is_active=department.is_active,
                can_approve_procedures=department.can_approve_procedures,
                can_reject_procedures=department.can_reject_procedures,
                requires_all_requirements=department.requires_all_requirements,
                created_at=department.created_at,
                updated_at=department.updated_at,
                roles=roles_data,
                requirements=requirements_data,
                user_count=total_users,
                active_user_count=active_users,
                requirement_count=len(requirements_data),
                pending_procedures=pending_procedures,
                completed_procedures=completed_procedures
            )
            
        except Exception as e:
            logger.error(f"Error getting department full info for ID {department_id}: {str(e)}")
            raise

    @classmethod
    async def add_role_to_department(
        cls,
        db: AsyncSession,
        department_id: int,
        role_id: int,
        municipality_id: int,
        permissions: Dict[str, bool] = None
    ) -> DepartmentRole:
        """Add a role to a department with specific permissions"""
        try:
            # Ensure the role is allowed
            role_stmt = select(UserRoleModel).where(UserRoleModel.id == role_id)
            role_result = await db.execute(role_stmt)
            role = role_result.scalar_one_or_none()
            
            if not role:
                raise ValueError(f"Role with ID {role_id} not found")
                
            role_name_lower = role.name.lower()
            allowed_roles = ["reviewer", "counter", "technician", "admin", "director"]
            
            if role_name_lower not in allowed_roles:
                raise ValueError(f"Role '{role.name}' is not allowed in departments. Allowed: {allowed_roles}")
            
            # Ensure it does not already exist
            existing_stmt = select(DepartmentRole).where(
                and_(
                    DepartmentRole.department_id == department_id,
                    DepartmentRole.role_id == role_id
                )
            )
            existing = await db.execute(existing_stmt)
            if existing.scalar_one_or_none():
                raise ValueError(f"Role {role.name} is already assigned to this department")

            # Create assignment with default or specified permissions
            default_permissions = {
                "can_review_requirements": True,
                "can_approve_department_review": role_name_lower in ["admin", "director"],
                "can_reject_department_review": role_name_lower in ["admin", "director", "reviewer"],
                "is_department_lead": False
            }
            
            if permissions:
                default_permissions.update(permissions)

            dept_role = DepartmentRole(
                department_id=department_id,
                role_id=role_id,
                municipality_id=municipality_id,
                **default_permissions
            )
            
            db.add(dept_role)
            await db.commit()
            await db.refresh(dept_role)
            
            logger.info(f"Added role {role.name} to department {department_id}")
            return dept_role
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error adding role to department: {str(e)}")
            raise

    @classmethod
    async def remove_role_from_department(
        cls,
        db: AsyncSession,
        department_id: int,
        role_id: int
    ) -> bool:
        """Remove a role from a department"""
        try:
            stmt = select(DepartmentRole).where(
                and_(
                    DepartmentRole.department_id == department_id,
                    DepartmentRole.role_id == role_id
                )
            )
            result = await db.execute(stmt)
            dept_role = result.scalar_one_or_none()
            
            if not dept_role:
                raise ValueError("Role assignment not found in department")
            
            await db.delete(dept_role)
            await db.commit()
            
            logger.info(f"Removed role {role_id} from department {department_id}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error removing role from department: {str(e)}")
            raise

    @classmethod
    async def add_field_to_department(
        cls,
        db: AsyncSession,
        department_id: int,
        field_id: int,
        municipality_id: int,
        procedure_type: str,
        assignment_config: Dict[str, Any] = None
    ) -> RequirementDepartmentAssignment:
        """Add a field/requirement to a department"""
        try:
            # Ensure the field exists
            field_stmt = select(Field).where(Field.id == field_id)
            field_result = await db.execute(field_stmt)
            field = field_result.scalar_one_or_none()
            
            if not field:
                raise ValueError(f"Field with ID {field_id} not found")
            
            # Ensure the assignment does not already exist
            existing_stmt = select(RequirementDepartmentAssignment).where(
                and_(
                    RequirementDepartmentAssignment.field_id == field_id,
                    RequirementDepartmentAssignment.department_id == department_id,
                    RequirementDepartmentAssignment.procedure_type == procedure_type
                )
            )
            existing = await db.execute(existing_stmt)
            if existing.scalar_one_or_none():
                raise ValueError(f"Field '{field.name}' is already assigned to this department for {procedure_type}")

            # Default configuration
            default_config = {
                "is_required_for_approval": True,
                "can_be_reviewed_in_parallel": True,
                "review_priority": 1,
                "requires_all_users_approval": False,
                "auto_approve_if_no_issues": False
            }
            
            if assignment_config:
                default_config.update(assignment_config)

            assignment = RequirementDepartmentAssignment(
                field_id=field_id,
                department_id=department_id,
                municipality_id=municipality_id,
                procedure_type=procedure_type,
                **default_config
            )
            
            db.add(assignment)
            await db.commit()
            await db.refresh(assignment)
            
            logger.info(f"Added field '{field.name}' to department {department_id} for {procedure_type}")
            return assignment
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error adding field to department: {str(e)}")
            raise

    @classmethod
    async def remove_field_from_department(
        cls,
        db: AsyncSession,
        department_id: int,
        field_id: int,
        procedure_type: str
    ) -> bool:
        """Remove a field/requirement from a department"""
        try:
            stmt = select(RequirementDepartmentAssignment).where(
                and_(
                    RequirementDepartmentAssignment.department_id == department_id,
                    RequirementDepartmentAssignment.field_id == field_id,
                    RequirementDepartmentAssignment.procedure_type == procedure_type
                )
            )
            result = await db.execute(stmt)
            assignment = result.scalar_one_or_none()
            
            if not assignment:
                raise ValueError("Field assignment not found in department")
            
            await db.delete(assignment)
            await db.commit()
            
            logger.info(f"Removed field {field_id} from department {department_id} for {procedure_type}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error removing field from department: {str(e)}")
            raise

    @classmethod
    async def get_department_users(
        cls,
        db: AsyncSession,
        department_id: int
    ) -> DepartmentUsersResponse:
        """Get all users assigned to a department with activation status"""
        try:
            # Get department
            dept_stmt = select(Department).where(Department.id == department_id)
            dept_result = await db.execute(dept_stmt)
            department = dept_result.scalar_one_or_none()
            
            if not department:
                raise ValueError(f"Department with ID {department_id} not found")

            # Import the new model
            from app.models.departments import DepartmentUserAssignment

            # Get users with direct assignments
            direct_assignments_stmt = select(
                UserModel.id,
                UserModel.name,
                UserModel.email,
                UserModel.is_active,
                UserRoleModel.name.label('role_name'),
                DepartmentUserAssignment.is_active_for_reviews,
                DepartmentUserAssignment.can_receive_assignments,
                DepartmentUserAssignment.can_review_requirements,
                DepartmentUserAssignment.can_approve_department_review,
                DepartmentUserAssignment.can_reject_department_review,
                DepartmentUserAssignment.is_backup_reviewer,
                DepartmentUserAssignment.last_activity_at,
                DepartmentUserAssignment.assigned_at,
                literal('direct').label('assignment_type')
            ).select_from(
                UserModel
            ).join(
                DepartmentUserAssignment, UserModel.id == DepartmentUserAssignment.user_id
            ).join(
                UserRoleModel, UserModel.role_id == UserRoleModel.id, isouter=True
            ).where(
                and_(
                    DepartmentUserAssignment.department_id == department_id,
                    UserModel.municipality_id == department.municipality_id,
                    UserModel.deleted_at.is_(None)
                )
            )

            # Get users through department roles (excluding those with direct assignment)
            role_assignments_stmt = select(
                UserModel.id,
                UserModel.name,
                UserModel.email,
                UserModel.is_active,
                UserRoleModel.name.label('role_name'),
                literal(True).label('is_active_for_reviews'),  # Default for role assignments
                literal(True).label('can_receive_assignments'),
                DepartmentRole.can_review_requirements,
                DepartmentRole.can_approve_department_review,
                DepartmentRole.can_reject_department_review,
                literal(False).label('is_backup_reviewer'),
                literal(None).label('last_activity_at'),
                literal(None).label('assigned_at'),
                literal('role').label('assignment_type')
            ).select_from(
                UserModel
            ).join(
                UserRoleModel, UserModel.role_id == UserRoleModel.id
            ).join(
                DepartmentRole, UserRoleModel.id == DepartmentRole.role_id
            ).where(
                and_(
                    DepartmentRole.department_id == department_id,
                    UserModel.municipality_id == department.municipality_id,
                    UserModel.deleted_at.is_(None),
                    # Exclude users with direct assignment
                    ~exists().where(
                        and_(
                            DepartmentUserAssignment.user_id == UserModel.id,
                            DepartmentUserAssignment.department_id == department_id
                        )
                    )
                )
            )

            # Combine both queries
            combined_stmt = direct_assignments_stmt.union_all(role_assignments_stmt).order_by('name')
            users_result = await db.execute(combined_stmt)
            users_data = users_result.fetchall()
            
            users = []
            active_count = 0
            active_for_reviews_count = 0
            
            for user_row in users_data:
                user_info = DepartmentUserInfo(
                    id=user_row.id,
                    name=user_row.name,
                    email=user_row.email,
                    role_name=user_row.role_name,
                    is_active=user_row.is_active,
                    is_active_for_reviews=user_row.is_active_for_reviews,
                    can_receive_assignments=user_row.can_receive_assignments,
                    can_review_requirements=user_row.can_review_requirements,
                    can_approve_department_review=user_row.can_approve_department_review,
                    can_reject_department_review=user_row.can_reject_department_review,
                    is_backup_reviewer=user_row.is_backup_reviewer,
                    last_activity_at=user_row.last_activity_at,
                    assigned_at=user_row.assigned_at
                )
                users.append(user_info)
                
                if user_row.is_active:
                    active_count += 1
                    
                if user_row.is_active_for_reviews:
                    active_for_reviews_count += 1

            return DepartmentUsersResponse(
                department_id=department_id,
                department_name=department.name,
                users=users,
                total_users=len(users),
                active_users=active_count,
                active_for_reviews=active_for_reviews_count
            )
            
        except Exception as e:
            logger.error(f"Error getting department users for ID {department_id}: {str(e)}")
            raise

    @classmethod
    async def get_department_requirements(
        cls,
        db: AsyncSession,
        department_id: int,
        procedure_type: Optional[str] = None
    ) -> DepartmentRequirementsResponse:
        """Get all requirements assigned to a department for a specific procedure type"""
        try:
            # Get department
            dept_stmt = select(Department).where(Department.id == department_id)
            dept_result = await db.execute(dept_stmt)
            department = dept_result.scalar_one_or_none()
            
            if not department:
                raise ValueError(f"Department with ID {department_id} not found")

            # Get requirement assignments
            assignments_stmt = select(
                RequirementDepartmentAssignment,
                Field.name.label('field_name'),
                Field.description.label('field_description'),
                Field.field_type.label('field_type'),
                Field.required.label('field_required')
            ).select_from(
                RequirementDepartmentAssignment
            ).join(
                Field, RequirementDepartmentAssignment.field_id == Field.id
            ).where(
                RequirementDepartmentAssignment.department_id == department_id
            )
            
            # Filter by procedure_type if provided
            if procedure_type:
                assignments_stmt = assignments_stmt.where(
                    RequirementDepartmentAssignment.procedure_type == procedure_type
                )
                
            assignments_stmt = assignments_stmt.order_by(
                RequirementDepartmentAssignment.review_priority, 
                Field.sequence
            )

            assignments_result = await db.execute(assignments_stmt)
            assignments_data = assignments_result.fetchall()
            
            requirements = []
            
            for assignment_row in assignments_data:
                assignment = assignment_row.RequirementDepartmentAssignment
                requirement_dict = {
                    "id": assignment.id,
                    "field_id": assignment.field_id,
                    "field_name": assignment_row.field_name,
                    "field_label": assignment_row.field_description or assignment_row.field_name,
                    "field_type": assignment_row.field_type,
                    "procedure_type": assignment.procedure_type,
                    "is_required_for_approval": assignment.is_required_for_approval,
                    "can_be_reviewed_in_parallel": assignment.can_be_reviewed_in_parallel,
                    "review_priority": assignment.review_priority,
                    "depends_on_department_id": assignment.depends_on_department_id,
                    "requires_all_users_approval": assignment.requires_all_users_approval,
                    "auto_approve_if_no_issues": assignment.auto_approve_if_no_issues,
                    "created_at": assignment.created_at.isoformat() if assignment.created_at else None
                }
                requirements.append(requirement_dict)

            return DepartmentRequirementsResponse(
                department_id=department_id,
                department_name=department.name,
                procedure_type=procedure_type,
                requirements=requirements,
                total_requirements=len(requirements)
            )
            
        except Exception as e:
            logger.error(f"Error getting department requirements for ID {department_id}: {str(e)}")
            raise

    @classmethod
    async def get_departments_for_municipality(
        cls,
        db: AsyncSession,
        municipality_id: int,
        include_inactive: bool = False
    ) -> List[Department]:
        """Get all departments for a municipality"""
        try:
            filters = [Department.municipality_id == municipality_id]
            if not include_inactive:
                filters.append(Department.is_active == True)
            
            stmt = select(Department).where(and_(*filters)).order_by(Department.name)
            result = await db.execute(stmt)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting departments for municipality {municipality_id}: {str(e)}")
            raise

    @classmethod
    async def update_department(
        cls,
        db: AsyncSession,
        department_id: int,
        update_data: dict
    ) -> Department:
        """Update an existing department"""
        try:
            # Get existing department
            stmt = select(Department).where(Department.id == department_id)
            result = await db.execute(stmt)
            department = result.scalar_one_or_none()
            
            if not department:
                raise ValueError(f"Department with ID {department_id} not found")
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(department, field):
                    setattr(department, field, value)
            
            department.updated_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(department)
            
            logger.info(f"Updated department {department.name} (ID: {department.id})")
            return department
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating department {department_id}: {str(e)}")
            raise

    @classmethod
    async def assign_user_to_department(
        cls,
        db: AsyncSession,
        department_id: int,
        user_id: int,
        municipality_id: int,
        assignment_config: Dict[str, Any] = None
    ) -> DepartmentUserAssignment:
        """Assign a user directly to a department with specific configuration"""
        try:
            from app.models.departments import DepartmentUserAssignment
            
            # Ensure the department exists
            dept_stmt = select(Department).where(Department.id == department_id)
            dept_result = await db.execute(dept_stmt)
            department = dept_result.scalar_one_or_none()
            
            if not department:
                raise ValueError(f"Department with ID {department_id} not found")
            
            # Ensure the user exists
            user_stmt = select(UserModel).where(UserModel.id == user_id)
            user_result = await db.execute(user_stmt)
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
            
            # Ensure the assignment does not already exist
            existing_stmt = select(DepartmentUserAssignment).where(
                and_(
                    DepartmentUserAssignment.department_id == department_id,
                    DepartmentUserAssignment.user_id == user_id
                )
            )
            existing = await db.execute(existing_stmt)
            if existing.scalar_one_or_none():
                raise ValueError(f"User {user.name} is already directly assigned to this department")

            # Default configuration
            default_config = {
                "is_active_for_reviews": True,
                "can_receive_assignments": True,
                "can_review_requirements": True,
                "can_approve_department_review": False,
                "can_reject_department_review": False,
                "is_backup_reviewer": False,
                "receive_email_notifications": True,
                "receive_urgent_notifications": True
            }
            
            if assignment_config:
                default_config.update(assignment_config)

            assignment = DepartmentUserAssignment(
                department_id=department_id,
                user_id=user_id,
                municipality_id=municipality_id,
                **default_config
            )
            
            db.add(assignment)
            await db.commit()
            await db.refresh(assignment)
            
            logger.info(f"Assigned user {user.name} directly to department {department.name}")
            return assignment
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error assigning user to department: {str(e)}")
            raise

    @classmethod
    async def update_user_department_assignment(
        cls,
        db: AsyncSession,
        department_id: int,
        user_id: int,
        update_data: Dict[str, Any]
    ) -> bool:
        """Update a user's department assignment settings (including the activation switch)"""
        try:
            from app.models.departments import DepartmentUserAssignment
            
            # Find the assignment
            assignment_stmt = select(DepartmentUserAssignment).where(
                and_(
                    DepartmentUserAssignment.department_id == department_id,
                    DepartmentUserAssignment.user_id == user_id
                )
            )
            assignment_result = await db.execute(assignment_stmt)
            assignment = assignment_result.scalar_one_or_none()
            
            if not assignment:
                raise ValueError(f"User assignment not found for user {user_id} in department {department_id}")
            
            # Update fields
            allowed_fields = {
                'is_active_for_reviews', 'can_receive_assignments', 'can_review_requirements',
                'can_approve_department_review', 'can_reject_department_review', 
                'is_backup_reviewer', 'receive_email_notifications', 'receive_urgent_notifications'
            }
            
            updated_fields = []
            for field, value in update_data.items():
                if field in allowed_fields and hasattr(assignment, field):
                    old_value = getattr(assignment, field)
                    setattr(assignment, field, value)
                    updated_fields.append(f"{field}: {old_value} -> {value}")
            
            # Update activity timestamp if activation status changed
            if 'is_active_for_reviews' in update_data:
                assignment.last_activity_at = datetime.utcnow()
                if not update_data['is_active_for_reviews']:
                    assignment.deactivated_at = datetime.utcnow()
                else:
                    assignment.deactivated_at = None
            
            assignment.updated_at = datetime.utcnow()
            
            await db.commit()
            
            logger.info(f"Updated user assignment for user {user_id} in department {department_id}. Changes: {', '.join(updated_fields)}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating user department assignment: {str(e)}")
            raise

    @classmethod
    async def toggle_user_activation_for_reviews(
        cls,
        db: AsyncSession,
        department_id: int,
        user_id: int,
        is_active: bool
    ) -> bool:
        """Toggle user activation for reviews in a department"""
        try:
            return await cls.update_user_department_assignment(
                db, department_id, user_id, 
                {"is_active_for_reviews": is_active}
            )
        except Exception as e:
            logger.error(f"Error toggling user activation: {str(e)}")
            raise

    @classmethod
    async def remove_user_from_department(
        cls,
        db: AsyncSession,
        department_id: int,
        user_id: int
    ) -> bool:
        """Remove a user's direct assignment from a department"""
        try:
            from app.models.departments import DepartmentUserAssignment
            
            assignment_stmt = select(DepartmentUserAssignment).where(
                and_(
                    DepartmentUserAssignment.department_id == department_id,
                    DepartmentUserAssignment.user_id == user_id
                )
            )
            assignment_result = await db.execute(assignment_stmt)
            assignment = assignment_result.scalar_one_or_none()
            
            if not assignment:
                raise ValueError(f"User assignment not found for user {user_id} in department {department_id}")
            
            await db.delete(assignment)
            await db.commit()
            
            logger.info(f"Removed user {user_id} direct assignment from department {department_id}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error removing user from department: {str(e)}")
            raise

