#!/usr/bin/env python3
"""
Create a test user for notifications endpoint testing
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.settings import SYNC_DATABASE_URL
from config.security import get_password_hash
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_user():
    """Create test user for notifications testing"""
    
    print("Starting test user creation...")
    
    # Create database connection
    try:
        engine = create_engine(SYNC_DATABASE_URL)
        print(f"Database engine created successfully")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print(f"Session maker created")
    except Exception as e:
        print(f"Error creating database connection: {e}")
        return
    
    with SessionLocal() as db:
        try:
            # Test user configuration
            USER_ID = 29
            USER_EMAIL = "test.user29@visorurbano.com"
            USER_PASSWORD = "testpass123"
            MUNICIPALITY_ID = 2
            
            logger.info(f"Creating test user: {USER_EMAIL}")
            
            # Hash the password
            hashed_password = get_password_hash(USER_PASSWORD)
            
            # Check if user already exists
            check_query = text("SELECT id FROM users WHERE id = :user_id OR email = :email")
            result = db.execute(check_query, {"user_id": USER_ID, "email": USER_EMAIL})
            existing_user = result.fetchone()
            
            if existing_user:
                logger.info(f"User already exists, updating password...")
                # Update existing user
                update_query = text("""
                    UPDATE users 
                    SET password = :password, 
                        updated_at = :updated_at,
                        is_active = true
                    WHERE id = :user_id
                """)
                db.execute(update_query, {
                    "password": hashed_password,
                    "updated_at": datetime.now(),
                    "user_id": USER_ID
                })
            else:
                # Create new user
                insert_query = text("""
                    INSERT INTO users (
                        id, name, paternal_last_name, maternal_last_name, 
                        email, password, cellphone, is_active, 
                        municipality_id, role_id, created_at, updated_at
                    ) VALUES (
                        :id, :name, :paternal_last_name, :maternal_last_name,
                        :email, :password, :cellphone, :is_active,
                        :municipality_id, :role_id, :created_at, :updated_at
                    )
                """)
                
                db.execute(insert_query, {
                    "id": USER_ID,
                    "name": "Test",
                    "paternal_last_name": "User",
                    "maternal_last_name": "Demo",
                    "email": USER_EMAIL,
                    "password": hashed_password,
                    "cellphone": "1234567890",
                    "is_active": True,
                    "municipality_id": MUNICIPALITY_ID,
                    "role_id": 3,  # Regular user role
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                })
            
            db.commit()
            
            logger.info("✅ Test user created/updated successfully!")
            logger.info(f"📧 Email: {USER_EMAIL}")
            logger.info(f"🔑 Password: {USER_PASSWORD}")
            logger.info(f"👤 User ID: {USER_ID}")
            logger.info(f"🏛️  Municipality ID: {MUNICIPALITY_ID}")
            
        except Exception as e:
            logger.error(f"❌ Error creating test user: {e}")
            db.rollback()
            raise

if __name__ == "__main__":
    create_test_user()
