from pydantic import BaseModel
from typing import List, Optional

class DailyStatistic(BaseModel):
    day: int
    month: int
    year: int
    count: int
    
class TechnicalSheetStatsResponse(BaseModel):
    total: int
    days: List[DailyStatistic]  
    
class MunicipalityStat(BaseModel):
    municipality: str
    sheets: int

class TechnicalSheetsByMunicipalityResponse(BaseModel):
    sheets: List[MunicipalityStat]
    total: int
    
class TechnicalSheetCreate(BaseModel):
    address: str
    square_meters: str
    coordinates: str
    image: str
    municipality_id: int
    technical_sheet_download_id: int

class TechnicalSheetResponse(BaseModel):
    uuid: str