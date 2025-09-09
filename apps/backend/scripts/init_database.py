#!/usr/bin/env python3
"""
Database Initialization Script

This script creates all database tables using SQLAlchemy's create_all method,
bypassing Alembic migration issues.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import SessionLocal, engine, Base

# Import all models to register them with Base
from app.models.municipality import Municipality
from app.models.user import UserModel  
from app.models.user_roles import UserRoleModel
from app.models.user_roles_assignments import UserRoleAssignment
from app.models.base_locality import BaseLocality


async def init_database():
    """Initialize database by creating all tables."""
    print("🗄️  Initializing database tables...")
    
    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database tables: {str(e)}")
        return False


async def main():
    """Entry point for the script."""
    try:
        success = await init_database()
        if success:
            print("\n✨ Database initialization completed successfully!")
        else:
            print("\n💥 Database initialization failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Database initialization failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
