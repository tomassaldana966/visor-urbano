#!/usr/bin/env python3
"""
Test Users Seeder Script

This script creates 6 test users with specific roles for the FastAPI backend.
Each user will have:
- Email format: user{role_id}@@bloombergcities.jhu.edu
- Password: BloombergcitiesTest2025.
- municipality_id: specified by parameter (default: 2)
- role_id: 1-6 respectively

If users with the same role_id already exist, they will be deleted first.
"""

import asyncio
import sys
import os
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import SessionLocal
from config.security import get_password_hash
from app.models.user import UserModel
from app.models.user_roles import UserRoleModel
from app.models.user_roles_assignments import UserRoleAssignment


async def create_required_roles(session: AsyncSession, municipality_id: int):
    """Create the required roles if they don't exist."""
    print("🔧 Ensuring required roles exist...")
    
    # Define the required roles (translated to English)
    required_roles = [
        {"id": 1, "name": "Citizen", "description": "Citizen role with basic permissions"},
        {"id": 2, "name": "Counter", "description": "Counter staff role for basic operations"},
        {"id": 3, "name": "Reviewer", "description": "Reviewer role for checking submissions"},
        {"id": 4, "name": "Director", "description": "Director role with administrative permissions"},
        {"id": 5, "name": "Admin", "description": "Administrator role with full system access"},
        {"id": 6, "name": "Technician", "description": "Technical role for system maintenance"}
    ]
    
    for role_data in required_roles:
        # Check if role exists
        stmt = select(UserRoleModel).where(UserRoleModel.id == role_data["id"])
        result = await session.execute(stmt)
        existing_role = result.scalar_one_or_none()
        
        if not existing_role:
            # Create the role with specific ID
            new_role = UserRoleModel(
                id=role_data["id"],
                name=role_data["name"],
                description=role_data["description"],
                municipality_id=municipality_id  # Use dynamic municipality_id
            )
            session.add(new_role)
            print(f"✅ Created role: {role_data['name']} (ID: {role_data['id']})")
        else:
            # Update existing role name if different
            if existing_role.name != role_data["name"]:
                existing_role.name = role_data["name"]
                existing_role.description = role_data["description"]
                print(f"🔄 Updated role: {role_data['name']} (ID: {role_data['id']})")
            else:
                print(f"ℹ️  Role already exists: {role_data['name']} (ID: {role_data['id']})")
    
    await session.commit()
    print("✅ All required roles are ready")


async def create_or_update_test_users(session: AsyncSession, municipality_id: int):
    """Create or update test users with role_id 1-6."""
    print("🔧 Creating or updating test users with role_id 1-6...")
    
    # Hash the password
    hashed_password = get_password_hash("BloombergcitiesTest2025.")
    
    # Define role names for user names (English translations)
    ROLE_NAMES = {
        1: "Citizen",
        2: "Counter", 
        3: "Reviewer",
        4: "Director",
        5: "Admin",
        6: "Technician"
    }
    
    created_or_updated_users = []
    
    for role_id in range(1, 7):
        email = f"user{role_id}@@bloombergcities.jhu.edu"
        role_name = ROLE_NAMES.get(role_id, f"User{role_id}")
        
        # Check if user already exists
        stmt = select(UserModel).where(UserModel.email == email)
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            # Update existing user
            existing_user.password = hashed_password
            existing_user.role_id = role_id
            existing_user.municipality_id = municipality_id  # Use dynamic municipality_id
            existing_user.is_active = True
            print(f"🔄 Updated existing user: {email} (role: {role_name}, role_id: {role_id})")
            created_or_updated_users.append(existing_user)
        else:
            # Create new user
            user_data = {
                "name": f"Test{role_name}",
                "paternal_last_name": "DeliveryAssociates",
                "maternal_last_name": "User",
                "cellphone": f"555-000-{role_id:04d}",
                "email": email,
                "password": hashed_password,
                "municipality_id": municipality_id,  # Use dynamic municipality_id
                "role_id": role_id,
                "username": f"test{role_name.lower()}{role_id}",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False
            }
            
            new_user = UserModel(**user_data)
            session.add(new_user)
            print(f"✅ Created new user: {email} (role: {role_name}, role_id: {role_id})")
            created_or_updated_users.append(new_user)
    
    await session.flush()  # Get user IDs for new users
    return created_or_updated_users


