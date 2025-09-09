from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import get_db
from app.schemas import user_roles as schemas
from app.models import user_roles as models
from config.security import get_current_user
from sqlalchemy import select


user_roles = APIRouter()

@user_roles.get("/", response_model=list[schemas.UserRoleOutSchema])
async def list_roles(db: AsyncSession = Depends(get_db)):
    stmt = select(models.UserRoleModel).limit(20)
    result = await db.execute(stmt)
    roles = result.scalars().all()
    return roles

@user_roles.get("/role_user", response_model=schemas.UserRoleOutSchema)
async def get_role_user(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
        
    result = await db.execute(select(models.UserRoleModel).filter(models.UserRoleModel.id == current_user.role_id))
    role = result.scalars().first()
        
    if not role:        
        raise HTTPException(status_code=404, detail="Role not found")
    
    return role

@user_roles.get("/role_user2", response_model=list[schemas.UserRoleOutSchema])
async def list_roles_user_extended(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user or not current_user.id:
        raise HTTPException(status_code=404, detail="Session Error")
    stmt = select(models.UserRoleModel).filter_by(user_id=current_user.id, municipality_id=current_user.municipality_data['id']).limit(1000)
    result = await db.execute(stmt)
    roles = result.scalars().all()
    return roles

@user_roles.get("/role_municipality", response_model=list[schemas.UserRoleOutSchema])
async def get_roles_by_municipality(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user.municipality_id:
        raise HTTPException(status_code=404, detail="No municipality assigned")
    stmt = select(models.UserRoleModel).filter_by(municipality_id=current_user.municipality_id)
    result = await db.execute(stmt)
    roles = result.scalars().all()
    return roles

@user_roles.get("/{role_id}", response_model=schemas.UserRoleOutSchema)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.UserRoleModel).where(models.UserRoleModel.id == role_id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@user_roles.post("/", response_model=schemas.UserRoleOutSchema)
async def create_role(role_data: schemas.UserRoleCreateSchema, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user.municipality_id:
        raise HTTPException(status_code=404, detail="No municipality assigned")

    stmt = select(models.UserRoleModel).filter_by(name=role_data.name)
    result = await db.execute(stmt)
    existing_role = result.scalar_one_or_none()
    if existing_role:
        raise HTTPException(status_code=409, detail="Role already exists")

    new_role = models.UserRoleModel(**role_data.model_dump(), municipality_id=current_user.municipality_id)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role

@user_roles.put("/{role_id}", response_model=schemas.UserRoleOutSchema)
async def update_role(role_id: int, role_data: schemas.UserRoleUpdateSchema, db: AsyncSession = Depends(get_db)):
    stmt = select(models.UserRoleModel).where(models.UserRoleModel.id == role_id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in role_data.model_dump(exclude_unset=True).items():
        setattr(role, field, value)

    await db.commit()
    await db.refresh(role)
    return role

@user_roles.delete("/{role_id}", response_model=schemas.MessageSchema)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(models.UserRoleModel).where(models.UserRoleModel.id == role_id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    await db.delete(role)
    await db.commit()
    return {"message": "Role deleted successfully"}
