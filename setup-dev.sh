#!/bin/bash

# Development Setup Script for Visor Urbano
# Creates municipality and seeds development users

echo "🏛️  Setting up Visor Urbano development data..."
echo ""

# Check if we're in the project root
if [ ! -f "package.json" ] || [ ! -d "apps/backend" ]; then
    echo "❌ This script must be run from the project root directory"
    echo "Please run: cd /path/to/visor-urbano && ./setup-dev.sh"
    exit 1
fi

# Function to check if Docker is running
check_docker() {
    echo "🐳 Checking Docker status..."
    if ! command -v docker &> /dev/null; then
        echo ""
        echo "❌ Docker is not installed on your system."
        echo "📥 Please download and install Docker Desktop from:"
        echo "   👉 https://www.docker.com/products/docker-desktop/"
        echo ""
        echo "After installation, please restart this script."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        echo ""
        echo "❌ Docker is installed but not running."
        echo "🔄 Please start Docker Desktop and wait for it to fully load."
        echo ""
        echo "After Docker is running, please restart this script."
        exit 1
    fi

    echo "✅ Docker is running and ready!"
    echo ""
}

# Function to check if backend container is running
check_backend_container() {
    echo "🔍 Checking if backend containers are running..."
    
    cd apps/backend
    
    # Check if containers are running
    if ! docker-compose ps | grep -q "Up"; then
        echo ""
        echo "🚀 Backend containers are not running. Starting them now..."
        echo "This may take a few minutes on first run..."
        echo ""
        
        # Start containers
        docker-compose up -d
        
        # Wait for database to be ready
        echo "⏳ Waiting for database to be ready..."
        sleep 20
        
        # Check if containers are now running
        if ! docker-compose ps | grep -q "Up"; then
            echo "❌ Failed to start backend containers"
            echo "Please check docker-compose.yaml and try again"
            exit 1
        fi
        
        echo "✅ Backend containers are now running"
    else
        echo "✅ Backend containers are already running"
    fi
    
    cd ../..
    echo ""
}

