"""
Intelligent Dependency Workflow Service

Manages smart workflow for dependency reviews, ensuring departments
are notified only when they can actually start their review work.
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, or_, func

from app.models.departments import (
    Department, DepartmentRole, RequirementDepartmentAssignment,
    ProcedureDepartmentFlow, DependencyReviewWorkflow
)
from app.models.procedures import Procedure
from app.models.dependency_reviews import DependencyReview
from app.models.user import UserModel
from app.services.emails.sendgrid_client import send_email, render_email_template

logger = logging.getLogger(__name__)


class IntelligentWorkflowService:
    """Service for managing intelligent dependency review workflows"""

    @classmethod
    async def initiate_procedure_workflow(
        cls,
        db: AsyncSession,
        procedure: Procedure
    ) -> List[DependencyReviewWorkflow]:
        """
        Initiate intelligent workflow for a new procedure.
        Only notifies departments that can immediately start reviewing.
        """
        try:
            logger.info(f"Initiating intelligent workflow for procedure {procedure.folio}")
            
            # 1. Get flow configuration for this procedure type
            flow_config = await cls._get_procedure_flow_config(
                db, procedure.procedure_type, procedure.municipality_id
            )
            
            if not flow_config:
                logger.warning(f"No workflow configuration found for {procedure.procedure_type} in municipality {procedure.municipality_id}")
                return []

            # 2. Create workflows for all configured departments
            workflows = []
            for config in flow_config:
                workflow = DependencyReviewWorkflow(
                    procedure_id=procedure.id,
                    department_id=config.department_id,
                    status='pending',
                    assigned_at=datetime.now(timezone.utc),
                    can_start_review=False,
                    dependency_completion_percentage=0
                )
                
                # Determine requirements assigned to this department
                assigned_requirements = await cls._get_department_requirements(
                    db, config.department_id, procedure.procedure_type
                )
                workflow.pending_requirements = [req.field_id for req in assigned_requirements]
                
                db.add(workflow)
                workflows.append(workflow)

            await db.commit()
            
            # 3. Refresh all workflows to get their IDs
            for workflow in workflows:
                await db.refresh(workflow)

            # 4. Calculate dependencies and determine which can start
            await cls._update_workflow_dependencies(db, workflows)
            
            # 5. Notify only departments that can start immediately
            available_workflows = [w for w in workflows if w.can_start_review]
            await cls._notify_available_departments(db, available_workflows)
            
            logger.info(f"Created {len(workflows)} workflows, {len(available_workflows)} can start immediately")
            return workflows
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error initiating workflow for procedure {procedure.folio}: {str(e)}")
            raise

    @classmethod
    async def complete_department_review(
        cls,
        db: AsyncSession,
        workflow_id: int,
        status: str,
        user_id: int,
        comments: Optional[str] = None,
        issues_found: Optional[List[Dict]] = None
    ) -> List[DependencyReviewWorkflow]:
        """
        Complete a department review and unlock dependent departments.
        Returns list of newly available workflows.
        """
        try:
            # 1. Update the completed workflow
            workflow_stmt = select(DependencyReviewWorkflow).where(
                DependencyReviewWorkflow.id == workflow_id
            )
            result = await db.execute(workflow_stmt)
            workflow = result.scalar_one_or_none()
            
            if not workflow:
                raise ValueError(f"Workflow with ID {workflow_id} not found")

            workflow.status = status
            workflow.completed_at = datetime.now(timezone.utc)
            workflow.assigned_user_id = user_id
            workflow.review_comments = comments
            workflow.issues_found = issues_found or []
            
            if status == 'approved':
                workflow.dependency_completion_percentage = 100
            elif status == 'rejected':
                workflow.dependency_completion_percentage = 0
            
            await db.commit()
            
            # 2. Get all workflows from the same procedure
            procedure_workflows_stmt = select(DependencyReviewWorkflow).where(
                DependencyReviewWorkflow.procedure_id == workflow.procedure_id
            )
            proc_workflows_result = await db.execute(procedure_workflows_stmt)
            all_workflows = proc_workflows_result.scalars().all()
            
            # 3. Recalculate dependencies for all workflows
            await cls._update_workflow_dependencies(db, all_workflows)
            
            # 4. Identify workflows that can now start
            newly_available = []
            for w in all_workflows:
                if (w.status == 'pending' and w.can_start_review and 
                    w.ready_at is None):  # Wasn't ready before
                    w.status = 'ready'
                    w.ready_at = datetime.now(timezone.utc)
                    newly_available.append(w)
            
            await db.commit()
            
            # 5. Notify newly available departments
            if newly_available:
                await cls._notify_available_departments(db, newly_available)
                logger.info(f"Completed review {workflow_id}, unlocked {len(newly_available)} new departments")
            
            return newly_available
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error completing department review {workflow_id}: {str(e)}")
            raise

    @classmethod
    async def _get_procedure_flow_config(
        cls,
        db: AsyncSession,
        procedure_type: str,
        municipality_id: int
    ) -> List[ProcedureDepartmentFlow]:
        """Get workflow configuration for a procedure type"""
        stmt = select(ProcedureDepartmentFlow).where(
            and_(
                ProcedureDepartmentFlow.procedure_type == procedure_type,
                ProcedureDepartmentFlow.municipality_id == municipality_id,
                ProcedureDepartmentFlow.is_active == True
            )
        ).order_by(ProcedureDepartmentFlow.step_order)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def _get_department_requirements(
        cls,
        db: AsyncSession,
        department_id: int,
        procedure_type: str
    ) -> List[RequirementDepartmentAssignment]:
        """Get requirements assigned to a department for a procedure type"""
        stmt = select(RequirementDepartmentAssignment).where(
            and_(
                RequirementDepartmentAssignment.department_id == department_id,
                RequirementDepartmentAssignment.procedure_type == procedure_type
            )
        ).order_by(RequirementDepartmentAssignment.review_priority)
        
        result = await db.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def _update_workflow_dependencies(
        cls,
        db: AsyncSession,
        workflows: List[DependencyReviewWorkflow]
    ) -> None:
        """Update dependency calculations for all workflows"""
        try:
            # Create mapping of department_id -> workflow for easy access
            dept_to_workflow = {w.department_id: w for w in workflows}
            
            for workflow in workflows:
                if workflow.status in ['approved', 'rejected', 'skipped']:
                    continue  # Already completed, doesn't need recalculation
                
                # Get dependency configuration for this department
                dept_assignments = await cls._get_department_requirements(
                    db, workflow.department_id, "business_license"  # TODO: use real procedure_type
                )
                
                blocking_departments = []
                total_dependencies = 0
                completed_dependencies = 0
                
                for assignment in dept_assignments:
                    if assignment.depends_on_department_id:
                        total_dependencies += 1
                        dependent_workflow = dept_to_workflow.get(assignment.depends_on_department_id)
                        
                        if dependent_workflow:
                            if dependent_workflow.status == 'approved':
                                completed_dependencies += 1
                            elif dependent_workflow.status in ['pending', 'ready', 'in_review']:
                                blocking_departments.append(assignment.depends_on_department_id)
                
                # Calculate if review can start
                if total_dependencies == 0:
                    # No dependencies, can start immediately
                    workflow.can_start_review = True
                    workflow.dependency_completion_percentage = 100
                else:
                    # Calculate percentage of completed dependencies
                    completion_pct = int((completed_dependencies / total_dependencies) * 100)
                    workflow.dependency_completion_percentage = completion_pct
                    
                    # Can start if all dependencies are complete
                    workflow.can_start_review = (completed_dependencies == total_dependencies)
                
                workflow.blocking_department_ids = blocking_departments if blocking_departments else None
                
                logger.debug(f"Workflow {workflow.id} - Dept {workflow.department_id}: "
                           f"can_start={workflow.can_start_review}, "
                           f"completion={workflow.dependency_completion_percentage}%, "
                           f"blocking={blocking_departments}")
            
            await db.commit()
            
        except Exception as e:
            logger.error(f"Error updating workflow dependencies: {str(e)}")
            raise

    @classmethod
    async def _notify_available_departments(
        cls,
        db: AsyncSession,
        workflows: List[DependencyReviewWorkflow]
    ) -> None:
        """Send notifications only to departments that can start reviewing"""
        try:
            for workflow in workflows:
                # Get department users who can review
                users_stmt = select(
                    UserModel.id,
                    UserModel.name, 
                    UserModel.email,
                    Department.name.label('department_name')
                ).select_from(
                    UserModel
                ).join(
                    DepartmentRole, UserModel.role_id == DepartmentRole.role_id
                ).join(
                    Department, DepartmentRole.department_id == Department.id
                ).where(
                    and_(
                        DepartmentRole.department_id == workflow.department_id,
                        DepartmentRole.can_review_requirements == True,
                        UserModel.is_active == True
                    )
                ).limit(5)  # Limit to avoid spam
                
                users_result = await db.execute(users_stmt)
                users_data = users_result.fetchall()
                
                # Get procedure information
                proc_stmt = select(Procedure).where(Procedure.id == workflow.procedure_id)
                proc_result = await db.execute(proc_stmt)
                procedure = proc_result.scalar_one_or_none()
                
                if not procedure:
                    logger.warning(f"Procedure {workflow.procedure_id} not found for notification")
                    continue
                
                # Count requirements assigned to the department
                req_count = len(workflow.pending_requirements) if workflow.pending_requirements else 0
                
                # Send notification to each user
                for user_data in users_data:
                    try:
                        html_content = render_email_template("intelligent_workflow_notification.html", {
                            "user_name": user_data.name,
                            "department_name": user_data.department_name,
                            "folio": procedure.folio,
                            "procedure_id": procedure.id,
                            "workflow_id": workflow.id,
                            "requirements_count": req_count,
                            "can_start_immediately": True,
                            "assigned_at": workflow.assigned_at.strftime("%d/%m/%Y %H:%M:%S"),
                            "current_year": datetime.now().year,
                            "portal_url": "https://visorurbano.com"
                        })
                        
                        send_email(
                            user_data.email,
                            f"Revisión Lista - Departamento {user_data.department_name} - Folio {procedure.folio}",
                            html_content
                        )
                        
                        logger.info(f"Sent intelligent notification to {user_data.email} for department {user_data.department_name}")
                        
                    except Exception as e:
                        logger.error(f"Failed to send notification to {user_data.email}: {str(e)}")
                
        except Exception as e:
            logger.error(f"Error sending department notifications: {str(e)}")
            # Don't throw exception - notification failures shouldn't break the workflow

    @classmethod
    async def get_department_pending_work(
        cls,
        db: AsyncSession,
        department_id: int,
        user_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get pending work for a department, optionally filtered by user"""
        try:
            # Workflows that can start or are in progress
            filters = [
                DependencyReviewWorkflow.department_id == department_id,
                DependencyReviewWorkflow.status.in_(['ready', 'in_review'])
            ]
            
            if user_id:
                filters.append(
                    or_(
                        DependencyReviewWorkflow.assigned_user_id == user_id,
                        DependencyReviewWorkflow.assigned_user_id.is_(None)  # Unassigned
                    )
                )
            
            workflows_stmt = select(
                DependencyReviewWorkflow,
                Procedure.folio,
                Procedure.procedure_type,
                Department.name.label('department_name')
            ).select_from(
                DependencyReviewWorkflow
            ).join(
                Procedure, DependencyReviewWorkflow.procedure_id == Procedure.id
            ).join(
                Department, DependencyReviewWorkflow.department_id == Department.id
            ).where(
                and_(*filters)
            ).order_by(DependencyReviewWorkflow.assigned_at)
            
            result = await db.execute(workflows_stmt)
            workflow_data = result.fetchall()
            
            pending_work = []
            for row in workflow_data:
                workflow = row.DependencyReviewWorkflow
                req_count = len(workflow.pending_requirements) if workflow.pending_requirements else 0
                
                work_item = {
                    "workflow_id": workflow.id,
                    "procedure_id": workflow.procedure_id,
                    "folio": row.folio,
                    "procedure_type": row.procedure_type,
                    "department_name": row.department_name,
                    "status": workflow.status,
                    "assigned_at": workflow.assigned_at,
                    "ready_at": workflow.ready_at,
                    "requirements_count": req_count,
                    "can_start_review": workflow.can_start_review,
                    "dependency_completion": workflow.dependency_completion_percentage,
                    "blocking_departments": workflow.blocking_department_ids,
                    "assigned_user_id": workflow.assigned_user_id
                }
                pending_work.append(work_item)
            
            return pending_work
            
        except Exception as e:
            logger.error(f"Error getting department pending work: {str(e)}")
            raise

    @classmethod
    async def assign_workflow_to_user(
        cls,
        db: AsyncSession,
        workflow_id: int,
        user_id: int
    ) -> DependencyReviewWorkflow:
        """Assign a specific workflow to a user and start the review"""
        try:
            workflow_stmt = select(DependencyReviewWorkflow).where(
                DependencyReviewWorkflow.id == workflow_id
            )
            result = await db.execute(workflow_stmt)
            workflow = result.scalar_one_or_none()
            
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            if workflow.status not in ['ready', 'pending']:
                raise ValueError(f"Workflow {workflow_id} is not available for assignment (status: {workflow.status})")
            
            workflow.assigned_user_id = user_id
            workflow.status = 'in_review'
            workflow.started_at = datetime.now(timezone.utc)
            
            await db.commit()
            await db.refresh(workflow)
            
            logger.info(f"Assigned workflow {workflow_id} to user {user_id}")
            return workflow
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error assigning workflow to user: {str(e)}")
            raise
