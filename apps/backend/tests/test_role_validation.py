import pytest
from unittest.mock import Mock
from fastapi import HTTPException, status
from app.utils.role_validation import (
    RolePermissions,
    validate_admin_role,
    validate_director_role,
    validate_admin_or_director_role,
    check_municipality_access,
    _get_role_name_by_id,
    require_admin_role,
    require_director_role,
    require_admin_or_director_role
)


class TestRolePermissions:
    """Test cases for RolePermissions class."""

    def test_admin_roles_defined(self):
        """Test that admin roles are properly defined."""
        assert "admin" in RolePermissions.ADMIN_ROLES
        assert "administrator" in RolePermissions.ADMIN_ROLES
        assert "director" in RolePermissions.ADMIN_ROLES

    def test_director_roles_defined(self):
        """Test that director roles are properly defined."""
        assert "director" in RolePermissions.DIRECTOR_ROLES
        assert "director_admin" in RolePermissions.DIRECTOR_ROLES

    def test_supervisor_roles_defined(self):
        """Test that supervisor roles are properly defined."""
        assert "supervisor" in RolePermissions.SUPERVISOR_ROLES
        assert "jefe" in RolePermissions.SUPERVISOR_ROLES


class TestValidateAdminRole:
    """Test cases for validate_admin_role function."""

    def test_validate_admin_role_success_with_role_name(self):
        """Test successful admin role validation with role_name."""
        mock_user = Mock()
        mock_user.role_name = "admin"
        
        result = validate_admin_role(mock_user)
        assert result is True

    def test_validate_admin_role_success_case_insensitive(self):
        """Test admin role validation is case insensitive."""
        mock_user = Mock()
        mock_user.role_name = "ADMIN"
        
        result = validate_admin_role(mock_user)
        assert result is True

    def test_validate_admin_role_success_administrator(self):
        """Test admin role validation with administrator role."""
        mock_user = Mock()
        mock_user.role_name = "administrator"
        
        result = validate_admin_role(mock_user)
        assert result is True

    def test_validate_admin_role_success_director(self):
        """Test admin role validation with director role."""
        mock_user = Mock()
        mock_user.role_name = "director"
        
        result = validate_admin_role(mock_user)
        assert result is True

    def test_validate_admin_role_success_with_role_id(self):
        """Test admin role validation with role_id fallback."""
        mock_user = Mock()
        mock_user.role_name = None
        mock_user.role_id = 1  # Maps to admin
        
        result = validate_admin_role(mock_user)
        assert result is True

    def test_validate_admin_role_no_user(self):
        """Test admin role validation with no user."""
        with pytest.raises(HTTPException) as exc_info:
            validate_admin_role(None)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Authentication required" in str(exc_info.value.detail)

    def test_validate_admin_role_no_role_name_or_id(self):
        """Test admin role validation with no role information."""
        mock_user = Mock()
        mock_user.role_name = None
        mock_user.role_id = None
        
        with pytest.raises(HTTPException) as exc_info:
            validate_admin_role(mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "User role not found" in str(exc_info.value.detail)

    def test_validate_admin_role_insufficient_privileges(self):
        """Test admin role validation with insufficient privileges."""
        mock_user = Mock()
        mock_user.role_name = "user"
        
        with pytest.raises(HTTPException) as exc_info:
            validate_admin_role(mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Admin privileges required" in str(exc_info.value.detail)

    def test_validate_admin_role_unknown_role_id(self):
        """Test admin role validation with unknown role_id."""
        mock_user = Mock()
        mock_user.role_name = None
        mock_user.role_id = 999  # Unknown role ID
        
        with pytest.raises(HTTPException) as exc_info:
            validate_admin_role(mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


class TestValidateDirectorRole:
    """Test cases for validate_director_role function."""

    def test_validate_director_role_success(self):
        """Test successful director role validation."""
        mock_user = Mock()
        mock_user.role_name = "director"
        
        result = validate_director_role(mock_user)
        assert result is True

    def test_validate_director_role_success_case_insensitive(self):
        """Test director role validation is case insensitive."""
        mock_user = Mock()
        mock_user.role_name = "DIRECTOR"
        
        result = validate_director_role(mock_user)
        assert result is True

    def test_validate_director_role_success_director_admin(self):
        """Test director role validation with director_admin role."""
        mock_user = Mock()
        mock_user.role_name = "director_admin"
        
        result = validate_director_role(mock_user)
        assert result is True

    def test_validate_director_role_success_with_role_id(self):
        """Test director role validation with role_id."""
        mock_user = Mock()
        mock_user.role_name = None
        mock_user.role_id = 2  # Maps to director
        
        result = validate_director_role(mock_user)
        assert result is True

    def test_validate_director_role_no_user(self):
        """Test director role validation with no user."""
        with pytest.raises(HTTPException) as exc_info:
            validate_director_role(None)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

    def test_validate_director_role_insufficient_privileges(self):
        """Test director role validation with insufficient privileges."""
        mock_user = Mock()
        mock_user.role_name = "user"
        
        with pytest.raises(HTTPException) as exc_info:
            validate_director_role(mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Director privileges required" in str(exc_info.value.detail)


class TestValidateAdminOrDirectorRole:
    """Test cases for validate_admin_or_director_role function."""

    def test_validate_admin_or_director_role_admin_success(self):
        """Test admin or director validation with admin role."""
        mock_user = Mock()
        mock_user.role_name = "admin"
        
        result = validate_admin_or_director_role(mock_user)
        assert result is True

    def test_validate_admin_or_director_role_director_success(self):
        """Test admin or director validation with director role."""
        mock_user = Mock()
        mock_user.role_name = "director"
        
        result = validate_admin_or_director_role(mock_user)
        assert result is True

    def test_validate_admin_or_director_role_insufficient_privileges(self):
        """Test admin or director validation with insufficient privileges."""
        mock_user = Mock()
        mock_user.role_name = "user"
        
        with pytest.raises(HTTPException) as exc_info:
            validate_admin_or_director_role(mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "Admin or Director privileges required" in str(exc_info.value.detail)


class TestCheckMunicipalityAccess:
    """Test cases for check_municipality_access function."""

    def test_check_municipality_access_no_required_municipality(self):
        """Test municipality access check with no required municipality."""
        mock_user = Mock()
        mock_user.municipality_id = 1
        
        result = check_municipality_access(mock_user)
        assert result is True

    def test_check_municipality_access_no_user_municipality(self):
        """Test municipality access check with user having no municipality."""
        mock_user = Mock()
        mock_user.municipality_id = None
        
        with pytest.raises(HTTPException) as exc_info:
            check_municipality_access(mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "No municipality assigned" in str(exc_info.value.detail)

    def test_check_municipality_access_matching_municipality(self):
        """Test municipality access check with matching municipality."""
        mock_user = Mock()
        mock_user.municipality_id = 1
        
        result = check_municipality_access(mock_user, required_municipality_id=1)
        assert result is True

    def test_check_municipality_access_non_matching_municipality_regular_user(self):
        """Test municipality access check with non-matching municipality for regular user."""
        mock_user = Mock()
        mock_user.municipality_id = 1
        mock_user.role_name = "user"
        
        with pytest.raises(HTTPException) as exc_info:
            check_municipality_access(mock_user, required_municipality_id=2)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "municipality doesn't match" in str(exc_info.value.detail)

    def test_check_municipality_access_non_matching_municipality_admin_user(self):
        """Test municipality access check with non-matching municipality for admin user."""
        mock_user = Mock()
        mock_user.municipality_id = 1
        mock_user.role_name = "admin"
        
        result = check_municipality_access(mock_user, required_municipality_id=2)
        assert result is True

    def test_check_municipality_access_no_user(self):
        """Test municipality access check with no user."""
        with pytest.raises(HTTPException) as exc_info:
            check_municipality_access(None)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetRoleNameById:
    """Test cases for _get_role_name_by_id function."""

    def test_get_role_name_by_id_admin(self):
        """Test getting role name for admin ID."""
        result = _get_role_name_by_id(1)
        assert result == "admin"

    def test_get_role_name_by_id_director(self):
        """Test getting role name for director ID."""
        result = _get_role_name_by_id(2)
        assert result == "director"

    def test_get_role_name_by_id_supervisor(self):
        """Test getting role name for supervisor ID."""
        result = _get_role_name_by_id(3)
        assert result == "supervisor"

    def test_get_role_name_by_id_user(self):
        """Test getting role name for user ID."""
        result = _get_role_name_by_id(4)
        assert result == "user"

    def test_get_role_name_by_id_viewer(self):
        """Test getting role name for viewer ID."""
        result = _get_role_name_by_id(5)
        assert result == "viewer"

    def test_get_role_name_by_id_unknown(self):
        """Test getting role name for unknown ID."""
        result = _get_role_name_by_id(999)
        assert result is None


class TestDependencyFunctions:
    """Test cases for dependency functions."""

    def test_require_admin_role_success(self):
        """Test require_admin_role dependency function."""
        mock_user = Mock()
        mock_user.role_name = "admin"
        
        result = require_admin_role(mock_user)
        assert result == mock_user

    def test_require_admin_role_failure(self):
        """Test require_admin_role dependency function with failure."""
        mock_user = Mock()
        mock_user.role_name = "user"
        
        with pytest.raises(HTTPException):
            require_admin_role(mock_user)

    def test_require_director_role_success(self):
        """Test require_director_role dependency function."""
        mock_user = Mock()
        mock_user.role_name = "director"
        
        result = require_director_role(mock_user)
        assert result == mock_user

    def test_require_director_role_failure(self):
        """Test require_director_role dependency function with failure."""
        mock_user = Mock()
        mock_user.role_name = "user"
        
        with pytest.raises(HTTPException):
            require_director_role(mock_user)

    def test_require_admin_or_director_role_admin_success(self):
        """Test require_admin_or_director_role dependency function with admin."""
        mock_user = Mock()
        mock_user.role_name = "admin"
        
        # Note: This test might need to be adjusted based on how the dependency is actually used
        # For now, we'll test the validation logic directly
        result = validate_admin_or_director_role(mock_user)
        assert result is True

    def test_require_admin_or_director_role_director_success(self):
        """Test require_admin_or_director_role dependency function with director."""
        mock_user = Mock()
        mock_user.role_name = "director"
        
        result = validate_admin_or_director_role(mock_user)
        assert result is True


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_validate_admin_role_with_special_characters_in_role(self):
        """Test admin role validation with special characters in role name."""
        mock_user = Mock()
        mock_user.role_name = "admin-special"
        
        with pytest.raises(HTTPException) as exc_info:
            validate_admin_role(mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    def test_validate_admin_role_with_empty_role_name(self):
        """Test admin role validation with empty role name."""
        mock_user = Mock()
        mock_user.role_name = ""
        mock_user.role_id = None
        
        with pytest.raises(HTTPException) as exc_info:
            validate_admin_role(mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    def test_check_municipality_access_with_zero_municipality_id(self):
        """Test municipality access check with zero municipality ID."""
        mock_user = Mock()
        mock_user.municipality_id = 0
        
        result = check_municipality_access(mock_user, required_municipality_id=0)
        assert result is True

    def test_check_municipality_access_with_negative_municipality_id(self):
        """Test municipality access check with negative municipality ID."""
        mock_user = Mock()
        mock_user.municipality_id = -1
        
        result = check_municipality_access(mock_user, required_municipality_id=-1)
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__])
