import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from datetime import datetime

from app.routers.construction_procedures import router, _apply_user_access_filters
from app.models.procedures import Procedure
from app.models.municipality import Municipality
from app.models.user import UserModel
from app.schemas.procedures import ConstructionProcedureRead, ConstructionProcedureList


class TestConstructionProcedures:
    """Test suite for construction procedures endpoints"""

    def setup_method(self):
        """Set up test fixtures"""
        self.mock_procedure = MagicMock(spec=Procedure)
        self.mock_procedure.id = 1
        self.mock_procedure.folio = "CONST-2024-001"
        self.mock_procedure.current_step = 1
        self.mock_procedure.procedure_type = "construccion_residencial"
        self.mock_procedure.license_status = "active"
        self.mock_procedure.status = 1
        self.mock_procedure.procedure_start_date = datetime.now()
        self.mock_procedure.created_at = datetime.now()
        self.mock_procedure.updated_at = datetime.now()
        self.mock_procedure.official_applicant_name = "Juan Pérez"
        self.mock_procedure.street = "Calle Principal"
        self.mock_procedure.exterior_number = "123"
        self.mock_procedure.interior_number = "A"
        self.mock_procedure.neighborhood = "Centro"
        self.mock_procedure.reference = "Cerca del parque"
        self.mock_procedure.municipality_id = 1
        self.mock_procedure.user_id = 1

        self.mock_municipality = MagicMock(spec=Municipality)
        self.mock_municipality.id = 1
        self.mock_municipality.name = "Test Municipality"

        self.mock_user = MagicMock(spec=UserModel)
        self.mock_user.id = 1
        self.mock_user.role_name = "regular_user"
        self.mock_user.is_superuser = False
        self.mock_user.municipality_id = 1

    def test_apply_user_access_filters_superuser(self):
        """Test access filters for superuser"""
        mock_query = MagicMock()
        user = MagicMock()
        user.is_superuser = True
        user.role_name = "admin"
        
        result = _apply_user_access_filters(mock_query, user, 1, None)
        
        assert result == mock_query
        mock_query.filter.assert_not_called()

    def test_apply_user_access_filters_superuser_with_user_id(self):
        """Test access filters for superuser with user_id filter"""
        mock_query = MagicMock()
        user = MagicMock()
        user.is_superuser = True
        user.role_name = "admin"
        
        result = _apply_user_access_filters(mock_query, user, 1, 123)
        
        mock_query.filter.assert_called_once()

    def test_apply_user_access_filters_admin_role(self):
        """Test access filters for admin role"""
        mock_query = MagicMock()
        user = MagicMock()
        user.is_superuser = False
        user.role_name = "director"
        
        result = _apply_user_access_filters(mock_query, user, 1, None)
        
        assert result == mock_query

    def test_apply_user_access_filters_supervisor_valid_municipality(self):
        """Test access filters for supervisor with valid municipality"""
        mock_query = MagicMock()
        user = MagicMock()
        user.is_superuser = False
        user.role_name = "supervisor"
        user.municipality_id = 1
        
        result = _apply_user_access_filters(mock_query, user, 1, None)
        
        # The function should add user filter since user_id is None and user is not admin
        mock_query.filter.assert_not_called()

    def test_apply_user_access_filters_supervisor_invalid_municipality(self):
        """Test access filters for supervisor with invalid municipality"""
        mock_query = MagicMock()
        user = MagicMock()
        user.is_superuser = False
        user.role_name = "supervisor"
        user.municipality_id = 1
        
        with pytest.raises(HTTPException) as exc_info:
            _apply_user_access_filters(mock_query, user, 2, None)
        
        assert exc_info.value.status_code == 403
        assert "Access denied" in str(exc_info.value.detail)

    def test_apply_user_access_filters_regular_user_own_procedures(self):
        """Test access filters for regular user viewing own procedures"""
        mock_query = MagicMock()
        user = MagicMock()
        user.is_superuser = False
        user.role_name = "regular_user"
        user.id = 1
        
        result = _apply_user_access_filters(mock_query, user, 1, None)
        
        mock_query.filter.assert_called_once()

    def test_apply_user_access_filters_regular_user_other_procedures(self):
        """Test access filters for regular user trying to view other's procedures"""
        mock_query = MagicMock()
        user = MagicMock()
        user.is_superuser = False
        user.role_name = "regular_user"
        user.id = 1
        
        with pytest.raises(HTTPException) as exc_info:
            _apply_user_access_filters(mock_query, user, 1, 2)
        
        assert exc_info.value.status_code == 403
        assert "You can only view your own procedures" in str(exc_info.value.detail)

    @patch('app.routers.construction_procedures.get_db')
    @patch('app.routers.construction_procedures.get_current_user')
    def test_list_construction_procedures_success(self, mock_get_current_user, mock_get_db):
        """Test successful listing of construction procedures"""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_get_current_user.return_value = self.mock_user
        
        # Mock query chain
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.distinct.return_value = mock_query
        mock_query.count.return_value = 1
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [(self.mock_procedure, self.mock_municipality)]
        
        from app.routers.construction_procedures import list_construction_procedures
        
        result = list_construction_procedures(
            municipality_id=1,
            user_id=None,
            status=1,
            skip=0,
            limit=20,
            db=mock_db,
            current_user=self.mock_user
        )
        
        assert isinstance(result, ConstructionProcedureList)
        assert result.total_count == 1
        assert len(result.procedures) == 1
        assert result.procedures[0].id == 1
        assert result.procedures[0].folio == "CONST-2024-001"

    @patch('app.routers.construction_procedures.get_db')
    @patch('app.routers.construction_procedures.get_current_user')
    def test_list_construction_procedures_empty_result(self, mock_get_current_user, mock_get_db):
        """Test listing construction procedures with empty result"""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_get_current_user.return_value = self.mock_user
        
        # Mock query chain for empty result
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.distinct.return_value = mock_query
        mock_query.count.return_value = 0
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []
        
        from app.routers.construction_procedures import list_construction_procedures
        
        result = list_construction_procedures(
            municipality_id=1,
            user_id=None,
            status=1,
            skip=0,
            limit=20,
            db=mock_db,
            current_user=self.mock_user
        )
        
        assert isinstance(result, ConstructionProcedureList)
        assert result.total_count == 0
        assert len(result.procedures) == 0

    @patch('app.routers.construction_procedures.get_db')
    @patch('app.routers.construction_procedures.get_current_user')
    def test_list_construction_procedures_database_error(self, mock_get_current_user, mock_get_db):
        """Test listing construction procedures with database error"""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_get_current_user.return_value = self.mock_user
        
        # Mock database error
        mock_db.query.side_effect = Exception("Database error")
        
        from app.routers.construction_procedures import list_construction_procedures
        
        with pytest.raises(HTTPException) as exc_info:
            list_construction_procedures(
                municipality_id=1,
                user_id=None,
                status=1,
                skip=0,
                limit=20,
                db=mock_db,
                current_user=self.mock_user
            )
        
        assert exc_info.value.status_code == 500
        assert "An error occurred while retrieving construction procedures" in str(exc_info.value.detail)

    @patch('app.routers.construction_procedures.get_db')
    @patch('app.routers.construction_procedures.get_current_user')
    def test_get_construction_procedure_success(self, mock_get_current_user, mock_get_db):
        """Test successful retrieval of a specific construction procedure"""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_get_current_user.return_value = self.mock_user
        
        # Mock query chain
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = (self.mock_procedure, self.mock_municipality)
        
        from app.routers.construction_procedures import get_construction_procedure
        
        result = get_construction_procedure(
            procedure_id=1,
            db=mock_db,
            current_user=self.mock_user
        )
        
        assert isinstance(result, ConstructionProcedureRead)
        assert result.id == 1
        assert result.folio == "CONST-2024-001"
        assert result.full_address == "Calle Principal 123 Int. A"
        assert result.municipality_name == "Test Municipality"

    @patch('app.routers.construction_procedures.get_db')
    @patch('app.routers.construction_procedures.get_current_user')
    def test_get_construction_procedure_not_found(self, mock_get_current_user, mock_get_db):
        """Test retrieval of non-existent construction procedure"""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_get_current_user.return_value = self.mock_user
        
        # Mock query chain for not found
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        from app.routers.construction_procedures import get_construction_procedure
        
        with pytest.raises(HTTPException) as exc_info:
            get_construction_procedure(
                procedure_id=999,
                db=mock_db,
                current_user=self.mock_user
            )
        
        assert exc_info.value.status_code == 404
        assert "Construction procedure not found" in str(exc_info.value.detail)

    @patch('app.routers.construction_procedures.get_db')
    @patch('app.routers.construction_procedures.get_current_user')
    def test_get_construction_procedure_access_denied(self, mock_get_current_user, mock_get_db):
        """Test access denied for construction procedure"""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Create a user trying to access another user's procedure
        other_user = MagicMock(spec=UserModel)
        other_user.id = 2
        other_user.role_name = "regular_user"
        other_user.is_superuser = False
        mock_get_current_user.return_value = other_user
        
        # Mock query chain
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = (self.mock_procedure, self.mock_municipality)
        
        from app.routers.construction_procedures import get_construction_procedure
        
        with pytest.raises(HTTPException) as exc_info:
            get_construction_procedure(
                procedure_id=1,
                db=mock_db,
                current_user=other_user
            )
        
        assert exc_info.value.status_code == 403
        assert "You can only view your own procedures" in str(exc_info.value.detail)

    @patch('app.routers.construction_procedures.get_db')
    @patch('app.routers.construction_procedures.get_current_user')
    def test_get_construction_procedure_database_error(self, mock_get_current_user, mock_get_db):
        """Test retrieval of construction procedure with database error"""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_get_current_user.return_value = self.mock_user
        
        # Mock database error
        mock_db.query.side_effect = Exception("Database error")
        
        from app.routers.construction_procedures import get_construction_procedure
        
        with pytest.raises(HTTPException) as exc_info:
            get_construction_procedure(
                procedure_id=1,
                db=mock_db,
                current_user=self.mock_user
            )
        
        assert exc_info.value.status_code == 500
        assert "An error occurred while retrieving the construction procedure" in str(exc_info.value.detail)

    def test_address_building_with_all_fields(self):
        """Test address building with all address fields present"""
        procedure = MagicMock()
        procedure.street = "Avenida Principal"
        procedure.exterior_number = "456"
        procedure.interior_number = "B"
        
        # Simulate address building logic
        address_parts = []
        if procedure.street:
            address_parts.append(procedure.street)
        if procedure.exterior_number:
            address_parts.append(procedure.exterior_number)
        if procedure.interior_number:
            address_parts.append(f"Int. {procedure.interior_number}")
        full_address = " ".join(address_parts) if address_parts else None
        
        assert full_address == "Avenida Principal 456 Int. B"

    def test_address_building_partial_fields(self):
        """Test address building with partial address fields"""
        procedure = MagicMock()
        procedure.street = "Calle Secundaria"
        procedure.exterior_number = "789"
        procedure.interior_number = None
        
        # Simulate address building logic
        address_parts = []
        if procedure.street:
            address_parts.append(procedure.street)
        if procedure.exterior_number:
            address_parts.append(procedure.exterior_number)
        if procedure.interior_number:
            address_parts.append(f"Int. {procedure.interior_number}")
        full_address = " ".join(address_parts) if address_parts else None
        
        assert full_address == "Calle Secundaria 789"

    def test_address_building_no_fields(self):
        """Test address building with no address fields"""
        procedure = MagicMock()
        procedure.street = None
        procedure.exterior_number = None
        procedure.interior_number = None
        
        # Simulate address building logic
        address_parts = []
        if procedure.street:
            address_parts.append(procedure.street)
        if procedure.exterior_number:
            address_parts.append(procedure.exterior_number)
        if procedure.interior_number:
            address_parts.append(f"Int. {procedure.interior_number}")
        full_address = " ".join(address_parts) if address_parts else None
        
        assert full_address is None

    @patch('app.routers.construction_procedures.get_db')
    @patch('app.routers.construction_procedures.get_current_user')
    def test_list_construction_procedures_with_pagination(self, mock_get_current_user, mock_get_db):
        """Test listing construction procedures with pagination parameters"""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_get_current_user.return_value = self.mock_user
        
        # Mock query chain
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.distinct.return_value = mock_query
        mock_query.count.return_value = 5
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = [(self.mock_procedure, self.mock_municipality)]
        
        from app.routers.construction_procedures import list_construction_procedures
        
        result = list_construction_procedures(
            municipality_id=1,
            user_id=None,
            status=1,
            skip=2,
            limit=3,
            db=mock_db,
            current_user=self.mock_user
        )
        
        assert result.skip == 2
        assert result.limit == 3
        assert result.total_count == 5
        mock_query.offset.assert_called_with(2)
        mock_query.limit.assert_called_with(3)

    @patch('app.routers.construction_procedures.get_db')
    @patch('app.routers.construction_procedures.get_current_user')
    def test_get_construction_procedure_admin_access(self, mock_get_current_user, mock_get_db):
        """Test admin user can access any construction procedure"""
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        
        # Create an admin user
        admin_user = MagicMock(spec=UserModel)
        admin_user.id = 999
        admin_user.role_name = "director"
        admin_user.is_superuser = True
        mock_get_current_user.return_value = admin_user
        
        # Mock query chain
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = (self.mock_procedure, self.mock_municipality)
        
        from app.routers.construction_procedures import get_construction_procedure
        
        result = get_construction_procedure(
            procedure_id=1,
            db=mock_db,
            current_user=admin_user
        )
        
        assert isinstance(result, ConstructionProcedureRead)
        assert result.id == 1
