#!/usr/bin/env python3
"""
Seed script for dependency_resolutions test data
This script populates the dependency_resolutions table with comprehensive test data
for testing the dependency_resolutions endpoints.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the parent directory to the path to import our modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from config.settings import engine


async def seed_dependency_resolutions():
    """Seed the dependency_resolutions table with test data"""
    
    # Read the SQL seed file
    seed_file_path = Path(__file__).parent / "seeds" / "dependency_resolutions_test_data.sql"
    
    if not seed_file_path.exists():
        print(f"❌ Seed file not found: {seed_file_path}")
        return False
    
    try:
        with open(seed_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("🌱 Starting dependency_resolutions seed process...")
        
        # Split the SQL content into individual statements
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        async with AsyncSession(engine) as session:
            for i, statement in enumerate(statements):
                # Skip comments and empty statements
                if statement.startswith('--') or not statement:
                    continue
                
                try:
                    print(f"📝 Executing statement {i+1}/{len(statements)}...")
                    result = await session.execute(text(statement))
                    
                    # If it's a SELECT statement, show results
                    if statement.upper().strip().startswith('SELECT'):
                        rows = result.fetchall()
                        if rows:
                            print(f"   ✅ Query returned {len(rows)} rows")
                            # Show first few rows for verification
                            for j, row in enumerate(rows[:5]):
                                print(f"      Row {j+1}: {row}")
                            if len(rows) > 5:
                                print(f"      ... and {len(rows) - 5} more rows")
                        else:
                            print("   ℹ️ Query returned no rows")
                    else:
                        # For INSERT/DELETE statements, show affected rows
                        if hasattr(result, 'rowcount') and result.rowcount is not None:
                            print(f"   ✅ Affected {result.rowcount} rows")
                        else:
                            print("   ✅ Statement executed successfully")
                    
                except Exception as e:
                    print(f"   ❌ Error executing statement: {e}")
                    if "INSERT" in statement.upper() or "DELETE" in statement.upper():
                        # Don't fail on INSERT/DELETE errors, might be duplicate data
                        print(f"   ⚠️ Continuing with next statement...")
                        continue
                    else:
                        raise
            
            # Commit all changes
            await session.commit()
            print("💾 All changes committed successfully")
        
        print("\n🎉 Dependency resolutions seed data created successfully!")
        print("\n📊 Summary of seeded data:")
        print("   • 16 dependency resolution records")
        print("   • 5 different procedures (PROC-001, PROC-002, string, PROC-004, PROC-005)")
        print("   • 5 different resolution statuses (1-5)")
        print("   • 3 different roles (1=Admin, 2=Director, 3=Technical)")
        print("   • Various resolution texts and files for testing")
        print("   • Date ranges from January 15 to February 1, 2024")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during seed process: {e}")
        return False


async def verify_seed_data():
    """Verify that the seed data was inserted correctly"""
    print("\n🔍 Verifying seed data...")
    
    try:
        async with AsyncSession(engine) as session:
            # Check total count
            result = await session.execute(text("SELECT COUNT(*) FROM dependency_resolutions"))
            total_count = result.scalar()
            print(f"   📊 Total dependency_resolutions: {total_count}")
            
            # Check by procedure
            result = await session.execute(text("""
                SELECT p.folio, COUNT(dr.id) as resolution_count
                FROM procedures p
                LEFT JOIN dependency_resolutions dr ON p.id = dr.procedure_id
                WHERE p.id IN (1, 2, 3, 4, 5)
                GROUP BY p.id, p.folio
                ORDER BY p.id
            """))
            procedures_data = result.fetchall()
            print("   📋 Resolutions by procedure:")
            for proc in procedures_data:
                print(f"      {proc[0]}: {proc[1]} resolutions")
            
            # Check by status
            result = await session.execute(text("""
                SELECT resolution_status, COUNT(*) as count
                FROM dependency_resolutions
                GROUP BY resolution_status
                ORDER BY resolution_status
            """))
            status_data = result.fetchall()
            print("   📊 Resolutions by status:")
            status_names = {1: "Aprobado", 2: "Observaciones", 3: "Rechazado", 4: "Pendiente", 5: "Aprobado con condiciones"}
            for status in status_data:
                status_name = status_names.get(status[0], f"Status {status[0]}")
                print(f"      {status_name}: {status[1]} resolutions")
            
            print("   ✅ Seed data verification completed")
            
    except Exception as e:
        print(f"   ❌ Error during verification: {e}")


if __name__ == "__main__":
    print("🚀 Dependency Resolutions Seed Script")
    print("=" * 50)
    
    async def main():
        success = await seed_dependency_resolutions()
        if success:
            await verify_seed_data()
            print("\n✨ Seed process completed successfully!")
            print("\n🧪 You can now run the dependency_resolutions tests:")
            print("   pytest tests/test_dependency_resolutions.py -v")
        else:
            print("\n💥 Seed process failed!")
            sys.exit(1)
    
    # Run the seed process
    asyncio.run(main())
