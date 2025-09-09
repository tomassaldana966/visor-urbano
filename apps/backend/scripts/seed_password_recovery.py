#!/usr/bin/env python3
"""
Password Recovery Seeder Script

This script creates test data for password recovery functionality.
It generates users and password recovery tokens for testing purposes.

Usage:
    python scripts/seed_password_recovery.py [--count COUNT] [--expired] [--used]

Options:
    --count COUNT    Number of password recovery records to create (default: 10)
    --expired        Create expired tokens for testing
    --used           Create used tokens for testing
    --cleanup        Remove all existing password recovery records
"""

import asyncio
import argparse
import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from config.settings import SessionLocal
from app.models.user import UserModel
from app.models.recover_password import PasswordRecovery
from config.security import get_password_hash


class PasswordRecoverySeeder:
    def __init__(self):
        self.session = None

    async def setup_session(self):
        """Initialize database session"""
        self.session = SessionLocal()

    async def cleanup_session(self):
        """Clean up database session"""
        if self.session:
            await self.session.close()

    async def cleanup_password_recoveries(self):
        """Remove all existing password recovery records"""
        print("🧹 Cleaning up existing password recovery records...")
        
        result = await self.session.execute(delete(PasswordRecovery))
        await self.session.commit()
        
        print(f"✅ Removed all password recovery records")

    async def create_test_users(self, count: int = 5):
        """Create test users if they don't exist"""
        print(f"👥 Creating {count} test users...")
        
        users_created = 0
        test_users = []
        
        for i in range(count):
            email = f"test_user_{i+1}@example.com"
            
            # Check if user already exists
            stmt = select(UserModel).where(UserModel.email == email)
            result = await self.session.execute(stmt)
            existing_user = result.scalars().first()
            
            if not existing_user:
                user = UserModel(
                    email=email,
                    password=get_password_hash(f"password123_{i+1}"),
                    name=f"Test User {i+1}",
                    paternal_last_name=f"LastName{i+1}",
                    cellphone=f"123456789{i}",
                    is_active=True
                )
                self.session.add(user)
                users_created += 1
            else:
                user = existing_user
            
            test_users.append(user)
        
        if users_created > 0:
            await self.session.commit()
            print(f"✅ Created {users_created} new test users")
        else:
            print("ℹ️  All test users already exist")
        
        return test_users

    async def create_valid_tokens(self, users: list, count: int = 10):
        """Create valid password recovery tokens"""
        print(f"🔑 Creating {count} valid password recovery tokens...")
        
        tokens_created = 0
        
        for i in range(count):
            user = users[i % len(users)]
            
            token = PasswordRecovery(
                email=user.email,
                token=str(uuid4()),
                expiration_date=PasswordRecovery.get_expiration_time(24),  # Valid for 24 hours
                used=0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.session.add(token)
            tokens_created += 1
        
        await self.session.commit()
        print(f"✅ Created {tokens_created} valid tokens")

    async def create_expired_tokens(self, users: list, count: int = 5):
        """Create expired password recovery tokens"""
        print(f"⏰ Creating {count} expired password recovery tokens...")
        
        tokens_created = 0
        
        for i in range(count):
            user = users[i % len(users)]
            
            # Create tokens that expired 1-24 hours ago
            hours_ago = 1 + (i % 24)
            
            token = PasswordRecovery(
                email=user.email,
                token=str(uuid4()),
                expiration_date=datetime.utcnow() - timedelta(hours=hours_ago),
                used=0,
                created_at=datetime.utcnow() - timedelta(hours=hours_ago + 1),
                updated_at=datetime.utcnow() - timedelta(hours=hours_ago + 1)
            )
            
            self.session.add(token)
            tokens_created += 1
        
        await self.session.commit()
        print(f"✅ Created {tokens_created} expired tokens")

    async def create_used_tokens(self, users: list, count: int = 3):
        """Create used password recovery tokens"""
        print(f"✅ Creating {count} used password recovery tokens...")
        
        tokens_created = 0
        
        for i in range(count):
            user = users[i % len(users)]
            
            token = PasswordRecovery(
                email=user.email,
                token=str(uuid4()),
                expiration_date=PasswordRecovery.get_expiration_time(24),
                used=1,  # Mark as used
                created_at=datetime.utcnow() - timedelta(hours=2),
                updated_at=datetime.utcnow() - timedelta(hours=1)  # Updated when used
            )
            
            self.session.add(token)
            tokens_created += 1
        
        await self.session.commit()
        print(f"✅ Created {tokens_created} used tokens")

    async def create_rate_limit_tokens(self, users: list, count: int = 2):
        """Create recent tokens for rate limiting tests"""
        print(f"⏱️  Creating {count} recent tokens for rate limiting tests...")
        
        tokens_created = 0
        
        for i in range(count):
            user = users[i % len(users)]
            
            # Create tokens that were created 2-4 minutes ago (within 5-minute rate limit)
            minutes_ago = 2 + (i % 3)
            
            token = PasswordRecovery(
                email=user.email,
                token=str(uuid4()),
                expiration_date=PasswordRecovery.get_expiration_time(24),
                used=0,
                created_at=datetime.utcnow() - timedelta(minutes=minutes_ago),
                updated_at=datetime.utcnow() - timedelta(minutes=minutes_ago)
            )
            
            self.session.add(token)
            tokens_created += 1
        
        await self.session.commit()
        print(f"✅ Created {tokens_created} recent tokens for rate limiting tests")

    async def display_summary(self):
        """Display summary of created data"""
        print("\n📊 Password Recovery Data Summary:")
        print("=" * 50)
        
        # Count users
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        user_count = len(result.scalars().all())
        print(f"👥 Total Users: {user_count}")
        
        # Count password recovery tokens by status
        stmt = select(PasswordRecovery)
        result = await self.session.execute(stmt)
        all_tokens = result.scalars().all()
        
        valid_tokens = [t for t in all_tokens if t.is_valid()]
        expired_tokens = [t for t in all_tokens if t.is_expired() and t.used == 0]
        used_tokens = [t for t in all_tokens if t.used == 1]
        
        print(f"🔑 Valid Tokens: {len(valid_tokens)}")
        print(f"⏰ Expired Tokens: {len(expired_tokens)}")
        print(f"✅ Used Tokens: {len(used_tokens)}")
        print(f"📝 Total Tokens: {len(all_tokens)}")
        
        # Show some example tokens
        if valid_tokens:
            print(f"\n🔍 Example Valid Token:")
            token = valid_tokens[0]
            print(f"   Email: {token.email}")
            print(f"   Token: {token.token}")
            print(f"   Expires: {token.expiration_date}")

    async def seed(self, count: int = 10, include_expired: bool = False, 
                   include_used: bool = False, cleanup: bool = False):
        """Main seeding method"""
        try:
            await self.setup_session()
            
            print("🌱 Starting Password Recovery Seeder...")
            print("=" * 50)
            
            if cleanup:
                await self.cleanup_password_recoveries()
            
            # Create test users first
            users = await self.create_test_users(max(5, count // 2))
            
            # Create valid tokens
            await self.create_valid_tokens(users, count)
            
            # Create rate limit test tokens
            await self.create_rate_limit_tokens(users, 2)
            
            if include_expired:
                await self.create_expired_tokens(users, max(3, count // 3))
            
            if include_used:
                await self.create_used_tokens(users, max(2, count // 5))
            
            await self.display_summary()
            
            print("\n🎉 Password Recovery seeding completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during seeding: {str(e)}")
            if self.session:
                await self.session.rollback()
            raise
        finally:
            await self.cleanup_session()


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Seed password recovery test data")
    parser.add_argument("--count", type=int, default=10, 
                       help="Number of password recovery records to create")
    parser.add_argument("--expired", action="store_true", 
                       help="Include expired tokens")
    parser.add_argument("--used", action="store_true", 
                       help="Include used tokens")
    parser.add_argument("--cleanup", action="store_true", 
                       help="Clean up existing data before seeding")
    
    args = parser.parse_args()
    
    seeder = PasswordRecoverySeeder()
    await seeder.seed(
        count=args.count,
        include_expired=args.expired,
        include_used=args.used,
        cleanup=args.cleanup
    )


if __name__ == "__main__":
    asyncio.run(main())
