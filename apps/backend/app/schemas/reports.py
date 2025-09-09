from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class ChartPoint(BaseModel):
    name: str
    value: int
    extra: Optional[int] = None

class LicensingStatusSummary(BaseModel):
    consultation: int
    initiated: int
    under_review: int
    issued: int
    
class BarListFilter(BaseModel):
    month: int
    start_date: date
    end_date: date
    municipality_id: Optional[int] = None  

class BarListItem(BaseModel):
    folio: str
    street: str
    neighborhood: str
    scian_code: str
    scian_name: str
    number_license: Optional[str]
    owner: Optional[str]
    license_year: Optional[str]
    
class ReviewStatusSummary(BaseModel):
    approved: int
    under_review: int
    corrected: int
    discarded: int
    
class MunicipalityPiePoint(BaseModel):
    name: str  
    value: int
    extra: int  

class MunicipalityLicenseSummary(BaseModel):
    id: int
    name: str
    total_refrendo: int
    total_nueva: int
    total_final: int

class MunicipalityHistoricSummary(BaseModel):
    id: int
    name: str
    total: int

class FullReportResponse(BaseModel):
    total_current: int
    total_refrendo_current: int
    total_nueva_current: int
    total_historic: int
    total_combined: int
    current_by_municipality: List[MunicipalityLicenseSummary]
    historic_by_municipality: List[MunicipalityHistoricSummary]
    
class TechnicalSheetDownload(BaseModel):
    id: int
    name: str
    email: str
    age: int
    city: str
    sector: str
    uses: List[str]
    address: str
    municipality: str
    created_at: datetime

class TechnicalSheetReportSummary(BaseModel):
    sectors_percentage: dict
    uses_percentage: dict
    age_distribution: dict
    top_cities: dict
    users_per_municipality: dict
    data: List[TechnicalSheetDownload]

# New schemas for calculated analytics data
class KPIsSummary(BaseModel):
    tiempo_promedio: float
    eficiencia: float
    total_procesados: int
    satisfaccion: float

class StatusDistribution(BaseModel):
    estado: str
    cantidad: int
    porcentaje: float
    color: str

class DependencyMetrics(BaseModel):
    id: str
    nombre: str
    tramites_procesados: int
    tiempo_promedio: float
    eficiencia: float
    estado: str

class CompleteAnalytics(BaseModel):
    kpis: KPIsSummary
    tendencias: List[ChartPoint]
    distribucion_estados: List[StatusDistribution]
    dependencias: List[DependencyMetrics]
    licensing_status: LicensingStatusSummary
    review_status: ReviewStatusSummary