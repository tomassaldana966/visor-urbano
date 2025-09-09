#!/usr/bin/env python3
"""
Procedures Test Data Seeder

This script inserts test data into the procedures and historical_procedures tables
for testing the procedures endpoints. It also creates related answer records.
"""

import sys
import os
import asyncio
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.settings import settings

async def create_test_users(session):
    """Create test users in auth_user table if they don't exist"""
    try:
        # Check if we need to create test users
        result = await session.execute(text("SELECT COUNT(*) FROM auth_user WHERE id IN (1, 2, 3, 4)"))
        count = result.scalar()
        
        if count < 4:
            logger.info(f"Creating test users (found {count} of 4 required users)")
            
            # Create test users with IDs 1-4
            await session.execute(text("""
                INSERT INTO auth_user (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
                VALUES 
                (1, 'pbkdf2_sha256$test_hash', FALSE, 'test_user1', 'Juan', 'Pérez', 'juan@test.com', FALSE, TRUE, NOW()),
                (2, 'pbkdf2_sha256$test_hash', FALSE, 'test_user2', 'María', 'González', 'maria@test.com', FALSE, TRUE, NOW()),
                (3, 'pbkdf2_sha256$test_hash', FALSE, 'test_user3', 'Carlos', 'Rodríguez', 'carlos@test.com', FALSE, TRUE, NOW()),
                (4, 'pbkdf2_sha256$test_hash', FALSE, 'test_user4', 'Admin', 'User', 'admin@test.com', TRUE, TRUE, NOW())
                ON CONFLICT (id) DO NOTHING
            """))
            
            # Set sequence to continue after our manually inserted IDs
            await session.execute(text("SELECT setval('auth_user_id_seq', 5, true)"))
            
            await session.commit()
            logger.info("Test users created successfully")
        else:
            logger.info("Test users already exist")
            
    except SQLAlchemyError as e:
        await session.rollback()
        logger.warning(f"Error creating test users: {e}")
        logger.info("Continuing with NULL values for foreign keys")

