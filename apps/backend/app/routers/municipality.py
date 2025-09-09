from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from config.settings import get_db
from config.security import get_current_user
from typing import List, Optional
import os
import uuid
import logging
from pathlib import Path as PathLib
from app.models.municipality import Municipality, MunicipalityGeom
from app.models.municipality_signature import MunicipalitySignature
from app.models.user import UserModel
from app.schemas.municipality import (
    MunicipalityResponse,
    MunicipalityCreate,
    MunicipalityUpdate,
    MunicipalityLegacyResponse,
    MunicipalityGeomLegacyResponse,
)
from app.schemas.municipality_signature import (
    MunicipalitySignatureCreate,
    MunicipalitySignatureUpdate,
    MunicipalitySignatureResponse,
)

municipalities = APIRouter()

# Configure logger for this module
logger = logging.getLogger(__name__)

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024
MUNICIPALITY_IMAGES_DIR = "uploads/municipality_images"
SIGNATURE_IMAGES_DIR = "uploads/municipality_signatures"

async def validate_image_upload(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    file_ext = PathLib(file.filename).suffix.lower()
    if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image format. Allowed types: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
    total_size = 0
    while True:
        chunk = await file.read(1024 * 1024)  
        if not chunk:
            break
        total_size += len(chunk)
        if total_size > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Image too large. Maximum size: {MAX_IMAGE_SIZE / (1024*1024)}MB"
            )
    await file.seek(0)  

@municipalities.get("/geom", response_model=dict)
async def list_municipalities_geom(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MunicipalityGeom))
    geom_records = result.scalars().all()
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": record.geom_type,
                "coordinates": record.coordinates
            },
            "properties": {
                "id": record.id,
                "name": record.name,
            }
        } for record in geom_records
    ]
    return {
        "type": "FeatureCollection",
        "features": features
    }

