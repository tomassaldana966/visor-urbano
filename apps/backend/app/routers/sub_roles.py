from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from config.settings import get_db
from app.schemas import sub_roles as schemas
from app.models import sub_role as models
from config.security import get_current_user

sub_roles = APIRouter()

@sub_roles.get("/", response_model=list[schemas.SubRoleOutSchema])
async def list_sub_roles(db: AsyncSession = Depends(get_db)):
    try:
        query = select(models.SubRoleModel).limit(20)
        result = await db.execute(query)
        subroles = result.scalars().all()
        return subroles
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

@sub_roles.get("/municipality", response_model=list[schemas.SubRoleOutSchema])
async def list_sub_roles_by_municipality(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if not current_user.municipality_id:
        raise HTTPException(status_code=404, detail="No municipality assigned")
    
    query = select(models.SubRoleModel).filter_by(municipality_id=current_user.municipality_id).limit(20)
    result = await db.execute(query)
    subroles = result.scalars().all()
    return subroles

@sub_roles.get("/{subrole_id}", response_model=schemas.SubRoleOutSchema)
async def get_sub_role(subrole_id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.SubRoleModel).filter_by(id=subrole_id)
    result = await db.execute(query)
    subrole = result.scalar_one_or_none()
    
    if not subrole:
        raise HTTPException(status_code=404, detail="SubRole not found")
    return subrole

@sub_roles.post("/", response_model=schemas.SubRoleOutSchema)
async def create_sub_role(subrole_data: schemas.SubRoleCreateSchema, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if not current_user.municipality_id:
        raise HTTPException(status_code=404, detail="No municipality assigned")

    # Create data dictionary and ensure municipality_id is properly set
    subrole_dict = subrole_data.model_dump(exclude={"municipality_id"})
    subrole_dict["municipality_id"] = current_user.municipality_id
    
    new_subrole = models.SubRoleModel(**subrole_dict)
    db.add(new_subrole)
    await db.commit()
    await db.refresh(new_subrole)
    return new_subrole

@sub_roles.put("/{subrole_id}", response_model=schemas.SubRoleOutSchema)
async def update_sub_role(subrole_id: int, subrole_data: schemas.SubRoleUpdateSchema, db: AsyncSession = Depends(get_db)):
    query = select(models.SubRoleModel).filter_by(id=subrole_id)
    result = await db.execute(query)
    subrole = result.scalar_one_or_none()
    
    if not subrole:
        raise HTTPException(status_code=404, detail="SubRole not found")

    update_data = subrole_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subrole, field, value)

    await db.commit()
    await db.refresh(subrole)
    return subrole

@sub_roles.delete("/{subrole_id}", response_model=schemas.MessageSchema)
async def delete_sub_role(subrole_id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.SubRoleModel).filter_by(id=subrole_id)
    result = await db.execute(query)
    subrole = result.scalar_one_or_none()
    
    if not subrole:
        raise HTTPException(status_code=404, detail="SubRole not found")

    await db.delete(subrole)
    await db.commit()
    return {"message": "SubRole deleted successfully"}