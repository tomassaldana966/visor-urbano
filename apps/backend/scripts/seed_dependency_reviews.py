#!/usr/bin/env python3
"""
Dependency Reviews Test Data Seeder
This script inserts test data into the dependency_reviews and technical_sheet_downloads tables
"""

import sys
import os
import asyncio
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.settings import settings

async def seed_dependency_reviews():
    """Seed dependency reviews test data"""
    
    # Create database URL
    database_url = f"postgresql+asyncpg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    
    # Create async engine
    engine = create_async_engine(database_url, echo=True)
    
    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            # Read the SQL seed file
            sql_file_path = os.path.join(
                os.path.dirname(__file__), 
                'seeds', 
                'dependency_reviews_test_data.sql'
            )
            
            with open(sql_file_path, 'r') as file:
                sql_content = file.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                # Skip comments and COMMIT statements
                if statement.startswith('--') or statement.upper() == 'COMMIT':
                    continue
                    
                print(f"Executing: {statement[:100]}...")
                await session.execute(text(statement))
            
            await session.commit()
            print("✅ Dependency reviews test data seeded successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding dependency reviews test data: {e}")
            raise
        finally:
            await engine.dispose()

async def verify_data():
    """Verify that the data was inserted correctly"""
    
    # Create database URL
    database_url = f"postgresql+asyncpg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    
    engine = create_async_engine(database_url, echo=False)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            # Count dependency reviews
            result = await session.execute(
                text("SELECT COUNT(*) as count FROM dependency_reviews WHERE folio LIKE 'TEST-%'")
            )
            dr_count = result.scalar()
            
            # Count technical sheet downloads
            result = await session.execute(
                text("SELECT COUNT(*) as count FROM technical_sheet_downloads WHERE name LIKE 'Test City%'")
            )
            tsd_count = result.scalar()
            
            print(f"📊 Verification Results:")
            print(f"   - Dependency Reviews: {dr_count} test records")
            print(f"   - Technical Sheet Downloads: {tsd_count} test records")
            
            # Show sample data
            result = await session.execute(
                text("""
                    SELECT folio, role, current_status, municipality_id, created_at 
                    FROM dependency_reviews 
                    WHERE folio LIKE 'TEST-%' 
                    ORDER BY created_at 
                    LIMIT 5
                """)
            )
            sample_data = result.fetchall()
            
            print(f"📝 Sample Data:")
            for row in sample_data:
                print(f"   - {row.folio}: Role {row.role}, Status {row.current_status}, Municipality {row.municipality_id}")
                
        except Exception as e:
            print(f"❌ Error verifying data: {e}")
        finally:
            await engine.dispose()

async def main():
    """Main function"""
    print("🌱 Starting Dependency Reviews Data Seeding...")
    
    try:
        await seed_dependency_reviews()
        await verify_data()
        print("🎉 Seeding completed successfully!")
        
    except Exception as e:
        print(f"💥 Seeding failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
