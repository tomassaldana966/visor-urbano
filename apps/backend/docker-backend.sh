#!/bin/bash
set -e

echo "Database is ready. Running migrations..."

export PGPASSWORD="$DATABASE_PASSWORD"
echo "Using database: $DATABASE_HOST:$DATABASE_PORT/$DATABASE_NAME as $DATABASE_USERNAME"

echo "Setting up migrations directory structure..."
mkdir -p /app/migrations/versions
touch /app/migrations/__init__.py
touch /app/migrations/versions/__init__.py
chmod -R 777 /app/migrations

# Check if alembic.ini exists in the container
if [ ! -f "/app/alembic.ini" ]; then
  echo "Copying alembic.ini from mounted volume..."
  cp /app/migrations/alembic.ini /app/alembic.ini 2>/dev/null || echo "No alembic.ini found in migrations directory"
fi

# Check if users table exists
USERS_TABLE_EXISTS=$(psql -h $DATABASE_HOST -U $DATABASE_USERNAME -d $DATABASE_NAME -t -c "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='users')" | xargs)
echo "Users table exists: $USERS_TABLE_EXISTS"

# Count existing tables (excluding system tables)
TABLES_EXIST=$(psql -h $DATABASE_HOST -U $DATABASE_USERNAME -d $DATABASE_NAME -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_name NOT IN ('spatial_ref_sys', 'alembic_version')" | xargs)
echo "Number of tables in database: $TABLES_EXIST"

if [ "$USERS_TABLE_EXISTS" != "t" ]; then
  echo "Users table does not exist. Creating tables..."
  
  # First, create an initial migration if needed
  MIGRATION_FILES=$(find /app/migrations/versions -name "*.py" ! -name "__init__.py" | wc -l)
  if [ "$MIGRATION_FILES" -eq 0 ]; then
    echo "No migration files found. Creating initial migration..."
    cd /app && alembic revision --autogenerate -m "Initial database setup"
  fi
  
  # Apply migrations
  echo "Applying migrations to create tables..."
  cd /app && alembic upgrade head || {
    echo "Migration failed. This can happen if tables already exist partially."
    echo "Attempting to create tables directly with SQLAlchemy..."
    
    # Create tables directly using SQLAlchemy
    python3 -c "
import asyncio
import sys
import os
sys.path.append('/app')

try:
    from config.settings import Base, engine
    from app.models import *
    
    async def create_tables():
        try:
            async with engine.begin() as conn:
                print('Dropping existing tables if any...')
                await conn.run_sync(Base.metadata.drop_all)
                print('Creating all tables...')
                await conn.run_sync(Base.metadata.create_all)
            await engine.dispose()
            print('✅ Tables created successfully with SQLAlchemy')
        except Exception as e:
            print(f'❌ Error creating tables: {e}')
            raise

    asyncio.run(create_tables())
except Exception as e:
    print(f'❌ Failed to import or create tables: {e}')
    sys.exit(1)
    " && {
      echo "✅ SQLAlchemy table creation successful. Stamping database..."
      cd /app && alembic stamp head
    } || {
      echo "SQLAlchemy table creation also failed. Marking database as stamped and continuing..."
      cd /app && alembic stamp head
    }
  }

  # Verify users table was created
  USERS_TABLE_CREATED=$(psql -h $DATABASE_HOST -U $DATABASE_USERNAME -d $DATABASE_NAME -t -c "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='users')" | xargs)
  
  if [ "$USERS_TABLE_CREATED" = "t" ]; then
    echo "Tables successfully created!"
  else
    echo "Tables not created by Alembic or SQLAlchemy. Checking available tables..."
    psql -h $DATABASE_HOST -U $DATABASE_USERNAME -d $DATABASE_NAME -c "\dt"
    
    echo "Stamping database with current migration..."
    cd /app && alembic stamp head
  fi
else
  echo "Users table already exists. Running any pending migrations..."
  cd /app && alembic upgrade head
fi

# Verificar que todos los modelos estén presentes
echo "🔍 Verificando integridad del esquema de base de datos..."
cd /app && python scripts/verify_models.py || {
  echo "⚠️  Problemas detectados en el esquema. Creando modelos faltantes..."
  
  # Crear migración automática para modelos faltantes
  echo "🔧 Generando migración automática para modelos faltantes..."
  alembic revision --autogenerate -m "Auto-fix missing models" || true
  
  # Aplicar la migración
  echo "📦 Aplicando migración automática..."
  alembic upgrade head || {
    echo "❌ Error al aplicar migración automática"
    echo "🚨 ADVERTENCIA: Algunas tablas pueden estar faltando"
  }
  
  # Verificar nuevamente
  echo "🔍 Verificación final..."
  python scripts/verify_models.py || {
    echo "⚠️  Aún hay problemas en el esquema, pero continuando..."
  }
}

echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000