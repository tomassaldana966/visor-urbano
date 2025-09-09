#!/usr/bin/env python3
"""
Script to verify that all models are correctly created in the database.
This script should be executed after migrations to ensure schema integrity.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import SessionLocal, engine
from config.settings import Base

# List of expected tables (based on models)
EXPECTED_TABLES = {
    'answers',
    'answers_json', 
    'auth_group',
    'auth_group_permissions',
    'auth_permission',
    'authtoken_token',
    'auth_user_groups',
    'auth_user_user_permissions',
    'base_administrative_division',
    'base_locality',
    'base_map_layer',
    'base_municipality',  # Table that was missing before
    'base_neighborhood',
    'blog',
    'building_footprints',
    'business_license_histories',
    'business_licenses',
    'business_line_configurations',
    'business_line_logs',
    'business_lines',
    'business_logs',
    'business_sector_certificates',
    'business_sector_configurations',
    'business_sector_impacts',
    'business_sectors',
    'business_signatures',
    'business_type_configurations',
    'block_footprints',
    'departments',
    'department_roles',
    'department_user_assignments',
    'dependency_resolutions',
    'dependency_reviews',
    'dependency_review_workflows',
    'dependency_revisions',
    'director_approvals',
    'economic_activity_base',
    'economic_activity_sector',
    'economic_supports',
    'economic_units_directory',
    'fields',
    'historical_procedures',
    'inactive_businesses',
    'issue_resolutions',
    'land_parcel_mapping',
    'map_layers',
    'maplayer_municipality',
    'municipalities',
    'municipality_geoms',
    'municipality_map_layer_base',
    'municipality_signatures',
    'national_id',
    'notifications',
    'password_recoveries',
    'permit_renewals',
    'procedure_department_flows',
    'procedure_registrations',
    'procedures',
    'provisional_openings',
    'public_space_mapping',
    'renewal_file_histories',
    'renewal_files',
    'renewals',
    'requirements',
    'requirement_department_assignments',
    'requirements_querys',
    'reviewers_chat',
    'sub_roles',
    'technical_sheet_downloads',
    'technical_sheets',
    'urban_development_zonings',
    'urban_development_zonings_standard',
    'users',
    'user_roles',
    'user_roles_assignments',
    'user_tax_id',
    'water_body_footprints',
    'zoning_control_regulations',
    'zoning_impact_level',
}

# System tables that we can ignore
SYSTEM_TABLES = {
    'alembic_version',
    'spatial_ref_sys',
    'geography_columns',
    'geometry_columns',
    'topology',
    'layer',
}

async def get_database_tables() -> set:
    """Get all tables that exist in the database."""
    async with SessionLocal() as session:
        result = await session.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        table_names = [row[0] for row in result.fetchall()]
        return set(table_names)

async def verify_tables_exist():
    """Verify that all expected tables exist in the database."""
    print("🔍 Checking tables in the database...")
    
    try:
        db_tables = await get_database_tables()
        
        # Filter system tables
        actual_tables = db_tables - SYSTEM_TABLES
        
        print(f"📊 Tables found in database: {len(actual_tables)}")
        print(f"📋 Expected tables: {len(EXPECTED_TABLES)}")
        
        # Check missing tables
        missing_tables = EXPECTED_TABLES - actual_tables
        if missing_tables:
            print("\n❌ MISSING TABLES:")
            for table in sorted(missing_tables):
                print(f"  - {table}")
            return False
        
        # Check extra tables (could be legacy or unexpected tables)
        extra_tables = actual_tables - EXPECTED_TABLES
        if extra_tables:
            print("\n⚠️  ADDITIONAL TABLES (possibly legacy):")
            for table in sorted(extra_tables):
                print(f"  - {table}")
        
        print("\n✅ All expected tables are present!")
        return True
        
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

async def verify_critical_models():
    """Verify that critical models have required minimum data."""
    print("\n🔍 Checking critical data...")
    
    async with SessionLocal() as session:
        try:
            # Verify that at least one municipality exists
            result = await session.execute(text("SELECT COUNT(*) FROM municipalities"))
            municipality_count = result.scalar()
            
            if municipality_count == 0:
                print("⚠️  No municipalities in the database")
                print("💡 Run: python scripts/create_municipality.py 'Development Municipality'")
            else:
                print(f"✅ Municipalities found: {municipality_count}")
            
            # Verify basic roles
            result = await session.execute(text("SELECT COUNT(*) FROM user_roles"))
            roles_count = result.scalar()
            
            if roles_count == 0:
                print("⚠️  No user roles defined")
                print("💡 Run the setup script to create basic roles")
            else:
                print(f"✅ User roles found: {roles_count}")
                
            return True
            
        except Exception as e:
            print(f"❌ Error checking critical data: {e}")
            return False

async def main():
    """Main function of the verification script."""
    print("🚀 Starting database models and schema verification")
    print("=" * 60)
    
    # Verify database connection
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        sys.exit(1)
    
    # Verify tables
    tables_ok = await verify_tables_exist()
    
    # Verify critical data
    data_ok = await verify_critical_models()
    
    print("\n" + "=" * 60)
    if tables_ok and data_ok:
        print("🎉 Verification completed successfully!")
        print("💚 Database schema is complete and working")
        sys.exit(0)
    else:
        print("⚠️  Problems found during verification")
        print("🔧 Review the previous messages to fix the issues")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
