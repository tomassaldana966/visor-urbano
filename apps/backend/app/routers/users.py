from fastapi import APIRouter, HTTPException, Path, Body, Depends, status, Query
from uuid import uuid4
import os
from sqlalchemy import select, or_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import config.security as security
from config.settings import get_session
import app.schemas.users as schemas
from app.services.emails.sendgrid_client import send_email, render_email_template
import app.models.user as UserModel
from app.models.user_roles import UserRoleModel
from app.models.user_roles_assignments import UserRoleAssignment
from app.models.municipality import Municipality
from app.schemas.user_roles import AssignRoleRequestSchema, RoleValidationResponse
from app.utils.role_validation import validate_director_role
from fastapi.responses import RedirectResponse

users = APIRouter()

@users.get("/test")
async def test_endpoint():
    """Simple test endpoint for testing purposes only"""
    return {"users": "test user"}

@users.get("/", response_model=list[schemas.UserOutSchema])
async def get_users(
    search: Optional[str] = Query(None, description="Search by name or email"),
    role: Optional[str] = Query(None, description="Filter by role name"),
    db: AsyncSession = Depends(get_session),
    current_user = Depends(security.get_current_user)
):
    """
    Get all users with optional search and role filtering
    """
    # Validate director role
    validate_director_role(current_user)
    
    # Base query with eager loading of related data
    query = select(UserModel.UserModel).options(
        selectinload(UserModel.UserModel.municipality),
        selectinload(UserModel.UserModel.user_roles)
    )
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                UserModel.UserModel.name.ilike(search_term),
                UserModel.UserModel.email.ilike(search_term),
                func.concat(
                    UserModel.UserModel.name, 
                    ' ', 
                    UserModel.UserModel.paternal_last_name
                ).ilike(search_term)
            )
        )
    
    # Apply role filter if provided
    if role:
        query = query.join(UserModel.UserModel.user_roles).where(
            UserRoleModel.name.ilike(f"%{role}%")
        )
    
    result = await db.execute(query)
    users = result.scalars().all()
    
    # Transform users to include role_name and municipality_data
    transformed_users = []
    for user in users:
        # Set role_name
        if user.user_roles:
            user.role_name = user.user_roles.name
        else:
            user.role_name = "User"
        
        # Set municipality_data if municipality exists
        if user.municipality:
            user.municipality_data = {
                "id": user.municipality.id,
                "name": user.municipality.name,
                "director": user.municipality.director,
                "address": user.municipality.address,
                "phone": user.municipality.phone
            }
        else:
            user.municipality_data = None
        
        transformed_users.append(user)
    
    return transformed_users

@users.get("/send_email")
def get_sendemail(email: str):
    
    html = render_email_template("emails/roles.html", {
    "url": "https://visorurbano.jalisco.gob.mx"
    })
    send_email(email, "[TEST #1] Role Updated", html)
    return {"message": "Email sent successfully"}