# Function to setup database and run migrations
setup_database() {
    echo "🗄️  Setting up database and running migrations..."
    echo ""
    
    cd apps/backend
    
    # Check if database migrations need to be run
    echo "🔄 Running database migrations..."
    
    # First, check current migration status
    echo "📋 Checking current migration status..."
    docker-compose exec -T backend alembic current
    
    # Run migrations
    docker-compose exec -T backend alembic upgrade head
    
    if [ $? -eq 0 ]; then
        echo "✅ Database migrations completed successfully"
        
        # Wait a moment for the database to be fully ready
        echo "⏳ Waiting for database to stabilize..."
        sleep 5
        
        # Verify tables exist by checking one key table
        echo "🔍 Verifying database tables exist..."
        docker-compose exec -T backend python -c "
import asyncio
from config.settings import SessionLocal
from sqlalchemy import text

async def check_tables():
    try:
        async with SessionLocal() as session:
            # Check if municipalities table exists
            result = await session.execute(text(\"SELECT 1 FROM information_schema.tables WHERE table_name = 'municipalities'\"))
            if result.fetchone():
                print('✅ Database tables verified successfully')
                return True
            else:
                print('❌ Municipality table not found')
                return False
    except Exception as e:
        print(f'❌ Error checking database tables: {e}')
        return False

import sys
result = asyncio.run(check_tables())
if not result:
    sys.exit(1)
"
        
        if [ $? -eq 0 ]; then
            echo "✅ Database is ready for seeding"
        else
            echo "❌ Database tables verification failed"
            echo "🔧 Attempting to create tables manually..."
            
            # Try to create tables using SQLAlchemy
            docker-compose exec -T backend python -c "
import asyncio
from config.settings import Base, engine

async def create_tables():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print('✅ Tables created successfully using SQLAlchemy')
        return True
    except Exception as e:
        print(f'❌ Error creating tables: {e}')
        return False

import sys
result = asyncio.run(create_tables())
if not result:
    sys.exit(1)
"
            
            if [ $? -eq 0 ]; then
                echo "✅ Database tables created successfully"
                
                # Verify tables were actually created
                echo "🔍 Re-verifying tables after manual creation..."
                docker-compose exec -T backend python -c "
import asyncio
from config.settings import SessionLocal
from sqlalchemy import text

async def recheck_tables():
    try:
        async with SessionLocal() as session:
            # Check if municipalities table exists
            result = await session.execute(text(\"SELECT 1 FROM information_schema.tables WHERE table_name = 'municipalities'\"))
            if result.fetchone():
                print('✅ Municipality table confirmed after creation')
                # Also check user_roles table
                result2 = await session.execute(text(\"SELECT 1 FROM information_schema.tables WHERE table_name = 'user_roles'\"))
                if result2.fetchone():
                    print('✅ User roles table confirmed after creation')
                    return True
                else:
                    print('❌ User roles table still missing')
                    return False
            else:
                print('❌ Municipality table still missing after creation')
                return False
    except Exception as e:
        print(f'❌ Error re-checking database tables: {e}')
        return False

import sys
result = asyncio.run(recheck_tables())
if not result:
    sys.exit(1)
"
                
                if [ $? -eq 0 ]; then
                    echo "✅ All required tables confirmed"
                else
                    echo "❌ Tables verification still failing"
                    echo "There may be a database schema or connection issue"
                    cd ../..
                    exit 1
                fi
            else
                echo "❌ Failed to create database tables"
                echo "Please check the backend configuration and try again"
                cd ../..
                exit 1
            fi
        fi
        
    else
        echo "❌ Database migrations failed"
        echo "Please check the backend logs for more details"
        cd ../..
        exit 1
    fi
    
    cd ../..
    echo ""
}

# Function to create municipality and seed users
seed_development_data() {
    echo "👥 Creating development municipality and users..."
    echo ""
    
    cd apps/backend
    
    # Wait a bit more to ensure database is fully ready
    echo "⏳ Ensuring database connection is stable..."
    sleep 3
    
    # Test database connection before seeding
    echo "🔍 Testing database connection..."
    docker-compose exec -T backend python -c "
import asyncio
from config.settings import SessionLocal
from sqlalchemy import text

async def test_connection():
    try:
        async with SessionLocal() as session:
            # Test basic connection
            await session.execute(text('SELECT 1'))
            print('✅ Database connection test successful')
            
            # List all tables to debug
            result = await session.execute(text(\"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name\"))
            tables = [row[0] for row in result.fetchall()]
            print(f'📋 Available tables: {tables}')
            
            if 'municipalities' in tables and 'user_roles' in tables and 'users' in tables:
                print('✅ All required tables are present')
                return True
            else:
                print('❌ Some required tables are missing')
                print(f'   Missing: {[t for t in [\"municipalities\", \"user_roles\", \"users\"] if t not in tables]}')
                return False
    except Exception as e:
        print(f'❌ Database connection test failed: {e}')
        return False

import sys
result = asyncio.run(test_connection())
if not result:
    sys.exit(1)
"
    
    if [ $? -ne 0 ]; then
        echo "❌ Database connection test failed"
        echo "Please check the backend logs and database configuration"
        cd ../..
        exit 1
    fi
    
    # Run the seeder script inside the backend container
    echo "🔄 Running development data seeder..."
    
    # First, copy the temp file into the container, then run it
    docker-compose exec -T backend python -c "
import asyncio
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path('/app')
sys.path.insert(0, str(project_root))

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from config.settings import SessionLocal
from config.security import get_password_hash
from app.models.user import UserModel
from app.models.municipality import Municipality
from app.models.user_roles import UserRoleModel
from datetime import datetime


async def create_development_data():
    \"\"\"Create development municipality and users.\"\"\"
    print('🏛️  Creating development municipality...')
    
    async with SessionLocal() as session:
        try:
            # Check if development municipality already exists
            stmt = select(Municipality).where(Municipality.name == 'Development Municipality')
            result = await session.execute(stmt)
            municipality = result.scalar_one_or_none()
            
            if municipality:
                print(f'ℹ️  Municipality already exists: {municipality.name} (ID: {municipality.id})')
                print('📋 Skipping municipality creation...')
            else:
                # Create development municipality
                municipality = Municipality(
                    name='Development Municipality',
                    director='Development Director',
                    address='123 Development Street, Dev City, DC 12345',
                    phone='+1 (555) 123-4567',
                    email='contact@devmunicipality.com',
                    website='https://devmunicipality.com',
                    responsible_area='Development Department',
                    allow_online_procedures=True,
                    allow_window_reviewer_licenses=True,
                    low_impact_license_cost='$50',
                    theme_color='#2563EB',
                    solving_days=30,
                    issue_license=1,
                    has_zoning=True,
                    initial_folio=1000
                )
                session.add(municipality)
                await session.commit()
                await session.refresh(municipality)
                print(f'✅ Created municipality: {municipality.name} (ID: {municipality.id})')
            
            # Ensure required roles exist
            print('🔧 Ensuring required roles exist...')
            required_roles = [
                {'id': 1, 'name': 'Citizen', 'description': 'Citizen role with basic permissions'},
                {'id': 2, 'name': 'Counter', 'description': 'Counter staff role for basic operations'},
                {'id': 3, 'name': 'Reviewer', 'description': 'Reviewer role for checking submissions'},
                {'id': 4, 'name': 'Director', 'description': 'Director role with administrative permissions'},
                {'id': 5, 'name': 'Admin', 'description': 'Administrator role with full system access'},
                {'id': 6, 'name': 'Technician', 'description': 'Technical role for system maintenance'}
            ]
            
            for role_data in required_roles:
                stmt = select(UserRoleModel).where(UserRoleModel.id == role_data['id'])
                result = await session.execute(stmt)
                existing_role = result.scalar_one_or_none()
                
                if not existing_role:
                    role = UserRoleModel(
                        id=role_data['id'],
                        name=role_data['name'],
                        description=role_data['description']
                    )
                    session.add(role)
                    print(f'✅ Created role: {role_data[\"name\"]}')
                else:
                    print(f'ℹ️  Role already exists: {role_data[\"name\"]}')
            
            await session.commit()
            
            # Create development users
            print('👥 Creating development users...')
            
            dev_users = [
                {
                    'name': 'Admin',
                    'paternal_last_name': 'User',
                    'maternal_last_name': 'Dev',
                    'email': 'admin@visorurbano.com',
                    'password': 'admin123',
                    'cellphone': '+1-555-0001',
                    'role_id': 5,  # Admin
                    'is_staff': True,
                    'is_superuser': True,
                    'username': 'admin'
                },
                {
                    'name': 'Director',
                    'paternal_last_name': 'Manager',
                    'maternal_last_name': 'Dev',
                    'email': 'director@visorurbano.com',
                    'password': 'director123',
                    'cellphone': '+1-555-0002',
                    'role_id': 4,  # Director
                    'is_staff': True,
                    'is_superuser': False,
                    'username': 'director'
                },
                {
                    'name': 'Reviewer',
                    'paternal_last_name': 'Check',
                    'maternal_last_name': 'Dev',
                    'email': 'reviewer@visorurbano.com',
                    'password': 'reviewer123',
                    'cellphone': '+1-555-0003',
                    'role_id': 3,  # Reviewer
                    'is_staff': True,
                    'is_superuser': False,
                    'username': 'reviewer'
                },
                {
                    'name': 'Counter',
                    'paternal_last_name': 'Staff',
                    'maternal_last_name': 'Dev',
                    'email': 'counter@visorurbano.com',
                    'password': 'counter123',
                    'cellphone': '+1-555-0004',
                    'role_id': 2,  # Counter
                    'is_staff': True,
                    'is_superuser': False,
                    'username': 'counter'
                },
                {
                    'name': 'John',
                    'paternal_last_name': 'Citizen',
                    'maternal_last_name': 'Doe',
                    'email': 'citizen@visorurbano.com',
                    'password': 'citizen123',
                    'cellphone': '+1-555-0005',
                    'role_id': 1,  # Citizen
                    'is_staff': False,
                    'is_superuser': False,
                    'username': 'citizen'
                }
            ]
            
            for user_data in dev_users:
                # Check if user already exists
                stmt = select(UserModel).where(UserModel.email == user_data['email'])
                result = await session.execute(stmt)
                existing_user = result.scalar_one_or_none()
                
                if existing_user:
                    print(f'ℹ️  User already exists: {user_data[\"email\"]} - skipping')
                else:
                    user = UserModel(
                        name=user_data['name'],
                        paternal_last_name=user_data['paternal_last_name'],
                        maternal_last_name=user_data['maternal_last_name'],
                        email=user_data['email'],
                        password=get_password_hash(user_data['password']),
                        cellphone=user_data['cellphone'],
                        municipality_id=municipality.id,
                        role_id=user_data['role_id'],
                        is_staff=user_data['is_staff'],
                        is_superuser=user_data['is_superuser'],
                        is_active=True,
                        username=user_data['username'],
                        date_joined=datetime.now()
                    )
                    session.add(user)
                    print(f'✅ Created user: {user_data[\"email\"]} (Role: {user_data[\"role_id\"]})')
            
            await session.commit()
            
            print('')
            print('🎉 Development data creation completed!')
            print('')
            print('📋 Development Users Created:')
            print('  👑 admin@visorurbano.com (password: admin123) - Administrator')
            print('  🏛️  director@visorurbano.com (password: director123) - Director')
            print('  📝 reviewer@visorurbano.com (password: reviewer123) - Reviewer')
            print('  🏪 counter@visorurbano.com (password: counter123) - Counter Staff')
            print('  👤 citizen@visorurbano.com (password: citizen123) - Citizen')
            print('')
            print(f'🏛️  Municipality: {municipality.name} (ID: {municipality.id})')
            print('')
            
        except Exception as e:
            print(f'❌ Error creating development data: {e}')
            await session.rollback()
            sys.exit(1)

asyncio.run(create_development_data())
"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 Development data setup completed successfully!"
        echo ""
        echo "🔐 You can now log in with the following development accounts:"
        echo "   👑 Admin: admin@visorurbano.com / admin123"
        echo "   🏛️  Director: director@visorurbano.com / director123"  
        echo "   📝 Reviewer: reviewer@visorurbano.com / reviewer123"
        echo "   🏪 Counter: counter@visorurbano.com / counter123"
        echo "   👤 Citizen: citizen@visorurbano.com / citizen123"
        echo ""
    else
        echo "❌ Failed to create development data"
        echo "Please check the backend logs for more details"
    fi
    
    cd ../..
}

# Main execution
echo "🚀 Starting development environment setup..."
echo ""

check_docker
check_backend_container
setup_database
seed_development_data

echo ""
echo "✨ Development setup complete!"
echo ""
echo "🌐 Your development environment is ready:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • Database: localhost:5432"
echo ""
echo "💡 To start the full development environment, run:"
echo "   pnpm dev"
echo ""
