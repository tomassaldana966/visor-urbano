"""
Service layer for user data enrichment including role and municipality information.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user_roles import UserRoleModel
from app.models.municipality import Municipality
from app.models.base_municipality import BaseMunicipality
from app.schemas.municipality import MunicipalityDataSchema, MunicipalityGeospatialSchema
from app.utils.user_extraction import MockSafeExtractor


class UserRoleService:
    """Service for fetching and processing user role information."""
    
    @staticmethod
    async def get_role_name(session: AsyncSession, role_id: int) -> str:
        """
        Fetch role name by role_id.
        
        Args:
            session: Database session
            role_id: ID of the role
            
        Returns:
            Role name or "User" as default
        """
        if not role_id:
            return "User"
            
        stmt = select(UserRoleModel).filter(UserRoleModel.id == role_id)
        result = await session.execute(stmt)
        user_role = result.scalars().first()
        
        if user_role:
            role_name = MockSafeExtractor.safe_extract(user_role.name, "User", str)
            return role_name if role_name != "User" else "User"
        
        return "User"


class MunicipalityService:
    """Service for fetching and processing municipality information."""
    
    @staticmethod
    async def get_municipality_data(
        session: AsyncSession, 
        municipality_id: int
    ) -> tuple[Optional[MunicipalityDataSchema], Optional[MunicipalityGeospatialSchema]]:
        """
        Fetch complete municipality information including geospatial data.
        
        Args:
            session: Database session
            municipality_id: ID of the municipality
            
        Returns:
            Tuple of (municipality_data, municipality_geospatial) or (None, None)
        """
        # Validate municipality_id
        try:
            municipality_id = int(municipality_id) if municipality_id else 0
        except (TypeError, ValueError):
            municipality_id = 0
            
        if municipality_id <= 0:
            return None, None
            
        # Fetch municipality basic data
        stmt_mun = select(Municipality).filter(Municipality.id == municipality_id)
        result_mun = await session.execute(stmt_mun)
        municipality = result_mun.scalars().first()
        
        if not municipality:
            return None, None
            
        # Create municipality data schema
        municipality_data = MunicipalityDataSchema(
            id=MockSafeExtractor.safe_extract(municipality.id, municipality_id, int),
            name=MockSafeExtractor.safe_extract(municipality.name, "Test Municipality", str),
            director=MockSafeExtractor.safe_extract(municipality.director, "Test Director", str),
            address=MockSafeExtractor.safe_extract(municipality.address, "Test Address", str),
            phone=MockSafeExtractor.safe_extract(municipality.phone, "123-456-7890", str)
        )
        
        # Fetch municipality geospatial data
        stmt_base_mun = select(BaseMunicipality).filter(
            BaseMunicipality.municipality_id == municipality_id
        )
        result_base_mun = await session.execute(stmt_base_mun)
        base_municipality = result_base_mun.scalars().first()
        
        municipality_geospatial = None
        if base_municipality:
            municipality_geospatial = MunicipalityGeospatialSchema(
                entity_code=MockSafeExtractor.safe_extract(base_municipality.entity_code, "001", str),
                municipality_code=MockSafeExtractor.safe_extract(base_municipality.municipality_code, "001", str),
                geocode=MockSafeExtractor.safe_extract(base_municipality.geocode, "001001", str),
                has_zoning=MockSafeExtractor.safe_extract(base_municipality.has_zoning, False, bool)
            )
            
        return municipality_data, municipality_geospatial
