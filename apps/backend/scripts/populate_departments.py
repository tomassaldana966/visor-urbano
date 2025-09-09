#!/usr/bin/env python3
"""
Script to populate initial department data and configurations
for the dependency management system.
"""

import asyncio
import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import SessionLocal
from app.models.departments import Department, DepartmentRole, RequirementDepartmentAssignment
from app.models.municipality import Municipality  
from app.models.user_roles import UserRoleModel
from app.models.field import Field
from app.services.department_service import DepartmentService


async def populate_departments():
    """Populate initial departments for testing"""
    
    async with SessionLocal() as db:
        try:
            print("🏢 Populating test departments...")
            
            # Search for municipality with ID 2 specifically
            from sqlalchemy.future import select
            municipality_result = await db.execute(select(Municipality).where(Municipality.id == 2))
            municipality = municipality_result.scalar_one_or_none()
            
            if not municipality:
                print("❌ Municipality with ID 2 not found. Searching for any municipality...")
                municipality_result = await db.execute(select(Municipality).limit(1))
                municipality = municipality_result.scalar_one_or_none()
                
                if not municipality:
                    print("❌ No municipality found. Creating a test municipality...")
                    municipality = Municipality(
                        name="Test Municipality",
                        state="Test State", 
                        director="Test Director"
                    )
                    db.add(municipality)
                    await db.commit()
                    await db.refresh(municipality)
            
            print(f"📍 Using municipality: {municipality.name} (ID: {municipality.id})")
            
            # Create test departments
            departments_data = [
                {
                    "name": "Public Works Department",
                    "code": "DOP",
                    "description": "Responsible for reviewing construction and public works projects",
                    "municipality_id": municipality.id,
                    "is_active": True
                },
                {
                    "name": "Urban Development Department", 
                    "code": "DDU",
                    "description": "Responsible for zoning and land use",
                    "municipality_id": municipality.id,
                    "is_active": True
                },
                {
                    "name": "Commercial Licenses Department",
                    "code": "DLC", 
                    "description": "Responsible for commercial operating licenses",
                    "municipality_id": municipality.id,
                    "is_active": True
                },
                {
                    "name": "Civil Protection Department",
                    "code": "DPC",
                    "description": "Responsible for safety and civil protection measures",
                    "municipality_id": municipality.id,
                    "is_active": True
                },
                {
                    "name": "Environmental Department",
                    "code": "DMA",
                    "description": "Responsible for environmental impact and sustainability",
                    "municipality_id": municipality.id,
                    "is_active": True
                }
            ]
            
            created_departments = []
            for dept_data in departments_data:
                # Check if it already exists
                existing = await db.execute(
                    select(Department).where(
                        Department.code == dept_data["code"],
                        Department.municipality_id == municipality.id
                    )
                )
                if existing.scalar_one_or_none():
                    print(f"⚠️  Department {dept_data['code']} already exists, skipping...")
                    continue
                
                department = Department(**dept_data)
                db.add(department)
                created_departments.append(department)
                print(f"✅ Created department: {dept_data['name']} ({dept_data['code']})")
            
            await db.commit()
            
            # Refresh to get IDs
            for dept in created_departments:
                await db.refresh(dept)
            
            print(f"🎉 {len(created_departments)} departments created successfully!")
            
            # Search for existing roles 
            roles_result = await db.execute(select(UserRoleModel))
            roles = roles_result.scalars().all()
            
            if roles:
                print(f"🔐 Found {len(roles)} available roles:")
                for role in roles:
                    print(f"   - {role.name} (ID: {role.id})")
            else:
                print("⚠️  No roles found in the system")
            
            # Search for existing fields
            fields_result = await db.execute(select(Field))
            fields = fields_result.scalars().all()
            
            if fields:
                print(f"📋 Found {len(fields)} available fields:")
                for field in fields[:5]:  # Show only the first 5
                    print(f"   - {field.name} (ID: {field.id})")
                if len(fields) > 5:
                    print(f"   ... and {len(fields) - 5} more fields")
            else:
                print("⚠️  No fields found in the system")
                
            print("\n🚀 Initial data populated successfully!")
            print("💡 You can now use the /v1/director/departments endpoints to manage departments")
            
        except Exception as e:
            print(f"❌ Error populating data: {str(e)}")
            await db.rollback()
            raise


if __name__ == "__main__":
    print("🔄 Starting department data population...")
    asyncio.run(populate_departments())
