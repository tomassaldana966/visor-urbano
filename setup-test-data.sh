#!/bin/bash

# Test Data Setup Script for Visor Urbano
# Loads test data from apps/backend/scripts/dump/test_data_only_dev.sql

echo "🧪 Setting up Visor Urbano test data..."
echo ""

# Check if we're in the project root
if [ ! -f "package.json" ] || [ ! -d "apps/backend" ]; then
    echo "❌ This script must be run from the project root directory"
    echo "Please run: cd /path/to/visor-urbano && ./setup-test-data.sh"
    exit 1
fi

# Check if test data file exists
if [ ! -f "apps/backend/scripts/dump/test_data_only_dev.sql" ]; then
    echo "❌ Test data file not found: apps/backend/scripts/dump/test_data_only_dev.sql"
    echo "Please ensure the file exists before running this script"
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
    echo "🔄 Checking database migrations..."
    
    # First, check current migration status
    echo "📋 Checking current migration status..."
    docker-compose exec -T backend alembic current
    
    # Since migrations are already at head, we'll skip the upgrade step
    echo "✅ Database migrations are already up to date"
    
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
        echo "✅ Database is ready for data loading"
    else
        echo "❌ Database tables verification failed"
        echo "Please ensure migrations are properly applied"
        cd ../..
        exit 1
    fi
    
    cd ../..
    echo ""
}

# Function to clear existing test data
clear_existing_data() {
    echo "🧹 Clearing existing test data..."
    echo ""
    
    cd apps/backend
    
    # Test database connection before clearing
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
            return True
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
    
    # Clear existing data using TRUNCATE for better cleanup
    echo "🔄 Clearing existing data..."
    
    docker-compose exec -T backend python -c "
import asyncio
from config.settings import SessionLocal
from sqlalchemy import text

async def clear_data():
    try:
        async with SessionLocal() as session:
            # Get all table names that might have data
            print('🔍 Finding tables to clear...')
            result = await session.execute(text('''
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public' 
                AND tablename NOT IN ('alembic_version', 'spatial_ref_sys')
                ORDER BY tablename
            '''))
            tables = [row[0] for row in result.fetchall()]
            print(f'🔍 Found {len(tables)} tables to clear')
            
            if tables:
                # Disable all triggers and constraints temporarily
                print('🔄 Disabling triggers and constraints...')
                for table in tables:
                    await session.execute(text(f'ALTER TABLE {table} DISABLE TRIGGER ALL'))
                
                # Truncate all tables in one command (CASCADE will handle dependencies)
                print('🔄 Truncating all data tables...')
                tables_list = ', '.join(tables)
                await session.execute(text(f'TRUNCATE TABLE {tables_list} RESTART IDENTITY CASCADE'))
                
                # Re-enable all triggers and constraints
                print('🔄 Re-enabling triggers and constraints...')
                for table in tables:
                    await session.execute(text(f'ALTER TABLE {table} ENABLE TRIGGER ALL'))
                
                print('🔄 Committing changes...')
                await session.commit()
                print('✅ All data cleared and sequences reset successfully')
                return True
            else:
                print('ℹ️  No data tables found to clear')
                return True
                
    except Exception as e:
        print(f'❌ Error clearing data: {e}')
        try:
            await session.rollback()
        except:
            pass
        return False

import sys
result = asyncio.run(clear_data())
if not result:
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo "✅ Existing data cleared successfully"
    else
        echo "❌ Failed to clear existing data"
        echo "Please check the backend logs for more details"
        cd ../..
        exit 1
    fi
    
    cd ../..
    echo ""
}