@municipalities.get("/", response_model=List[MunicipalityResponse])
async def list_municipalities(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = Query(None, description="Filter by municipality name"),
    has_zoning: Optional[bool] = Query(None, description="Filter by zoning availability"),
    cvegeo: Optional[str] = Query(None, description="Filter by geographic code"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Municipality).options(selectinload(Municipality.signatures))
    if name:
        query = query.where(Municipality.name.ilike(f"%{name}%"))
    if has_zoning is not None:
        query = query.where(Municipality.has_zoning == has_zoning)
    if cvegeo := cvegeo:
        query = query.where(Municipality.cvegeo == cvegeo)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    municipalities_list = result.scalars().all()
    return municipalities_list

@municipalities.post("/", response_model=MunicipalityResponse, status_code=status.HTTP_201_CREATED)
async def create_municipality(municipality: MunicipalityCreate, db: AsyncSession = Depends(get_db)):
    new_municipality = Municipality(**municipality.model_dump())
    db.add(new_municipality)
    await db.commit()
    await db.refresh(new_municipality, ["signatures"])
    return new_municipality

@municipalities.get("/geo_data", response_model=List[MunicipalityLegacyResponse])
async def list_municipalities_geo_data(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    Get municipalities with geographic data in legacy format compatible with /municipios GET endpoint.
    
    Returns municipalities with legacy field names and structure:
    - nombre (name)
    - tiene_zonificacion (has_zoning)
    - cve_ent, cve_mun, cvegeo (generated or default values)
    """
    query = select(Municipality).offset(skip).limit(limit)
    result = await db.execute(query)
    municipalities_list = result.scalars().all()
    
    # Convert to legacy format with default values for missing fields
    legacy_municipalities = []
    for muni in municipalities_list:
        legacy_muni = {
            "id": muni.id,
            "nombre": muni.name,  # Use Spanish field name directly
            "cve_ent": "08",  # Default state code (Chihuahua)
            "cve_mun": f"{muni.id:03d}",  # Generate municipality code from ID
            "cvegeo": f"08{muni.id:03d}",  # Generate geographic code
            "tiene_zonificacion": muni.has_zoning  # Use Spanish field name directly
        }
        legacy_municipalities.append(MunicipalityLegacyResponse.model_validate(legacy_muni))
    
    return legacy_municipalities

@municipalities.get("/geom/{municipality_id}", response_model=MunicipalityGeomLegacyResponse)
async def get_municipality_geom_legacy_format(
    municipality_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Get municipality geometry in legacy format compatible with /rest/v1/municipios-geom/{id} GET endpoint.
    
    Returns municipality with geometry data in GeoJSON Feature format.
    """
    # First check if municipality exists
    result = await db.execute(select(Municipality).where(Municipality.id == municipality_id))
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(status_code=404, detail="Municipality not found")
    
    # Check if geometry data exists
    result = await db.execute(select(MunicipalityGeom).where(MunicipalityGeom.municipality_id == municipality_id))
    geom_record = result.scalars().first()
    
    if geom_record:
        # Use actual geometry data
        geometry = {
            "type": geom_record.geom_type,
            "coordinates": geom_record.coordinates
        }
    else:
        # Generate default geometry (simple rectangle around a default coordinate)
        geometry = {
            "type": "Polygon", 
            "coordinates": [
                [
                    [381010.5544004806, 3295344.9501948184],
                    [383879.440900454, 3293858.15319479],
                    [383953.7020004322, 3293761.4491947885],
                    [384090.7772004276, 3293722.557294786],
                    [384454.4509004486, 3293607.5418947786],
                    [379675.40730047977, 3295596.10179483],
                    [381010.5544004806, 3295344.9501948184]
                ]
            ]
        }
    
    properties = {
        "nombre": municipality.name,
        "cve_ent": "08",
        "cve_mun": f"{municipality.id:03d}",
        "cvegeo": f"08{municipality.id:03d}",
        "tiene_zonificacion": municipality.has_zoning or False
    }
    
    return MunicipalityGeomLegacyResponse(
        id=municipality.id,
        type="Feature",
        geometry=geometry,
        properties=properties
    )

@municipalities.get("/{municipality_id}", response_model=MunicipalityResponse)
async def get_municipality(municipality_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Municipality)
        .options(selectinload(Municipality.signatures))
        .where(Municipality.id == municipality_id)
    )
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(status_code=404, detail="Municipality not found")
    
    # Convert to dict and map signature fields
    municipality_dict = {
        'id': municipality.id,
        'name': municipality.name,
        'director': municipality.director,
        'address': municipality.address,
        'phone': municipality.phone,
        'email': municipality.email,
        'website': municipality.website,
        'responsible_area': municipality.responsible_area,
        'solving_days': municipality.solving_days,
        'initial_folio': municipality.initial_folio,
        'low_impact_license_cost': municipality.low_impact_license_cost,
        'license_additional_text': municipality.license_additional_text,
        'allow_online_procedures': municipality.allow_online_procedures,
        'allow_window_reviewer_licenses': municipality.allow_window_reviewer_licenses,
        'theme_color': municipality.theme_color,
        'image': municipality.image,
        'created_at': municipality.created_at,
        'updated_at': municipality.updated_at,
        'signatures': []
    }
    
    # Map signatures with correct field names
    if municipality.signatures:
        municipality_dict['signatures'] = [
            {
                'id': sig.id,
                'municipality_id': sig.municipality_id,
                'signer_name': sig.signer_name,
                'position_title': sig.department,  # Map department to position_title
                'order_index': sig.orden,          # Map orden to order_index
                'signature_image': sig.signature,  # Map signature to signature_image
                'is_active': 'Y',
                'created_at': sig.created_at,
                'updated_at': sig.updated_at
            }
            for sig in municipality.signatures
        ]
    
    return municipality_dict

@municipalities.put("/{municipality_id}", response_model=MunicipalityResponse)
async def update_municipality(
    municipality_id: int,
    municipality_update: MunicipalityUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Municipality)
        .options(selectinload(Municipality.signatures))
        .where(Municipality.id == municipality_id)
    )
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(status_code=404, detail="Municipality not found")
    update_data = municipality_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(municipality, key, value)
    await db.commit()
    await db.refresh(municipality)
    
    # Convert to dict and map signature fields (same as get_municipality)
    municipality_dict = {
        'id': municipality.id,
        'name': municipality.name,
        'director': municipality.director,
        'address': municipality.address,
        'phone': municipality.phone,
        'email': municipality.email,
        'website': municipality.website,
        'responsible_area': municipality.responsible_area,
        'solving_days': municipality.solving_days,
        'initial_folio': municipality.initial_folio,
        'low_impact_license_cost': municipality.low_impact_license_cost,
        'license_additional_text': municipality.license_additional_text,
        'allow_online_procedures': municipality.allow_online_procedures,
        'allow_window_reviewer_licenses': municipality.allow_window_reviewer_licenses,
        'theme_color': municipality.theme_color,
        'image': municipality.image,
        'created_at': municipality.created_at,
        'updated_at': municipality.updated_at,
        'signatures': []
    }
    
    # Map signatures with correct field names
    if municipality.signatures:
        municipality_dict['signatures'] = [
            {
                'id': sig.id,
                'municipality_id': sig.municipality_id,
                'signer_name': sig.signer_name,
                'position_title': sig.department,
                'order_index': sig.orden,
                'signature_image': sig.signature,
                'is_active': 'Y',
                'created_at': sig.created_at,
                'updated_at': sig.updated_at
            }
            for sig in municipality.signatures
        ]
    
    return municipality_dict

