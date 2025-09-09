from fastapi import APIRouter, Depends, HTTPException, Query, status, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime, timezone
import os
import logging
from app.models.user import UserModel as User
from config.security import get_current_user

from app.models.dependency_revision import DependencyRevision
from app.models.requirements_query import RequirementsQuery
from app.schemas.dependency_revision import (
    DependencyRevisionCreate,
    DependencyRevisionRead,
    DependencyRevisionUpdate
)
from config.settings import get_db
from app.utils.role_validation import validate_admin_role, validate_director_role, require_admin_role, require_director_role
from app.services.emails.sendgrid_client import send_email, render_email_template

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/dependency_revisions",    
)

@router.get("/", response_model=List[DependencyRevisionRead])
async def list_dependency_revisions(
    dependency_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(DependencyRevision)
    if dependency_id is not None:
        query = query.where(DependencyRevision.dependency_id == dependency_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{id}", response_model=DependencyRevisionRead)
async def get_dependency_revision(id: int, db: AsyncSession = Depends(get_db)):
    revision = await db.get(DependencyRevision, id)
    if not revision:
        raise HTTPException(status_code=404, detail="Dependency revision not found")
    return revision

@router.post("/", response_model=DependencyRevisionRead, status_code=status.HTTP_201_CREATED)
async def create_dependency_revision(data: DependencyRevisionCreate, db: AsyncSession = Depends(get_db)):
    if data.dependency_id:
        rq = await db.get(RequirementsQuery, data.dependency_id)
        if not rq:
            raise HTTPException(status_code=400, detail="Invalid dependency_id: RequirementsQuery not found")
    revision = DependencyRevision(**data.model_dump())
    db.add(revision)
    await db.commit()
    await db.refresh(revision)
    return revision

@router.patch("/{id}", response_model=DependencyRevisionRead)
async def update_dependency_revision(id: int, data: DependencyRevisionUpdate, db: AsyncSession = Depends(get_db)):
    revision = await db.get(DependencyRevision, id)
    if not revision:
        raise HTTPException(status_code=404, detail="Dependency revision not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(revision, key, value)
    await db.commit()
    await db.refresh(revision)
    return revision

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dependency_revision(id: int, db: AsyncSession = Depends(get_db)):
    revision = await db.get(DependencyRevision, id)
    if not revision:
        raise HTTPException(status_code=404, detail="Dependency revision not found")
    await db.delete(revision)
    await db.commit()

@router.get("/by_folio/{folio}", response_model=List[DependencyRevisionRead])
async def get_dependency_revisions_by_folio(folio: str, db: AsyncSession = Depends(get_db)):
    rq_stmt = select(RequirementsQuery).where(RequirementsQuery.folio == folio)
    rq_result = await db.execute(rq_stmt)
    rq = rq_result.scalar_one_or_none()
    if not rq:
        raise HTTPException(status_code=404, detail="RequirementsQuery with provided folio not found.")
    rev_stmt = select(DependencyRevision).where(DependencyRevision.dependency_id == rq.id)
    rev_result = await db.execute(rev_stmt)
    return rev_result.scalars().all()

@router.post("/by_folio/{folio}", response_model=DependencyRevisionRead)
async def create_revision_by_folio(
    folio: str,
    revision: DependencyRevisionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rq_stmt = select(RequirementsQuery).where(RequirementsQuery.folio == folio)
    rq_result = await db.execute(rq_stmt)
    rq = rq_result.scalar_one_or_none()
    if not rq:
        raise HTTPException(status_code=404, detail="Procedure with the specified folio not found.")
    if rq.municipality_id != current_user.municipality_id:
        raise HTTPException(status_code=403, detail="Access denied: municipality mismatch.")
    new_revision = DependencyRevision(
        dependency_id=rq.id,
        revision_notes=revision.revision_notes,
        revised_at=datetime.now(timezone.utc),
    )
    db.add(new_revision)
    await db.commit()
    await db.refresh(new_revision)
    return new_revision

@router.post("/upload_file/{id}", response_model=DependencyRevisionRead)
async def upload_file(
    id: int, 
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    revision = await db.get(DependencyRevision, id)
    if not revision:
        raise HTTPException(status_code=404, detail="Dependency revision not found")
    file_location = f"files/{file.filename}"
    with open(file_location, "wb") as file_object:
        file_object.write(file.file.read())
    revision.file_path = file_location
    await db.commit()
    await db.refresh(revision)
    try:
        frontend_url = os.getenv("APP_FRONT", "http://localhost:3000")
        portal_url = os.getenv("PORTAL_URL", frontend_url)
        html_content = render_email_template("dependency_revision_file_upload.html", {
            "folio": f"REV-{id}",
            "revision_id": id,
            "user_email": current_user.email if hasattr(current_user, 'email') else "system@visorurbano.com",
            "uploaded_at": datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S"),
            "file_name": file.filename,
            "current_year": datetime.now().year,
            "portal_url": portal_url
        })
        user_email = current_user.email if hasattr(current_user, 'email') else "system@visorurbano.com"
        send_email(user_email, f"File uploaded for revision {id}", html_content)
        logger.info(f"File upload notification email sent to: {user_email}")
    except Exception as e:
        logger.error(f"Failed to send file upload notification email: {str(e)}")
    return revision

@router.get("/download_file/{id}", response_class=FileResponse)
async def download_file(
    id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    revision = await db.get(DependencyRevision, id)
    if not revision:
        raise HTTPException(status_code=404, detail="Dependency revision not found")
    file_path = revision.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/octet-stream')

@router.post("/update/{id}")
async def update_dependency_revision_status(
    id: int,
    data: DependencyRevisionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        revision = await db.get(DependencyRevision, id)
        if not revision:
            raise HTTPException(status_code=404, detail="Dependency revision not found")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        for field, value in update_data.items():
            setattr(revision, field, value)
        revision.revised_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(revision)
        try:
            frontend_url = os.getenv("APP_FRONT", "http://localhost:3000")
            portal_url = os.getenv("PORTAL_URL", frontend_url)
            html_content = render_email_template("dependency_revision_status_update.html", {
                "folio": f"REV-{id}",
                "revision_id": id,
                "comment": data.revision_notes or "Status updated",
                "updated_at": datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S"),
                "current_year": datetime.now().year,
                "portal_url": portal_url
            })
            user_email = current_user.email if hasattr(current_user, 'email') else "system@visorurbano.com"
            send_email(user_email, f"Dependency revision updated - ID {id}", html_content)
            logger.info(f"Status update notification email sent to: {user_email}")
        except Exception as e:
            logger.error(f"Failed to send status update notification email: {str(e)}")
        return {"detail": "Revision successfully updated"}
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating revision: {str(e)}")

@router.post("/update_director/{id}")
async def update_director_revision(
    id: int,
    data: DependencyRevisionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_director_role)
):
    try:
        revision = await db.get(DependencyRevision, id)
        if not revision:
            raise HTTPException(status_code=404, detail="Dependency revision not found")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        for field, value in update_data.items():
            setattr(revision, field, value)
        revision.revised_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(revision)
        try:
            frontend_url = os.getenv("APP_FRONT", "http://localhost:3000")
            portal_url = os.getenv("PORTAL_URL", frontend_url)
            html_content = render_email_template("dependency_revision_notification.html", {
                "folio": f"REV-{id}",
                "revision_id": id,
                "comment": f"Director Update: {data.revision_notes or 'Status updated'}",
                "updated_at": datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S"),
                "current_year": datetime.now().year,
                "portal_url": portal_url
            })
            user_email = current_user.email if hasattr(current_user, 'email') else "system@visorurbano.com"
            send_email(user_email, f"Dependency revision updated by Director - ID {id}", html_content)
            logger.info(f"Director update notification email sent to: {user_email}")
        except Exception as e:
            logger.error(f"Failed to send director update notification email: {str(e)}")
        return {"detail": "Revision successfully updated by director"}
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating revision as director: {str(e)}")

@router.get("/full_report")
async def get_full_revision_report(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_role)
):
    try:
        stmt = select(DependencyRevision).order_by(DependencyRevision.revised_at.desc())
        result = await db.execute(stmt)
        revisions = result.scalars().all()
        response = [
            {
                "id": r.id,
                "dependency_id": r.dependency_id,
                "revision_notes": r.revision_notes,
                "revised_at": r.revised_at.isoformat() if r.revised_at else None,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None
            }
            for r in revisions
        ]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving full revision report: {str(e)}")

@router.get("/analytics/revisions_by_date")
async def get_revisions_by_date(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_role)
):
    try:
        from sqlalchemy import func
        stmt = select(
            func.date(DependencyRevision.revised_at).label("revision_date"),
            func.count().label("total")
        ).group_by(func.date(DependencyRevision.revised_at))
        if start_date:
            stmt = stmt.where(DependencyRevision.revised_at >= start_date)
        if end_date:
            stmt = stmt.where(DependencyRevision.revised_at <= end_date)
        stmt = stmt.order_by(func.date(DependencyRevision.revised_at))
        result = await db.execute(stmt)
        data = result.all()
        response = [
            {
                "date": str(row.revision_date),
                "total": row.total
            }
            for row in data
        ]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving revisions by date: {str(e)}")

@router.get("/analytics/revisions_by_dependency")
async def get_revisions_by_dependency(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_role)
):
    try:
        from sqlalchemy import func
        stmt = select(
            DependencyRevision.dependency_id,
            func.count().label("total_revisions")
        ).group_by(DependencyRevision.dependency_id).order_by(func.count().desc())
        result = await db.execute(stmt)
        data = result.all()
        response = [
            {
                "dependency_id": row.dependency_id,
                "total_revisions": row.total_revisions
            }
            for row in data
        ]
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving revisions by dependency: {str(e)}")

@router.post("/bulk_update")
async def bulk_update_revisions(
    revision_ids: List[int],
    data: DependencyRevisionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_role)
):
    try:
        if not revision_ids:
            raise HTTPException(status_code=400, detail="No revision IDs provided")
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        updated_count = 0
        for revision_id in revision_ids:
            revision = await db.get(DependencyRevision, revision_id)
            if revision:
                for field, value in update_data.items():
                    setattr(revision, field, value)
                revision.revised_at = datetime.now(timezone.utc)
                updated_count += 1
        await db.commit()
        return {
            "detail": f"Successfully updated {updated_count} revisions",
            "updated_count": updated_count,
            "total_requested": len(revision_ids)
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error in bulk update: {str(e)}")

@router.post("/upload_multiple_files/{id}")
async def upload_multiple_files(
    id: int,
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        revision = await db.get(DependencyRevision, id)
        if not revision:
            raise HTTPException(status_code=404, detail="Dependency revision not found")
        saved_files = []
        upload_dir = f"files/dependency_revisions/{id}"
        os.makedirs(upload_dir, exist_ok=True)
        for file in files:
            if file.size > 10 * 1024 * 1024:
                raise HTTPException(status_code=413, detail=f"File {file.filename} too large (max 10MB)")
            file_location = os.path.join(upload_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
            with open(file_location, "wb") as file_object:
                content = await file.read()
                file_object.write(content)
            saved_files.append(file_location)
        revision.file_path = ";".join(saved_files)
        await db.commit()
        await db.refresh(revision)
        try:
            frontend_url = os.getenv("APP_FRONT", "http://localhost:3000")
            portal_url = os.getenv("PORTAL_URL", frontend_url)
            html_content = render_email_template("dependency_revision_file_upload.html", {
                "folio": f"REV-{id}",
                "revision_id": id,
                "user_email": current_user.email if hasattr(current_user, 'email') else "system@visorurbano.com",
                "uploaded_at": datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S"),
                "file_name": f"{len(saved_files)} files uploaded",
                "current_year": datetime.now().year,
                "portal_url": portal_url
            })
            user_email = current_user.email if hasattr(current_user, 'email') else "system@visorurbano.com"
            send_email(user_email, f"Multiple files uploaded for revision {id}", html_content)
            logger.info(f"Multiple files upload notification email sent to: {user_email}")
        except Exception as e:
            logger.error(f"Failed to send multiple files upload notification email: {str(e)}")
        return {
            "detail": f"Successfully uploaded {len(saved_files)} files",
            "files": [os.path.basename(f) for f in saved_files],
            "revision_id": id
        }
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")

@router.delete("/delete_file/{id}")
async def delete_revision_file(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        revision = await db.get(DependencyRevision, id)
        if not revision:
            raise HTTPException(status_code=404, detail="Dependency revision not found")
        if revision.file_path:
            file_paths = revision.file_path.split(";")
            deleted_files = []
            for file_path in file_paths:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_files.append(os.path.basename(file_path))
            revision.file_path = None
            await db.commit()
            await db.refresh(revision)
            return {
                "detail": f"Successfully deleted {len(deleted_files)} files",
                "deleted_files": deleted_files
            }
        else:
            raise HTTPException(status_code=404, detail="No files found for this revision")
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting files: {str(e)}")
