from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import config.security as security
from config.security import create_access_token, authenticate_user
from config.settings import get_session
from app.schemas.auth import AuthLoginSchema, AuthResponseSchema

auth = APIRouter()

@auth.post("/token", response_model=dict, status_code=status.HTTP_200_OK)
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """
    OAuth2 compatible token endpoint for Swagger UI authentication.
    Uses username (email) and password from form data.
    """
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=security.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user.email, 
        "user_id": str(user.id),  
        "municipality_id": user.municipality_id  
    }
    access_token = create_access_token(data=token_data, expires_delta=access_token_expires)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@auth.post("/login", response_model=AuthResponseSchema, status_code=status.HTTP_200_OK)
async def login(
    auth_data: AuthLoginSchema,
    session: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(session, auth_data.email, auth_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=security.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user.email, 
        "user_id": str(user.id),  
        "municipality_id": user.municipality_id  
    }
    token = create_access_token(data=token_data, expires_delta=access_token_expires)

    return AuthResponseSchema(access_token=token, token_type="bearer", user=user)
