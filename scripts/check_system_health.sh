#!/bin/bash

# Script to quickly verify the system model status
# Location: /scripts/check_system_health.sh

echo "🚀 Checking Visor Urbano system status..."
echo "================================================"

# Change to backend directory
cd "$(dirname "$0")/../apps/backend"

# 1. Verify that containers are running
echo "📦 Docker containers status:"
docker-compose ps

echo ""
echo "🔍 Verifying database model integrity..."

# 2. Run model verification
docker-compose exec backend python scripts/verify_models.py

VERIFICATION_EXIT_CODE=$?

echo ""
echo "🌐 Verifying API access..."

# 3. Verify that API responds
API_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs || echo "000")

if [ "$API_RESPONSE" = "200" ]; then
    echo "✅ Backend API responds correctly"
    echo "📖 Documentation available at: http://localhost:8000/docs"
else
    echo "❌ Backend API not responding (HTTP $API_RESPONSE)"
fi

echo ""
echo "📊 Healthcheck summary:"
echo "================================================"

if [ $VERIFICATION_EXIT_CODE -eq 0 ] && [ "$API_RESPONSE" = "200" ]; then
    echo "🎉 ✅ SYSTEM FULLY FUNCTIONAL"
    echo "   - Database: ✅ All tables present"
    echo "   - Backend API: ✅ Responding correctly"
    echo "   - Models: ✅ Verified and complete"
else
    echo "⚠️  ❌ ISSUES DETECTED"
    
    if [ $VERIFICATION_EXIT_CODE -ne 0 ]; then
        echo "   - Database: ❌ Problems in model verification"
    fi
    
    if [ "$API_RESPONSE" != "200" ]; then
        echo "   - Backend API: ❌ Not responding correctly"
    fi
    
    echo ""
    echo "🔧 Commands to diagnose:"
    echo "   docker-compose logs backend --tail=50"
    echo "   docker-compose restart backend"
    echo "   docker-compose exec backend python scripts/verify_models.py"
fi

echo ""
echo "📝 For more information, see:"
echo "   📖 /docs/SISTEMA_VERIFICACION_MODELOS.md"
echo "   📖 /apps/backend/docs/MODELO_VERIFICATION.md"
