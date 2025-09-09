#!/usr/bin/env python3
"""
Fields Seeder Script

This script creates test fields for municipality_id=2 to test the public fields endpoint.
It includes various field types and sequences to demonstrate the functionality.

Run with: python scripts/seed_fields.py
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import SessionLocal
from app.models.field import Field

# Field data for municipality_id=2
FIELD_DATA = [
    {
        "name": "Business Name",
        "field_type": "text",
        "description": "Legal name of the business or establishment",
        "description_rec": "Enter the exact name as it appears on official documents",
        "rationale": "Required for business identification and licensing",
        "sequence": 1,
        "required": 1,
        "municipality_id": 2,
        "step": 1,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Business Email",
        "field_type": "email",
        "description": "Primary email address for business communications",
        "description_rec": "Provide a valid email address that you check regularly",
        "rationale": "Required for official communications and notifications",
        "sequence": 2,
        "required": 1,
        "municipality_id": 2,
        "step": 1,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Business Address",
        "field_type": "textarea",
        "description": "Complete physical address of the business",
        "description_rec": "Include street number, street name, city, state, and postal code",
        "rationale": "Required for location verification and inspections",
        "sequence": 3,
        "required": 1,
        "municipality_id": 2,
        "step": 1,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Number of Employees",
        "field_type": "number",
        "description": "Total number of employees working at this location",
        "description_rec": "Include full-time, part-time, and temporary employees",
        "rationale": "Used to determine safety requirements and permit fees",
        "sequence": 4,
        "required": 1,
        "municipality_id": 2,
        "step": 2,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Business Type",
        "field_type": "select",
        "description": "Primary type of business activity",
        "description_rec": "Select the category that best describes your business",
        "rationale": "Determines applicable regulations and requirements",
        "options": "Restaurant,Retail Store,Office,Manufacturing,Service Provider,Healthcare,Educational,Other",
        "options_description": "Choose from the available business categories",
        "sequence": 5,
        "required": 1,
        "municipality_id": 2,
        "step": 2,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Opening Date",
        "field_type": "date",
        "description": "Planned or actual opening date of the business",
        "description_rec": "Use MM/DD/YYYY format",
        "rationale": "Required for permit validity and inspection scheduling",
        "sequence": 6,
        "required": 1,
        "municipality_id": 2,
        "step": 2,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Has Outdoor Seating",
        "field_type": "boolean",
        "description": "Does the business have outdoor seating or service areas?",
        "description_rec": "Check if your business serves customers in outdoor spaces",
        "rationale": "Additional permits may be required for outdoor operations",
        "sequence": 7,
        "required": 0,
        "municipality_id": 2,
        "step": 3,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Special Requirements",
        "field_type": "textarea",
        "description": "Any special requirements or accommodations needed",
        "description_rec": "Describe any unique aspects of your business operation",
        "rationale": "Helps identify additional permits or inspections needed",
        "sequence": 8,
        "required": 0,
        "municipality_id": 2,
        "step": 3,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 0,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Business Size Category",
        "field_type": "select",
        "description": "Size category of your business",
        "description_rec": "Select based on annual revenue or employee count",
        "rationale": "Different regulations apply to different business sizes",
        "options": "Micro (1-10 employees),Small (11-50 employees),Medium (51-250 employees),Large (250+ employees)",
        "options_description": "Choose the category that matches your business size",
        "sequence": 9,
        "required": 1,
        "municipality_id": 2,
        "step": 3,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Contact Phone",
        "field_type": "text",
        "description": "Primary phone number for business contact",
        "description_rec": "Include area code and extension if applicable",
        "rationale": "Required for emergency contact and official communications",
        "sequence": 10,
        "required": 1,
        "municipality_id": 2,
        "step": 1,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Additional fields for municipality_id=2 (these will be combined with FIELD_DATA)
ADDITIONAL_FIELD_DATA = [
    {
        "name": "Applicant Full Name",
        "field_type": "text",
        "description": "Full legal name of the person applying for the permit",
        "description_rec": "Enter first name, middle name (if any), and last name",
        "rationale": "Required for legal documentation and verification",
        "sequence": 11,  # After the other fields
        "required": 1,
        "municipality_id": 2,
        "step": 4,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Application Date",
        "field_type": "date",
        "description": "Date when the application is being submitted",
        "description_rec": "This will be automatically filled with today's date",
        "rationale": "Required for tracking application processing times",
        "sequence": 12,
        "required": 1,
        "municipality_id": 2,
        "step": 4,
        "status": 1,
        "editable": 0,  # Not editable by user
        "static_field": 1,  # Static field
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "name": "Terms and Conditions Acceptance",
        "field_type": "boolean",
        "description": "I agree to the terms and conditions",
        "description_rec": "Please read and accept the terms and conditions to proceed",
        "rationale": "Legal requirement for application submission",
        "sequence": 13,
        "required": 1,
        "municipality_id": 2,
        "step": 4,
        "status": 1,
        "editable": 1,
        "static_field": 0,
        "required_official": 1,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

async def seed_fields():
    """Seed fields for municipality_id=2."""
    async with SessionLocal() as db:
        try:
            print("🌱 Starting fields seeding...")
            
            # Delete existing fields for municipality_id=2
            print("🗑️  Cleaning existing fields for municipality_id=2...")
            await db.execute(
                delete(Field).where(Field.municipality_id == 2)
            )
            await db.commit()
            print("✅ Existing fields cleaned")
            
            # Combine all field data
            all_field_data = FIELD_DATA + ADDITIONAL_FIELD_DATA
            
            # Add municipality-specific fields
            print(f"📝 Creating {len(all_field_data)} fields for municipality_id=2...")
            for field_data in all_field_data:
                field = Field(**field_data)
                db.add(field)
            
            await db.commit()
            
            # Verify the seeded data
            print("🔍 Verifying seeded data...")
            
            # Count municipality-specific fields
            result = await db.execute(
                select(Field).where(Field.municipality_id == 2)
            )
            municipality_fields = result.scalars().all()
            print(f"✅ Created {len(municipality_fields)} fields for municipality_id=2")
            
            # Display some sample fields
            print("\n📋 Sample created fields:")
            sample_fields = municipality_fields[:5]
            for field in sample_fields:
                print(f"  - {field.name} ({field.field_type}) - Sequence: {field.sequence} - Required: {bool(field.required)}")
            
            if len(municipality_fields) > 5:
                print(f"  ... and {len(municipality_fields) - 5} more fields")
            
            print(f"\n🎉 Fields seeding completed successfully!")
            print(f"📊 Total fields created: {len(municipality_fields)}")
            print(f"🌐 You can now test the public endpoint: GET /municipality/2")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Error during fields seeding: {str(e)}")
            raise

if __name__ == "__main__":
    print("🚀 Field Seeder Script")
    print("======================")
    asyncio.run(seed_fields())
