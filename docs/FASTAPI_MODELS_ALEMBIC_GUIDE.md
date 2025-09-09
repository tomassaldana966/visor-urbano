# FastAPI Models and Alembic Integration Guide

## Overview

This document provides a comprehensive guide to understanding how FastAPI models work with Alembic migrations in the Visor Urbano project. It covers the relationship between SQLAlchemy models, Pydantic schemas, and the database migration process.

## Architecture Overview

### Technology Stack Integration

```mermaid
graph TB
    A[FastAPI Application] --> B[Pydantic Schemas]
    A --> C[SQLAlchemy Models]
    C --> D[Alembic Migrations]
    D --> E[PostgreSQL Database]
    C --> F[Database Sessions]
    F --> E
    B --> G[API Endpoints]
    G --> A

    subgraph "Database Layer"
        E --> H[PostGIS Extension]
        E --> I[Spatial Indexes]
        E --> J[Triggers & Constraints]
    end

    subgraph "Application Layer"
        A --> K[Controllers]
        A --> L[Services]
        A --> M[Utilities]
    end

    subgraph "Migration Layer"
        D --> N[Version Control]
        D --> O[Schema Changes]
        D --> P[Data Migrations]
    end
```

## SQLAlchemy Models Structure

### Base Model Configuration

```python
# config/settings.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

# Database configuration
DATABASE_URL = "postgresql+asyncpg://user:password@host:port/database"
SYNC_DATABASE_URL = "postgresql://user:password@host:port/database"

# Async engine and session
engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Sync engine for Alembic
sync_engine = create_engine(SYNC_DATABASE_URL)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Base class for all models
Base = declarative_base()
```

### Model Architecture Patterns

#### 1. Standard Entity Pattern

```python
# Example: User Model
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.settings import Base

class UserModel(Base):
    __tablename__ = 'users'

    # Primary key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Core fields
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    # Foreign keys
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    role_id = Column(BigInteger, ForeignKey('user_roles.id'), nullable=True)

    # Audit fields
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)  # Soft deletion

    # Relationships
    municipality = relationship("Municipality", back_populates="users")
    role = relationship("UserRoleModel", back_populates="users")
    answers = relationship("Answer", back_populates="user")
```

#### 2. Geospatial Entity Pattern

```python
# Example: Procedure Registration with Spatial Data
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.settings import Base

class ProcedureRegistration(Base):
    __tablename__ = 'procedure_registrations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference = Column(String(100), nullable=True)
    area = Column(Float, nullable=False, default=0)

    # Spatial geometry - UTM Zone 13N for Mexico
    geom = Column(
        Geometry('POLYGON', srid=32613, use_typmod=False, spatial_index=False),
        nullable=True
    )

    # Foreign key relationship
    municipality_id = Column(Integer, ForeignKey('municipalities.id'), nullable=True)
    municipality = relationship("Municipality", back_populates="procedure_registrations")
```

#### 3. Many-to-Many Relationship Pattern

```python
# Example: Map Layer to Municipality Association
from sqlalchemy import Table, Column, ForeignKey
from config.settings import Base

# Association table for many-to-many relationship
maplayer_municipality = Table(
    "maplayer_municipality",
    Base.metadata,
    Column("maplayer_id", ForeignKey("map_layers.id"), primary_key=True),
    Column("municipality_id", ForeignKey("municipalities.id"), primary_key=True),
)

class MapLayer(Base):
    __tablename__ = 'map_layers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(100), nullable=False)
    label = Column(String(180), nullable=False)

    # Many-to-many relationship
    municipalities = relationship(
        "Municipality",
        secondary=maplayer_municipality,
        back_populates="map_layers"
    )

class Municipality(Base):
    __tablename__ = 'municipalities'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)

    # Many-to-many relationship
    map_layers = relationship(
        "MapLayer",
        secondary=maplayer_municipality,
        back_populates="municipalities"
    )
```

## Pydantic Schemas Integration

### Schema Architecture

```python
# Example: User Schemas
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema with common fields"""
    name: str
    email: EmailStr
    cellphone: str
    municipality_id: Optional[int] = None

class UserCreate(UserBase):
    """Schema for creating users"""
    password: str
    paternal_last_name: str
    maternal_last_name: Optional[str] = None
    national_id: Optional[str] = None
    user_tax_id: Optional[str] = None

class UserUpdate(BaseModel):
    """Schema for updating users"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cellphone: Optional[str] = None
    municipality_id: Optional[int] = None

class UserResponse(UserBase):
    """Schema for user responses"""
    id: int
    username: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Related data
    municipality: Optional['MunicipalityResponse'] = None
    role: Optional['UserRoleResponse'] = None

    model_config = ConfigDict(from_attributes=True)

class UserListResponse(BaseModel):
    """Schema for paginated user lists"""
    users: List[UserResponse]
    total: int
    page: int
    size: int
    pages: int
```

