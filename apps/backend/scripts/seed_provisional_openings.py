#!/usr/bin/env python3
"""
Provisional Openings Test Data Seeder
This script inserts comprehensive fake test data into the provisional_openings table
"""

import sys
import os
import base64
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from config.settings import get_database_url
from models.provisional_openings import ProvisionalOpening

def create_test_data():
    """Create comprehensive test data for provisional openings"""
    
    # Helper function to encode folio to base64
    def encode_folio(folio):
        return base64.b64encode(folio.encode()).decode()
    
    # Current date for calculations
    now = datetime.now()
    
    test_records = [
        # Active Provisional Openings - Restaurant Business
        {
            'folio': encode_folio('APO-REST-001-2024'),
            'procedure_id': 1,
            'counter': 1001,
            'granted_by_user_id': 1,
            'granted_role': 1,
            'start_date': now - timedelta(days=15),
            'end_date': now + timedelta(days=45),
            'status': 1,  # Active
            'municipality_id': 1,
            'created_by': 1,
        },
        
        # Active Provisional Opening - Pharmacy
        {
            'folio': encode_folio('APO-PHARM-002-2024'),
            'procedure_id': 1,
            'counter': 1002,
            'granted_by_user_id': 2,
            'granted_role': 1,
            'start_date': now - timedelta(days=10),
            'end_date': now + timedelta(days=50),
            'status': 1,  # Active
            'municipality_id': 1,
            'created_by': 2,
        },
        
        # Near Expiry - Coffee Shop (expires in 5 days)
        {
            'folio': encode_folio('APO-COFFEE-003-2024'),
            'procedure_id': 3,
            'counter': 1003,
            'granted_by_user_id': 1,
            'granted_role': 1,
            'start_date': now - timedelta(days=55),
            'end_date': now + timedelta(days=5),
            'status': 1,  # Active but near expiry
            'municipality_id': 1,
            'created_by': 1,
        },
        
        # Expired Provisional Opening - Electronics Store
        {
            'folio': encode_folio('APO-ELEC-004-2024'),
            'procedure_id': 1,
            'counter': 1004,
            'granted_by_user_id': 2,
            'granted_role': 1,
            'start_date': now - timedelta(days=90),
            'end_date': now - timedelta(days=10),
            'status': 0,  # Expired/Inactive
            'municipality_id': 1,
            'created_by': 2,
        },
        
        # Suspended - Bar (Municipality 1)
        {
            'folio': encode_folio('APO-BAR-005-2024'),
            'procedure_id': 1,
            'counter': 1005,
            'granted_by_user_id': 1,
            'granted_role': 1,
            'start_date': now - timedelta(days=30),
            'end_date': now + timedelta(days=30),
            'status': 2,  # Suspended
            'municipality_id': 1,
            'created_by': 1,
        },
        
        # Active - Auto Repair Shop (Municipality 2)
        {
            'folio': encode_folio('APO-AUTO-006-2024'),
            'procedure_id': 5,
            'counter': 2001,
            'granted_by_user_id': 3,
            'granted_role': 1,
            'start_date': now - timedelta(days=5),
            'end_date': now + timedelta(days=85),
            'status': 1,  # Active
            'municipality_id': 2,
            'created_by': 3,
        },
        
        # Active - Beauty Salon (Municipality 2)
        {
            'folio': encode_folio('APO-BEAUTY-007-2024'),
            'procedure_id': 3,
            'counter': 2002,
            'granted_by_user_id': 4,
            'granted_role': 1,
            'start_date': now - timedelta(days=8),
            'end_date': now + timedelta(days=52),
            'status': 1,  # Active
            'municipality_id': 2,
            'created_by': 4,
        },
        
        # Cancelled - Bakery (Municipality 2)
        {
            'folio': encode_folio('APO-BAKERY-008-2024'),
            'procedure_id': 4,
            'counter': 2003,
            'granted_by_user_id': 3,
            'granted_role': 1,
            'start_date': now - timedelta(days=60),
            'end_date': now + timedelta(days=0),
            'status': 3,  # Cancelled
            'municipality_id': 2,
            'created_by': 3,
        },
        
        # Active - Grocery Store (Municipality 3)
        {
            'folio': encode_folio('APO-GROCERY-009-2024'),
            'procedure_id': 1,
            'counter': 3001,
            'granted_by_user_id': 5,
            'granted_role': 1,
            'start_date': now - timedelta(days=3),
            'end_date': now + timedelta(days=87),
            'status': 1,  # Active
            'municipality_id': 3,
            'created_by': 5,
        },
        
        # Under Review - Hardware Store (Municipality 3)
        {
            'folio': encode_folio('APO-HARDWARE-010-2024'),
            'procedure_id': 1,
            'counter': 3002,
            'granted_by_user_id': 5,
            'granted_role': 1,
            'start_date': now + timedelta(days=2),
            'end_date': now + timedelta(days=92),
            'status': 4,  # Under Review/Pending
            'municipality_id': 3,
            'created_by': 5,
        },
        
        # Recently Expired - Fitness Center
        {
            'folio': encode_folio('APO-FITNESS-011-2024'),
            'procedure_id': 3,
            'counter': 3003,
            'granted_by_user_id': 5,
            'granted_role': 1,
            'start_date': now - timedelta(days=120),
            'end_date': now - timedelta(days=5),
            'status': 0,  # Expired
            'municipality_id': 3,
            'created_by': 5,
        },
        
        # Long-term Active - Warehouse (Municipality 2)
        {
            'folio': encode_folio('APO-WAREHOUSE-012-2024'),
            'procedure_id': 2,
            'counter': 2004,
            'granted_by_user_id': 4,
            'granted_role': 1,
            'start_date': now - timedelta(days=30),
            'end_date': now + timedelta(days=335),  # Nearly a year
            'status': 1,  # Active
            'municipality_id': 2,
            'created_by': 4,
        },
        
        # Very Recent - Print Shop (started yesterday)
        {
            'folio': encode_folio('APO-PRINT-013-2024'),
            'procedure_id': 1,
            'counter': 1006,
            'granted_by_user_id': 2,
            'granted_role': 1,
            'start_date': now - timedelta(days=1),
            'end_date': now + timedelta(days=89),
            'status': 1,  # Active
            'municipality_id': 1,
            'created_by': 2,
        },
        
        # Future Start Date - Laundromat (starts next week)
        {
            'folio': encode_folio('APO-LAUNDRY-014-2024'),
            'procedure_id': 3,
            'counter': 1007,
            'granted_by_user_id': 1,
            'granted_role': 1,
            'start_date': now + timedelta(days=7),
            'end_date': now + timedelta(days=97),
            'status': 4,  # Pending start
            'municipality_id': 1,
            'created_by': 1,
        },
        
        # Short Duration - Food Truck (10 days only)
        {
            'folio': encode_folio('APO-FOODTRUCK-015-2024'),
            'procedure_id': 4,
            'counter': 2005,
            'granted_by_user_id': 3,
            'granted_role': 1,
            'start_date': now - timedelta(days=2),
            'end_date': now + timedelta(days=8),
            'status': 1,  # Active but short term
            'municipality_id': 2,
            'created_by': 3,
        },
        
        # Test case for pagination - Multiple similar entries
        {
            'folio': encode_folio('APO-MULTI-016-2024'),
            'procedure_id': 1,
            'counter': 3004,
            'granted_by_user_id': 5,
            'granted_role': 1,
            'start_date': now - timedelta(days=20),
            'end_date': now + timedelta(days=40),
            'status': 1,
            'municipality_id': 3,
            'created_by': 5,
        },
        
        {
            'folio': encode_folio('APO-MULTI-017-2024'),
            'procedure_id': 1,
            'counter': 3005,
            'granted_by_user_id': 5,
            'granted_role': 1,
            'start_date': now - timedelta(days=18),
            'end_date': now + timedelta(days=42),
            'status': 1,
            'municipality_id': 3,
            'created_by': 5,
        },
        
        {
            'folio': encode_folio('APO-MULTI-018-2024'),
            'procedure_id': 1,
            'counter': 3006,
            'granted_by_user_id': 5,
            'granted_role': 1,
            'start_date': now - timedelta(days=16),
            'end_date': now + timedelta(days=44),
            'status': 1,
            'municipality_id': 3,
            'created_by': 5,
        },
        
        # Special characters test case
        {
            'folio': encode_folio('APO-SPECIAL-ñáéíóú-019-2024'),
            'procedure_id': 1,
            'counter': 1008,
            'granted_by_user_id': 2,
            'granted_role': 1,
            'start_date': now - timedelta(days=12),
            'end_date': now + timedelta(days=48),
            'status': 1,
            'municipality_id': 1,
            'created_by': 2,
        },
        
        # Edge case - Same day start and end (very short duration)
        {
            'folio': encode_folio('APO-ONEDAY-020-2024'),
            'procedure_id': 3,
            'counter': 2006,
            'granted_by_user_id': 4,
            'granted_role': 1,
            'start_date': now.replace(hour=8, minute=0, second=0, microsecond=0),
            'end_date': now.replace(hour=18, minute=0, second=0, microsecond=0),
            'status': 1,
            'municipality_id': 2,
            'created_by': 4,
        }
    ]
    
    return test_records

