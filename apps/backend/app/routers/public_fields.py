from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config.settings import get_db
from app.models.field import Field
from app.models.requirements import Requirement
from app.schemas.field import (
    FieldCreate,
    FieldUpdate,
    FieldResponse,    
    RequirementToggle,
    FieldsAndAnswersResponse
)
from config.security import get_current_user
from typing import List, Dict, Any
from base64 import b64decode
import binascii

from app.models.answer import Answer
from app.models.requirements_query import RequirementsQuery
from app.models.renewal import Renewal
from app.models.procedures import Procedure

router = APIRouter()

GLOBAL_MUNICIPALITY_ID = 0

async def fetch_fields_and_answers(
    db: AsyncSession,
    municipality_id: int,
    query_id: int,
    filter_requirements: bool = True
) -> Dict[str, Any]:
    
    stmt_fields = (
        select(Field)
        .join(Requirement)
        .where(
            Requirement.municipality_id == municipality_id,
            Requirement.field_id == Field.id,
            Field.municipality_id.in_([GLOBAL_MUNICIPALITY_ID, municipality_id])
        )
    )

    if filter_requirements:
        stmt_fields = stmt_fields.where(Requirement.requirement_code.isnot(None))

    stmt_fields = stmt_fields.order_by(Field.sequence.asc(), Field.id.asc())
    result_fields = await db.execute(stmt_fields)
    dynamic_fields = result_fields.scalars().all()

    stmt_static = select(Field).where(Field.static_field == 1).order_by(Field.sequence.asc(), Field.id.asc())
    static_fields = (await db.execute(stmt_static)).scalars().all()

    # Get ALL answers for this procedure (not just annexes)
    stmt_answers = select(Answer).where(Answer.procedure_id == query_id)
    result_answers = await db.execute(stmt_answers)
    answers = result_answers.scalars().all()
    answer_map = {a.name: a.value for a in answers}

    static_fields_with_values = []
    for field in static_fields:
        field_dict = FieldResponse.model_validate(field).model_dump()
        
        # Convert boolean fields for static fields too - treat None/null as False
        field_dict["required"] = bool(field_dict.get("required") or False)
        field_dict["editable"] = bool(field_dict.get("editable") or False)
        field_dict["static_field"] = bool(field_dict.get("static_field") or False)
        field_dict["required_official"] = bool(field_dict.get("required_official") or False)
        
        if field.name in answer_map:
            field_dict["value"] = answer_map[field.name]
        static_fields_with_values.append(field_dict)

    # Process dynamic fields and add values
    dynamic_fields_with_values = []
    for field in dynamic_fields:
        field_dict = FieldResponse.model_validate(field).model_dump()
        
        # Convert boolean fields - treat None/null as False
        field_dict["required"] = bool(field_dict.get("required") or False)
        field_dict["editable"] = bool(field_dict.get("editable") or False)
        field_dict["static_field"] = bool(field_dict.get("static_field") or False)
        field_dict["required_official"] = bool(field_dict.get("required_official") or False)
        
        # Add value if found in answers
        if field.name in answer_map:
            field_dict["value"] = answer_map[field.name]
            
        dynamic_fields_with_values.append(field_dict)

    return {
        "dynamic_fields": dynamic_fields_with_values,
        "static_fields": static_fields_with_values
    }

