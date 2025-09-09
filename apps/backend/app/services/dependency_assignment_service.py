"""
Dependency Assignment Service

This service handles the automatic assignment of dependency reviewers 
when a new procedure is created, using the department-based system
and requirement mappings configured in the database.
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, or_

from app.models.procedures import Procedure
from app.models.dependency_reviews import DependencyReview
from app.models.user import UserModel
from app.models.departments import Department, RequirementDepartmentAssignment, DepartmentUserAssignment, DepartmentRole
from app.services.department_service import DepartmentService
from app.services.emails.sendgrid_client import send_email, render_email_template

logger = logging.getLogger(__name__)


class DependencyAssignmentService:
    """Service for automatically assigning dependency reviewers to procedures using the department system"""

    @classmethod
    async def assign_dependencies_to_procedure(
        cls,
        db: AsyncSession,
        procedure: Procedure,
        force_reassign: bool = False
    ) -> List[DependencyReview]:
        """
        Automatically assign dependency reviewers to a new procedure based on
        department requirements configured in the database.
        
        Args:
            db: Database session
            procedure: The procedure that needs dependency assignment
            force_reassign: Whether to reassign even if dependencies already exist
            
        Returns:
            List of created DependencyReview records
        """
        try:
            # Check if dependencies are already assigned (unless forcing reassign)
            if not force_reassign:
                existing_reviews = await db.execute(
                    select(DependencyReview).where(
                        DependencyReview.procedure_id == procedure.id
                    )
                )
                if existing_reviews.scalars().first():
                    logger.info(f"Dependencies already assigned to procedure {procedure.folio}")
                    return []

            # Get departments that need to review this procedure type
            required_departments = await cls._get_required_departments_for_procedure(
                db, procedure
            )
            
            if not required_departments:
                logger.warning(f"No departments found for procedure {procedure.folio} of type {procedure.procedure_type}")
                return []

            # Create dependency review records for each required department
            created_reviews = []
            newly_created_reviews = []
            
            for department in required_departments:
                # Check if this department dependency already exists
                existing_review = await db.execute(
                    select(DependencyReview).where(
                        DependencyReview.procedure_id == procedure.id,
                        DependencyReview.department_id == department.id
                    )
                )
                
                existing_review_record = existing_review.scalars().first()
                if existing_review_record and not force_reassign:
                    logger.info(f"Department {department.name} already assigned to procedure {procedure.folio} (Review ID: {existing_review_record.id}) - skipping notification")
                    created_reviews.append(existing_review_record)
                    continue
                elif existing_review_record and force_reassign:
                    logger.info(f"Force reassigning department {department.name} to procedure {procedure.folio} - will send notification")
                    created_reviews.append(existing_review_record)
                    newly_created_reviews.append(existing_review_record)
                    continue
                
                # Get primary role for backward compatibility with DependencyReview.role field
                role_id = await cls._get_primary_role_for_department(db, department.id)
                
                review = DependencyReview(
                    procedure_id=procedure.id,
                    municipality_id=procedure.municipality_id,
                    folio=procedure.folio,
                    role=role_id,  # For backward compatibility
                    department_id=department.id,  # New department-based system
                    start_date=datetime.now(),  # Remove timezone for PostgreSQL compatibility
                    current_status=0,  # Pending
                    director_approved=0,
                    sent_to_reviewers=datetime.now()  # Remove timezone for PostgreSQL compatibility
                )
                
                db.add(review)
                created_reviews.append(review)
                newly_created_reviews.append(review)
                
                logger.info(f"Created NEW dependency review for procedure {procedure.folio}, department {department.name}")

            # Commit all assignments
            await db.commit()
            
            # Refresh newly created reviews to get their IDs
            for review in newly_created_reviews:
                if review.id is None:  # Only refresh if it's a new record
                    await db.refresh(review)

            # Send notifications only for newly created or force-reassigned reviews
            if newly_created_reviews:
                await cls._send_reviewer_notifications(db, newly_created_reviews)
                logger.info(f"Sent notifications for {len(newly_created_reviews)} new/reassigned dependency assignments")
            else:
                logger.info(f"No new assignments to notify for procedure {procedure.folio}")
            
            logger.info(f"Successfully processed {len(created_reviews)} dependencies for procedure {procedure.folio} ({len(newly_created_reviews)} new notifications sent)")
            return created_reviews
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error assigning dependencies to procedure {procedure.folio}: {str(e)}")
            raise

    @classmethod
    async def _get_required_departments_for_procedure(
        cls, 
        db: AsyncSession, 
        procedure: Procedure
    ) -> List[Department]:
        """
        Get departments that need to review this procedure based on
        requirement-department assignments configured in the database.
        Now correctly looks for departments that handle the specific fields required for this folio.
        
        Args:
            db: Database session
            procedure: The procedure to analyze
            
        Returns:
            List of Department instances that need to review this procedure
        """
        try:
            procedure_type = procedure.procedure_type or ""
            
            # First, try to get departments based on specific required fields for this folio
            # We need to look at the RequirementsQuery associated with this procedure
            departments = []
            
            # Check if this procedure has an associated requirements_query that can tell us
            # what specific fields are required
            if hasattr(procedure, 'folio') and procedure.folio:
                logger.info(f"Looking for departments based on required fields for folio {procedure.folio}")
                
                # Get the RequirementsQuery for this folio to know what fields are required
                from app.models.requirements_query import RequirementsQuery
                req_query_stmt = select(RequirementsQuery).where(
                    RequirementsQuery.folio == procedure.folio
                ).limit(1)
                req_query_result = await db.execute(req_query_stmt)
                req_query = req_query_result.scalar_one_or_none()
                
                if req_query:
                    # Get dynamic fields/answers that were provided for this specific folio
                    from app.models.answer import Answer
                    answers_stmt = select(Answer).where(
                        Answer.requirements_query_id == req_query.id
                    )
                    answers_result = await db.execute(answers_stmt)
                    answers = answers_result.scalars().all()
                    
                    # Extract field names that have answers (meaning they were required/filled)
                    required_field_names = [answer.name for answer in answers if answer.name]
                    
                    if required_field_names:
                        logger.info(f"Found {len(required_field_names)} answered fields for folio {procedure.folio}: {required_field_names}")
                        
                        # Find field IDs from field names
                        from app.models.field import Field
                        fields_stmt = select(Field.id, Field.name).where(
                            Field.name.in_(required_field_names)
                        )
                        fields_result = await db.execute(fields_stmt)
                        field_mappings = fields_result.fetchall()
                        required_field_ids = [field.id for field in field_mappings]
                        
                        logger.info(f"Mapped field names to IDs: {[(f.name, f.id) for f in field_mappings]}")
                        
                        if required_field_ids:
                            # Find departments that handle these specific fields
                            # KEY CHANGE: Remove procedure_type filter to focus on requirements/fields only
                            departments_stmt = select(Department).distinct().join(
                                RequirementDepartmentAssignment,
                                Department.id == RequirementDepartmentAssignment.department_id
                            ).where(
                                and_(
                                    Department.municipality_id == procedure.municipality_id,
                                    Department.is_active == True,
                                    Department.can_approve_procedures == True,
                                    RequirementDepartmentAssignment.field_id.in_(required_field_ids),
                                    RequirementDepartmentAssignment.is_required_for_approval == True
                                )
                            )
                            
                            departments_result = await db.execute(departments_stmt)
                            departments = departments_result.scalars().all()
                            
                            if departments:
                                logger.info(f"✅ Found {len(departments)} departments handling specific requirements {required_field_names} for folio {procedure.folio}")
                                for dept in departments:
                                    logger.info(f"   - Department: {dept.name} (ID: {dept.id})")
                                return departments
                            else:
                                logger.warning(f"No departments found for required fields {required_field_names} (IDs: {required_field_ids}) for folio {procedure.folio}")
                                
                                # Debug: Check what assignments exist for these fields
                                debug_stmt = select(RequirementDepartmentAssignment, Department.name).join(
                                    Department, RequirementDepartmentAssignment.department_id == Department.id
                                ).where(
                                    RequirementDepartmentAssignment.field_id.in_(required_field_ids)
                                )
                                debug_result = await db.execute(debug_stmt)
                                debug_assignments = debug_result.fetchall()
                                
                                logger.info(f"Debug: Found {len(debug_assignments)} total assignments for these fields:")
                                for assignment, dept_name in debug_assignments:
                                    logger.info(f"   - Field {assignment.field_id} → {dept_name} (Municipality: {assignment.municipality_id}, Procedure: {assignment.procedure_type})")
                        else:
                            logger.warning(f"No field IDs found for field names {required_field_names}")
                    else:
                        logger.warning(f"No required field names found in answers for folio {procedure.folio}")
                else:
                    logger.warning(f"No RequirementsQuery found for folio {procedure.folio}")
            
            # Fallback 1: Query departments that have requirements assigned for this procedure type
            logger.info(f"Falling back to procedure type based assignment for type '{procedure_type}'")
            departments_stmt = select(Department).distinct().join(
                RequirementDepartmentAssignment,
                Department.id == RequirementDepartmentAssignment.department_id
            ).where(
                and_(
                    Department.municipality_id == procedure.municipality_id,
                    Department.is_active == True,
                    Department.can_approve_procedures == True,
                    RequirementDepartmentAssignment.procedure_type == procedure_type,
                    RequirementDepartmentAssignment.is_required_for_approval == True
                )
            )
            
            departments_result = await db.execute(departments_stmt)
            departments = departments_result.scalars().all()
            
            if departments:
                logger.info(f"Found {len(departments)} departments for procedure type '{procedure_type}'")
                return departments
            
            # Fallback 2: Get default departments if no specific requirements are configured
            logger.warning(f"No departments found for procedure type '{procedure_type}', using default departments")
            default_departments_stmt = select(Department).where(
                and_(
                    Department.municipality_id == procedure.municipality_id,
                    Department.is_active == True,
                    Department.can_approve_procedures == True
                )
            ).limit(2)  # Get at least 2 departments for basic review
            
            default_result = await db.execute(default_departments_stmt)
            default_departments = default_result.scalars().all()
            
            logger.warning(f"Using {len(default_departments)} default departments for procedure {procedure.folio}")
            return default_departments
            
        except Exception as e:
            logger.error(f"Error getting required departments for procedure: {str(e)}")
            return []

    @classmethod
    async def _get_primary_role_for_department(
        cls,
        db: AsyncSession,
        department_id: int
    ) -> int:
        """
        Get the primary role ID for a department (for backward compatibility with DependencyReview.role)
        
        Args:
            db: Database session
            department_id: Department to get role for
            
        Returns:
            Primary role ID for the department
        """
        try:
            # Get the first role assigned to this department
            role_stmt = select(DepartmentRole.role_id).where(
                DepartmentRole.department_id == department_id
            ).limit(1)
            
            role_result = await db.execute(role_stmt)
            role_id = role_result.scalar_one_or_none()
            
            # Default to role 1 if no role is found
            return role_id or 1
            
        except Exception as e:
            logger.error(f"Error getting primary role for department {department_id}: {str(e)}")
            return 1  # Default role

    @classmethod
    async def _get_role_display_name(
        cls,
        db: AsyncSession,
        role_id: int
    ) -> str:
        """
        Get display name for a role by looking up associated departments.
        
        Args:
            db: Database session
            role_id: Role ID to get name for
            
        Returns:
            Display name for the role
        """
        try:
            # Get departments that have this role
            dept_stmt = select(Department.name).join(
                DepartmentRole, Department.id == DepartmentRole.department_id
            ).where(DepartmentRole.role_id == role_id).limit(1)
            
            result = await db.execute(dept_stmt)
            dept_name = result.scalar_one_or_none()
            
            return dept_name or f"Role {role_id}"
            
        except Exception as e:
            logger.error(f"Error getting role display name for role {role_id}: {str(e)}")
            return f"Role {role_id}"

    @classmethod
    async def _get_department_name(
        cls,
        db: AsyncSession,
        department_id: int
    ) -> str:
        """
        Get display name for a department.
        
        Args:
            db: Database session
            department_id: Department ID to get name for
            
        Returns:
            Display name for the department
        """
        try:
            dept_stmt = select(Department.name).where(Department.id == department_id)
            result = await db.execute(dept_stmt)
            dept_name = result.scalar_one_or_none()
            
            return dept_name or f"Department {department_id}"
            
        except Exception as e:
            logger.error(f"Error getting department name for department {department_id}: {str(e)}")
            return f"Department {department_id}"

    @classmethod
    async def _get_active_users_for_role_fallback(
        cls,
        db: AsyncSession,
        role_id: int,
        municipality_id: int
    ) -> List[UserModel]:
        """
        Fallback method to get active users by role when department assignments are not available.
        
        Args:
            db: Database session
            role_id: The role ID to find users for
            municipality_id: Municipality to search in
            
        Returns:
            List of active UserModel instances
        """
        try:
            fallback_stmt = select(UserModel).where(
                UserModel.role_id == role_id,
                UserModel.municipality_id == municipality_id,
                UserModel.is_active == True,
                UserModel.deleted_at.is_(None)
            ).limit(5)
            
            result = await db.execute(fallback_stmt)
            active_users = result.scalars().all()
            
            logger.info(f"Found {len(active_users)} active users for role {role_id} (fallback) in municipality {municipality_id}")
            return active_users
            
        except Exception as e:
            logger.error(f"Error getting fallback users for role {role_id}: {str(e)}")
            return []

    @classmethod
    async def _get_active_users_for_department(
        cls,
        db: AsyncSession,
        department_id: int,
        municipality_id: int
    ) -> List[UserModel]:
        """
        Get active users for a specific department using the new department system.
        Only returns users who are active for reviews in the specified department.
        
        Args:
            db: Database session
            department_id: The department ID to find users for
            municipality_id: Municipality to search in
            
        Returns:
            List of active UserModel instances
        """
        try:
            # Query to find users who:
            # 1. Are assigned to the specified department
            # 2. Are in the specified municipality
            # 3. Are active users
            # 4. Have is_active_for_reviews=True for this department
            users_stmt = select(UserModel).distinct().join(
                DepartmentUserAssignment, UserModel.id == DepartmentUserAssignment.user_id
            ).where(
                and_(
                    DepartmentUserAssignment.department_id == department_id,
                    DepartmentUserAssignment.municipality_id == municipality_id,
                    DepartmentUserAssignment.is_active_for_reviews == True,
                    UserModel.municipality_id == municipality_id,
                    UserModel.is_active == True,
                    UserModel.deleted_at.is_(None)
                )
            ).limit(10)  # Reasonable limit to avoid spam
            
            result = await db.execute(users_stmt)
            active_users = result.scalars().all()
            
            logger.info(f"Found {len(active_users)} active users for department {department_id} in municipality {municipality_id}")
            return active_users
            
        except Exception as e:
            logger.error(f"Error getting active users for department {department_id}: {str(e)}")
            return []

    @classmethod
    async def _send_reviewer_notifications(
        cls,
        db: AsyncSession,
        reviews: List[DependencyReview]
    ) -> None:
        """
        Send email notifications to assigned reviewers using the department system.
        Only notify users who are active for reviews in the relevant department.
        Includes duplicate prevention tracking.
        
        Args:
            db: Database session
            reviews: List of dependency reviews to notify about
        """
        notification_errors = []
        
        try:
            from app.models.notifications import Notification
            
            for review in reviews:
                try:
                    if review.department_id:
                        # Use new department-based system
                        assigned_users = await cls._get_active_users_for_department(
                            db, review.department_id, review.municipality_id
                        )
                        
                        # Get department name for display
                        department_name = await cls._get_department_name(db, review.department_id)
                    else:
                        # Fallback to role-based system for backward compatibility
                        logger.warning(f"No department_id found for review {review.id}, using role fallback")
                        assigned_users = await cls._get_active_users_for_role_fallback(
                            db, review.role, review.municipality_id
                        )
                        department_name = f"Role {review.role}"
                    
                    # Send notifications only to users who are active for reviews
                    for user in assigned_users:
                        if user.email:
                            # Check if this user has already been notified for this review
                            # Use multiple checks to be absolutely sure no duplicate notifications
                            existing_notifications = await db.execute(
                                select(Notification).where(
                                    and_(
                                        Notification.user_id == user.id,
                                        Notification.review_id == review.id,
                                        Notification.folio == review.folio,
                                        or_(
                                            Notification.email_sent == True,
                                            and_(
                                                Notification.notification_type == 1,  # Assignment notification
                                                Notification.creation_date >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # Today
                                            )
                                        )
                                    )
                                )
                            )
                            
                            existing_notification = existing_notifications.scalars().first()
                            if existing_notification:
                                logger.info(f"User {user.email} already notified for review {review.id} (folio {review.folio}) - skipping (Notification ID: {existing_notification.id})")
                                continue
                            
                            try:
                                # Send email notification
                                html_content = render_email_template("dependency_revision_notification.html", {
                                    "folio": review.folio,
                                    "revision_id": review.id,
                                    "role_name": department_name,
                                    "procedure_id": review.procedure_id,
                                    "reviewer_name": user.name or user.email,
                                    "assigned_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                    "current_year": datetime.now().year,
                                    "portal_url": "https://visorurbano.com"  # TODO: Get from environment
                                })
                                
                                send_email(
                                    user.email,
                                    f"Nueva revisión asignada - Folio {review.folio}",
                                    html_content
                                )
                                
                                # Create notification record to track that this user was notified
                                notification = Notification(
                                    user_id=user.id,
                                    review_id=review.id,
                                    folio=review.folio,
                                    applicant_email=user.email,
                                    comment=f"Asignación automática de revisión - Departamento: {department_name}",
                                    creation_date=datetime.now(),
                                    notification_type=1,  # Assignment notification type
                                    email_sent=True,
                                    email_sent_at=datetime.now(),
                                    notifying_department=review.department_id
                                )
                                
                                db.add(notification)
                                # Commit each notification immediately to avoid rollback issues
                                await db.commit()
                                
                                logger.info(f"✅ Sent assignment notification to {user.email} for folio {review.folio} (Review: {review.id})")
                                
                            except Exception as email_error:
                                error_msg = f"Failed to send notification to {user.email}: {str(email_error)}"
                                logger.error(f"❌ {error_msg}")
                                notification_errors.append(error_msg)
                                
                                # Rollback any pending changes from this notification attempt
                                await db.rollback()
                                
                                # Create notification record even if email failed, but mark as not sent
                                try:
                                    notification = Notification(
                                        user_id=user.id,
                                        review_id=review.id,
                                        folio=review.folio,
                                        applicant_email=user.email,
                                        comment=f"Error enviando notificación: {str(email_error)[:250]}",
                                        creation_date=datetime.now(),
                                        notification_type=1,
                                        email_sent=False,
                                        notifying_department=review.department_id
                                    )
                                    
                                    db.add(notification)
                                    await db.commit()
                                    
                                except Exception as record_error:
                                    logger.error(f"❌ Failed to create error notification record: {record_error}")
                                    await db.rollback()
                    
                    if not assigned_users:
                        logger.warning(f"No active users found for department {review.department_id or 'N/A'} (role {review.role}) in municipality {review.municipality_id} for folio {review.folio}")
                        
                except Exception as review_error:
                    error_msg = f"Error processing review {review.id}: {str(review_error)}"
                    logger.error(f"❌ {error_msg}")
                    notification_errors.append(error_msg)
                    await db.rollback()
                
        except Exception as e:
            logger.error(f"❌ Critical error sending reviewer notifications: {str(e)}")
            notification_errors.append(f"Critical error: {str(e)}")
            # Don't raise - notifications failing shouldn't break the assignment process
        
        # Log summary of errors if any occurred
        if notification_errors:
            logger.warning(f"⚠️ {len(notification_errors)} notification errors occurred:")
            for error in notification_errors[:5]:  # Log max 5 errors to avoid spam
                logger.warning(f"   - {error}")
            if len(notification_errors) > 5:
                logger.warning(f"   ... and {len(notification_errors) - 5} more errors")

    @classmethod
    async def assign_director_review(
        cls,
        db: AsyncSession,
        procedure: Procedure,
        director_user_id: Optional[int] = None
    ) -> Optional[DependencyReview]:
        """
        Assign a director review for procedures that require director approval.
        Now uses department-based configuration instead of hardcoded rules.
        
        Args:
            db: Database session
            procedure: The procedure that needs director review
            director_user_id: Specific director to assign (optional)
            
        Returns:
            Created DependencyReview record for director, or None if not needed
        """
        try:
            # Check if director review already exists for this procedure
            existing_director_review = await db.execute(
                select(DependencyReview).where(
                    and_(
                        DependencyReview.procedure_id == procedure.id,
                        DependencyReview.role == 4  # Director role
                    )
                )
            )
            
            existing_review = existing_director_review.scalars().first()
            if existing_review:
                logger.info(f"Director review already exists for procedure {procedure.folio} (Review ID: {existing_review.id})")
                return existing_review

            # Also check if there's already a review with this folio (to avoid unique constraint error)
            existing_folio_review = await db.execute(
                select(DependencyReview).where(
                    and_(
                        DependencyReview.folio == procedure.folio,
                        DependencyReview.role == 4  # Director role
                    )
                )
            )
            
            existing_folio = existing_folio_review.scalars().first()
            if existing_folio:
                logger.info(f"Director review already exists for folio {procedure.folio} (Review ID: {existing_folio.id})")
                return existing_folio

            # Check if this procedure type requires director approval from database configuration
            requires_director = await cls._requires_director_approval_from_db(db, procedure)
            
            if not requires_director:
                logger.info(f"Procedure {procedure.folio} of type {procedure.procedure_type} does not require director approval")
                return None

            # Find director department or fallback to role-based assignment
            director_department = await cls._get_director_department(db, procedure.municipality_id)
            
            if director_department:
                # Use department-based assignment
                directors = await cls._get_active_users_for_department(
                    db, director_department.id, procedure.municipality_id
                )
                department_id = director_department.id
            else:
                # Fallback to role-based assignment
                logger.warning(f"No director department found, falling back to role-based assignment")
                directors = await cls._get_active_users_for_role_fallback(
                    db, 4, procedure.municipality_id  # Director role = 4
                )
                department_id = None
                
            if directors and not director_user_id:
                director_user_id = directors[0].id  # Take the first active director
            elif not directors and not director_user_id:
                logger.warning(f"No active director found for municipality {procedure.municipality_id}")
                return None

            # Create director review
            director_review = DependencyReview(
                procedure_id=procedure.id,
                municipality_id=procedure.municipality_id,
                folio=procedure.folio,
                role=4,  # Director role for backward compatibility
                department_id=department_id,
                start_date=datetime.now(),  # Remove timezone for PostgreSQL compatibility
                current_status=0,  # Pending
                user_id=director_user_id,
                director_approved=0
            )
            
            db.add(director_review)
            await db.commit()
            await db.refresh(director_review)
            
            logger.info(f"Created director review for procedure {procedure.folio}")
            return director_review
            
        except Exception as e:
            await db.rollback()
            # Use a safe error message that doesn't access potentially corrupted attributes
            error_msg = f"Error assigning director review: {str(e)}"
            logger.error(error_msg)
            return None  # Don't raise, just return None to allow procedure creation to continue

    @classmethod
    async def _requires_director_approval_from_db(
        cls,
        db: AsyncSession,
        procedure: Procedure
    ) -> bool:
        """
        Determine if a procedure requires director approval based on database configuration.
        
        Args:
            db: Database session
            procedure: The procedure to check
            
        Returns:
            True if director approval is required
        """
        try:
            # Check if there are any departments with high priority that require approval for this procedure type
            # High priority departments (priority 1) typically require director oversight
            high_priority_requirement_stmt = select(RequirementDepartmentAssignment).join(
                Department, RequirementDepartmentAssignment.department_id == Department.id
            ).where(
                and_(
                    RequirementDepartmentAssignment.procedure_type == procedure.procedure_type,
                    RequirementDepartmentAssignment.is_required_for_approval == True,
                    RequirementDepartmentAssignment.review_priority == 1,  # High priority
                    Department.municipality_id == procedure.municipality_id,
                    Department.is_active == True,
                    Department.can_approve_procedures == True
                )
            )
            
            result = await db.execute(high_priority_requirement_stmt)
            high_priority_requirements = result.scalars().all()
            
            # If there are 3 or more high-priority departments involved, require director approval
            if len(high_priority_requirements) >= 3:
                logger.info(f"Director approval required for procedure type {procedure.procedure_type} due to {len(high_priority_requirements)} high-priority departments")
                return True
            
            # Check if any department requires all users approval (complex procedures)
            complex_requirement_stmt = select(RequirementDepartmentAssignment).join(
                Department, RequirementDepartmentAssignment.department_id == Department.id
            ).where(
                and_(
                    RequirementDepartmentAssignment.procedure_type == procedure.procedure_type,
                    RequirementDepartmentAssignment.requires_all_users_approval == True,
                    Department.municipality_id == procedure.municipality_id,
                    Department.is_active == True
                )
            )
            
            complex_result = await db.execute(complex_requirement_stmt)
            complex_requirement = complex_result.scalars().first()
            
            if complex_requirement:
                logger.info(f"Director approval required for procedure type {procedure.procedure_type} due to complex approval requirements")
                return True
            
            # Fallback to legacy logic if no database configuration suggests director approval
            logger.info(f"No database configuration found requiring director approval, using legacy logic for procedure type {procedure.procedure_type}")
            return cls._requires_director_approval_legacy(procedure)
            
        except Exception as e:
            logger.error(f"Error checking director approval requirement: {str(e)}")
            # Fallback to legacy logic on error
            return cls._requires_director_approval_legacy(procedure)

    @classmethod
    def _requires_director_approval_legacy(cls, procedure: Procedure) -> bool:
        """
        Legacy method to determine if a procedure requires director approval.
        Used as fallback when database configuration is not available.
        
        Args:
            procedure: The procedure to check
            
        Returns:
            True if director approval is required
        """
        procedure_type = procedure.procedure_type or ""
        procedure_type_lower = procedure_type.lower()
        
        # Procedures that traditionally require director approval
        high_impact_types = [
            "construction", "construccion",
            "expansion", "ampliacion", 
            "building", "edificacion"
        ]
        
        return any(keyword in procedure_type_lower for keyword in high_impact_types)

    @classmethod
    async def _get_director_department(
        cls,
        db: AsyncSession,
        municipality_id: int
    ) -> Optional[Department]:
        """
        Get the director department for a municipality.
        
        Args:
            db: Database session
            municipality_id: Municipality to search in
            
        Returns:
            Director Department instance or None
        """
        try:
            # Look for a department that has director roles assigned
            director_dept_stmt = select(Department).distinct().join(
                DepartmentRole, Department.id == DepartmentRole.department_id
            ).where(
                and_(
                    Department.municipality_id == municipality_id,
                    Department.is_active == True,
                    DepartmentRole.role_id == 4  # Director role
                )
            ).limit(1)
            
            result = await db.execute(director_dept_stmt)
            director_department = result.scalars().first()
            
            if director_department:
                logger.info(f"Found director department: {director_department.name}")
            else:
                logger.warning(f"No director department found for municipality {municipality_id}")
            
            return director_department
            
        except Exception as e:
            logger.error(f"Error getting director department: {str(e)}")
            return None

    @classmethod
    async def get_procedure_review_status(
        cls,
        db: AsyncSession,
        procedure_id: int
    ) -> Dict:
        """
        Get the current review status for a procedure
        
        Args:
            db: Database session
            procedure_id: ID of the procedure
            
        Returns:
            Dictionary with review status information
        """
        try:
            reviews_stmt = select(DependencyReview).options(
                selectinload(DependencyReview.resolutions)
            ).where(DependencyReview.procedure_id == procedure_id)
            
            reviews_result = await db.execute(reviews_stmt)
            reviews = reviews_result.scalars().all()
            
            status = {
                "total_dependencies": len(reviews),
                "pending_reviews": len([r for r in reviews if r.current_status == 0]),
                "approved_reviews": len([r for r in reviews if r.current_status == 1]),
                "rejected_reviews": len([r for r in reviews if r.current_status == 2]),
                "prevention_reviews": len([r for r in reviews if r.current_status == 3]),
                "director_approved": any(r.director_approved == 1 for r in reviews if r.role == 4),
                "overall_status": "pending"
            }
            
            # Determine overall status
            if status["rejected_reviews"] > 0:
                status["overall_status"] = "rejected"
            elif status["prevention_reviews"] > 0:
                status["overall_status"] = "prevention_required"
            elif status["pending_reviews"] == 0 and status["total_dependencies"] > 0:
                if status["director_approved"]:
                    status["overall_status"] = "approved"
                else:
                    status["overall_status"] = "pending_director"
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting review status for procedure {procedure_id}: {str(e)}")
            return {"error": str(e)}
