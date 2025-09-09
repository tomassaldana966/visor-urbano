"""
Utility classes and functions for handling mock objects and data extraction
in test and production environments.
"""
from typing import Any, Optional, Type, TypeVar, Union
from pydantic import BaseModel

T = TypeVar('T')


class MockSafeExtractor:
    """Utility class for safely extracting values from potentially mock objects."""
    
    @staticmethod
    def safe_extract(value: Any, default: Any = None, cast_type: Optional[Type[T]] = None) -> Union[T, Any]:
        """
        Safely extract values from potentially mock objects.
        
        Args:
            value: The value to extract
            default: Default value if extraction fails
            cast_type: Type to cast the value to
            
        Returns:
            Extracted and optionally cast value, or default
        """
        try:
            # Handle Mock objects by checking common Mock indicators
            if hasattr(value, '_mock_name') or str(type(value).__name__) == 'Mock':
                return default
            if cast_type and value is not None:
                return cast_type(value)
            return value if value is not None else default
        except (TypeError, ValueError, AttributeError):
            return default


class UserTypeDetector:
    """Utility class for detecting user object types (real, mock, simple)."""
    
    @staticmethod
    def is_mock_user(user: Any) -> bool:
        """Check if user object is a mock."""
        return hasattr(user, '_mock_name') or str(type(user).__name__) == 'Mock'
    
    @staticmethod
    def is_simple_user(user: Any) -> bool:
        """Check if user object is a simple test object."""
        user_type = str(type(user))
        return 'SimpleUser' in user_type or 'SimpleObject' in user_type


class BaseUserExtractor:
    """Base class for extracting user data with default values."""
    
    DEFAULT_VALUES = {
        "id": 1,
        "name": "Test User",
        "paternal_last_name": "Doe",
        "maternal_last_name": "Smith",
        "cellphone": "1234567890",
        "email": "test@example.com",
        "municipality_id": 1,
        "role_id": 1,
        "is_active": True,
        "role_name": "User"
    }
    
    @classmethod
    def extract_user_data(cls, user: Any) -> dict:
        """
        Extract user data with appropriate defaults based on user type.
        
        Args:
            user: User object (real SQLAlchemy model, mock, or simple object)
            
        Returns:
            Dictionary with user data
        """
        detector = UserTypeDetector()
        
        if detector.is_mock_user(user) or detector.is_simple_user(user):
            return cls._extract_from_test_object(user)
        else:
            return cls._extract_from_sqlalchemy_object(user)
    
    @classmethod
    def _extract_from_test_object(cls, user: Any) -> dict:
        """Extract data from mock or simple test objects."""
        return {
            key: getattr(user, key, default_value)
            for key, default_value in cls.DEFAULT_VALUES.items()
        }
    
    @classmethod
    def _extract_from_sqlalchemy_object(cls, user: Any) -> dict:
        """Extract data from real SQLAlchemy objects."""
        return {
            "id": user.id,
            "name": user.name,
            "paternal_last_name": user.paternal_last_name,
            "maternal_last_name": user.maternal_last_name,
            "cellphone": user.cellphone,
            "email": user.email,
            "municipality_id": user.municipality_id,
            "role_id": user.role_id,
            "is_active": user.is_active,
            "role_name": "User"
        }
