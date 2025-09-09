from fastapi import HTTPException, status, Depends
from typing import List, Optional
from app.models.user_roles import UserRoleModel
from config.security import get_current_user
from fastapi import Depends


class RolePermissions:
    """Define role-based permissions"""
    ADMIN_ROLES = ["admin", "administrator", "administrador", "director", "director_admin"]
    
    DIRECTOR_ROLES = ["director", "director_admin", "director_municipal"]
    
    SUPERVISOR_ROLES = ["supervisor", "jefe", "coordinador", "revisor", "reviewer", "ventanilla"]


def validate_admin_role(current_user) -> bool:
    """
    Validate if current user has admin privileges.
    
    Args:
        current_user: User object from get_current_user dependency
        
    Returns:
        bool: True if user has admin role
        
    Raises:
        HTTPException: If user doesn't have admin privileges
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Check if user has role information
    user_role_name = getattr(current_user, 'role_name', None)
    if not user_role_name:
        # If no role name, check role_id mapping or other role indicators
        role_id = getattr(current_user, 'role_id', None)
        if role_id:
            # Map role_id to role names if needed
            # This might need adjustment based on your role system
            user_role_name = _get_role_name_by_id(role_id)
    
    if not user_role_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role not found or insufficient privileges"
        )
    
    # Check if user's role is in admin roles list
    if user_role_name.lower() not in [role.lower() for role in RolePermissions.ADMIN_ROLES]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required for this operation"
        )
    
    return True


def validate_director_role(current_user) -> bool:
    """
    Validate if current user has director privileges.
    
    Args:
        current_user: User object from get_current_user dependency
        
    Returns:
        bool: True if user has director role
        
    Raises:
        HTTPException: If user doesn't have director privileges
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user_role_name = getattr(current_user, 'role_name', None)
    if not user_role_name:
        role_id = getattr(current_user, 'role_id', None)
        if role_id:
            user_role_name = _get_role_name_by_id(role_id)
    
    if not user_role_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role not found or insufficient privileges"
        )
    
    # Check if user's role is in director roles list
    if user_role_name.lower() not in [role.lower() for role in RolePermissions.DIRECTOR_ROLES]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Director privileges required for this operation"
        )
    
    return True


def validate_admin_or_director_role(current_user) -> bool:
    """
    Validate if current user has admin or director privileges.
    
    Args:
        current_user: User object from get_current_user dependency
        
    Returns:
        bool: True if user has admin or director role
        
    Raises:
        HTTPException: If user doesn't have admin or director privileges
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user_role_name = getattr(current_user, 'role_name', None)
    if not user_role_name:
        role_id = getattr(current_user, 'role_id', None)
        if role_id:
            user_role_name = _get_role_name_by_id(role_id)
    
    if not user_role_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role not found or insufficient privileges"
        )
    
    # Check if user's role is in admin or director roles list
    all_privileged_roles = RolePermissions.ADMIN_ROLES + RolePermissions.DIRECTOR_ROLES
    if user_role_name.lower() not in [role.lower() for role in all_privileged_roles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or Director privileges required for this operation"
        )
    
    return True


def validate_reviewer_role(current_user) -> bool:
    """
    Validate if current user has reviewer privileges.
    
    Args:
        current_user: User object from get_current_user dependency
        
    Returns:
        bool: True if user has reviewer role
        
    Raises:
        HTTPException: If user doesn't have reviewer privileges
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user_role_name = getattr(current_user, 'role_name', None)
    if not user_role_name:
        role_id = getattr(current_user, 'role_id', None)
        if role_id:
            user_role_name = _get_role_name_by_id(role_id)
    
    if not user_role_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role not found or insufficient privileges"
        )
    
    # Define reviewer roles - these can review dependencies
    reviewer_roles = [
        "reviewer", "revisor", "dependencia_reviewer",
        "dependency_reviewer", "analista", "evaluador"
    ] + RolePermissions.ADMIN_ROLES + RolePermissions.DIRECTOR_ROLES + RolePermissions.SUPERVISOR_ROLES
    
    # Check if user's role is in reviewer roles list
    if user_role_name.lower() not in [role.lower() for role in reviewer_roles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reviewer privileges required for this operation"
        )
    
    return True


def check_municipality_access(current_user, required_municipality_id: Optional[int] = None) -> bool:
    """
    Check if user has access to specific municipality data.
    
    Args:
        current_user: User object from get_current_user dependency
        required_municipality_id: Municipality ID to check access for
        
    Returns:
        bool: True if user has access
        
    Raises:
        HTTPException: If user doesn't have access to municipality
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user_municipality_id = getattr(current_user, 'municipality_id', None)
    
    # If no required municipality specified, check if user has any municipality
    if required_municipality_id is None:
        if not user_municipality_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No municipality assigned to user"
            )
        return True
    
    # Check if user's municipality matches required municipality
    if user_municipality_id != required_municipality_id:
        # Check if user is admin (admins might have cross-municipality access)
        try:
            validate_admin_role(current_user)
            return True  # Admin can access any municipality
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: User municipality doesn't match required municipality"
            )
    
    return True


def _get_role_name_by_id(role_id: int) -> Optional[str]:
    """
    Helper function to get role name by role ID.
    This is a placeholder - you'll need to implement actual role lookup.
    
    Args:
        role_id: Role ID to look up
        
    Returns:
        str: Role name or None if not found
    """
    # Common role ID mappings - adjust based on your system
    role_mappings = {
        1: "admin",
        2: "director", 
        3: "supervisor",
        4: "user",
        5: "viewer",
        6: "dependency_reviewer",
        7: "analista",
        8: "evaluador",
        9: "citizen",
        10: "reviewer"
    }
    
    return role_mappings.get(role_id)


def require_admin_role(current_user):
    """
    Dependency function to require admin role.
    Use this as a FastAPI dependency.
    """
    validate_admin_role(current_user)
    return current_user


def require_director_role(current_user):
    """
    Dependency function to require director role.
    Use this as a FastAPI dependency.
    """
    validate_director_role(current_user)
    return current_user


def require_admin_or_director_role(current_user=Depends(get_current_user)):
    """
    Dependency function to require admin or director role.
    Validates via get_current_user, then checks role.
    """
    validate_admin_or_director_role(current_user)
    return current_user


def require_reviewer_role(current_user=Depends(get_current_user)):
    """
    Dependency function to require reviewer role.
    Validates via get_current_user, then checks role.
    """
    validate_reviewer_role(current_user)
    return current_user


def require_reviewer_role(current_user):
    """
    Dependency function to require reviewer role.
    Use this as a FastAPI dependency.
    """
    validate_reviewer_role(current_user)
    return current_user


def has_procedure_approval_permissions(current_user) -> bool:
    """
    Check if current user has permissions to access procedure approvals.
    
    Args:
        current_user: User object from get_current_user dependency
        
    Returns:
        bool: True if user has procedure approval permissions
    """
    if not current_user:
        return False
    
    user_role_id = getattr(current_user, 'role_id', 1) or 1
    
    # Basic requirement: role_id > 1
    if user_role_id <= 1:
        return False
    
    # Check if user has admin or director privileges first
    try:
        validate_admin_or_director_role(current_user)
        return True
    except HTTPException:
        pass
    
    # Define role IDs that have procedure approval permissions
    procedure_approval_role_ids = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    return user_role_id in procedure_approval_role_ids
