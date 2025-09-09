import pytest
import base64
import json
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.requirements_queries import RequirementsQueriesService
from app.models.requirements_query import RequirementsQuery
from app.models.procedures import Procedure
from app.schemas.requirements_queries import (
    ProcedureInfoSchema,
    ProcedureTypeInfoSchema,
    ProcedureRenewalInfoSchema,
    RequirementsQueryCreateSchema,
)


class TestRequirementsQueriesService:
    """Test cases for RequirementsQueriesService."""

    @pytest.fixture
    def mock_db_session(self):
        """Create a mock database session."""
        return AsyncMock(spec=AsyncSession)

    @pytest.fixture
    def sample_requirements_query(self):
        """Create a sample requirements query."""
        query = Mock(spec=RequirementsQuery)
        query.id = 1
        query.folio = "TEST-001"
        query.street = "Main Street 123"
        query.neighborhood = "Downtown"
        query.municipality_name = "Test City"
        query.scian_code = "123456"
        query.scian_name = "Test Commercial Activity"
        query.property_area = 100.5
        query.activity_area = 75.2
        query.applicant_name = "John Doe"
        query.status = 1
        query.alcohol_sales = 0
        query.primary_folio = "PRIMARY-001"
        query.created_at = datetime(2025, 6, 14, 12, 0, 0)
        query.renewals = []
        return query

    @pytest.fixture
    def sample_procedure(self):
        """Create a sample procedure."""
        procedure = Mock(spec=Procedure)
        procedure.id = 1
        procedure.name = "Test Procedure"
        procedure.status = "active"
        procedure.requirements = ["Requirement 1", "Requirement 2"]
        return procedure

    @pytest.mark.asyncio
    async def test_get_procedure_info_success(self, mock_db_session, sample_requirements_query, sample_procedure):
        """Test successful procedure info retrieval."""
        # Mock database queries
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        # Mock procedures query
        mock_proc_result = Mock()
        mock_proc_result.scalars.return_value.all.return_value = [sample_procedure]
        mock_db_session.execute.side_effect = [mock_result, mock_proc_result]
        
        result = await RequirementsQueriesService.get_procedure_info("TEST-001", mock_db_session)
        
        assert isinstance(result, ProcedureInfoSchema)
        assert result.folio == "TEST-001"
        assert result.status == "active"
        assert result.procedure_data["folio"] == "TEST-001"
        assert result.procedure_data["street"] == "Main Street 123"
        assert result.procedure_data["property_area"] == 100.5
        assert len(result.requirements) == 1
        assert result.requirements[0]["name"] == "Test Procedure"

    @pytest.mark.asyncio
    async def test_get_procedure_info_not_found(self, mock_db_session):
        """Test procedure info retrieval when folio not found."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        with pytest.raises(HTTPException) as exc_info:
            await RequirementsQueriesService.get_procedure_info("NONEXISTENT", mock_db_session)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_procedure_info_database_error(self, mock_db_session):
        """Test procedure info retrieval with database error."""
        mock_db_session.execute.side_effect = Exception("Database connection failed")
        
        with pytest.raises(HTTPException) as exc_info:
            await RequirementsQueriesService.get_procedure_info("TEST-001", mock_db_session)
        
        assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Internal server error" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_procedure_type_standard(self, mock_db_session, sample_requirements_query):
        """Test procedure type retrieval for standard procedure."""
        sample_requirements_query.alcohol_sales = 0
        sample_requirements_query.scian_name = "Retail Food Service"
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        result = await RequirementsQueriesService.get_procedure_info_type("TEST-001", mock_db_session)
        
        assert isinstance(result, ProcedureTypeInfoSchema)
        assert result.folio == "TEST-001"
        assert result.procedure_type == "standard"
        assert result.type_data["type"] == "standard"
        assert result.type_data["alcohol_sales"] == 0

    @pytest.mark.asyncio
    async def test_get_procedure_type_alcohol_sales(self, mock_db_session, sample_requirements_query):
        """Test procedure type retrieval for alcohol sales procedure."""
        sample_requirements_query.alcohol_sales = 1
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        result = await RequirementsQueriesService.get_procedure_info_type("TEST-001", mock_db_session)
        
        assert result.procedure_type == "alcohol_sales"
        assert result.type_data["type"] == "alcohol_sales"
        assert result.type_data["alcohol_sales"] == 1

    @pytest.mark.asyncio
    async def test_get_procedure_type_industrial(self, mock_db_session, sample_requirements_query):
        """Test procedure type retrieval for industrial procedure."""
        sample_requirements_query.alcohol_sales = 0
        sample_requirements_query.scian_name = "Industrial Manufacturing Activity"
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        result = await RequirementsQueriesService.get_procedure_info_type("TEST-001", mock_db_session)
        
        assert result.procedure_type == "industrial"
        assert result.type_data["type"] == "industrial"

    @pytest.mark.asyncio
    async def test_get_procedure_type_commercial(self, mock_db_session, sample_requirements_query):
        """Test procedure type retrieval for commercial procedure."""
        sample_requirements_query.alcohol_sales = 0
        sample_requirements_query.scian_name = "Commercial Retail Activity"
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        result = await RequirementsQueriesService.get_procedure_info_type("TEST-001", mock_db_session)
        
        assert result.procedure_type == "commercial"
        assert result.type_data["type"] == "commercial"

    @pytest.mark.asyncio
    async def test_get_procedure_renewal_info_success(self, mock_db_session, sample_requirements_query):
        """Test successful procedure renewal info retrieval."""
        # Mock renewal data
        mock_renewal = Mock()
        mock_renewal.id = 1
        mock_renewal.procedure_id = 123
        mock_renewal.created_at = datetime(2025, 6, 10, 10, 0, 0)
        sample_requirements_query.renewals = [mock_renewal]
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        result = await RequirementsQueriesService.get_procedure_info_renewal("TEST-001", mock_db_session)
        
        assert isinstance(result, ProcedureRenewalInfoSchema)
        assert result.folio == "TEST-001"
        assert result.renewal_data["original_folio"] == "TEST-001"
        assert result.renewal_data["primary_folio"] == "PRIMARY-001"
        assert result.renewal_data["renewals_count"] == 1
        assert len(result.renewal_data["renewals"]) == 1
        assert len(result.renewal_requirements) == 3

    @pytest.mark.asyncio
    async def test_get_procedure_renewal_info_no_renewals(self, mock_db_session, sample_requirements_query):
        """Test procedure renewal info retrieval with no renewals."""
        sample_requirements_query.renewals = []
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        result = await RequirementsQueriesService.get_procedure_info_renewal("TEST-001", mock_db_session)
        
        assert result.renewal_data["renewals_count"] == 0
        assert len(result.renewal_data["renewals"]) == 0

    @pytest.mark.asyncio
    async def test_get_procedure_renewal_info_not_found(self, mock_db_session):
        """Test procedure renewal info retrieval when folio not found."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        with pytest.raises(HTTPException) as exc_info:
            await RequirementsQueriesService.get_procedure_info_renewal("NONEXISTENT", mock_db_session)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_inactive_procedure_status(self, mock_db_session, sample_requirements_query, sample_procedure):
        """Test procedure info with inactive status."""
        sample_requirements_query.status = 0  # Inactive
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        mock_proc_result = Mock()
        mock_proc_result.scalars.return_value.all.return_value = [sample_procedure]
        mock_db_session.execute.side_effect = [mock_result, mock_proc_result]
        
        result = await RequirementsQueriesService.get_procedure_info("TEST-001", mock_db_session)
        
        assert result.status == "inactive"

    @pytest.mark.asyncio
    async def test_procedure_with_no_requirements(self, mock_db_session, sample_requirements_query):
        """Test procedure info with no associated procedures."""
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        mock_proc_result = Mock()
        mock_proc_result.scalars.return_value.all.return_value = []
        mock_db_session.execute.side_effect = [mock_result, mock_proc_result]
        
        result = await RequirementsQueriesService.get_procedure_info("TEST-001", mock_db_session)
        
        assert len(result.requirements) == 0

    @pytest.mark.asyncio
    async def test_procedure_with_none_created_at(self, mock_db_session, sample_requirements_query, sample_procedure):
        """Test procedure info with None created_at."""
        sample_requirements_query.created_at = None
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        mock_proc_result = Mock()
        mock_proc_result.scalars.return_value.all.return_value = [sample_procedure]
        mock_db_session.execute.side_effect = [mock_result, mock_proc_result]
        
        result = await RequirementsQueriesService.get_procedure_info("TEST-001", mock_db_session)
        
        assert result.procedure_data["created_at"] is None

    @pytest.mark.asyncio
    async def test_renewal_with_no_procedure_id(self, mock_db_session, sample_requirements_query):
        """Test renewal info with renewal having no procedure_id."""
        mock_renewal = Mock()
        mock_renewal.id = 1
        mock_renewal.procedure_id = None
        mock_renewal.created_at = datetime(2025, 6, 10, 10, 0, 0)
        sample_requirements_query.renewals = [mock_renewal]
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = sample_requirements_query
        mock_db_session.execute.return_value = mock_result
        
        result = await RequirementsQueriesService.get_procedure_info_renewal("TEST-001", mock_db_session)
        
        renewal = result.renewal_data["renewals"][0]
        assert renewal["notes"] == "General renewal"


if __name__ == "__main__":
    pytest.main([__file__])
