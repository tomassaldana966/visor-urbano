"""
Comprehensive test configuration for requirements queries.
Sets up test models and fixtures specific to requirements queries functionality.
"""
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
app_dir = backend_dir / "app"
sys.path.insert(0, str(app_dir))

import pytest
import pytest_asyncio
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean, Text, BigInteger, ForeignKey, Numeric, JSON
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Any


# Create test metadata for requirements queries
requirements_metadata = MetaData()

# Test table definitions specific to requirements queries
requirements_querys_test_table = Table(
    'requirements_querys',
    requirements_metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('folio', String(255), nullable=True),
    Column('street', String(100), nullable=False),
    Column('neighborhood', String(100), nullable=False),
    Column('municipality_name', String(50), nullable=False),
    Column('municipality_id', Integer, ForeignKey('municipalities.id'), nullable=False),
    Column('scian_code', String(100), nullable=False),
    Column('scian_name', String(100), nullable=False),
    Column('property_area', Numeric(8, 2), nullable=False, default=0),
    Column('activity_area', Numeric(8, 2), nullable=False, default=0),
    Column('applicant_name', String(100), nullable=True),
    Column('applicant_character', String(100), nullable=True),
    Column('person_type', String(100), nullable=True),
    Column('minimap_url', Text, nullable=True),
    Column('restrictions', JSON, nullable=True),
    Column('status', Integer, nullable=False, default=1),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False, default=0),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
    Column('year_folio', Integer, nullable=False, default=1),
    Column('alcohol_sales', Integer, nullable=False, default=0),
    Column('primary_folio', String(255), nullable=True),
)