### Schema Validation Patterns

```python
# Example: Business License Schema with Validation
from pydantic import BaseModel, validator, Field
from typing import Optional
import re

class BusinessLicenseCreate(BaseModel):
    owner: str = Field(..., min_length=2, max_length=200)
    commercial_activity: str = Field(..., min_length=5, max_length=200)
    industry_classification_code: str = Field(..., regex=r'^\d{6}$')  # SCIAN code
    authorized_area: str = Field(..., min_length=1, max_length=200)
    opening_time: str = Field(..., regex=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    closing_time: str = Field(..., regex=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')

    @validator('closing_time')
    def validate_closing_time(cls, v, values):
        if 'opening_time' in values:
            opening = values['opening_time']
            if v <= opening:
                raise ValueError('Closing time must be after opening time')
        return v

    @validator('industry_classification_code')
    def validate_scian_code(cls, v):
        if not re.match(r'^\d{6}$', v):
            raise ValueError('SCIAN code must be 6 digits')
        return v

class BusinessLicenseResponse(BaseModel):
    id: int
    owner: str
    license_folio: str
    commercial_activity: str
    industry_classification_code: str
    authorized_area: str
    opening_time: str
    closing_time: str
    license_status: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
```

## Alembic Migration System

### Migration Configuration

```python
# migrations/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from config.settings import Base, SYNC_DATABASE_URL
from app.models import *  # Import all models

# Alembic Config object
config = context.config

# Set the database URL
config.set_main_option('sqlalchemy.url', SYNC_DATABASE_URL)

# Target metadata for autogenerate
target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Migration Generation Process

#### 1. Automatic Migration Generation

```bash
# Generate migration from model changes
alembic revision --autogenerate -m "add_new_table_or_field"