async def fetch_fields_and_answers_by_type(
    db: AsyncSession,
    municipality_id: int,
    query_id: int,
    procedure_type: str,
    filter_requirements: bool = True
) -> Dict[str, Any]:
    
    stmt_fields = (
        select(Field)
        .join(Requirement)
        .where(
            Requirement.municipality_id == municipality_id,
            Requirement.field_id == Field.id,
            Field.municipality_id.in_([GLOBAL_MUNICIPALITY_ID, municipality_id]),
            Field.procedure_type == procedure_type  # Filter by procedure type
        )
    )

    if filter_requirements:
        stmt_fields = stmt_fields.where(Requirement.requirement_code.isnot(None))

    stmt_fields = stmt_fields.order_by(Field.sequence.asc(), Field.id.asc())
    result_fields = await db.execute(stmt_fields)
    dynamic_fields = result_fields.scalars().all()

    stmt_static = select(Field).where(Field.static_field == 1).order_by(Field.sequence.asc(), Field.id.asc())
    static_fields = (await db.execute(stmt_static)).scalars().all()
    
    stmt_answers = select(Answer).where(Answer.procedure_id == query_id)
    result_answers = await db.execute(stmt_answers)
    answers = result_answers.scalars().all()
    answer_map = {a.name: a.value for a in answers}    

    static_fields_with_values = []
    for field in static_fields:
        field_dict = FieldResponse.model_validate(field).model_dump()
        
        # Convert boolean fields for static fields too - treat None/null as False
        field_dict["required"] = bool(field_dict.get("required") or False)
        field_dict["editable"] = bool(field_dict.get("editable") or False)
        field_dict["static_field"] = bool(field_dict.get("static_field") or False)
        field_dict["required_official"] = bool(field_dict.get("required_official") or False)
        
        if field.name in answer_map:
            field_dict["value"] = answer_map[field.name]
        static_fields_with_values.append(field_dict)

    # Process dynamic fields and add values
    dynamic_fields_with_values = []
    for field in dynamic_fields:
        field_dict = FieldResponse.model_validate(field).model_dump()
        
        # Convert boolean fields - treat None/null as False
        field_dict["required"] = bool(field_dict.get("required") or False)
        field_dict["editable"] = bool(field_dict.get("editable") or False)
        field_dict["static_field"] = bool(field_dict.get("static_field") or False)
        field_dict["required_official"] = bool(field_dict.get("required_official") or False)
        
        # Add value if found in answers
        if field.name in answer_map:
            field_dict["value"] = answer_map[field.name]
            
        dynamic_fields_with_values.append(field_dict)

    return {
        "dynamic_fields": dynamic_fields_with_values,
        "static_fields": static_fields_with_values
    }