async def ensure_role_assignments(session: AsyncSession, users):
    """Ensure role assignments exist for all users."""
    print("🔧 Ensuring role assignments...")
    
    for user in users:
        # Check if role assignment exists
        stmt = select(UserRoleAssignment).where(UserRoleAssignment.user_id == user.id)
        result = await session.execute(stmt)
        existing_assignment = result.scalar_one_or_none()
        
        if existing_assignment:
            # Update existing assignment
            existing_assignment.role_id = user.role_id
            existing_assignment.role_status = "active"
            print(f"🔄 Updated role assignment for user {user.email}")
        else:
            # Create new assignment
            role_assignment = UserRoleAssignment(
                user_id=user.id,
                role_id=user.role_id,
                role_status="active"
            )
            session.add(role_assignment)
            print(f"✅ Created role assignment for user {user.email}")


async def delete_existing_test_users(session: AsyncSession):
    """Delete existing users with role_id 1-6 to avoid conflicts."""
    print("🗑️  Deleting existing test users with role_id 1-6...")
    
    # Delete user role assignments first (foreign key constraint)
    delete_assignments_stmt = delete(UserRoleAssignment).where(
        UserRoleAssignment.user_id.in_(
            select(UserModel.id).where(UserModel.role_id.in_([1, 2, 3, 4, 5, 6]))
        )
    )
    await session.execute(delete_assignments_stmt)
    
    # Delete users with role_id 1-6
    delete_users_stmt = delete(UserModel).where(UserModel.role_id.in_([1, 2, 3, 4, 5, 6]))
    result = await session.execute(delete_users_stmt)
    
    print(f"✅ Deleted {result.rowcount} existing test users")
    await session.commit()


async def seed_test_users(municipality_id: int = 2):
    """Main function to seed test users."""
    print(f"🌱 Starting test users seeding process for municipality_id: {municipality_id}...")
    
    async with SessionLocal() as session:
        try:
            # First, ensure all required roles exist
            await create_required_roles(session, municipality_id)
            
            # Create or update test users (no deletion to avoid foreign key conflicts)
            users = await create_or_update_test_users(session, municipality_id)
            
            # Ensure role assignments exist for all users
            await ensure_role_assignments(session, users)
            
            # Commit all changes
            await session.commit()
            
            print(f"\n🎉 Successfully processed {len(users)} test users!")
            print("\n📋 Summary of users:")
            print("-" * 80)
            print(f"{'Email':<35} {'Role':<12} {'Role ID':<8} {'Municipality ID'}")
            print("-" * 80)
            
            role_names = {
                1: "Citizen", 2: "Counter", 3: "Reviewer", 
                4: "Director", 5: "Admin", 6: "Technician"
            }
            
            for user in users:
                role_name = role_names.get(user.role_id, f"Role{user.role_id}")
                print(f"{user.email:<35} {role_name:<12} {user.role_id:<8} {user.municipality_id}")
            
            print("-" * 80)
            print("Password for all users: BloombergcitiesTest2025.")
            print("\n✨ Special note: user4@@bloombergcities.jhu.edu IS A DIRECTOR! ✨")
                
        except Exception as e:
            print(f"❌ Error during seeding: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def main():
    """Entry point for the script."""
    parser = argparse.ArgumentParser(description="Seed test users for FastAPI backend")
    parser.add_argument(
        "--municipality-id", 
        type=int, 
        default=2,
        help="Municipality ID to assign to all test users (default: 2)"
    )
    
    args = parser.parse_args()
    
    try:
        await seed_test_users(municipality_id=args.municipality_id)
        print(f"\n✨ Test users seeding completed successfully for municipality ID: {args.municipality_id}!")
    except Exception as e:
        print(f"\n💥 Seeding failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
