import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore
from dotenv import load_dotenv
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
import os

load_dotenv()

class DatabaseSettings(BaseSettings):
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")  
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "default_database")
    DATABASE_USERNAME: str = os.getenv("DATABASE_USERNAME", 'default_user')  
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", 'default_password')
    DATABASE_SCHEMA: str = os.getenv("DATABASE_SCHEMA", "public")   
            
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "True").lower() in ("true", "1", "t")
    DATABASE_CONNECTION: str = os.getenv("DATABASE_CONNECTION", "postgresql")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY",   "your-secret-key")
    JWT_EXPIRATION_TIME: str = os.getenv("JWT_EXPIRATION_TIME", "15")
    GDAL_LIBRARY_PATH: str = os.getenv("GDAL_LIBRARY_PATH", "default_path")
    PATH: str = os.getenv("PATH", "default_path")
    PGDATA: str = os.getenv("PGDATA", "default_path")
    
    APP_BLOG_PASS: str = os.getenv("APP_BLOG_PASS", "default_blog_password")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    URL_GEOSERVER: str = os.getenv("URL_GEOSERVER", "https://datahub.mpiochih.gob.mx/")
    DEFAULT_GEOSERVER: str = 'https://api-visorurbano.jalisco.gob.mx/geoserver/'
    APP_URL: str = os.getenv("APP_URL", "http://localhost:8000/")
    APP_BASE_URL: str = os.getenv("APP_BASE_URL", "http://localhost:8000/")
    APP_LOGO: str = os.getenv("APP_LOGO", "https://api-visorurbano.jalisco.gob.mx/images/isologo_jalisco_h.svg")
    URL_MINIMAPA: str = os.getenv("URL_MINIMAPA", "https://visorurbano.jalisco.gob.mx/minimapa/")
    
    # Dashboard configuration
    DASHBOARD_ALERT_THRESHOLD_DAYS: int = int(os.getenv("DASHBOARD_ALERT_THRESHOLD_DAYS", "10"))
    DASHBOARD_DEFAULT_PROCESSING_TIME_DAYS: float = float(os.getenv("DASHBOARD_DEFAULT_PROCESSING_TIME_DAYS", "8.5"))
    DASHBOARD_HISTORICAL_PERIOD_DAYS: int = int(os.getenv("DASHBOARD_HISTORICAL_PERIOD_DAYS", "90"))
    DASHBOARD_RECENT_ACTIVITIES_LIMIT: int = int(os.getenv("DASHBOARD_RECENT_ACTIVITIES_LIMIT", "10"))
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = DatabaseSettings()

def get_database_url():    
        return f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    
def get_session_local():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

DATABASE_URL = get_database_url().replace("postgresql://", "postgresql+asyncpg://")
SYNC_DATABASE_URL = get_database_url()

# Async engine and session
engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Sync engine and session
sync_engine = create_engine(SYNC_DATABASE_URL)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

Base = declarative_base()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

async def get_db():
    """
    Dependency that provides a SQLAlchemy async session using SessionLocal.
    """
    async with SessionLocal() as session:
        yield session

def get_sync_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a synchronous SQLAlchemy session.
    
    Yields:
        db (Session): A synchronous SQLAlchemy session.
    """
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
