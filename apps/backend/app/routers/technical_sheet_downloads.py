from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import app.models.technical_sheet_downloads as model_module
from app.schemas.technical_sheet_downloads import TechnicalSheetDownloadCreate, TechnicalSheetDownloadResponse
from config.settings import get_db
import json

router = APIRouter()

@router.post("/", response_model=TechnicalSheetDownloadResponse)
async def create_technical_sheet_download(data: TechnicalSheetDownloadCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_download = model_module.TechnicalSheetDownload(
            city=data.city,
            email=data.email,
            age=data.age,
            name=data.name,
            sector=data.sector,
            uses=json.dumps(data.uses), 
            municipality_id=data.municipality_id,
            address=data.address
        )
        db.add(new_download)
        await db.commit()
        await db.refresh(new_download)

        return {"id": new_download.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