@users.post("/", response_model=schemas.UserOutSchema)
async def create_user(user: schemas.UserCreateSchema, db: AsyncSession = Depends(get_session)):  
    existing_user = await db.execute(
        UserModel.UserModel.__table__.select().where(UserModel.UserModel.email == user.email)
    )
    existing_user = existing_user.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    hashed_password = security.get_password_hash(user.password)
    db_user = UserModel.UserModel(
        name=user.name,
        paternal_last_name=user.paternal_last_name,
        maternal_last_name=user.maternal_last_name,
        cellphone=user.cellphone,
        email=user.email,
        password=hashed_password,
        municipality_id=user.municipality_id,
        role_id=user.role_id,
        is_active=True
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    # Create safe user schema with enriched data
    return await security.create_safe_user_schema(db, db_user)


@users.get("/{user_id}", response_model=schemas.UserOutSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    stmt = select(UserModel.UserModel).where(UserModel.UserModel.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create safe user schema with enriched data
    return await security.create_safe_user_schema(db, db_user)

@users.put("/{user_id}", response_model=schemas.UserOutSchema)
async def update_user(
    user_id: int, 
    user: schemas.UserUpdateSchema, 
    db: AsyncSession = Depends(get_session)
):
    stmt = select(UserModel.UserModel).where(UserModel.UserModel.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields if they exist in the request
    update_data = user.model_dump(exclude_unset=True)
    
    if "password" in update_data and update_data["password"]:
        hashed_password = security.get_password_hash(update_data["password"])
        update_data["password"] = hashed_password
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    await db.commit()
    await db.refresh(db_user)
    
    # Create safe user schema with enriched data
    return await security.create_safe_user_schema(db, db_user)

@users.delete("/{user_id}", response_model=schemas.MessageSchema)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):  
    stmt = select(UserModel.UserModel).where(UserModel.UserModel.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted successfully"}

@users.post("/{user_id}/assign-role")
async def assign_role(
    user_id: int = Path(...),
    payload: AssignRoleRequestSchema = Body(...),
    db: AsyncSession = Depends(get_session)  # Cambiado a get_session para AsyncSession
):           
    stmt = select(UserModel.UserModel).where(UserModel.UserModel.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    stmt = select(UserRoleModel).where(UserRoleModel.id == payload.role_id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    stmt = select(Municipality).where(Municipality.id == user.municipality_id)
    result = await db.execute(stmt)
    municipality = result.scalar_one_or_none()
    if not municipality:
        raise HTTPException(status_code=404, detail="Municipality not found")

    token = str(uuid4())
    
    stmt = select(UserRoleAssignment).where(UserRoleAssignment.user_id == user_id)
    result = await db.execute(stmt)
    assignment = result.scalar_one_or_none()
    
    if not assignment:
        assignment = UserRoleAssignment(user_id=user_id)
        db.add(assignment)

    assignment.pending_role_id = payload.role_id
    assignment.token = token
    assignment.role_status = "pending"

    
    await db.commit()
    await db.refresh(assignment)
    email_context = {
        "app_url": os.getenv("APP_FRONT", "https://visorurbano.jalisco.gob.mx"),
        "token": token,
        "municipio": municipality.name,
        "role_name": role.name,
        "email": user.email
    }
    html = render_email_template("emails/role.html", email_context)

    send_email(user.email, "Role Update Notification", html)
    send_email(os.getenv("MAIL_FROM_ADDRESS", 'test@visorurbano.com'), "Role Update Notification", html)

    return {"detail": "Role assignment email sent", "token": token}

@users.get("/validate-role/{token}", response_model=RoleValidationResponse)
async def validate_user_role(
    token: str = Path(..., description="The validation token sent via email"),
    db: AsyncSession = Depends(get_session)  # Cambiamos a get_session para obtener AsyncSession
):    
        
    stmt = select(UserRoleAssignment).where(UserRoleAssignment.token == token)
    result = await db.execute(stmt)
    assignment = result.scalar_one_or_none()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Role assignment not found. The token may be invalid or expired."
        )
        
    stmt = select(UserModel.UserModel).where(UserModel.UserModel.id == assignment.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    if assignment.role_status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="This role has already been validated or is no longer pending"
        )
    
    stmt = select(UserRoleModel).where(UserRoleModel.id == assignment.pending_role_id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
        
    assignment.role_id = assignment.pending_role_id
    assignment.pending_role_id = None
    assignment.token = None
    assignment.role_status = "active"
    
    await db.commit()
    
    if role:
        email_context = {
            "app_url": os.getenv("APP_FRONT", "https://visorurbano.jalisco.gob.mx"),
            "user_name": f"{user.name} {user.paternal_last_name}",
            "role_name": role.name,
            "email": user.email
        }
        html = render_email_template("emails/role_confirmation.html", email_context)
                
        send_email(user.email, "Role Assignment Confirmed", html)
                
        send_email(
            os.getenv("MAIL_FROM_ADDRESS", 'test@visorurbano.com'), 
            f"User {user.email} confirmed role assignment", 
            html
        )

    return {"detail": "Role successfully validated and assigned."}

@users.get("/validate-role-redirect/{token}")
async def validate_role_redirect(
    token: str = Path(..., description="The validation token sent via email"),
):        
    frontend_url = os.getenv("APP_FRONT", "https://visorurbano.jalisco.gob.mx")
    redirect_url = f"{frontend_url}/validate-role?token={token}"
        
    return RedirectResponse(url=redirect_url)
