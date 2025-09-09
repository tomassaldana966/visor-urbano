"""
Director Department Management Router

Provides quick actions for directors to manage departments,
view requirements, assign users, and monitor workflows.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from config.settings import get_db
from app.models.departments import Department
from app.models.user import UserModel
from app.schemas.departments import (
    DepartmentCreate, DepartmentUpdate, DepartmentFullInfoSchema,
    DepartmentQuickActionRequest, DepartmentQuickActionResponse,
    DepartmentUsersResponse, DepartmentRequirementsResponse
)
from app.services.department_service import DepartmentService
from app.services.intelligent_workflow_service import IntelligentWorkflowService
from app.utils.role_validation import require_director_role
from config.security import get_current_user

router = APIRouter(prefix="/director/departments", tags=["Director - Department Management"])


@router.get("", response_model=List[DepartmentFullInfoSchema])
async def get_municipality_departments(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    include_inactive: bool = Query(False, description="Include inactive departments")
):
    """Get all departments for director's municipality with full information"""
    try:
        # Verify that the user is a director
        require_director_role(current_user)
        
        departments = await DepartmentService.get_departments_for_municipality(
            db, current_user.municipality_id, include_inactive
        )
        
        # Get full information for each department
        full_info_departments = []
        for dept in departments:
            full_info = await DepartmentService.get_department_full_info(db, dept.id)
            if full_info:
                full_info_departments.append(full_info)
        
        return full_info_departments
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving departments: {str(e)}"
        )


@router.post("", response_model=DepartmentFullInfoSchema)
async def create_department(
    department_data: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Create a new department"""
    try:
        require_director_role(current_user)
        
        # Ensure the department is created in the director's municipality
        department_data.municipality_id = current_user.municipality_id
        
        department = await DepartmentService.create_department(db, department_data)
        full_info = await DepartmentService.get_department_full_info(db, department.id)
        
        return full_info
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating department: {str(e)}"
        )


@router.get("/{department_id}", response_model=DepartmentFullInfoSchema)
async def get_department_details(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get detailed information about a specific department"""
    try:
        require_director_role(current_user)
        
        full_info = await DepartmentService.get_department_full_info(db, department_id)
        
        if not full_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        # Verify that the department belongs to the director's municipality
        if full_info.municipality_id != current_user.municipality_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Department belongs to a different municipality"
            )
        
        return full_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving department details: {str(e)}"
        )


@router.get("/{department_id}/users", response_model=DepartmentUsersResponse)
async def get_department_users(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all users assigned to a department"""
    try:
        require_director_role(current_user)
        
        users_response = await DepartmentService.get_department_users(db, department_id)
        
        return users_response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving department users: {str(e)}"
        )


@router.get("/{department_id}/requirements", response_model=DepartmentRequirementsResponse)
async def get_department_requirements(
    department_id: int,
    procedure_type: Optional[str] = Query(None, description="Procedure type to filter requirements"),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get all requirements assigned to a department for a specific procedure type"""
    try:
        require_director_role(current_user)
        
        requirements_response = await DepartmentService.get_department_requirements(
            db, department_id, procedure_type
        )
        
        return requirements_response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving department requirements: {str(e)}"
        )


