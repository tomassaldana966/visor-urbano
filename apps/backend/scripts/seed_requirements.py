#!/usr/bin/env python3
"""
Requirements Seeder Script

This script populates the requirements table with standard business licensing requirements
that are currently hardcoded in the requirements_queries service. It creates requirements
for all existing municipalities and maps them to appropriate fields.

Run with: python scripts/seed_requirements.py
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import select, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import SessionLocal
from app.models.requirements import Requirement
from app.models.field import Field
from app.models.municipality import Municipality

# Standard requirements data that should be in the database instead of hardcoded
STANDARD_REQUIREMENTS = [
    {
        "title": "Official identification of the owner",
        "description": "Present valid official identification (voting card, passport, or professional license).",
        "department_issued": False,
        "field_name": "Official ID",
        "field_type": "file"
    },
    {
        "title": "Property ownership proof", 
        "description": "Document proving legal ownership of the property (public deed, purchase contract, etc.).",
        "department_issued": False,
        "field_name": "Property Ownership Document",
        "field_type": "file"
    },
    {
        "title": "Proof of address",
        "description": "Proof of address no older than 3 months.",
        "department_issued": False,
        "field_name": "Address Proof",
        "field_type": "file"
    },
    {
        "title": "Property tax payment",
        "description": "Updated property tax payment receipt for the current year.",
        "department_issued": False,
        "field_name": "Property Tax Receipt",
        "field_type": "file"
    }
]

async def create_requirement_fields():
    """Create fields for requirements if they don't exist."""
    async with SessionLocal() as db:
        try:
            print("📝 Creating requirement fields...")
            
            # Get all municipalities
            result = await db.execute(select(Municipality))
            municipalities = result.scalars().all()
            
            if not municipalities:
                print("❌ No municipalities found. Please seed municipalities first.")
                return False
            
            fields_created = 0
            
            for municipality in municipalities:
                for req_data in STANDARD_REQUIREMENTS:
                    # Check if field already exists for this municipality
                    existing_field_result = await db.execute(
                        select(Field).where(
                            Field.name == req_data["field_name"],
                            Field.municipality_id == municipality.id
                        )
                    )
                    existing_field = existing_field_result.scalar_one_or_none()
                    
                    if not existing_field:
                        # Create the field
                        field = Field(
                            name=req_data["field_name"],
                            field_type=req_data["field_type"],
                            description=req_data["description"],
                            description_rec=f"Required: {req_data['description']}",
                            rationale="Required for business license application",
                            sequence=fields_created + 1,
                            required=1,
                            municipality_id=municipality.id,
                            step=1,
                            status=1,
                            editable=1,
                            static_field=0,
                            required_official=1,
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        db.add(field)
                        fields_created += 1
                        print(f"  ✅ Created field '{req_data['field_name']}' for {municipality.name}")
            
            await db.commit()
            print(f"📋 Created {fields_created} requirement fields")
            return True
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Error creating requirement fields: {str(e)}")
            return False

async def seed_requirements():
    """Seed standard requirements for all municipalities."""
    async with SessionLocal() as db:
        try:
            print("🌱 Starting requirements seeding...")
            
            # Clean existing requirements
            print("🗑️  Cleaning existing requirements...")
            await db.execute(delete(Requirement))
            await db.commit()
            print("✅ Existing requirements cleaned")
            
            # Get all municipalities
            result = await db.execute(select(Municipality))
            municipalities = result.scalars().all()
            
            if not municipalities:
                print("❌ No municipalities found. Please seed municipalities first.")
                return
            
            print(f"🏛️  Found {len(municipalities)} municipalities")
            
            requirements_created = 0
            
            # Create requirements for each municipality
            for municipality in municipalities:
                print(f"\n📝 Creating requirements for {municipality.name} (ID: {municipality.id})")
                
                for req_data in STANDARD_REQUIREMENTS:
                    # Find the corresponding field for this requirement
                    field_result = await db.execute(
                        select(Field).where(
                            Field.name == req_data["field_name"],
                            Field.municipality_id == municipality.id
                        )
                    )
                    field = field_result.scalar_one_or_none()
                    
                    if field:
                        # Create the requirement
                        requirement = Requirement(
                            municipality_id=municipality.id,
                            field_id=field.id,
                            requirement_code=f"REQ-{municipality.id}-{field.id}",
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        db.add(requirement)
                        requirements_created += 1
                        print(f"  ✅ Created requirement: {req_data['title']}")
                    else:
                        print(f"  ⚠️  Field '{req_data['field_name']}' not found for {municipality.name}")
            
            await db.commit()
            
            # Verify the seeded data
            print("\n🔍 Verifying seeded data...")
            
            total_requirements_result = await db.execute(select(Requirement))
            total_requirements = len(total_requirements_result.scalars().all())
            
            print(f"✅ Created {requirements_created} requirements")
            print(f"📊 Total requirements in database: {total_requirements}")
            
            # Show summary by municipality
            print("\n📋 Requirements summary by municipality:")
            for municipality in municipalities:
                muni_req_result = await db.execute(
                    select(Requirement).where(Requirement.municipality_id == municipality.id)
                )
                muni_requirements = muni_req_result.scalars().all()
                print(f"  🏛️  {municipality.name}: {len(muni_requirements)} requirements")
            
            print(f"\n🎉 Requirements seeding completed successfully!")
            print(f"📊 Total requirements created: {requirements_created}")
            print(f"🔗 Requirements are now linked to fields in the database")
            print(f"📄 Next step: Update the requirements service to use database data")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Error during requirements seeding: {str(e)}")
            raise

async def main():
    """Main seeder function."""
    print("🚀 Requirements Seeder Script")
    print("=============================")
    
    # First create the required fields
    fields_success = await create_requirement_fields()
    if not fields_success:
        print("❌ Failed to create requirement fields. Aborting.")
        return
    
    # Then create the requirements
    await seed_requirements()

if __name__ == "__main__":
    asyncio.run(main())
