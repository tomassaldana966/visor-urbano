#!/bin/bash

# Database initialization script for new developers
# This script sets up a complete Visor Urbano database environment

set -e

echo "======================================"
echo "Visor Urbano Database Initialization"
echo "======================================"

# Load environment variables if available
if [ -f ../../.env ]; then
    echo "Loading environment variables from .env..."
    source ../../.env
fi

# Default values
DATABASE_HOST=${DATABASE_HOST:-localhost}
DATABASE_PORT=${DATABASE_PORT:-5432}
DATABASE_NAME=${DATABASE_NAME:-visor_urbano}
DATABASE_USERNAME=${DATABASE_USERNAME:-postgres}
DATABASE_PASSWORD=${DATABASE_PASSWORD:-password}

echo ""
echo "Configuration:"
echo "  Host: $DATABASE_HOST:$DATABASE_PORT"
echo "  Database: $DATABASE_NAME"
echo "  User: $DATABASE_USERNAME"
echo ""

# Check if PostgreSQL is running
echo "Checking PostgreSQL connection..."
if ! pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" > /dev/null 2>&1; then
    echo "❌ Cannot connect to PostgreSQL server"
    echo "Please ensure PostgreSQL is running and accessible"
    exit 1
fi
echo "✅ PostgreSQL is running"

# Set password for psql commands
export PGPASSWORD="$DATABASE_PASSWORD"

# Check if database exists
echo "Checking if database exists..."
if psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" -lqt | cut -d \| -f 1 | grep -qw "$DATABASE_NAME"; then
    echo "⚠️  Database '$DATABASE_NAME' already exists"
    if [ "${AUTO_CONFIRM}" = "true" ]; then
        echo "AUTO_CONFIRM is enabled. Dropping and recreating the database automatically..."
        REPLY="y"
    else
        read -p "Do you want to drop and recreate it? (y/N): " -n 1 -r
        echo
    fi
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Dropping existing database..."
        dropdb -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" "$DATABASE_NAME"
        echo "✅ Database dropped"
    else
        echo "Skipping database creation"
    fi
fi

# Create database if it doesn't exist
if ! psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" -lqt | cut -d \| -f 1 | grep -qw "$DATABASE_NAME"; then
    echo "Creating database..."
    createdb -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" "$DATABASE_NAME"
    echo "✅ Database '$DATABASE_NAME' created"
fi

# Check for existing dump files
DUMP_DIR="./database_dumps"
if [ -d "$DUMP_DIR" ]; then
    LATEST_DUMP=$(ls -t "$DUMP_DIR"/visor_urbano_full_*.sql 2>/dev/null | head -1)
    if [ -n "$LATEST_DUMP" ]; then
        echo "Found database dump: $LATEST_DUMP"
        read -p "Do you want to restore from this dump? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Restoring database from dump..."
            psql -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USERNAME" -d "$DATABASE_NAME" < "$LATEST_DUMP"
            echo "✅ Database restored from dump"
            
            # Unset password
            unset PGPASSWORD
            
            echo ""
            echo "======================================"
            echo "✅ Database initialization completed!"
            echo "======================================"
            echo ""
            echo "Next steps:"
            echo "1. Install Python dependencies: pip install -r requirements.txt"
            echo "2. Run the application: python main.py"
            echo "3. Access the API documentation: http://localhost:8000/docs"
            exit 0
        fi
    fi
fi

# If no dump restoration, run migrations
echo "Setting up database schema with Alembic migrations..."

# Check if Alembic is available
if ! command -v alembic &> /dev/null; then
    echo "❌ Alembic not found. Please install requirements: pip install -r requirements.txt"
    exit 1
fi

# Initialize Alembic if not already done
if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
    echo "No migrations found. Please ensure migrations are available."
    exit 1
fi

# Run migrations
echo "Running database migrations..."
cd ../..
alembic upgrade head
cd scripts/dump

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migration failed"
    exit 1
fi

# Run seeders if available
echo "Checking for seed data..."
if [ -f "../seeder.py" ]; then
    read -p "Do you want to load seed data? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Loading seed data..."
        cd ..
        python seeder.py
        cd dump
        echo "✅ Seed data loaded"
    fi
fi

# Unset password
unset PGPASSWORD

echo ""
echo "======================================"
echo "✅ Database initialization completed!"
echo "======================================"
echo ""
echo "Database is ready! Next steps:"
echo "1. Install Python dependencies: pip install -r requirements.txt"
echo "2. Run the application: python main.py"
echo "3. Access the API documentation: http://localhost:8000/docs"
echo ""
echo "Useful commands:"
echo "- Create database dump: ./create_db_dump.sh"
echo "- Run migrations: alembic upgrade head"
echo "- Check migration status: alembic current"
