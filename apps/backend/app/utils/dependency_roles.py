"""
Utilities for role validation in dependency reviews context
Handles permission logic according to legacy system
"""

from typing import Union
from app.models.user import UserModel as User

class DependencyRoles:
    """Constants for dependency roles"""
    CITIZEN = 1
    WINDOW = 2
    TECHNICAL_REVIEWER = 3
    DIRECTOR = 4
    SPECIALIZED_DEPT_MIN = 6

def check_review_permissions(user: User) -> bool:
    """
    Checks if a user has permissions to review procedures
    """
    if not user or not hasattr(user, 'role'):
        return False
    
    # Roles that can review: technical (3), director (4), specialized departments (6+)
    return user.role >= DependencyRoles.TECHNICAL_REVIEWER

def check_director_permissions(user: User) -> bool:
    """
    Checks if a user has director permissions
    """
    if not user or not hasattr(user, 'role'):
        return False
    
    return user.role == DependencyRoles.DIRECTOR

def check_specialized_department_permissions(user: User) -> bool:
    """
    Checks if a user belongs to a specialized department
    """
    if not user or not hasattr(user, 'role'):
        return False
    
    return user.role >= DependencyRoles.SPECIALIZED_DEPT_MIN

def get_resolution_permissions(user: User) -> dict:
    """
    Gets specific permissions for resolutions based on role
    
    Returns:
        dict: Dictionary with available permissions
    """
    if not user or not hasattr(user, 'role'):
        return {
            'can_approve': False,
            'can_reject': False,
            'can_prevent': False,
            'can_discard': False,
            'rejection_label': 'reject'
        }
    
    role = user.role
    
    # Basic permissions
    permissions = {
        'can_approve': role >= DependencyRoles.TECHNICAL_REVIEWER,
        'can_prevent': role >= DependencyRoles.TECHNICAL_REVIEWER,
        'can_reject': False,
        'can_discard': False,
        'rejection_label': 'reject'
    }
    
    # Role-specific permissions
    if role == DependencyRoles.TECHNICAL_REVIEWER or role == DependencyRoles.DIRECTOR:
        # Roles 3 and 4 can "discard"
        permissions['can_discard'] = True
        permissions['rejection_label'] = 'discard'
    elif role >= DependencyRoles.SPECIALIZED_DEPT_MIN:
        # Roles 6+ can "reject"
        permissions['can_reject'] = True
        permissions['rejection_label'] = 'reject'
    
    return permissions

def can_insert_director_review(user: User, reviews_completed: bool) -> bool:
    """
    Determines if a director review should be inserted
    """
    if not user or not hasattr(user, 'role'):
        return False
    
    # Only if not director and all reviews are completed
    return user.role != DependencyRoles.DIRECTOR and reviews_completed

def get_status_flow_next_step(current_status: int, user_role: int, total_reviews: int, completed_reviews: int) -> dict:
    """
    Determines the next step in the flow based on current status and role
    
    Args:
        current_status: Current resolution status (1=approved, 2=rejected, 3=prevent)
        user_role: Current user role
        total_reviews: Total reviews for the procedure
        completed_reviews: Number of completed reviews
        
    Returns:
        dict: Information about the next step
    """
    next_step = {
        'insert_director': False,
        'send_notification': False,
        'notification_type': None,
        'process_complete': False
    }
    
    # If it's director
    if user_role == DependencyRoles.DIRECTOR:
        if current_status == 1:  # Approved by director
            next_step['send_notification'] = True
            next_step['notification_type'] = 'payment_order'
            next_step['process_complete'] = True
        return next_step
    
    # If not director
    if total_reviews == 1:
        # Only one department - send directly to director
        next_step['insert_director'] = True
    elif completed_reviews == total_reviews:
        # All departments have responded - send to director
        next_step['insert_director'] = True
    
    # Notifications for specialized departments
    if user_role >= DependencyRoles.SPECIALIZED_DEPT_MIN and current_status == 1:
        next_step['send_notification'] = True
        next_step['notification_type'] = 'approval'
    
    return next_step

def validate_resolution_status(status: int) -> bool:
    """
    Validates that the resolution status is valid
    """
    valid_statuses = [0, 1, 2, 3, 4]  # 0=pending, 1=approved, 2=rejected, 3=prevent, 4=license issued
    return status in valid_statuses

def can_emit_license(user: User, review_status: int) -> bool:
    """
    Determines if a user can issue the license
    """
    if not check_director_permissions(user):
        return False
    
    # Can only issue if approved (status 1)
    return review_status == 1
