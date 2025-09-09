#!/usr/bin/env python3
"""
Municipality Creation Script

This script creates a new municipality in the database with the provided information.

Example: ./create_municipality.py "My Municipality" --director "John Doe" --address "123 Main St" --phone "555-1234" --email director@municipality.com"
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import SessionLocal
from app.models.municipality import Municipality


async def create_municipality(
    name: str,
    director: str = None,
    address: str = None,
    phone: str = None,
    email: str = None,
    website: str = None,
    responsible_area: str = None,
    theme_color: str = "#1976d2"
) -> int:
    """Create a new municipality and return its ID."""
    print(f"🏛️  Creating municipality: {name}")
    
    async with SessionLocal() as session:
        try:
            # Check if municipality with same name already exists
            stmt = select(Municipality).where(Municipality.name == name)
            result = await session.execute(stmt)
            existing_municipality = result.scalar_one_or_none()
            
            if existing_municipality:
                print(f"⚠️  Municipality '{name}' already exists with ID: {existing_municipality.id}")
                return existing_municipality.id
            
            # Create new municipality
            municipality_data = {
                "name": name,
                "director": director,
                "address": address,
                "phone": phone,
                "email": email,
                "website": website,
                "responsible_area": responsible_area,
                "theme_color": theme_color,
                "process_sheet": 1,
                "solving_days": 30,
                "issue_license": 0,
                "allow_online_procedures": True,
                "allow_window_reviewer_licenses": True,
                "window_license_generation": 0,
                "initial_folio": 1,
                "has_zoning": False
            }
            
            new_municipality = Municipality(**municipality_data)
            session.add(new_municipality)
            await session.flush()  # Get the ID
            
            municipality_id = new_municipality.id
            
            await session.commit()
            
            print(f"✅ Municipality '{name}' created successfully with ID: {municipality_id}")
            print(f"📋 Municipality details:")
            print(f"   - Name: {name}")
            print(f"   - Director: {director or 'Not specified'}")
            print(f"   - Address: {address or 'Not specified'}")
            print(f"   - Phone: {phone or 'Not specified'}")
            print(f"   - Email: {email or 'Not specified'}")
            print(f"   - Website: {website or 'Not specified'}")
            print(f"   - Responsible Area: {responsible_area or 'Not specified'}")
            print(f"   - Theme Color: {theme_color}")
            
            return municipality_id
            
        except Exception as e:
            print(f"❌ Error creating municipality: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def main():
    """Entry point for the script."""
    parser = argparse.ArgumentParser(description="Create a new municipality")
    parser.add_argument("name", help="Municipality name (required)")
    parser.add_argument("--director", help="Director name")
    parser.add_argument("--address", help="Municipality address")
    parser.add_argument("--phone", help="Phone number")
    parser.add_argument("--email", help="Email address")
    parser.add_argument("--website", help="Website URL")
    parser.add_argument("--responsible-area", help="Responsible area")
    parser.add_argument("--theme-color", default="#1976d2", help="Theme color (hex format, default: #1976d2)")
    
    args = parser.parse_args()
    
    try:
        municipality_id = await create_municipality(
            name=args.name,
            director=args.director,
            address=args.address,
            phone=args.phone,
            email=args.email,
            website=args.website,
            responsible_area=args.responsible_area,
            theme_color=args.theme_color
        )
        print(f"\n✨ Municipality creation completed successfully! Municipality ID: {municipality_id}")
        return municipality_id
    except Exception as e:
        print(f"\n💥 Municipality creation failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
