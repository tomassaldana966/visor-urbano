#!/usr/bin/env python3
"""
Procedure Registrations Test Data Seeder
This script inserts test data into the procedure_registrations table
"""

import sys
import os
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.settings import settings

async def seed_procedure_registrations():
    """Seed procedure_registrations test data"""
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
                'procedure_registrations_test_data.sql'
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
            print("✅ Procedure registrations test data seeded successfully!")
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding procedure registrations test data: {e}")
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
            # Count procedure registrations
            result = await session.execute(
                text("SELECT COUNT(*) as count FROM procedure_registrations WHERE reference LIKE 'REF-%'")
            )
            pr_count = result.scalar()
            print(f"📊 Verification Results:")
            print(f"   - Procedure Registrations: {pr_count} test records")
            # Show sample data
            result = await session.execute(
                text("""
                    SELECT reference, area, business_sector, procedure_type, municipality_id
                    FROM procedure_registrations
                    WHERE reference LIKE 'REF-%'
                    ORDER BY area DESC
                    LIMIT 5
                """)
            )
            sample_data = result.fetchall()
            print(f"📝 Sample Data:")
            for row in sample_data:
                print(f"   - {row.reference}: {row.business_sector}, {row.procedure_type}, Area: {row.area}, Municipality: {row.municipality_id}")
        except Exception as e:
            print(f"❌ Error verifying data: {e}")
        finally:
            await engine.dispose()

async def main():
    """Main function"""
    print("🌱 Starting Procedure Registrations Data Seeding...")
    try:
        await seed_procedure_registrations()
        await verify_data()
        print("🎉 Seeding completed successfully!")
    except Exception as e:
        print(f"💥 Seeding failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
