from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, desc, func
from typing import Optional
import logging
import json
from datetime import datetime, date

from app.models.business_line_log import BusinessLineLog
from app.schemas.business_line_log import (
    BusinessLineLogResponse, 
    BusinessLineLogCreate,
    BusinessLineLogListResponse
)
from config.settings import get_db
from config.security import get_current_user
from app.utils.role_validation import require_admin_or_director_role

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def get_client_info(request: Request) -> dict:
    try:
        return {
            "host": request.headers.get("host", ""),
            "user_ip": request.client.host if request.client else "",
            "user_agent": request.headers.get("user-agent", "")
        }
    except Exception as e:
        logger.error(f"Error extracting client info: {str(e)}", exc_info=True)
        raise

@router.get("/consult/{log_type}", response_model=BusinessLineLogListResponse)
async def get_logs_by_type(
    log_type: int, 
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    action_filter: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin_or_director_role)
):
    try:
        query = select(BusinessLineLog).options(
            selectinload(BusinessLineLog.user)
        )
        if log_type != 0:
            query = query.where(BusinessLineLog.log_type == log_type)
        filters = []
        if start_date:
            filters.append(BusinessLineLog.created_at >= start_date)
        if end_date is not None:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            filters.append(BusinessLineLog.created_at <= end_datetime)
        if action_filter:
            filters.append(BusinessLineLog.action.ilike(f"%{action_filter}%"))
        if filters:
            query = query.where(and_(*filters))
        count_query = select(func.count(BusinessLineLog.id))
        if log_type != 0:
            count_query = count_query.where(BusinessLineLog.log_type == log_type)
        if filters:
            count_query = count_query.where(and_(*filters))
        count_result = await db.execute(count_query)
        total_count = count_result.scalar()
        query = query.order_by(desc(BusinessLineLog.created_at)).offset(skip).limit(limit)
        result = await db.execute(query)
        logs = result.scalars().all()
        logger.info(f"Retrieved {len(logs)} logs (total: {total_count}) for type {log_type} by user {current_user.id}")
        return BusinessLineLogListResponse(
            logs=logs,
            total_count=total_count,
            skip=skip,
            limit=limit
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving logs: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving logs"
        )

@router.get("/{log_id}", response_model=BusinessLineLogResponse)
async def get_log_by_id(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin_or_director_role)
):
    try:
        if log_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid log ID"
            )
        query = select(BusinessLineLog).options(
            selectinload(BusinessLineLog.user)
        ).where(BusinessLineLog.id == log_id)
        result = await db.execute(query)
        log = result.scalar_one_or_none()
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Log not found"
            )
        logger.info(f"Retrieved log {log_id} by user {current_user.id}")
        return log
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving log {log_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving log"
        )

@router.post("/", response_model=BusinessLineLogResponse)
async def create_log(
    log_data: BusinessLineLogCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        if not log_data.action or not log_data.action.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Action field is required and cannot be empty"
            )
        if log_data.log_type is None or log_data.log_type < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valid log_type is required"
            )
        client_info = get_client_info(request)
        new_log = BusinessLineLog(
            action=log_data.action.strip(),
            previous=log_data.previous.strip() if log_data.previous else None,
            user_id=current_user.id,
            log_type=log_data.log_type,
            procedure_id=log_data.procedure_id,
            host=client_info["host"],
            user_ip=client_info["user_ip"],
            role_id=getattr(current_user, 'role_id', None),
            user_agent=client_info["user_agent"],
            post_request=log_data.post_request.strip() if log_data.post_request else None
        )
        db.add(new_log)
        await db.commit()
        await db.refresh(new_log)
        logger.info(f"Created log entry {new_log.id} by user {current_user.id} - Action: {log_data.action}")
        return new_log
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating log: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating log entry"
        )

@router.post("/log_action")
async def log_action(
    action: str,
    log_type: int,
    previous: Optional[str] = None,
    procedure_id: Optional[int] = None,
    post_request: Optional[str] = None,
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        if not action or not action.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Action is required and cannot be empty"
            )
        if log_type is None or log_type < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Valid log_type is required"
            )
        
        client_info = get_client_info(request)
        
        # Handle post_request if not provided
        if not post_request and request:
            try:
                post_request = json.dumps(dict(request.query_params)) if request.query_params else None
            except Exception:
                post_request = None
        
        log_entry = BusinessLineLog(
            action=action.strip(),
            previous=previous.strip() if previous else None,
            user_id=current_user.id,
            log_type=log_type,
            procedure_id=procedure_id,
            host=client_info["host"],
            user_ip=client_info["user_ip"],
            role_id=getattr(current_user, 'role_id', None),
            user_agent=client_info["user_agent"],
            post_request=post_request
        )
        
        db.add(log_entry)
        await db.commit()
        await db.refresh(log_entry)
        
        logger.info(f"Quick logged action '{action}' by user {current_user.id} - Log ID: {log_entry.id}")
        
        return {
            "message": "Action logged successfully", 
            "log_id": log_entry.id,
            "created_at": log_entry.created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error logging action: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error logging action '{action}' with log_type '{log_type}'"
        )