@router.get("/", response_model=List[FieldResponse])
async def list_fields(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if not user.municipality_id:
        raise HTTPException(status_code=404, detail="No municipality assigned")
    
    try:
        stmt = select(Field).where(Field.municipality_id == user.municipality_id)
        result = await db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/municipality/{municipality_id}", response_model=List[FieldResponse])
async def get_fields_by_municipality(
    municipality_id: int = Path(..., description="Municipality ID to get fields for"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all fields associated with a specific municipality.
    This is a public endpoint that doesn't require authentication.
    Returns field structure with English property names.
    """
    try:
        # Include both municipality-specific fields and global fields (municipality_id = 0)
        stmt = select(Field).where(
            Field.municipality_id.in_([GLOBAL_MUNICIPALITY_ID, municipality_id])
        ).order_by(Field.sequence.asc(), Field.id.asc())
        
        result = await db.execute(stmt)
        fields = result.scalars().all()
        
        if not fields:
            raise HTTPException(
                status_code=404, 
                detail=f"No fields found for municipality {municipality_id}"
            )
        
        # Convert boolean fields for all fields
        fields_with_booleans = []
        for field in fields:
            field_dict = FieldResponse.model_validate(field).model_dump()
            
            # Convert boolean fields - treat None/null as False
            field_dict["required"] = bool(field_dict.get("required") or False)
            field_dict["editable"] = bool(field_dict.get("editable") or False)
            field_dict["static_field"] = bool(field_dict.get("static_field") or False)
            field_dict["required_official"] = bool(field_dict.get("required_official") or False)
                
            fields_with_booleans.append(field_dict)
        
        return fields_with_booleans
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/{id}", response_model=FieldResponse)
async def get_field(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Field).where(Field.id == id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Field not found")
    return item


@router.post("/", response_model=FieldResponse)
async def create_field(data: FieldCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if not user.municipality_id:
        raise HTTPException(status_code=404, detail="No municipality assigned")
    
    try:
        field_data = data.model_dump()
        field_data['municipality_id'] = user.municipality_id
        # Don't set status=1 explicitly since it's already in the schema default
        new_field = Field(**field_data)
        db.add(new_field)
        
        # Flush to get the field ID without committing
        await db.flush()
        
        # Create requirement in the same transaction
        requirement = Requirement(
            municipality_id=user.municipality_id,
            field_id=new_field.id,
            requirement_code=None
        )
        db.add(requirement)
        
        # Single commit for both operations
        await db.commit()
        await db.refresh(new_field)
        
        return new_field
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


@router.put("/{id}", response_model=FieldResponse)
async def update_field(id: int, data: FieldUpdate, db: AsyncSession = Depends(get_db)):
    stmt = select(Field).where(Field.id == id)
    result = await db.execute(stmt)
    field = result.scalar_one_or_none()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(field, key, value)

    await db.commit()
    await db.refresh(field)
    return field


@router.delete("/{id}", status_code=204)
async def delete_field(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Field).where(Field.id == id)
    result = await db.execute(stmt)
    field = result.scalar_one_or_none()
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    await db.delete(field)
    await db.commit()


@router.post("/toggle_requirement", status_code=202, response_model=RequirementToggle)
async def toggle_requirement(
    data: RequirementToggle,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    
    if data.requirement_id == 0:
        new_req = Requirement(
            field_id=data.field_id,
            municipality_id=user.municipality_id,
            requirement_code=None
        )
        db.add(new_req)
        await db.commit()
        await db.refresh(new_req)
        return {
            "field_id": data.field_id,
            "requirement_id": new_req.id,
            "status": "created"
        }
    
    stmt = select(Requirement).where(Requirement.id == data.requirement_id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="Requirement not found")

    field_id = existing.field_id  
    await db.delete(existing)
    await db.commit()
        
    return {
        "field_id": field_id,
        "requirement_id": data.requirement_id,
        "status": "deleted"
    }


@router.get("/{id}/requirements", response_model=List[dict])
async def get_field_requirements(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Requirement).where(Requirement.field_id == id)
    result = await db.execute(stmt)
    items = result.scalars().all()

    return [  
        {
            "id": r.id,
            "requirement_code": r.requirement_code,
            "municipality_id": r.municipality_id
        } for r in items
    ]


@router.get("/by_folio/{folio}", response_model=FieldsAndAnswersResponse)
async def get_fields_by_folio(
    folio: str = Path(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        decoded_folio = b64decode(folio).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="Invalid base64 folio")
    
    # First, get the procedure to obtain its type
    procedure_stmt = select(Procedure).where(Procedure.folio == decoded_folio)
    procedure_result = await db.execute(procedure_stmt)
    procedure = procedure_result.scalar_one_or_none()
    
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    
    # Then get the requirements query
    stmt = select(RequirementsQuery).where(RequirementsQuery.folio == decoded_folio)
    result = await db.execute(stmt)
    query = result.scalar_one_or_none()

    if not query:
        raise HTTPException(status_code=404, detail="Requirements query not found")
    
    # Map the procedure type to the corresponding field type
    field_type = map_procedure_type_to_field_type(procedure.procedure_type)
    
    # Use the new function that filters by procedure type
    # Use procedure.id instead of query.id to get the correct answers
    return await fetch_fields_and_answers_by_type(
        db=db,
        municipality_id=query.municipality_id,
        query_id=procedure.id,  # Use procedure.id to get answers from Answer table
        procedure_type=field_type,
        filter_requirements=True
    )
        
@router.get("/by_renewal/{folio}", response_model=FieldsAndAnswersResponse)
async def get_fields_by_renewal(
    folio: str = Path(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        decoded_folio = b64decode(folio).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="Invalid base64 folio")

    if not decoded_folio.isdigit():
        raise HTTPException(status_code=400, detail="Decoded folio must be an integer")

    stmt = select(Renewal).where(Renewal.id == int(decoded_folio))
    result = await db.execute(stmt)
    renewal = result.scalar_one_or_none()
    if not renewal:
        raise HTTPException(status_code=404, detail="Renewal not found")

    stmt_q = select(RequirementsQuery).where(RequirementsQuery.id == renewal.license_id)
    result_q = await db.execute(stmt_q)
    query = result_q.scalar_one_or_none()
    if not query:
        raise HTTPException(status_code=404, detail="RequirementsQuery not found")
    
    return await fetch_fields_and_answers(
        db=db,
        municipality_id=query.municipality_id,
        query_id=query.id,
        filter_requirements=False  
    )

def map_procedure_type_to_field_type(procedure_type: str) -> str:
    """
    Map procedure types to their corresponding field types.
    All business/commercial procedures are unified under business_license.
    Construction procedures are unified under permits_building_license.
    """
    type_mapping = {
        "giro_comercial": "business_license",
        "business_commercial": "business_license", 
        "check_requirements": "business_license",
        "giro": "business_license",
        "comercial": "business_license",
        "construction": "permits_building_license",
        "licencia_construccion": "permits_building_license",
        "permits_building": "permits_building_license",
    }
    
    return type_mapping.get(procedure_type, procedure_type)
