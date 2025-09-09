from fastapi import APIRouter

from app.routers.users import users as users_router
from app.routers.user_roles import user_roles
from app.routers.municipality import municipalities
from app.routers.auth import auth
from app.routers.procedures import procedures
from app.routers.sub_roles import sub_roles
from app.routers.system import router as system_router
from app.routers.technical_sheets import router as technical_sheets_router
from app.routers.blog import router as blog_router, news_router
from app.routers.geocode import router as geocode_router
from app.routers.reports import router as reports_router
from app.routers.commercial import router as commercial_router
from app.routers.business_licenses import router as business_licenses
from app.routers.technical_sheet_downloads import router as technical_sheet_downloads_router
from app.routers.zoning_control_regulations  import router as zoning_control_regulations
from app.routers.procedure_registrations import router as procedure_registrations_router
from app.routers.map_layers import router as map_layers_router
from app.routers.business_types import router as business_types_router
from app.routers.zoning_impact_levels import router as zoning_impact_levels_router
from app.routers.public_fields import router as public_fields_router
from app.routers.business_license_histories import router as business_license_histories_router
from app.routers.provisional_openings import router as provisional_openings_router
from app.routers.dependency_reviews import router as dependency_reviews_router
from app.routers.dependency_resolutions import router as dependency_resolutions_router
from app.routers.password import router as password_router
from app.routers.business_signatures import router as business_signatures_router
from app.routers.business_line_log import router as business_line_log_router
from app.routers.requirements_queries import router as requirements_queries_router
from app.routers.dependency_revisions import router as dependency_revisions_router
from app.routers.requirements import requirements as requirements_router
from app.routers.notifications import router as notifications_router
from app.routers.business_commercial_procedures import router as business_commercial_procedures_router
from app.routers.construction_procedures import router as construction_procedures_router
from app.routers.director import router as director_router
from app.routers.director_departments import router as director_departments_router
from app.routers.procedures_workflow import router as procedures_workflow_router
from app.routers.submit_procedures import router as submit_procedures

api_v1 = APIRouter()

api_v1.include_router(users_router, prefix="/users", tags=["Users"])
api_v1.include_router(user_roles, prefix="/roles", tags=["User Roles"])
api_v1.include_router(municipalities, prefix="/municipalities", tags=["Municipalities"])
api_v1.include_router(auth, prefix="/auth", tags=["Auth"])
api_v1.include_router(procedures, prefix='/procedures', tags=['Procedures'])
api_v1.include_router(submit_procedures, prefix='/submit_procedures', tags=['Submit Procedures'])
api_v1.include_router(sub_roles, prefix="/sub_roles", tags=["Sub Roles"])
api_v1.include_router(system_router, prefix="/system", tags=["System"])
api_v1.include_router(technical_sheets_router, prefix='/technical_sheets', tags=["Technical Sheets"])
api_v1.include_router(commercial_router, tags=["Commercial"])
api_v1.include_router(business_licenses, prefix='/business_licenses', tags=["Business Licenses"])
api_v1.include_router(technical_sheet_downloads_router,  prefix="/technical_sheet_downloads", tags=["Technical Sheet Downloads"])
api_v1.include_router(zoning_control_regulations, prefix="/zoning_control_regulations", tags=["Zoning Control Regulations"])
api_v1.include_router(procedure_registrations_router, prefix="/procedure_registrations", tags=["Procedure Registrations"])
api_v1.include_router(map_layers_router, prefix="/map_layers", tags=["Map Layers"])
api_v1.include_router(business_types_router, prefix="/business_types", tags=["Business Types"])
api_v1.include_router(zoning_impact_levels_router, prefix="/zoning_impact_levels", tags=["Zoning Impact Levels"])
api_v1.include_router(public_fields_router, prefix="/fields", tags=["Public Fields"])
api_v1.include_router(business_license_histories_router, prefix="/business_license_histories", tags=["Business License Histories"])
api_v1.include_router(provisional_openings_router, prefix="/provisional_openings", tags=["Provisional Openings"])
api_v1.include_router(business_line_log_router, prefix="/business_line_log", tags=["Business Line Log"])
api_v1.include_router(dependency_reviews_router, tags=["Dependency Reviews"])
api_v1.include_router(dependency_resolutions_router, tags=["Dependency Resolutions"])
api_v1.include_router(dependency_revisions_router, tags=["Dependency Revisions"])
api_v1.include_router(blog_router, tags=["Blog"])
api_v1.include_router(news_router, tags=["News"])  # Add news router
api_v1.include_router(geocode_router, tags=["Geocode"])
api_v1.include_router(reports_router, tags=["Reports"])
api_v1.include_router(password_router, tags=["Password"])
api_v1.include_router(business_signatures_router, prefix="/business_signatures", tags=["Business Signatures"])
api_v1.include_router(requirements_router, prefix="/requirements", tags=["Requirements"])
api_v1.include_router(requirements_queries_router, prefix="/requirements-queries", tags=["Requirements Queries"])
api_v1.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])
api_v1.include_router(business_commercial_procedures_router, prefix="/business_commercial_procedures", tags=["Business Commercial Procedures"])
api_v1.include_router(construction_procedures_router, prefix="/construction_procedures", tags=["Construction Procedures"])
api_v1.include_router(director_router, prefix="/director", tags=["Director Analytics"])
api_v1.include_router(director_departments_router, tags=["Director - Department Management"])
api_v1.include_router(procedures_workflow_router, prefix="/procedure-workflow", tags=["Procedures Workflow"])
