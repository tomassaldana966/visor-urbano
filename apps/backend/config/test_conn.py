import sys
import os

# Add the parent directory to the sys.path to allow importing from config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config.settings import settings

DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("Connection to the database was successful!")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()