# Review generated migration file
# Edit if necessary for custom logic
```

#### 2. Manual Migration Creation

```python
# Example: Custom migration for data transformation
"""add_business_license_categories

Revision ID: abc123def456
Revises: previous_revision
Create Date: 2024-01-01 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'abc123def456'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None

def upgrade():
    # Add new column
    op.add_column('business_licenses',
                  sa.Column('category_id', sa.Integer(), nullable=True))

    # Create new table
    op.create_table('business_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Add foreign key constraint
    op.create_foreign_key('fk_business_license_category',
                         'business_licenses', 'business_categories',
                         ['category_id'], ['id'])

    # Data migration
    connection = op.get_bind()
    connection.execute(
        sa.text("""
            INSERT INTO business_categories (name, description)
            VALUES ('Low Impact', 'Low impact business activities'),
                   ('Medium Impact', 'Medium impact business activities'),
                   ('High Impact', 'High impact business activities')
        """)
    )

def downgrade():
    # Remove foreign key
    op.drop_constraint('fk_business_license_category', 'business_licenses', type_='foreignkey')

    # Remove column
    op.drop_column('business_licenses', 'category_id')

    # Drop table
    op.drop_table('business_categories')
```

#### 3. Geospatial Migration Patterns

```python
# Example: Adding spatial columns and indexes
def upgrade():
    # Add spatial column
    op.add_column('procedures',
                  sa.Column('location',
                           geoalchemy2.types.Geometry(geometry_type='POINT',
                                                     srid=4326),
                           nullable=True))

    # Create spatial index
    op.create_index('idx_procedures_location', 'procedures', ['location'],
                    unique=False, postgresql_using='gist')

    # Add spatial constraint
    op.execute(
        "ALTER TABLE procedures ADD CONSTRAINT enforce_srid_location "
        "CHECK (st_srid(location) = 4326)"
    )

def downgrade():
    # Drop spatial constraint
    op.execute("ALTER TABLE procedures DROP CONSTRAINT enforce_srid_location")

    # Drop spatial index
    op.drop_index('idx_procedures_location', table_name='procedures')

    # Drop spatial column
    op.drop_column('procedures', 'location')
```

## Database Session Management

### Async Session Patterns

```python
# Example: Service layer with async sessions
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from config.settings import get_db

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """Get user by ID with relationships"""
        result = await self.db.execute(
            select(UserModel)
            .options(selectinload(UserModel.municipality))
            .options(selectinload(UserModel.role))
            .where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> UserModel:
        """Create new user"""
        user = UserModel(**user_data.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserModel]:
        """Update existing user"""
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        if user:
            for field, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)

            await self.db.commit()
            await self.db.refresh(user)

        return user

    async def delete_user(self, user_id: int) -> bool:
        """Soft delete user"""
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        if user:
            user.deleted_at = func.now()
            await self.db.commit()
            return True

        return False
```

### FastAPI Dependency Injection

```python
# Example: FastAPI endpoints with dependency injection
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import get_db
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get user by ID"""
    service = UserService(db)
    user = await service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new user"""
    service = UserService(db)

    try:
        user = await service.create_user(user_data)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update user"""
    service = UserService(db)
    user = await service.update_user(user_id, user_data)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete user (soft delete)"""
    service = UserService(db)
    success = await service.delete_user(user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}
```

## Model Relationships and Querying

### Complex Relationship Queries

```python
# Example: Complex queries with multiple relationships
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import and_, or_

class ProcedureService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_procedures_with_reviews(self, municipality_id: int):
        """Get procedures with all related data"""
        result = await self.db.execute(
            select(Procedure)
            .options(selectinload(Procedure.user))
            .options(selectinload(Procedure.municipality))
            .options(selectinload(Procedure.dependency_reviews)
                    .selectinload(DependencyReview.department))
            .options(selectinload(Procedure.dependency_reviews)
                    .selectinload(DependencyReview.reviewer))
            .where(Procedure.project_municipality_id == municipality_id)
            .order_by(Procedure.created_at.desc())
        )
        return result.scalars().all()

    async def get_pending_procedures_by_department(self, department_id: int):
        """Get procedures pending review by department"""
        result = await self.db.execute(
            select(Procedure)
            .join(DependencyReview)
            .where(
                and_(
                    DependencyReview.department_id == department_id,
                    DependencyReview.review_status == 'pending'
                )
            )
            .options(selectinload(Procedure.user))
            .order_by(Procedure.created_at.asc())
        )
        return result.scalars().all()
```

### Spatial Queries

```python
# Example: Spatial queries with PostGIS
from geoalchemy2.functions import ST_Contains, ST_Intersects, ST_Distance
from sqlalchemy import func

class SpatialService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_procedures_within_area(self, polygon_wkt: str):
        """Get procedures within a polygon area"""
        result = await self.db.execute(
            select(ProcedureRegistration)
            .where(
                ST_Contains(
                    func.ST_GeomFromText(polygon_wkt, 32613),
                    ProcedureRegistration.geom
                )
            )
        )
        return result.scalars().all()

    async def get_nearby_procedures(self, point_wkt: str, distance_meters: float):
        """Get procedures within distance of a point"""
        result = await self.db.execute(
            select(ProcedureRegistration)
            .where(
                ST_Distance(
                    func.ST_GeomFromText(point_wkt, 32613),
                    ProcedureRegistration.geom
                ) <= distance_meters
            )
            .order_by(
                ST_Distance(
                    func.ST_GeomFromText(point_wkt, 32613),
                    ProcedureRegistration.geom
                )
            )
        )
        return result.scalars().all()
```

## Testing Strategies

### Database Testing Setup

```python
# Example: Test database setup
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config.settings import Base, get_db
from app.main import app

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_db"

@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def test_db(test_engine):
    """Create test database session"""
    TestSessionLocal = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with TestSessionLocal() as session:
        yield session

@pytest.fixture
async def test_client(test_db):
    """Create test client with database override"""
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
```

### Model Testing

```python
# Example: Model tests
import pytest
from app.models.user import UserModel
from app.models.municipality import Municipality

@pytest.mark.asyncio
async def test_create_user(test_db):
    """Test user creation"""
    # Create municipality first
    municipality = Municipality(name="Test Municipality")
    test_db.add(municipality)
    await test_db.commit()
    await test_db.refresh(municipality)

    # Create user
    user = UserModel(
        name="Test User",
        email="test@example.com",
        password="hashed_password",
        cellphone="1234567890",
        municipality_id=municipality.id
    )

    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)

    assert user.id is not None
    assert user.name == "Test User"
    assert user.municipality_id == municipality.id

@pytest.mark.asyncio
async def test_user_relationships(test_db):
    """Test user relationships"""
    # Create municipality
    municipality = Municipality(name="Test Municipality")
    test_db.add(municipality)
    await test_db.commit()
    await test_db.refresh(municipality)

    # Create user
    user = UserModel(
        name="Test User",
        email="test@example.com",
        password="hashed_password",
        cellphone="1234567890",
        municipality_id=municipality.id
    )

    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)

    # Test relationship
    result = await test_db.execute(
        select(UserModel)
        .options(selectinload(UserModel.municipality))
        .where(UserModel.id == user.id)
    )
    loaded_user = result.scalar_one()

    assert loaded_user.municipality is not None
    assert loaded_user.municipality.name == "Test Municipality"
```

## Performance Optimization

### Query Optimization

```python
# Example: Optimized queries
class OptimizedProcedureService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_procedures_dashboard(self, municipality_id: int, limit: int = 10):
        """Optimized dashboard query"""
        # Use single query with proper joins
        result = await self.db.execute(
            select(
                Procedure.id,
                Procedure.folio,
                Procedure.status,
                Procedure.created_at,
                UserModel.name.label('user_name'),
                UserModel.email.label('user_email')
            )
            .join(UserModel)
            .where(Procedure.project_municipality_id == municipality_id)
            .order_by(Procedure.created_at.desc())
            .limit(limit)
        )
        return result.all()

    async def get_procedure_statistics(self, municipality_id: int):
        """Get aggregated statistics"""
        result = await self.db.execute(
            select(
                Procedure.status,
                func.count(Procedure.id).label('count')
            )
            .where(Procedure.project_municipality_id == municipality_id)
            .group_by(Procedure.status)
        )
        return result.all()
```

### Caching Strategies

```python
# Example: Caching with Redis
from functools import wraps
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expire_seconds=300):
    """Decorator for caching query results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute function
            result = await func(*args, **kwargs)

            # Cache result
            redis_client.setex(
                cache_key,
                expire_seconds,
                json.dumps(result, default=str)
            )

            return result
        return wrapper
    return decorator

