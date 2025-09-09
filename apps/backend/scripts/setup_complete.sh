#!/bin/bash
# Complete setup script to ensure everything is in order

set -e

echo "🚀 Starting complete Visor Urbano Backend setup"
echo "=" * 60

# 1. Verify database connectivity
echo "1️⃣  Verifying database connectivity..."
python -c "
import asyncio
from sqlalchemy import text
from config.settings import engine

async def test_connection():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text('SELECT version()'))
            version = result.scalar()
            print(f'✅ PostgreSQL connected: {version[:50]}...')
        await engine.dispose()
        return True
    except Exception as e:
        print(f'❌ Connection error: {e}')
        return False

success = asyncio.run(test_connection())
exit(0 if success else 1)
"

# 2. Create automatic migration if necessary
echo -e "\n2️⃣  Generating automatic migrations..."
alembic revision --autogenerate -m "Auto-setup missing models" || {
    echo "⚠️  Could not generate automatic migrations (may be normal if everything is up to date)"
}

# 3. Apply all migrations
echo -e "\n3️⃣  Applying migrations..."
alembic upgrade head

# 4. Verify that all models are present
echo -e "\n4️⃣  Verifying models and schema..."
python scripts/verify_models.py

# 5. Create basic data if it doesn't exist
echo -e "\n5️⃣  Verifying basic data..."
python -c "
import asyncio
from sqlalchemy import text
from config.settings import SessionLocal

async def setup_basic_data():
    async with SessionLocal() as session:
        # Verify municipalities
        result = await session.execute(text('SELECT COUNT(*) FROM municipalities'))
        municipality_count = result.scalar()
        
        if municipality_count == 0:
            print('📦 Creating development municipality...')
            await session.execute(text('''
                INSERT INTO municipalities (name, director, address, phone, email, has_zoning, initial_folio)
                VALUES ('Development Municipality', 'Development Director', 
                       'Main Street 123', '+52 123 456 7890', 
                       'contact@municipality.dev', true, 1000)
            '''))
            await session.commit()
            print('✅ Development municipality created')
        else:
            print(f'✅ Existing municipalities: {municipality_count}')
        
        # Verify roles
        result = await session.execute(text('SELECT COUNT(*) FROM user_roles'))
        roles_count = result.scalar()
        
        if roles_count == 0:
            print('📦 Creating basic roles...')
            roles = [
                (1, 'Citizen', 'Citizen with basic permissions'),
                (2, 'Counter', 'Counter staff'),
                (3, 'Reviewer', 'Procedure reviewer'),
                (4, 'Director', 'Municipal director'),
                (5, 'Admin', 'System administrator')
            ]
            for role_id, name, description in roles:
                await session.execute(text('''
                    INSERT INTO user_roles (id, name, description)
                    VALUES (:id, :name, :description)
                    ON CONFLICT (id) DO NOTHING
                '''), {'id': role_id, 'name': name, 'description': description})
            await session.commit()
            print('✅ Basic roles created')
        else:
            print(f'✅ Existing roles: {roles_count}')

asyncio.run(setup_basic_data())
"

echo -e "\n✅ Complete setup finished!"
echo "🎉 The backend is ready to use"
echo -e "\n📋 Next steps:"
echo "   - Run: uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo "   - Access: http://localhost:8000/docs to view the API"