@municipalities.delete("/{municipality_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_municipality(municipality_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Municipality).where(Municipality.id == municipality_id))
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(status_code=404, detail="Municipality not found")
    await db.delete(municipality)
    await db.commit()
    return None

@municipalities.post("/{municipality_id}/image", response_model=MunicipalityResponse)
async def upload_municipality_image(
    municipality_id: int,
    image: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Municipality)
        .options(selectinload(Municipality.signatures))
        .where(Municipality.id == municipality_id)
    )
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Municipality not found"
        )
    if not hasattr(current_user, 'municipality_id') or current_user.municipality_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no municipality assigned"
        )
    await validate_image_upload(image)
    
    logger.info(
        f"Starting image upload for municipality {municipality_id}",
        extra={
            'municipality_id': municipality_id,
            'user_id': getattr(current_user, 'id', None),
            'uploaded_filename': getattr(image, 'filename', None)
        }
    )
    
    try:
        os.makedirs(MUNICIPALITY_IMAGES_DIR, exist_ok=True)
        file_ext = PathLib(image.filename).suffix.lower()
        filename = f"municipality_{municipality_id}_{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(MUNICIPALITY_IMAGES_DIR, filename)
        total_size = 0
        with open(file_path, "wb") as buffer:
            while chunk := await image.read(8192):
                total_size += len(chunk)
                if total_size > MAX_IMAGE_SIZE:
                    buffer.close()
                    os.unlink(file_path)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"Image too large. Maximum size: {MAX_IMAGE_SIZE / (1024*1024)}MB"
                    )
                buffer.write(chunk)
        # Clean up old image if it exists
        if municipality.image and os.path.exists(municipality.image):
            try:
                os.unlink(municipality.image)
                logger.info(f"Removed old image: {municipality.image}")
            except OSError as e:
                logger.warning(f"Failed to remove old image {municipality.image}: {e}")
        
        # Update municipality with new image path
        municipality.image = file_path
        await db.commit()
        
        # Reload municipality with signatures to avoid lazy loading issues
        result = await db.execute(
            select(Municipality)
            .options(selectinload(Municipality.signatures))
            .where(Municipality.id == municipality_id)
        )
        municipality = result.scalars().first()
        
        logger.info(
            f"Successfully uploaded image for municipality {municipality_id}",
            extra={
                'municipality_id': municipality_id,
                'user_id': getattr(current_user, 'id', None),
                'new_image_path': file_path
            }
        )
        
        # Convert to dict and map signature fields (same as get_municipality)
        municipality_dict = {
            'id': municipality.id,
            'name': municipality.name,
            'director': municipality.director,
            'address': municipality.address,
            'phone': municipality.phone,
            'email': municipality.email,
            'website': municipality.website,
            'responsible_area': municipality.responsible_area,
            'solving_days': municipality.solving_days,
            'initial_folio': municipality.initial_folio,
            'low_impact_license_cost': municipality.low_impact_license_cost,
            'license_additional_text': municipality.license_additional_text,
            'allow_online_procedures': municipality.allow_online_procedures,
            'allow_window_reviewer_licenses': municipality.allow_window_reviewer_licenses,
            'theme_color': municipality.theme_color,
            'image': municipality.image,
            'created_at': municipality.created_at,
            'updated_at': municipality.updated_at,
            'signatures': []
        }
        
        # Map signatures with correct field names
        if municipality.signatures:
            municipality_dict['signatures'] = [
                {
                    'id': sig.id,
                    'municipality_id': sig.municipality_id,
                    'signer_name': sig.signer_name,
                    'position_title': sig.department,
                    'order_index': sig.orden,
                    'signature_image': sig.signature,
                    'is_active': 'Y',
                    'created_at': sig.created_at,
                    'updated_at': sig.updated_at
                }
                for sig in municipality.signatures
            ]
        
        return municipality_dict
    except Exception as e:
        # Log the full exception details for debugging
        logger.error(
            f"Failed to upload image for municipality {municipality_id}: {str(e)}",
            exc_info=True,
            extra={
                'municipality_id': municipality_id,
                'user_id': getattr(current_user, 'id', None),
                'uploaded_filename': getattr(image, 'filename', None)
            }
        )
        
        # Clean up the uploaded file if it was created
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                os.unlink(file_path)
                logger.info(f"Cleaned up failed upload file: {file_path}")
            except OSError as cleanup_error:
                logger.warning(f"Failed to clean up file {file_path}: {cleanup_error}")
        
        # Re-raise HTTPExceptions as-is
        if isinstance(e, HTTPException):
            raise e
        
        # Convert other exceptions to HTTP 500 with generic message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload municipality image"
        )

