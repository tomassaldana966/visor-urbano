#!/usr/bin/env python3
"""
Dependency Revisions Test Data Seeder
This script inserts test data into the dependency_revisions table
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

async def seed_dependency_revisions():
    """Seed dependency revisions test data"""
    
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
            # Clear existing test data
            await session.execute(text("DELETE FROM dependency_revisions WHERE revision_notes LIKE 'TEST-%'"))
            print("✅ Cleared existing test data")
            
            # Insert test data directly instead of reading from file
            test_revisions = [
                (2, 'TEST-REV-001: Initial review - Documentation incomplete. Missing building permits and safety certificates.', '2024-01-15 09:00:00'),
                (2, 'TEST-REV-002: Second review - Building permits submitted but safety certificates still pending. Fire department approval required.', '2024-01-22 14:30:00'),
                (2, 'TEST-REV-003: Third review - All documents submitted. Technical review in progress. Minor corrections needed in structural plans.', '2024-01-29 11:15:00'),
                (2, 'TEST-REV-004: Final review - All requirements met. Approved for next phase. License ready for issuance.', '2024-02-05 16:45:00'),
                (3, 'TEST-REV-005: Environmental impact assessment required. Property located near protected wetlands. Additional studies needed.', '2024-01-18 10:20:00'),
                (3, 'TEST-REV-006: Environmental studies submitted. Mitigation plan approved. Proceed with standard review process.', '2024-02-01 13:45:00'),
                (4, 'TEST-REV-007: Zoning compliance review - Current zoning allows commercial use but density restrictions apply. Variance may be required.', '2024-01-20 08:30:00'),
                (4, 'TEST-REV-008: Zoning variance approved. Parking requirements modified. Additional landscaping required along street frontage.', '2024-02-03 15:20:00'),
                (5, 'TEST-REV-009: Technical review - HVAC system specifications do not meet current building codes. Updated plans required.', '2024-01-25 12:10:00'),
                (5, 'TEST-REV-010: Electrical system review - Load calculations incorrect. Professional engineer certification required.', '2024-01-30 09:45:00'),
                (2, 'TEST-REV-011: Post-approval revision - Minor modification to façade design. Does not affect structural integrity.', '2024-02-10 14:00:00'),
                (3, 'TEST-REV-012: Compliance check - Site inspection completed. All requirements met according to approved plans.', '2024-02-08 11:30:00'),
                (4, 'TEST-REV-013: Amendment request - Business scope expansion requires additional review. New SCIAN classification needed.', '2024-02-12 16:15:00'),
                (5, 'TEST-REV-014: Emergency revision - Code violation reported. Immediate compliance required for safety systems.', '2024-02-15 08:00:00'),
                (2, 'TEST-REV-015: Historical revision - Legacy system migration. Previous approvals verified and documented.', '2023-12-01 10:00:00'),
                (3, 'TEST-REV-016: Annual review - Periodic compliance check. All permits current and valid.', '2023-11-15 14:30:00'),
                (4, 'TEST-REV-017: Current revision - New accessibility requirements. ADA compliance assessment in progress.', '2024-06-01 09:15:00'),
                (5, 'TEST-REV-018: Latest revision - Digital submission review. Electronic documents verified and accepted.', '2024-06-01 15:45:00'),
                (2, 'TEST-REV-019: Special characters test - Revisión con caracteres especiales: ñáéíóú. Review completed successfully.', '2024-05-28 12:00:00'),
                (3, 'TEST-REV-020: Long note test - This is a very long revision note intended to test the system handling of extensive text content. It includes multiple sentences and various punctuation marks to ensure proper storage and retrieval.', '2024-05-30 17:30:00'),
                (4, None, '2024-05-25 10:45:00'),  # NULL revision_notes test
                (5, '', '2024-05-26 13:20:00'),  # Empty revision_notes test
            ]
            
            # Insert test data
            for dependency_id, notes, revised_at in test_revisions:
                # Convert string timestamp to datetime object
                revised_datetime = datetime.strptime(revised_at, '%Y-%m-%d %H:%M:%S')
                
                await session.execute(text("""
                    INSERT INTO dependency_revisions (dependency_id, revision_notes, revised_at, created_at, updated_at)
                    VALUES (:dependency_id, :notes, :revised_at, :revised_at, :revised_at)
                """), {
                    'dependency_id': dependency_id,
                    'notes': notes,
                    'revised_at': revised_datetime
                })
            
            await session.commit()
            print("✅ Dependency revisions test data seeded successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding dependency revisions test data: {e}")
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
            # Count dependency revisions
            result = await session.execute(
                text("SELECT COUNT(*) as count FROM dependency_revisions WHERE revision_notes LIKE 'TEST-%'")
            )
            dr_count = result.scalar()
            
            print(f"📊 Verification Results:")
            print(f"   - Dependency Revisions: {dr_count} test records")
            
            # Show sample data
            result = await session.execute(
                text("""
                    SELECT dr.id, dr.dependency_id, LEFT(dr.revision_notes, 50) || '...' as notes_preview, 
                           dr.revised_at, rq.folio 
                    FROM dependency_revisions dr
                    LEFT JOIN requirements_querys rq ON dr.dependency_id = rq.id
                    WHERE dr.revision_notes LIKE 'TEST-%' 
                    ORDER BY dr.revised_at DESC
                    LIMIT 5
                """)
            )
            sample_data = result.fetchall()
            
            print(f"📝 Sample Data:")
            for row in sample_data:
                print(f"   - ID {row.id}: Dependency {row.dependency_id} ({row.folio}), Notes: {row.notes_preview}")
                
        except Exception as e:
            print(f"❌ Error verifying data: {e}")
        finally:
            await engine.dispose()

async def main():
    """Main function"""
    print("🌱 Starting Dependency Revisions Data Seeding...")
    
    try:
        await seed_dependency_revisions()
        await verify_data()
        print("🎉 Seeding completed successfully!")
        
    except Exception as e:
        print(f"💥 Seeding failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