procedures_test_table = Table(
    'procedures',
    requirements_metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('folio', String(255), nullable=True),
    Column('name', String(255), nullable=False),
    Column('status', Integer, nullable=False, default=1),
    Column('requirements', JSON, nullable=True),
    Column('requirements_query_id', Integer, ForeignKey('requirements_querys.id'), nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

permit_renewals_test_table = Table(
    'permit_renewals',
    requirements_metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('requirements_query_id', Integer, ForeignKey('requirements_querys.id'), nullable=True),
    Column('procedure_id', Integer, ForeignKey('procedures.id'), nullable=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

municipalities_test_table = Table(
    'municipalities',
    requirements_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(250), nullable=False),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)

users_test_table = Table(
    'users',
    requirements_metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(150), nullable=False),
    Column('email', String(255), nullable=False),
    Column('password_hash', String(128), nullable=False),
    Column('is_active', Boolean, nullable=False, default=True),
    Column('created_at', DateTime, nullable=True),
    Column('updated_at', DateTime, nullable=True),
)


# Sample test data
@pytest.fixture
def sample_requirements_query_data():
    """Sample data for creating requirements queries"""
    return {
        "street": "Av. Revolución 123",
        "neighborhood": "Centro",
        "municipality_name": "Guadalajara",
        "municipality_id": 1,
        "scian_code": "461110",
        "scian_name": "Comercio al por menor de abarrotes, alimentos, bebidas, hielo y tabaco",
        "property_area": Decimal("150.50"),
        "activity_area": Decimal("100.25"),
        "applicant_name": "Juan Pérez García",
        "applicant_character": "Propietario",
        "person_type": "Física",
        "alcohol_sales": 0,
        "restrictions": {"zoning": "commercial", "parking_required": True}
    }


@pytest.fixture
def sample_requirements_query_with_alcohol():
    """Sample data for requirements query with alcohol sales"""
    return {
        "street": "Calle Morelos 456",
        "neighborhood": "Zona Dorada",
        "municipality_name": "Guadalajara",
        "municipality_id": 1,
        "scian_code": "722411",
        "scian_name": "Restaurantes con servicio de bar",
        "property_area": Decimal("200.00"),
        "activity_area": Decimal("180.00"),
        "applicant_name": "María González López",
        "applicant_character": "Representante Legal",
        "person_type": "Moral",
        "alcohol_sales": 1,
        "restrictions": {"alcohol_license": True, "sound_permit": True}
    }


@pytest.fixture
def sample_procedure_data():
    """Sample procedure data related to requirements queries"""
    return [
        {
            "id": 1,
            "folio": "PROC-2025-000001",
            "name": "Licencia de Funcionamiento",
            "status": 1,
            "requirements": [
                {"id": 1, "name": "Acta constitutiva", "required": True},
                {"id": 2, "name": "Identificación oficial", "required": True},
                {"id": 3, "name": "Comprobante de domicilio", "required": True}
            ],
            "requirements_query_id": 1
        },
        {
            "id": 2,
            "folio": "PROC-2025-000002",
            "name": "Permiso de Construcción",
            "status": 1,
            "requirements": [
                {"id": 4, "name": "Planos arquitectónicos", "required": True},
                {"id": 5, "name": "Memoria de cálculo", "required": True}
            ],
            "requirements_query_id": 1
        }
    ]


@pytest.fixture
def sample_renewal_data():
    """Sample renewal data for testing"""
    return [
        {
            "id": 1,
            "requirements_query_id": 1,
            "procedure_id": 1,
            "created_at": datetime.now() - timedelta(days=30)
        },
        {
            "id": 2,
            "requirements_query_id": 1,
            "procedure_id": 2,
            "created_at": datetime.now() - timedelta(days=15)
        }
    ]


@pytest.fixture
def encoded_folio():
    """Base64 encoded folio for testing"""
    import base64
    folio = "REQ-2025-000001"
    return base64.b64encode(folio.encode()).decode()


@pytest.fixture
def encoded_requirement_id():
    """Base64 encoded requirement ID for testing"""
    import base64
    req_id = "1"
    return base64.b64encode(req_id.encode()).decode()


@pytest.fixture
def invalid_encoded_folio():
    """Invalid base64 encoded folio for testing"""
    return "invalid-base64-string!"


@pytest.fixture
def test_municipality():
    """Test municipality data"""
    return {
        "id": 1,
        "name": "Guadalajara",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }


@pytest.fixture
def test_user():
    """Test user data"""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": "hashed_password",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }


# Test response schemas
@pytest.fixture
def expected_procedure_info_response():
    """Expected response structure for procedure info"""
    return {
        "folio": "REQ-2025-000001",
        "procedure_data": {
            "id": 1,
            "folio": "REQ-2025-000001",
            "street": "Av. Revolución 123",
            "neighborhood": "Centro",
            "municipality_name": "Guadalajara",
            "scian_code": "461110",
            "scian_name": "Comercio al por menor de abarrotes, alimentos, bebidas, hielo y tabaco",
            "property_area": 150.50,
            "activity_area": 100.25,
            "applicant_name": "Juan Pérez García",
            "status": 1
        },
        "requirements": [
            {
                "id": 1,
                "name": "Licencia de Funcionamiento",
                "status": 1,
                "requirements": [
                    {"id": 1, "name": "Acta constitutiva", "required": True},
                    {"id": 2, "name": "Identificación oficial", "required": True}
                ]
            }
        ],
        "status": "active"
    }


@pytest.fixture
def expected_procedure_type_response():
    """Expected response structure for procedure type info"""
    return {
        "folio": "REQ-2025-000001",
        "procedure_type": "commercial",
        "type_data": {
            "type": "commercial",
            "scian_code": "461110",
            "scian_name": "Comercio al por menor de abarrotes, alimentos, bebidas, hielo y tabaco",
            "alcohol_sales": 0,
            "property_area": 150.50,
            "activity_area": 100.25
        }
    }


@pytest.fixture
def expected_renewal_response():
    """Expected response structure for renewal info"""
    return {
        "folio": "REQ-2025-000001",
        "renewal_data": {
            "original_folio": "REQ-2025-000001",
            "primary_folio": None,
            "renewals_count": 2,
            "renewals": [
                {
                    "id": 1,
                    "procedure_id": 1,
                    "notes": "Renewal for procedure 1"
                },
                {
                    "id": 2,
                    "procedure_id": 2,
                    "notes": "Renewal for procedure 2"
                }
            ]
        },
        "renewal_requirements": [
            {"name": "Updated business license", "required": True},
            {"name": "Property verification", "required": True},
            {"name": "Tax compliance certificate", "required": True}
        ]
    }


@pytest.fixture
def expected_pdf_response():
    """Expected response structure for PDF generation"""
    return {
        "folio": "REQ-2025-000001",
        "requirement_id": 1,
        "pdf_data": "base64_encoded_pdf_content",
        "filename": "requirements_REQ-2025-000001_1.pdf"
    }