async def seed_procedures():
    """Seed procedures and historical_procedures test data"""
    # Create database URL
    database_url = f"postgresql+asyncpg://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
    # Create async engine
    engine = create_async_engine(database_url, echo=False)
    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    # Clear existing test data first
    async with async_session() as session:
        try:
            logger.info("Cleaning up existing test data...")
            # Delete from answers table first (due to foreign key constraints)
            await session.execute(text("""
                DELETE FROM answers 
                WHERE procedure_id IN (
                    SELECT id FROM procedures WHERE folio LIKE 'TEST-%'
                )
            """))
            
            # Delete test procedures
            await session.execute(text("""
                DELETE FROM procedures 
                WHERE folio LIKE 'TEST-%' OR folio LIKE 'TEST-NEW-%'
            """))
            
            # Delete test historical procedures
            await session.execute(text("""
                DELETE FROM historical_procedures 
                WHERE folio LIKE 'HIST-%'
            """))
            
            await session.commit()
            logger.info("Existing test data cleanup complete")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Error cleaning up existing test data: {e}")
            # Continue with seeding despite cleanup errors
    
    # Begin seeding new data
    async with async_session() as session:
        try:
            # Create test users to satisfy foreign key constraints
            await create_test_users(session)
            
            # First, check if the upload directory exists and create it if not
            upload_base_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
            upload_dirs = ['payment_orders', 'licenses']
            
            for dir_name in upload_dirs:
                dir_path = os.path.join(upload_base_dir, dir_name)
                if not os.path.exists(dir_path):
                    logger.info(f"Creating directory {dir_path}")
                    os.makedirs(dir_path, exist_ok=True)
            
            # Create dummy placeholder files for file paths mentioned in the SQL
            dummy_files = [
                'uploads/payment_orders/order_test_001.pdf',
                'uploads/payment_orders/order_test_002.pdf',
                'uploads/payment_orders/order_test_003.pdf',
                'uploads/payment_orders/order_test_004.pdf',
                'uploads/payment_orders/order_hist_001.pdf',
                'uploads/payment_orders/order_hist_002.pdf',
                'uploads/payment_orders/order_hist_003.pdf',
                'uploads/licenses/license_test_002.pdf',
                'uploads/licenses/license_hist_001.pdf',
                'uploads/licenses/license_hist_002.pdf',
            ]
            
            for file_path in dummy_files:
                full_path = os.path.join(os.path.dirname(__file__), '..', file_path)
                if not os.path.exists(full_path):
                    dir_name = os.path.dirname(full_path)
                    if not os.path.exists(dir_name):
                        os.makedirs(dir_name, exist_ok=True)
                    with open(full_path, 'w') as f:
                        f.write(f"Dummy file for testing: {os.path.basename(file_path)}")
                    logger.info(f"Created dummy file: {file_path}")
            
            # Insert test procedures directly
            logger.info("Inserting test procedures...")
            
            # Regular procedures
            await session.execute(text("""
                INSERT INTO procedures (
                    folio, current_step, user_signature, user_id, window_user_id, 
                    entry_role, documents_submission_date, procedure_start_date, 
                    window_seen_date, license_delivered_date, has_signature, 
                    official_applicant_name, status, procedure_type, 
                    license_status, payment_order
                ) VALUES 
                ('TEST-001', 2, 'user_signature_data_1', 1, 2, 1, 
                 NOW() - INTERVAL '30 days', NOW() - INTERVAL '29 days', 
                 NOW() - INTERVAL '28 days', NULL, 1, 
                 'Juan Pérez', 1, 'licencia_construccion', 'en_proceso',
                 '/uploads/payment_orders/order_test_001.pdf'),
                ('TEST-002', 4, 'user_signature_data_2', 2, 3, 1, 
                 NOW() - INTERVAL '90 days', NOW() - INTERVAL '89 days', 
                 NOW() - INTERVAL '85 days', NOW() - INTERVAL '30 days', 1,
                 'María González', 2, 'licencia_comercial', 'completado',
                 '/uploads/payment_orders/order_test_002.pdf'),
                ('TEST-003', 3, 'user_signature_data_3', 2, 3, 1,
                 NOW() - INTERVAL '15 days', NOW() - INTERVAL '14 days',
                 NOW() - INTERVAL '12 days', NULL, 1,
                 'María González', 1, 'refrendo', 'en_proceso',
                 '/uploads/payment_orders/order_test_003.pdf'),
                ('TEST-004', 2, 'user_signature_data_4', 3, 4, 1,
                 NOW() - INTERVAL '45 days', NOW() - INTERVAL '44 days',
                 NOW() - INTERVAL '40 days', NULL, 1,
                 'Carlos Rodríguez', 3, 'licencia_construccion', 'rechazado',
                 '/uploads/payment_orders/order_test_004.pdf')
            """))
            
            # Update TEST-003 to point to TEST-002 as the renewed_folio
            await session.execute(text("""
                UPDATE procedures
                SET renewed_folio = 'TEST-002'
                WHERE folio = 'TEST-003'
            """))
            
            # Historical procedures
            logger.info("Inserting historical procedures...")
            await session.execute(text("""
                INSERT INTO historical_procedures (
                    folio, current_step, user_signature, user_id, window_user_id, 
                    entry_role, documents_submission_date, procedure_start_date, 
                    window_seen_date, license_delivered_date, has_signature, 
                    official_applicant_name, status, procedure_type, 
                    license_status, payment_order
                ) VALUES 
                ('HIST-001', 4, 'user_signature_data_hist_1', 1, 2, 1,
                 NOW() - INTERVAL '2 years', NOW() - INTERVAL '2 years', 
                 NOW() - INTERVAL '2 years' + INTERVAL '5 days', 
                 NOW() - INTERVAL '2 years' + INTERVAL '30 days', 1,
                 'Juan Pérez', 2, 'licencia_construccion', 'completado',
                 '/uploads/payment_orders/order_hist_001.pdf'),
                ('HIST-002', 4, 'user_signature_data_hist_2', 2, 3, 1,
                 NOW() - INTERVAL '1 year', NOW() - INTERVAL '1 year',
                 NOW() - INTERVAL '1 year' + INTERVAL '5 days',
                 NOW() - INTERVAL '1 year' + INTERVAL '30 days', 1,
                 'María González', 2, 'licencia_comercial', 'completado',
                 '/uploads/payment_orders/order_hist_002.pdf'),
                ('HIST-003', 2, 'user_signature_data_hist_3', 3, 4, 1,
                 NOW() - INTERVAL '1 year' - INTERVAL '6 months',
                 NOW() - INTERVAL '1 year' - INTERVAL '6 months', 
                 NOW() - INTERVAL '1 year' - INTERVAL '6 months' + INTERVAL '5 days', 
                 NULL, 1,
                 'Carlos Rodríguez', 3, 'licencia_construccion', 'rechazado',
                 '/uploads/payment_orders/order_hist_003.pdf')
            """))
            
            # Get the IDs of the procedures we just inserted
            logger.info("Inserting procedure answers...")
            result = await session.execute(text("SELECT id, folio FROM procedures WHERE folio LIKE 'TEST-%'"))
            proc_ids = {row[1]: row[0] for row in result.fetchall()}
            
            # Debug output
            logger.info(f"Procedure IDs: {proc_ids}")
            
            if 'TEST-001' in proc_ids:
                proc_id = proc_ids['TEST-001']
                await session.execute(text(f"""
                    INSERT INTO answers (procedure_id, name, value, user_id, status)
                    VALUES
                    ({proc_id}, 'construction_type', 'residential', 1, 1),
                    ({proc_id}, 'area_sq_meters', '250', 1, 1),
                    ({proc_id}, 'floors_number', '2', 1, 1),
                    ({proc_id}, 'parking_spaces', '2', 1, 1)
                """))
                logger.info(f"Added answers for TEST-001 (ID: {proc_id})")
            
            if 'TEST-002' in proc_ids:
                proc_id = proc_ids['TEST-002']
                await session.execute(text(f"""
                    INSERT INTO answers (procedure_id, name, value, user_id, status)
                    VALUES
                    ({proc_id}, 'business_name', 'Café La Esquina', 2, 1),
                    ({proc_id}, 'business_type', 'restaurant', 2, 1),
                    ({proc_id}, 'employee_count', '12', 2, 1),
                    ({proc_id}, 'has_liquor_license', 'true', 2, 1)
                """))
                logger.info(f"Added answers for TEST-002 (ID: {proc_id})")
            
            if 'TEST-003' in proc_ids:
                proc_id = proc_ids['TEST-003']
                await session.execute(text(f"""
                    INSERT INTO answers (procedure_id, name, value, user_id, status)
                    VALUES
                    ({proc_id}, 'business_name', 'Café La Esquina', 2, 1),
                    ({proc_id}, 'business_type', 'restaurant', 2, 1),
                    ({proc_id}, 'employee_count', '15', 2, 1),
                    ({proc_id}, 'has_liquor_license', 'true', 2, 1)
                """))
                logger.info(f"Added answers for TEST-003 (ID: {proc_id})")
            
            if 'TEST-004' in proc_ids:
                proc_id = proc_ids['TEST-004']
                await session.execute(text(f"""
                    INSERT INTO answers (procedure_id, name, value, user_id, status)
                    VALUES
                    ({proc_id}, 'construction_type', 'commercial', 3, 1),
                    ({proc_id}, 'area_sq_meters', '450', 3, 1),
                    ({proc_id}, 'floors_number', '3', 3, 1),
                    ({proc_id}, 'parking_spaces', '8', 3, 1)
                """))
                logger.info(f"Added answers for TEST-004 (ID: {proc_id})")
            
            # Get historical procedure IDs
            result = await session.execute(text("SELECT id, folio FROM historical_procedures WHERE folio LIKE 'HIST-%'"))
            hist_ids = {row[1]: row[0] for row in result.fetchall()}
            logger.info(f"Historical procedure IDs: {hist_ids}")
            
            await session.commit()
            logger.info("✅ Procedures test data seeded successfully!")
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Error seeding procedures test data: {e}", exc_info=True)

async def main():
    """Main entry point"""
    await seed_procedures()

if __name__ == "__main__":
    asyncio.run(main())