class CachedMunicipalityService:
    def __init__(self, db: AsyncSession):
        self.db = db

    @cache_result(expire_seconds=600)
    async def get_municipality_config(self, municipality_id: int):
        """Get cached municipality configuration"""
        result = await self.db.execute(
            select(Municipality).where(Municipality.id == municipality_id)
        )
        municipality = result.scalar_one_or_none()

        if municipality:
            return {
                'id': municipality.id,
                'name': municipality.name,
                'theme_color': municipality.theme_color,
                'allow_online_procedures': municipality.allow_online_procedures,
                'license_price': municipality.license_price
            }
        return None
```

## Error Handling and Logging

### Database Error Handling

```python
# Example: Error handling patterns
from sqlalchemy.exc import IntegrityError, DataError
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def safe_create_user(self, user_data: UserCreate):
        """Create user with error handling"""
        try:
            user = UserModel(**user_data.model_dump())
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user

        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"Integrity error creating user: {e}")

            if "email" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Email already exists"
                )
            elif "municipality_id" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid municipality"
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Database constraint violation"
                )

        except DataError as e:
            await self.db.rollback()
            logger.error(f"Data error creating user: {e}")
            raise HTTPException(
                status_code=400,
                detail="Invalid data format"
            )

        except Exception as e:
            await self.db.rollback()
            logger.error(f"Unexpected error creating user: {e}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )
```

## Migration Best Practices

### Migration Checklist

1. **Before Creating Migration**
   - Review model changes carefully
   - Consider backward compatibility
   - Plan for data migration if needed
   - Test on development database

2. **Migration Content**
   - Always include both upgrade and downgrade
   - Add appropriate indexes
   - Include foreign key constraints
   - Handle data transformations safely

3. **After Migration**
   - Test migration on staging environment
   - Verify all constraints work
   - Check performance impact
   - Document any manual steps required

### Migration Templates

```python
# Template: Adding new table
def upgrade():
    op.create_table('new_table',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('municipality_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['municipality_id'], ['municipalities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Add indexes
    op.create_index('idx_new_table_municipality', 'new_table', ['municipality_id'])
    op.create_index('idx_new_table_name', 'new_table', ['name'])

def downgrade():
    op.drop_index('idx_new_table_name', table_name='new_table')
    op.drop_index('idx_new_table_municipality', table_name='new_table')
    op.drop_table('new_table')
```

## Conclusion

The integration of FastAPI models with Alembic provides a robust foundation for database management in the Visor Urbano project. Key benefits include:

1. **Type Safety**: Pydantic schemas ensure data validation
2. **Async Performance**: Async SQLAlchemy enables high concurrency
3. **Migration Control**: Alembic provides reliable schema evolution
4. **Relationship Management**: SQLAlchemy ORM handles complex relationships
5. **Spatial Support**: PostGIS integration for geospatial data

By following these patterns and best practices, developers can maintain a scalable, performant, and maintainable database layer while ensuring data integrity and system reliability.
