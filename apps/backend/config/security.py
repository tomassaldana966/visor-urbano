import os
from datetime import datetime, timedelta, timezone
from authlib.jose import jwt
from authlib.jose.errors import JoseError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import UserModel
from app.schemas.users import UserOutSchema
from app.utils.user_extraction import BaseUserExtractor
from app.services.user_enrichment import UserRoleService, MunicipalityService
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from config.settings import get_db

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRATION_TIME", 3600))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def create_safe_user_schema(session: AsyncSession, user: UserModel, municipality_id: int = None) -> UserOutSchema:
    """
    Create a safe UserOutSchema object with enriched municipality data and role information.
    
    Args:
        session: Database session
        user: UserModel instance
        municipality_id: Optional municipality ID to override user's municipality_id
        
    Returns:
        UserOutSchema: Safe user object without sensitive data
    """
    # Extract basic user data using the new extractor
    user_data = BaseUserExtractor.extract_user_data(user)
    
    # Enrich with role information
    role_name = await UserRoleService.get_role_name(session, user_data["role_id"])
    user_data["role_name"] = role_name
    
    # Use provided municipality_id or fall back to user's municipality_id
    target_municipality_id = municipality_id if municipality_id is not None else user_data["municipality_id"]
    
    # Enrich with municipality information
    municipality_data, municipality_geospatial = await MunicipalityService.get_municipality_data(
        session, target_municipality_id
    )
    
    # Add municipality data to user_data if available
    if municipality_data:
        user_data["municipality_data"] = municipality_data.model_dump()
        
    if municipality_geospatial:
        user_data["municipality_geospatial"] = municipality_geospatial.model_dump()
    
    return UserOutSchema(**user_data)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    # Create header for authlib
    header = {"alg": JWT_ALGORITHM}
    encoded_jwt = jwt.encode(header, to_encode, JWT_SECRET_KEY)
    return encoded_jwt.decode('utf-8') if isinstance(encoded_jwt, bytes) else encoded_jwt

async def authenticate_user(session: AsyncSession, email: str, password: str):
    stmt = select(UserModel).filter(UserModel.email == email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if not user:
        return None
    
    if not verify_password(password, user.password):
        return None
        
    enriched_user = await get_user_by_email_and_municipality(session, user.email, user.municipality_id)
    if not enriched_user:
        return None
        
    return enriched_user

async def get_user_by_email_and_municipality(session: AsyncSession, email: str, municipality_id: int) -> UserOutSchema:
    """
    Retrieve a user filtered by email and municipality_id, enriched with municipality data.
    
    If the user has a municipality association (municipality_id > 0):
    - Get additional geospatial details from the BaseMunicipality table
    - Enrich the user object with this data
    
    If not (municipality_id <= 0):
    - Just return the user without additional municipality data
    
    Returns:
        UserOutSchema: Safe user object with enriched data
    """    
    stmt = select(UserModel).filter(UserModel.email == email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    
    if not user:
        return None
    
    return await create_safe_user_schema(session, user, municipality_id)

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> UserOutSchema:
    """
    Get current user from JWT token.
    
    Returns:
        UserOutSchema: Safe user object with enriched data
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY)
        # Extract claims  
        email: str = payload.get("sub")
        municipality_id: int = payload.get("municipality_id")

        if email is None:
            raise credentials_exception
        
    except JoseError:
        raise credentials_exception

    stmt = select(UserModel).filter(UserModel.email == email)
    result = await db.execute(stmt)
    user = result.scalars().first()
    if user is None:
        raise credentials_exception

    return await create_safe_user_schema(db, user, municipality_id)