@router.post("/quick-action", response_model=DepartmentQuickActionResponse)
async def department_quick_action(
    action_request: DepartmentQuickActionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Perform quick actions on departments:
    - add_field: Add a field/requirement to department
    - remove_field: Remove a field/requirement from department  
    - add_role: Add a role to department
    - remove_role: Remove a role from department
    """
    try:
        require_director_role(current_user)
        
        response = DepartmentQuickActionResponse(
            success=False,
            message="",
            department_id=action_request.department_id,
            action_performed=action_request.action
        )
        
        if action_request.action == "add_field":
            if not action_request.field_id or not action_request.procedure_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="field_id and procedure_type are required for add_field action"
                )
            
            assignment = await DepartmentService.add_field_to_department(
                db=db,
                department_id=action_request.department_id,
                field_id=action_request.field_id,
                municipality_id=current_user.municipality_id,
                procedure_type=action_request.procedure_type
            )
            
            response.success = True
            response.message = f"Field added to department successfully"
            response.affected_item_id = assignment.id
            
        elif action_request.action == "remove_field":
            if not action_request.field_id or not action_request.procedure_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="field_id and procedure_type are required for remove_field action"
                )
            
            success = await DepartmentService.remove_field_from_department(
                db=db,
                department_id=action_request.department_id,
                field_id=action_request.field_id,
                procedure_type=action_request.procedure_type
            )
            
            response.success = success
            response.message = f"Field removed from department successfully"
            response.affected_item_id = action_request.field_id
            
        elif action_request.action == "add_role":
            if not action_request.role_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="role_id is required for add_role action"
                )
            
            dept_role = await DepartmentService.add_role_to_department(
                db=db,
                department_id=action_request.department_id,
                role_id=action_request.role_id,
                municipality_id=current_user.municipality_id
            )
            
            response.success = True
            response.message = f"Role added to department successfully"
            response.affected_item_id = dept_role.id
            
        elif action_request.action == "remove_role":
            if not action_request.role_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="role_id is required for remove_role action"
                )
            
            success = await DepartmentService.remove_role_from_department(
                db=db,
                department_id=action_request.department_id,
                role_id=action_request.role_id
            )
            
            response.success = success
            response.message = f"Role removed from department successfully"
            response.affected_item_id = action_request.role_id
            
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown action: {action_request.action}. Allowed: add_field, remove_field, add_role, remove_role"
            )
        
        return response
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing quick action: {str(e)}"
        )


@router.get("/{department_id}/pending-work")
async def get_department_pending_work(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get pending work items for a department"""
    try:
        require_director_role(current_user)
        
        pending_work = await IntelligentWorkflowService.get_department_pending_work(
            db, department_id
        )
        
        return {
            "department_id": department_id,
            "pending_items": pending_work,
            "total_pending": len(pending_work),
            "can_start_immediately": len([item for item in pending_work if item["can_start_review"]])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving pending work: {str(e)}"
        )


@router.put("/{department_id}", response_model=DepartmentFullInfoSchema)
async def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Update department information"""
    try:
        require_director_role(current_user)
        
        # Verify that the department exists and belongs to the director's municipality
        full_info = await DepartmentService.get_department_full_info(db, department_id)
        
        if not full_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        if full_info.municipality_id != current_user.municipality_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Department belongs to a different municipality"
            )
        
        # Update department using service
        update_dict = department_data.model_dump(exclude_unset=True)
        updated_department = await DepartmentService.update_department(
            db, department_id, update_dict
        )
        
        # Return updated full info
        updated_full_info = await DepartmentService.get_department_full_info(db, department_id)
        return updated_full_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating department: {str(e)}"
        )


@router.put("/{department_id}/users/{user_id}/toggle-activation", response_model=dict)
async def toggle_user_activation_for_reviews(
    department_id: int,
    user_id: int,
    is_active: bool = Query(..., description="New activation status for reviews"),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Toggle user activation for reviews in a department"""
    try:
        require_director_role(current_user)
        
        # Verify that the department belongs to the director's municipality
        department = await db.get(Department, department_id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        
        if department.municipality_id != current_user.municipality_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Department belongs to a different municipality"
            )
        
        # If no direct assignment exists, create a new one
        success = False
        try:
            success = await DepartmentService.toggle_user_activation_for_reviews(
                db, department_id, user_id, is_active
            )
        except ValueError as ve:
            # If no direct assignment exists, create a new one
            if "User assignment not found" in str(ve):
                await DepartmentService.assign_user_to_department(
                    db, department_id, user_id, current_user.municipality_id,
                    {"is_active_for_reviews": is_active}
                )
                success = True
            else:
                raise ve
        
        return {
            "success": success,
            "message": f"User {'activated' if is_active else 'deactivated'} for reviews in department",
            "department_id": department_id,
            "user_id": user_id,
            "is_active_for_reviews": is_active
        }
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling user activation: {str(e)}"
        )