def seed_database():
    """Seed the database with test data"""
    
    try:
        # Get database URL
        database_url = get_database_url()
        print(f"Connecting to database: {database_url}")
        
        # Create engine and session
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        
        print("🌱 Starting database seeding for Provisional Openings...")
        
        # Check if test data already exists
        existing_count = session.query(ProvisionalOpening).filter(
            ProvisionalOpening.folio.like('%APO-%')
        ).count()
        
        if existing_count > 0:
            print(f"⚠️  Found {existing_count} existing test records.")
            print("   Do you want to delete existing test data and re-seed? (y/N): ", end="")
            response = input().strip().lower()
            if response != 'y':
                print("   Skipping seeding.")
                return True
            else:
                # Delete existing test data
                session.query(ProvisionalOpening).filter(
                    ProvisionalOpening.folio.like('%APO-%')
                ).delete()
                session.commit()
                print("   Deleted existing test data.")
        
        # Create test records
        test_records = create_test_data()
        records_added = 0
        
        for record_data in test_records:
            try:
                # Create new record
                record = ProvisionalOpening(**record_data)
                session.add(record)
                records_added += 1
                
                # Decode folio for display
                decoded_folio = base64.b64decode(record_data['folio']).decode()
                print(f"✅ Added: {decoded_folio} (Status: {record_data['status']}, Municipality: {record_data['municipality_id']})")
                
            except Exception as e:
                decoded_folio = base64.b64decode(record_data['folio']).decode() if 'folio' in record_data else 'Unknown'
                print(f"❌ Error adding record {decoded_folio}: {str(e)}")
                continue
        
        # Commit all changes
        session.commit()
        print(f"\n🎉 Successfully seeded {records_added} provisional opening records!")
        
        # Print summary statistics
        total_count = session.query(ProvisionalOpening).count()
        
        active_count = session.query(ProvisionalOpening).filter(
            ProvisionalOpening.status == 1
        ).count()
        
        expired_count = session.query(ProvisionalOpening).filter(
            ProvisionalOpening.status == 0
        ).count()
        
        suspended_count = session.query(ProvisionalOpening).filter(
            ProvisionalOpening.status == 2
        ).count()
        
        cancelled_count = session.query(ProvisionalOpening).filter(
            ProvisionalOpening.status == 3
        ).count()
        
        pending_count = session.query(ProvisionalOpening).filter(
            ProvisionalOpening.status == 4
        ).count()
        
        mun1_count = session.query(ProvisionalOpening).filter(
            ProvisionalOpening.municipality_id == 1
        ).count()
        
        mun2_count = session.query(ProvisionalOpening).filter(
            ProvisionalOpening.municipality_id == 2
        ).count()
        
        mun3_count = session.query(ProvisionalOpening).filter(
            ProvisionalOpening.municipality_id == 3
        ).count()
        
        print(f"\n📊 Database Summary:")
        print(f"   Total Provisional Openings: {total_count}")
        print(f"   Active (Status 1): {active_count}")
        print(f"   Expired (Status 0): {expired_count}")
        print(f"   Suspended (Status 2): {suspended_count}")
        print(f"   Cancelled (Status 3): {cancelled_count}")
        print(f"   Pending (Status 4): {pending_count}")
        print(f"\n   By Municipality:")
        print(f"   Municipality 1 (Guadalajara): {mun1_count}")
        print(f"   Municipality 2 (Zapopan): {mun2_count}")
        print(f"   Municipality 3 (Tlaquepaque): {mun3_count}")
        
        print(f"\n🚀 You can now test the Provisional Openings API endpoints!")
        print(f"   Test endpoints:")
        print(f"   - GET /api/provisional-openings/")
        print(f"   - GET /api/provisional-openings/by_folio/{{base64_folio}}")
        print(f"   - GET /api/provisional-openings/pdf/{{base64_folio}}")
        print(f"   - POST /api/provisional-openings/")
        print(f"   - PATCH /api/provisional-openings/{{id}}")
        print(f"   - DELETE /api/provisional-openings/{{id}}")
        
        print(f"\n📋 Sample Base64 Folios for testing:")
        sample_records = test_records[:5]
        for record in sample_records:
            decoded = base64.b64decode(record['folio']).decode()
            print(f"   - {decoded} → {record['folio']}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        if 'session' in locals():
            session.rollback()
        return False
        
    finally:
        if 'session' in locals():
            session.close()
    
    return True

if __name__ == "__main__":
    print("Provisional Openings Test Data Seeder")
    print("=====================================")
    
    if seed_database():
        print("\n✅ Seeding completed successfully!")
    else:
        print("\n❌ Seeding failed!")
        sys.exit(1)
