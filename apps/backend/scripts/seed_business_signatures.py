#!/usr/bin/env python3
"""
Business Signatures Seeder
Creates test data for business signatures for development and testing
"""

import asyncio
import base64
import hashlib
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# Add the parent directory to the path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from config.settings import engine, get_session
from app.models.business_signatures import BusinessSignature
from app.models.auth_user import AuthUser
from app.models.procedures import Procedure


def get_utc_naive_now():
    """Get current UTC datetime as naive (for consistency with database storage)"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class BusinessSignatureSeeder:
    """Seeder class for business signatures"""
    
    def __init__(self):
        self.session: AsyncSession = None
    
    async def get_db_session(self):
        """Get database session"""
        self.session = AsyncSession(engine)
    
    async def cleanup_existing_data(self):
        """Remove existing test business signatures"""
        try:
            # Delete existing test business signatures
            delete_stmt = delete(BusinessSignature).where(
                BusinessSignature.response.op('->>')('test_data') == 'true'
            )
            result = await self.session.execute(delete_stmt)
            await self.session.commit()
            
            deleted_count = result.rowcount
            print(f"✓ Deleted {deleted_count} existing test business signatures")
            
        except Exception as e:
            print(f"✗ Error cleaning up existing data: {e}")
            await self.session.rollback()
            raise
    
    async def get_test_users(self) -> list:
        """Get test users for seeding"""
        try:
            query = select(AuthUser).limit(5)
            result = await self.session.execute(query)
            users = result.scalars().all()
            
            if not users:
                print("⚠ No users found. Please run user seeder first.")
                return []
            
            print(f"✓ Found {len(users)} users for business signature seeding")
            return users
            
        except Exception as e:
            print(f"✗ Error getting test users: {e}")
            return []
    
    async def get_test_procedures(self) -> list:
        """Get test procedures for seeding"""
        try:
            query = select(Procedure).limit(10)
            result = await self.session.execute(query)
            procedures = result.scalars().all()
            
            if not procedures:
                print("⚠ No procedures found. Business signatures will use dummy procedure IDs.")
                return []
            
            print(f"✓ Found {len(procedures)} procedures for business signature seeding")
            return procedures
            
        except Exception as e:
            print(f"✗ Error getting test procedures: {e}")
            return []
    
    def generate_test_signatures_data(self, users: list, procedures: list) -> list:
        """Generate test business signatures data"""
        test_curps = [
            "ABCD123456HDFRRL09",
            "XYZW654321MDFGGR08", 
            "JUAN850315HDFRNT02",
            "MARIA900420MDFRMR05",
            "CARLOS751010HDFRRL01"
        ]
        
        test_chains = [
            "chain_comercial_license_data_to_sign",
            "chain_industrial_permit_data_to_sign",
            "chain_restaurant_license_data_to_sign",
            "chain_retail_permit_data_to_sign",
            "chain_service_license_data_to_sign"
        ]
        
        test_signatures_data = []
        
        for i in range(min(15, len(users) * 3)):  # Create up to 15 signatures
            user = users[i % len(users)]
            procedure_id = procedures[i % len(procedures)].id if procedures else (i % 10) + 1
            curp = test_curps[i % len(test_curps)]
            chain = test_chains[i % len(test_chains)]
            
            # Generate different types of test signatures
            signature_types = [
                "business_license_application",
                "permit_renewal", 
                "license_modification",
                "regulatory_compliance",
                "inspection_certification"
            ]
            
            signature_type = signature_types[i % len(signature_types)]
            
            # Create realistic signed hash (Base64 encoded)
            hash_input = f"{curp}_{chain}_{get_utc_naive_now().isoformat()}"
            signed_hash = base64.b64encode(
                hashlib.sha256(hash_input.encode()).digest()
            ).decode()
            
            # Create response metadata
            response_data = {
                "signed_hash": signed_hash,
                "generated_at": get_utc_naive_now().isoformat(),
                "curp": curp,
                "procedure_id": procedure_id,
                "procedure_part": signature_type,
                "cert_filename": f"certificate_{i+1}.cer",
                "key_filename": f"private_key_{i+1}.key",
                "signature_type": signature_type,
                "test_data": "true",  # Mark as test data
                "seeder_version": "1.0"
            }
            
            signature_data = {
                "procedure_id": procedure_id,
                "user_id": user.id,
                "role": getattr(user, 'role_id', 1),
                "hash_to_sign": chain,
                "signed_hash": signed_hash,
                "response": response_data,
                "created_at": get_utc_naive_now(),
                "updated_at": get_utc_naive_now()
            }
            
            test_signatures_data.append(signature_data)
        
        return test_signatures_data
    
    async def create_business_signatures(self, signatures_data: list):
        """Create business signatures in database"""
        try:
            created_signatures = []
            
            for signature_data in signatures_data:
                signature = BusinessSignature(**signature_data)
                self.session.add(signature)
                created_signatures.append(signature)
            
            await self.session.commit()
            
            # Refresh to get IDs
            for signature in created_signatures:
                await self.session.refresh(signature)
            
            print(f"✓ Created {len(created_signatures)} business signatures")
            return created_signatures
            
        except Exception as e:
            print(f"✗ Error creating business signatures: {e}")
            await self.session.rollback()
            raise
    
    async def verify_seeded_data(self):
        """Verify that the seeded data was created correctly"""
        try:
            # Count test business signatures
            query = select(BusinessSignature).where(
                BusinessSignature.response.op('->>')('test_data') == 'true'
            )
            result = await self.session.execute(query)
            signatures = result.scalars().all()
            
            print(f"✓ Verification: Found {len(signatures)} test business signatures in database")
            
            # Show sample data
            if signatures:
                sample = signatures[0]
                print(f"  - Sample signature ID: {sample.id}")
                print(f"  - Procedure ID: {sample.procedure_id}")
                print(f"  - User ID: {sample.user_id}")
                print(f"  - CURP: {sample.response.get('curp', 'N/A')}")
                print(f"  - Signature type: {sample.response.get('signature_type', 'N/A')}")
                print(f"  - Created at: {sample.created_at}")
            
            return len(signatures)
            
        except Exception as e:
            print(f"✗ Error verifying seeded data: {e}")
            return 0
    
    async def run_seeder(self, cleanup: bool = True):
        """Run the complete seeding process"""
        print("🌱 Starting Business Signatures Seeder...")
        print("=" * 50)
        
        try:
            await self.get_db_session()
            
            if cleanup:
                await self.cleanup_existing_data()
            
            # Get test data dependencies
            users = await self.get_test_users()
            procedures = await self.get_test_procedures()
            
            if not users:
                print("❌ Cannot proceed without users. Please run user seeder first.")
                return False
            
            # Generate test data
            signatures_data = self.generate_test_signatures_data(users, procedures)
            print(f"✓ Generated {len(signatures_data)} business signature records")
            
            # Create business signatures
            await self.create_business_signatures(signatures_data)
            
            # Verify
            count = await self.verify_seeded_data()
            
            print("=" * 50)
            print(f"🎉 Business Signatures Seeder completed successfully!")
            print(f"📊 Total business signatures created: {count}")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ Seeder failed: {e}")
            if self.session:
                await self.session.rollback()
            return False
        
        finally:
            if self.session:
                await self.session.close()


async def main():
    """Main function to run the seeder"""
    print("Business Signatures Seeder")
    print("This will create test business signatures for development/testing")
    
    # Check command line arguments
    cleanup = True
    if len(sys.argv) > 1 and sys.argv[1] == "--no-cleanup":
        cleanup = False
        print("⚠ Running without cleanup (existing test data will be preserved)")
    
    seeder = BusinessSignatureSeeder()
    success = await seeder.run_seeder(cleanup=cleanup)
    
    if success:
        print("\n✅ Business signatures seeding completed successfully!")
        print("\nYou can now:")
        print("- Test business signature endpoints")
        print("- Run business signature tests")
        print("- Use test data for development")
    else:
        print("\n❌ Business signatures seeding failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