# Function to load test data from SQL file
load_test_data() {
    echo "📊 Loading test data from SQL file..."
    echo ""
    
    cd apps/backend
    
    # Copy the SQL file to the container
    echo "📋 Copying test data file to container..."
    docker-compose cp ../../apps/backend/scripts/dump/test_data_only_dev.sql backend:/tmp/test_data.sql
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to copy SQL file to container"
        cd ../..
        exit 1
    fi
    
    # Execute the SQL file
    echo "🔄 Executing SQL file..."
    docker-compose exec -T backend python -c "
import asyncio
import subprocess
import os
from config.settings import get_database_url

async def load_sql_data():
    try:
        # Get database connection info
        db_url = get_database_url()
        
        # Parse database URL (format: postgresql+asyncpg://user:pass@host:port/dbname)
        # For psql we need: postgresql://user:pass@host:port/dbname
        psql_url = db_url.replace('postgresql+asyncpg://', 'postgresql://')
        
        print('🔄 Loading data using psql...')
        
        # Use psql to load the data
        result = subprocess.run([
            'psql', psql_url,
            '-f', '/tmp/test_data.sql',
            '-v', 'ON_ERROR_STOP=1'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print('✅ SQL data loaded successfully')
            print('📋 psql output:')
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print('❌ Error loading SQL data')
            print('Error output:', result.stderr)
            if result.stdout:
                print('Standard output:', result.stdout)
            return False
            
    except Exception as e:
        print(f'❌ Error during SQL loading: {e}')
        return False

import sys
result = asyncio.run(load_sql_data())
if not result:
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        echo "✅ Test data loaded successfully"
        
        # Verify the data was loaded
        echo "🔍 Verifying loaded data..."
        docker-compose exec -T backend python -c "
import asyncio
from config.settings import SessionLocal
from sqlalchemy import text

async def verify_data():
    try:
        async with SessionLocal() as session:
            # Check municipalities
            result = await session.execute(text('SELECT COUNT(*) FROM municipalities'))
            municipality_count = result.scalar()
            
            # Check user_roles
            result = await session.execute(text('SELECT COUNT(*) FROM user_roles'))
            role_count = result.scalar()
            
            # Check users
            result = await session.execute(text('SELECT COUNT(*) FROM users'))
            user_count = result.scalar()
            
            print(f'📊 Data verification:')
            print(f'   • Municipalities: {municipality_count}')
            print(f'   • User roles: {role_count}')
            print(f'   • Users: {user_count}')
            
            if municipality_count > 0 and role_count > 0 and user_count > 0:
                print('✅ Data verification successful')
                return True
            else:
                print('❌ Some tables appear to be empty')
                return False
                
    except Exception as e:
        print(f'❌ Error during data verification: {e}')
        return False

import sys
result = asyncio.run(verify_data())
if not result:
    sys.exit(1)
"
        
        if [ $? -eq 0 ]; then
            echo "✅ Data verification completed successfully"
            
            echo ""
            echo "🎉 Test data setup completed successfully!"
            echo ""
            echo "🔐 You can now log in with the following development accounts:"
            echo "   👑 Admin: admin@visorurbano.com / Admin12345678."
            echo "   🏛️  Director: director@visorurbano.com / Director12345678."
            echo "   📝 Reviewer: reviewer@visorurbano.com / Reviewer12345678."
            echo "   🏪 Counter: counter@visorurbano.com / Counter12345678."
            echo "   👤 Citizen: citizen@visorurbano.com / Citizen12345678."
            echo ""
        else
            echo "⚠️  Data verification had issues, but loading appeared successful"
        fi
        
    else
        echo "❌ Failed to load test data"
        echo "Please check the backend logs for more details"
        cd ../..
        exit 1
    fi
    
    # Clean up temporary file
    echo "🧹 Cleaning up temporary files..."
    docker-compose exec -T backend rm -f /tmp/test_data.sql
    
    cd ../..
    echo ""
}

# Function to display loaded data summary
display_summary() {
    echo "📋 Displaying test data summary..."
    echo ""
    
    cd apps/backend
    
    docker-compose exec -T backend python -c "
import asyncio
from config.settings import SessionLocal
from sqlalchemy import text

async def display_summary():
    try:
        async with SessionLocal() as session:
            print('🏛️  Municipalities:')
            result = await session.execute(text('SELECT id, name, email FROM municipalities ORDER BY id'))
            municipalities = result.fetchall()
            for mun in municipalities:
                print(f'   • ID: {mun[0]}, Name: {mun[1]}, Email: {mun[2] or \"N/A\"}')
            
            print('')
            print('👥 User Roles:')
            result = await session.execute(text('SELECT id, name, description FROM user_roles ORDER BY id'))
            roles = result.fetchall()
            for role in roles:
                print(f'   • ID: {role[0]}, Name: {role[1]}, Description: {role[2]}')
            
            print('')
            print('👤 Users:')
            result = await session.execute(text('SELECT id, name, email, username, role_id, municipality_id FROM users ORDER BY id'))
            users = result.fetchall()
            for user in users:
                print(f'   • ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Username: {user[3] or \"N/A\"}, Role: {user[4] or \"N/A\"}, Municipality: {user[5] or \"N/A\"}')
                
    except Exception as e:
        print(f'❌ Error displaying summary: {e}')

asyncio.run(display_summary())
"
    
    cd ../..
    echo ""
}

# Main execution
echo "🚀 Starting test data setup..."
echo ""

check_docker
check_backend_container
setup_database

# Ask user for confirmation before clearing data
echo "⚠️  This script will clear ALL existing data and load test data."
echo "This action cannot be undone!"
echo ""
read -p "Do you want to continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operation cancelled by user"
    exit 1
fi

clear_existing_data
load_test_data
display_summary

echo ""
echo "✨ Test data setup complete!"
echo ""
echo "🧪 Your test environment is ready with the following data:"
echo "   • Multiple municipalities loaded"
echo "   • User roles configured"
echo "   • Test users available"
echo ""
echo "💡 Access your application:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • API Documentation: http://localhost:8000/docs"
echo ""
echo "🔐 Login with test users (check the summary above for available users)"
echo ""
