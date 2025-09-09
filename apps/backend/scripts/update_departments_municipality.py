#!/usr/bin/env python3
"""
Script to update existing departments to the correct municipality
"""

import asyncio
import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import SessionLocal
from app.models.departments import Department
from sqlalchemy.future import select

async def update_departments():
    async with SessionLocal() as db:
        try:
            # Update existing departments to be in municipality 2
            result = await db.execute(select(Department))
            departments = result.scalars().all()
            
            print(f'Found {len(departments)} existing departments:')
            for dept in departments:
                print(f'  - {dept.name} (code: {dept.code}, municipality: {dept.municipality_id})')
                dept.municipality_id = 2
                
            await db.commit()
            print('✅ Departments updated to municipality ID 2')
            
        except Exception as e:
            print(f"❌ Error updating departments: {e}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(update_departments())
