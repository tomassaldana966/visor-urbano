import logging
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_, text

from app.models.procedures import Procedure
from app.models.dependency_reviews import DependencyReview
from config.settings import get_db
from config.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/procedures-state")
async def debug_procedures_state(
    days_back: int = Query(7, description="Number of days back to analyze"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        # Calculate date threshold
        date_threshold = datetime.now() - timedelta(days=days_back)
        
        # Get recent procedures
        stmt = select(Procedure).where(
            Procedure.created_at >= date_threshold
        ).order_by(Procedure.created_at.desc())
        
        result = await db.execute(stmt)
        procedures = result.scalars().all()
        
        # Analyze each procedure
        analysis = []
        for procedure in procedures:
            # Get related dependency reviews
            reviews_stmt = select(DependencyReview).where(
                DependencyReview.procedure_id == procedure.id
            )
            reviews_result = await db.execute(reviews_stmt)
            reviews = reviews_result.scalars().all()
            
            # Build analysis object
            procedure_analysis = {
                "folio": procedure.folio,
                "id": procedure.id,
                "created_at": procedure.created_at.isoformat() if procedure.created_at else None,
                "procedure_type": procedure.procedure_type,
                
                # Core status fields that affect display
                "status": procedure.status,
                "director_approval": procedure.director_approval,
                "sent_to_reviewers": procedure.sent_to_reviewers,
                "step_one": procedure.step_one,
                "step_two": procedure.step_two,
                "step_three": procedure.step_three,
                "step_four": procedure.step_four,
                "window_license_generated": procedure.window_license_generated,
                
                # Dependencies information
                "dependency_reviews_count": len(reviews),
                "dependency_reviews": [
                    {
                        "id": review.id,
                        "role": review.role,
                        "department_id": review.department_id,
                        "current_status": review.current_status,
                        "director_approved": review.director_approved,
                        "start_date": review.start_date.isoformat() if review.start_date else None
                    }
                    for review in reviews
                ],
                
                # Frontend display logic prediction
                "predicted_frontend_status": predict_frontend_status(procedure),
                
                # Timestamps
                "procedure_start_date": procedure.procedure_start_date.isoformat() if procedure.procedure_start_date else None,
                "sent_to_reviewers_date": procedure.sent_to_reviewers_date.isoformat() if procedure.sent_to_reviewers_date else None,
            }
            
            analysis.append(procedure_analysis)
        
        # Summary statistics
        total_procedures = len(procedures)
        procedures_with_director_approval_1 = len([p for p in procedures if p.director_approval == 1])
        procedures_with_sent_to_reviewers_1 = len([p for p in procedures if p.sent_to_reviewers == 1])
        procedures_with_status_above_0 = len([p for p in procedures if p.status and p.status > 0])
        
        summary = {
            "total_procedures_analyzed": total_procedures,
            "procedures_with_director_approval_1": procedures_with_director_approval_1,
            "procedures_with_sent_to_reviewers_1": procedures_with_sent_to_reviewers_1,
            "procedures_with_status_above_0": procedures_with_status_above_0,
            "date_range": f"From {date_threshold.isoformat()} to now",
            "percentage_showing_as_approved": round(
                (procedures_with_director_approval_1 / total_procedures * 100) if total_procedures > 0 else 0, 2
            )
        }
        
        return {
            "summary": summary,
            "procedures": analysis,
            "debug_info": {
                "query_executed_at": datetime.now().isoformat(),
                "user_role": getattr(current_user, 'role_id', None),
                "municipality_id": getattr(current_user, 'municipality_id', None)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in debug endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Debug error: {str(e)}")


def predict_frontend_status(procedure: Procedure) -> str:
    """
    Predict what status the frontend will show based on the getStatusDisplay logic
    """
    # Match the logic from procedure-approvals.tsx
    if procedure.status == 1:
        return "approved"
    elif procedure.status == 2:
        return "rejected"
    elif procedure.status == 3:
        return "prevention"
    elif procedure.status == 4:
        return "approvedByDirector"
    elif procedure.status in [7, 8, 9]:
        return "licenseIssued"
    else:
        # Default case logic (the problematic part)
        if procedure.director_approval == 1 and (
            procedure.sent_to_reviewers == 1 or 
            procedure.step_one == 1 or 
            procedure.step_two == 1
        ):
            return "approved (DEFAULT CASE)"
        elif procedure.sent_to_reviewers == 1:
            return "inReview (DEFAULT CASE)"
        else:
            return "new (DEFAULT CASE)"


@router.post("/fix-director-approval")
async def fix_director_approval_values(
    folio: Optional[str] = Query(None, description="Specific folio to fix, or leave empty for all recent"),
    dry_run: bool = Query(True, description="If true, only show what would be changed"),
    fix_status: bool = Query(True, description="If true, also fix status field for new procedures"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Fix incorrect director_approval values for procedures that should show as "New"
    """
    try:
        # Only allow admin users to run this
        if not hasattr(current_user, 'role_id') or current_user.role_id <= 2:
            raise HTTPException(
                status_code=403,
                detail="Administrative privileges required"
            )
        
        # Build query based on what to fix
        if folio:
            stmt = select(Procedure).where(Procedure.folio == folio)
        else:
            # Fix recent procedures (last 30 days) that have problematic values
            date_threshold = datetime.now() - timedelta(days=30)
            
            if fix_status:
                # Find procedures with status=1 but should be "new" (no workflow progress)
                stmt = select(Procedure).where(
                    and_(
                        Procedure.created_at >= date_threshold,
                        Procedure.status == 1,  # Status 1 shows as "approved" but should be "new"
                        # Should be "new" procedures - no meaningful workflow progress
                        or_(
                            Procedure.director_approval == 0,
                            Procedure.director_approval.is_(None)
                        ),
                        or_(
                            Procedure.sent_to_reviewers == 0,
                            Procedure.sent_to_reviewers.is_(None)
                        ),
                        or_(
                            Procedure.step_one == 0,
                            Procedure.step_one.is_(None)
                        ),
                        or_(
                            Procedure.step_two == 0,
                            Procedure.step_two.is_(None)
                        )
                    )
                )
            else:
                # Original logic for director_approval only
                stmt = select(Procedure).where(
                    and_(
                        Procedure.created_at >= date_threshold,
                        Procedure.director_approval == 1,
                        # Should be "new" procedures - no meaningful workflow progress
                        or_(
                            Procedure.sent_to_reviewers == 0,
                            Procedure.sent_to_reviewers.is_(None)
                        ),
                        or_(
                            Procedure.step_one == 0,
                            Procedure.step_one.is_(None)
                        ),
                        or_(
                            Procedure.step_two == 0,
                            Procedure.step_two.is_(None)
                        )
                    )
                )
        
        result = await db.execute(stmt)
        procedures_to_fix = result.scalars().all()
        
        if not procedures_to_fix:
            return {
                "message": "No procedures found that need fixing",
                "count": 0,
                "dry_run": dry_run
            }
        
        # Prepare fix operations
        fix_operations = []
        for procedure in procedures_to_fix:
            fix_operations.append({
                "folio": procedure.folio,
                "id": procedure.id,
                "current_status": procedure.status,
                "current_director_approval": procedure.director_approval,
                "current_sent_to_reviewers": procedure.sent_to_reviewers,
                "current_step_one": procedure.step_one,
                "current_step_two": procedure.step_two,
                "predicted_status_before": predict_frontend_status(procedure),
                "will_change_to": "new (after fix)"
            })
            
            if not dry_run:
                # Fix the values
                if fix_status and procedure.status == 1:
                    procedure.status = 0
                    logger.info(f"Fixed status for procedure {procedure.folio}: 1 -> 0")
                    
                if procedure.director_approval == 1:
                    procedure.director_approval = 0
                    logger.info(f"Fixed director_approval for procedure {procedure.folio}: 1 -> 0")
        
        if not dry_run:
            await db.commit()
            logger.info(f"Fixed {len(procedures_to_fix)} procedures")
        
        return {
            "message": f"{'Would fix' if dry_run else 'Fixed'} {len(procedures_to_fix)} procedures",
            "count": len(procedures_to_fix),
            "dry_run": dry_run,
            "operations": fix_operations
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error fixing director_approval values: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fix error: {str(e)}")


@router.get("/{folio}")
async def debug_procedure_workflow(
    folio: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Endpoint to get detailed workflow status for a specific procedure folio.
    The folio parameter should be base64 encoded to handle special characters like slashes.
    """
    try:
        # Decode the folio from base64
        import base64
        try:
            decoded_folio = base64.b64decode(folio).decode('utf-8')
        except Exception:
            # If decoding fails, use the folio as is
            decoded_folio = folio
        
        # Get procedure by decoded folio
        stmt = select(Procedure).where(Procedure.folio == decoded_folio)
        result = await db.execute(stmt)
        procedure = result.scalar_one_or_none()
        
        if not procedure:
            raise HTTPException(status_code=404, detail=f"Procedure with folio {decoded_folio} (encoded: {folio}) not found")
        
        # Get related dependency reviews
        reviews_stmt = select(DependencyReview).where(
            DependencyReview.procedure_id == procedure.id
        )
        reviews_result = await db.execute(reviews_stmt)
        reviews = reviews_result.scalars().all()
        
        # Determine current workflow step based on status and flags
        current_step = determine_current_workflow_step(procedure)
        
        # Build comprehensive status information
        workflow_status = {
            "folio": procedure.folio,
            "procedure_id": procedure.id,
            "procedure_type": procedure.procedure_type,
            "created_at": procedure.created_at.isoformat() if procedure.created_at else None,
            
            # Core status fields
            "status": procedure.status,
            "director_approval": procedure.director_approval,
            "sent_to_reviewers": procedure.sent_to_reviewers,
            "step_one": procedure.step_one,
            "step_two": procedure.step_two,
            "step_three": procedure.step_three,
            "step_four": procedure.step_four,
            "window_license_generated": procedure.window_license_generated,
            
            # Calculated workflow information
            "current_workflow_step": current_step,
            "workflow_progress_percentage": calculate_workflow_progress(procedure),
            "can_proceed_to_next_step": can_procedure_proceed(procedure),
            "blocking_factors": get_blocking_factors(procedure),
            
            # Frontend display prediction
            "predicted_frontend_status": predict_frontend_status(procedure),
            
            # Dependencies
            "dependency_reviews_count": len(reviews),
            "dependency_reviews": [
                {
                    "id": review.id,
                    "role": review.role,
                    "department_id": review.department_id,
                    "current_status": review.current_status,
                    "director_approved": review.director_approved,
                    "start_date": review.start_date.isoformat() if review.start_date else None
                }
                for review in reviews
            ],
            
            # Debug information
            "debug_info": {
                "query_executed_at": datetime.now().isoformat(),
                "user_role": getattr(current_user, 'role_id', None),
                "municipality_id": getattr(current_user, 'municipality_id', None)
            }
        }
        
        return workflow_status
        
    except Exception as e:
        logger.error(f"Error getting workflow status for folio {folio}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Workflow status error: {str(e)}")


def determine_current_workflow_step(procedure: Procedure) -> str:
    """
    Determine the current step in the workflow based on procedure state
    """
    if procedure.status == 2:
        return "rejected"
    elif procedure.status == 3:
        return "prevention"
    elif procedure.status >= 7:
        return "completed"
    elif procedure.window_license_generated == 1:
        return "finalizacion"
    elif procedure.director_approval == 1:
        return "aprobacion_completed"
    elif procedure.sent_to_reviewers == 1 or procedure.step_one == 1:
        return "revision"
    elif procedure.procedure_start_date or procedure.status > 0:
        return "inicio"
    else:
        return "new"


def calculate_workflow_progress(procedure: Procedure) -> float:
    """
    Calculate workflow progress percentage
    """
    total_steps = 4  # inicio, revision, aprobacion, finalizacion
    completed_steps = 0
    
    # Step 1: Inicio
    if procedure.procedure_start_date or procedure.status > 0:
        completed_steps += 1
    
    # Step 2: Revision
    if procedure.sent_to_reviewers == 1 or procedure.step_one == 1:
        completed_steps += 1
    
    # Step 3: Aprobacion
    if procedure.director_approval == 1:
        completed_steps += 1
    
    # Step 4: Finalizacion
    if procedure.window_license_generated == 1 or procedure.status >= 7:
        completed_steps += 1
    
    return (completed_steps / total_steps) * 100


def can_procedure_proceed(procedure: Procedure) -> bool:
    """
    Determine if procedure can proceed to next step
    """
    if procedure.status == 2:  # Rejected
        return False
    elif procedure.status == 3:  # Prevention
        return False  # Needs user action
    elif procedure.status >= 7:  # Completed
        return False  # Already done
    else:
        return True


def get_blocking_factors(procedure: Procedure) -> list:
    """
    Get list of factors blocking procedure progress
    """
    blocking_factors = []
    
    if procedure.status == 2:
        blocking_factors.append("Procedure has been rejected")
    elif procedure.status == 3:
        blocking_factors.append("Procedure in prevention - additional information required")
    elif procedure.status >= 7:
        blocking_factors.append("Procedure already completed")
    
    # Check specific workflow blockers
    if procedure.sent_to_reviewers != 1 and procedure.step_one != 1 and procedure.status == 0:
        blocking_factors.append("Procedure not yet sent to reviewers")
    
    if procedure.step_one != 1 and procedure.director_approval == 1:
        blocking_factors.append("Director approval without technical review")
    
    return blocking_factors