# Endpoints for municipality signatures
@municipalities.get("/{municipality_id}/signatures", response_model=List[MunicipalitySignatureResponse])
async def get_municipality_signatures(
    municipality_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all signatures for a municipality"""
    result = await db.execute(select(Municipality).where(Municipality.id == municipality_id))
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(status_code=404, detail="Municipality not found")
    
    signatures_result = await db.execute(
        select(MunicipalitySignature)
        .where(MunicipalitySignature.municipality_id == municipality_id)
        .order_by(MunicipalitySignature.orden)  # Use actual field name
    )
    signatures = signatures_result.scalars().all()
    
    # Map signatures with correct field names
    return [
        {
            'id': sig.id,
            'municipality_id': sig.municipality_id,
            'signer_name': sig.signer_name,
            'position_title': sig.department,
            'order_index': sig.orden,
            'signature_image': sig.signature,
            'is_active': 'Y',
            'created_at': sig.created_at,
            'updated_at': sig.updated_at
        }
        for sig in signatures
    ]

@municipalities.post("/{municipality_id}/signatures", response_model=MunicipalitySignatureResponse)
async def create_municipality_signature(
    municipality_id: int,
    signature_data: MunicipalitySignatureCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new signature for a municipality"""
    # Verify municipality exists
    result = await db.execute(select(Municipality).where(Municipality.id == municipality_id))
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(status_code=404, detail="Municipality not found")
    
    # Verify user belongs to this municipality
    if not hasattr(current_user, 'municipality_id') or current_user.municipality_id != municipality_id:
        raise HTTPException(status_code=403, detail="User not authorized for this municipality")
    
    # Create the signature
    new_signature = MunicipalitySignature(
        municipality_id=municipality_id,
        signer_name=signature_data.signer_name,
        department=signature_data.position_title,  # Map position_title to department
        orden=signature_data.order_index,  # Map order_index to orden
    )
    db.add(new_signature)
    await db.commit()
    await db.refresh(new_signature)
    
    # Return mapped signature
    return {
        'id': new_signature.id,
        'municipality_id': new_signature.municipality_id,
        'signer_name': new_signature.signer_name,
        'position_title': new_signature.department,
        'order_index': new_signature.orden,
        'signature_image': new_signature.signature,
        'is_active': 'Y',
        'created_at': new_signature.created_at,
        'updated_at': new_signature.updated_at
    }

@municipalities.put("/{municipality_id}/signatures/{signature_id}", response_model=MunicipalitySignatureResponse)
async def update_municipality_signature(
    municipality_id: int,
    signature_id: int,
    signature_update: MunicipalitySignatureUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a municipality signature"""
    # Verify municipality exists
    result = await db.execute(select(Municipality).where(Municipality.id == municipality_id))
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(status_code=404, detail="Municipality not found")
    
    # Verify user belongs to this municipality
    if not hasattr(current_user, 'municipality_id') or current_user.municipality_id != municipality_id:
        raise HTTPException(status_code=403, detail="User not authorized for this municipality")
    
    # Get the signature
    signature_result = await db.execute(
        select(MunicipalitySignature)
        .where(MunicipalitySignature.id == signature_id)
        .where(MunicipalitySignature.municipality_id == municipality_id)
    )
    signature = signature_result.scalars().first()
    if signature is None:
        raise HTTPException(status_code=404, detail="Signature not found")
    
    # Update the signature
    update_data = signature_update.model_dump(exclude_unset=True)
    
    # Map schema fields to model fields
    field_mapping = {
        'position_title': 'department',
        'order_index': 'orden',
        'signature_image': 'signature'
    }
    
    for key, value in update_data.items():
        model_field = field_mapping.get(key, key)
        setattr(signature, model_field, value)
    
    await db.commit()
    await db.refresh(signature)
    
    # Return mapped signature
    return {
        'id': signature.id,
        'municipality_id': signature.municipality_id,
        'signer_name': signature.signer_name,
        'position_title': signature.department,
        'order_index': signature.orden,
        'signature_image': signature.signature,
        'is_active': 'Y',
        'created_at': signature.created_at,
        'updated_at': signature.updated_at
    }

@municipalities.post("/{municipality_id}/signatures/{signature_id}/image", response_model=MunicipalitySignatureResponse)
async def upload_signature_image(
    municipality_id: int,
    signature_id: int,
    image: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload an image for a municipality signature"""
    # Verify municipality exists
    result = await db.execute(select(Municipality).where(Municipality.id == municipality_id))
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(status_code=404, detail="Municipality not found")
    
    # Verify user belongs to this municipality
    if not hasattr(current_user, 'municipality_id') or current_user.municipality_id != municipality_id:
        raise HTTPException(status_code=403, detail="User not authorized for this municipality")
    
    # Get the signature
    signature_result = await db.execute(
        select(MunicipalitySignature)
        .where(MunicipalitySignature.id == signature_id)
        .where(MunicipalitySignature.municipality_id == municipality_id)
    )
    signature = signature_result.scalars().first()
    if signature is None:
        raise HTTPException(status_code=404, detail="Signature not found")
    
    # Validate the uploaded image
    await validate_image_upload(image)
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(SIGNATURE_IMAGES_DIR, exist_ok=True)
        
        # Generate unique filename
        file_ext = PathLib(image.filename).suffix.lower()
        filename = f"signature_{municipality_id}_{signature_id}_{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(SIGNATURE_IMAGES_DIR, filename)
        
        # Save the file
        total_size = 0
        with open(file_path, "wb") as buffer:
            while chunk := await image.read(8192):
                total_size += len(chunk)
                if total_size > MAX_IMAGE_SIZE:
                    buffer.close()
                    os.unlink(file_path)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"Image too large. Maximum size: {MAX_IMAGE_SIZE / (1024*1024)}MB"
                    )
                buffer.write(chunk)
        
        # Clean up old image if it exists
        if signature.signature and os.path.exists(signature.signature):
            try:
                os.unlink(signature.signature)
                logger.info(f"Removed old signature image: {signature.signature}")
            except OSError as e:
                logger.warning(f"Failed to remove old signature image {signature.signature}: {e}")
        
        # Update signature with new image path (using the actual database field)
        signature.signature = file_path
        await db.commit()
        await db.refresh(signature)
        
        logger.info(
            f"Successfully uploaded signature image for municipality {municipality_id}, signature {signature_id}",
            extra={
                'municipality_id': municipality_id,
                'signature_id': signature_id,
                'user_id': getattr(current_user, 'id', None),
                'new_image_path': file_path
            }
        )
        
        # Return mapped signature
        return {
            'id': signature.id,
            'municipality_id': signature.municipality_id,
            'signer_name': signature.signer_name,
            'position_title': signature.department,
            'order_index': signature.orden,
            'signature_image': signature.signature,
            'is_active': 'Y',
            'created_at': signature.created_at,
            'updated_at': signature.updated_at
        }
        
    except Exception as e:
        logger.error(
            f"Failed to upload signature image: {str(e)}",
            exc_info=True,
            extra={
                'municipality_id': municipality_id,
                'signature_id': signature_id,
                'user_id': getattr(current_user, 'id', None),
            }
        )
        
        # Clean up the uploaded file if it was created
        if 'file_path' in locals() and os.path.exists(file_path):
            try:
                os.unlink(file_path)
            except OSError:
                pass
        
        if isinstance(e, HTTPException):
            raise e
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload signature image"
        )

