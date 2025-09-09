from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, or_
from config.settings import get_session
from app.schemas.password import (
    PasswordResetRequestSchema,
    PasswordResetSchema,
    AuthenticatedPasswordChangeSchema,
    PasswordResetResponseSchema
)
from app.models.user import UserModel
from app.models.recover_password import PasswordRecovery
from config.security import get_password_hash, verify_password, get_current_user
from app.services.emails.sendgrid_client import send_email, render_email_template
from uuid import uuid4
from datetime import datetime, timedelta, timezone
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/password")

PASSWORD_RESET_RATE_LIMIT_MINUTES = 5

def get_utc_naive_now():
    """Get current UTC datetime as naive (for consistency with database storage)"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


@router.post("/reset-password-request", status_code=status.HTTP_200_OK, response_model=PasswordResetResponseSchema)
async def request_password_reset(
    payload: PasswordResetRequestSchema,
    db: AsyncSession = Depends(get_session)
):
    """
    Request a password reset link via email.
    Automatically cleans up expired tokens and prevents spam.
    """
    stmt = select(UserModel).where(UserModel.email == payload.email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        logger.warning(f"Password reset attempted for non-existent email: {payload.email}")
        return PasswordResetResponseSchema(
            detail="If this email exists, you will receive a password reset link",
            success=True
        )

    await db.execute(
        delete(PasswordRecovery).where(
            or_(
                PasswordRecovery.expiration_date < get_utc_naive_now(),
                PasswordRecovery.used == 1
            )
        )
    )

    stmt = select(PasswordRecovery).where(
        and_(
            PasswordRecovery.email == payload.email,
            PasswordRecovery.expiration_date > get_utc_naive_now(),
            PasswordRecovery.used == 0
        )
    )
    result = await db.execute(stmt)
    existing_token = result.scalars().first()

    if existing_token:
        time_since_creation = get_utc_naive_now() - existing_token.created_at
        if time_since_creation < timedelta(minutes=PASSWORD_RESET_RATE_LIMIT_MINUTES):
            logger.warning(f"Password reset rate limit hit for email: {payload.email}")
            return PasswordResetResponseSchema(
                detail=f"Please wait {PASSWORD_RESET_RATE_LIMIT_MINUTES} minutes before requesting another password reset",
                success=False
            )
        await db.execute(delete(PasswordRecovery).where(PasswordRecovery.id == existing_token.id))

    token = str(uuid4())
    new_token = PasswordRecovery(
        email=payload.email,
        token=token,
        expiration_date=PasswordRecovery.get_expiration_time(24),
        created_at=get_utc_naive_now()
    )
    db.add(new_token)
    await db.commit()

    try:
        frontend_url = os.getenv("APP_FRONT", "http://localhost:3000")
        reset_link = f"{frontend_url}/reset-password?token={token}"
        html_content = render_email_template("emails/recover.html", {
            "reset_link": reset_link,
            "user_name": user.name if hasattr(user, 'name') else user.email,
            "expiration_hours": 24
        })

        send_email(payload.email, "Password Reset Request", html_content)
        logger.info(f"Password reset email sent to: {payload.email}")
        
        return PasswordResetResponseSchema(
            detail="Check your inbox for a password reset link",
            success=True
        )
    except Exception as e:
        logger.error(f"Failed to send password reset email to {payload.email}: {str(e)}")
        await db.execute(delete(PasswordRecovery).where(PasswordRecovery.id == new_token.id))
        await db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send password reset email"
        )


@router.post("/change-password", status_code=status.HTTP_200_OK, response_model=PasswordResetResponseSchema)
async def reset_password_with_token(
    payload: PasswordResetSchema,
    db: AsyncSession = Depends(get_session)
):
    """
    Reset password using a valid token.
    Validates token expiration and usage status.
    """
    stmt = select(PasswordRecovery).where(
        and_(
            PasswordRecovery.email == payload.email,
            PasswordRecovery.token == payload.token
        )
    )
    result = await db.execute(stmt)
    token_entry = result.scalars().first()

    if not token_entry:
        logger.warning(f"Invalid password reset attempt for email: {payload.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired token"
        )

    if not token_entry.is_valid():
        reason = "expired" if token_entry.is_expired() else "already used"
        logger.warning(f"Password reset token {reason} for email: {payload.email}")
        await db.execute(delete(PasswordRecovery).where(PasswordRecovery.id == token_entry.id))
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    stmt = select(UserModel).where(UserModel.email == payload.email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        logger.error(f"User not found during password reset: {payload.email}")
        await db.execute(delete(PasswordRecovery).where(PasswordRecovery.id == token_entry.id))
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    user.password = get_password_hash(payload.password)
    
    # Delete all password recovery tokens for this email (security best practice)
    await db.execute(delete(PasswordRecovery).where(PasswordRecovery.email == payload.email))
    await db.commit()
    
    logger.info(f"Password successfully reset for user: {payload.email}")

    return PasswordResetResponseSchema(detail="Password successfully updated", success=True)


@router.post("/change-authenticated", status_code=status.HTTP_202_ACCEPTED)
async def change_authenticated_password(
    payload: AuthenticatedPasswordChangeSchema,
    db: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_user)
):
    if not verify_password(payload.current_password, current_user.password):
        raise HTTPException(status_code=422, detail="Current password is incorrect")

    current_user.password = get_password_hash(payload.new_password)
    await db.commit()

    return {"detail": "Password changed successfully"}