@municipalities.delete("/{municipality_id}/signatures/{signature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_municipality_signature(
    municipality_id: int,
    signature_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a municipality signature"""
    # Verify municipality exists
    result = await db.execute(select(Municipality).where(Municipality.id == municipality_id))
    municipality = result.scalars().first()
    if municipality is None:
        raise HTTPException(status_code=404, detail="Municipality not found")
    
    # Verify user belongs to this municipality
    if not hasattr(current_user, 'municipality_id') or current_user.municipality_id != municipality_id:
        raise HTTPException(status_code=403, detail="User not authorized for this municipality")
    
    # Get the signature
    signature_result = await db.execute(
        select(MunicipalitySignature)
        .where(MunicipalitySignature.id == signature_id)
        .where(MunicipalitySignature.municipality_id == municipality_id)
    )
    signature = signature_result.scalars().first()
    if signature is None:
        raise HTTPException(status_code=404, detail="Signature not found")
    
    # Clean up signature image if it exists
    if signature.signature and os.path.exists(signature.signature):
        try:
            os.unlink(signature.signature)
            logger.info(f"Removed signature image: {signature.signature}")
        except OSError as e:
            logger.warning(f"Failed to remove signature image {signature.signature}: {e}")
    
    # Delete the signature
    await db.delete(signature)
    await db.commit()
    
    return None

