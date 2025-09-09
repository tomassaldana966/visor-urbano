#!/bin/bash

# Script to validate complete API-Storybook-Swagger integration
# Author: Visor Urbano Team
# Description: Verifies that all services are working correctly
            echo -e "${YELLOW}⚠️ EMPTY${NC}"
        fi
    else
        echo -e "${RED}❌ DOES NOT EXIST${NC}"
    fi

echo "🔍 Validating API-Storybook-Swagger integration..."

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# URLs a validar
BACKEND_URL="http://localhost:8000"
SWAGGER_URL="http://localhost:8000/docs"
REDOC_URL="http://localhost:8000/redoc"
FRONTEND_URL="http://localhost:3000"
STORYBOOK_URL="http://localhost:6006"
DOCS_URL="http://localhost:3001"

# Function to verify if a service is running
check_service() {
    local url="$1"
    local name="$2"
    
    echo -n "   Verifying $name... "
    
    if curl -s --max-time 5 "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        return 1
    fi
}

# Function to verify specific endpoint
check_endpoint() {
    local url="$1"
    local name="$2"
    
    echo -n "   Verifying endpoint $name... "
    
    response=$(curl -s -w "%{http_code}" --max-time 5 "$url" 2>/dev/null)
    http_code="${response: -3}"
    
    if [[ "$http_code" =~ ^[2-3][0-9][0-9]$ ]]; then
        echo -e "${GREEN}✅ OK (${http_code})${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED (${http_code})${NC}"
        return 1
    fi
}

# Contador de servicios funcionando
services_ok=0
total_services=6

echo ""
echo -e "${BLUE}📊 Verifying main services...${NC}"

# Backend
if check_service "$BACKEND_URL/health" "Backend API"; then
    ((services_ok++))
fi

# Swagger
if check_service "$SWAGGER_URL" "Swagger Documentation"; then
    ((services_ok++))
fi

# ReDoc
if check_service "$REDOC_URL" "ReDoc Documentation"; then
    ((services_ok++))
fi

# Frontend
if check_service "$FRONTEND_URL" "Frontend Application"; then
    ((services_ok++))
fi

# Storybook
if check_service "$STORYBOOK_URL" "Storybook Components"; then
    ((services_ok++))
fi

# Documentation
if check_service "$DOCS_URL" "Docusaurus Documentation"; then
    ((services_ok++))
fi

echo ""
echo -e "${BLUE}🛣️ Verifying critical endpoints...${NC}"

# Critical backend endpoints
endpoints=(
    "$BACKEND_URL/v1/health:Health Check"
    "$BACKEND_URL/v1/business-licenses/:Business Licenses"
    "$BACKEND_URL/v1/auth/me:Auth Status"
    "$BACKEND_URL/v1/map/layers:Map Layers"
)

endpoint_ok=0
for endpoint_info in "${endpoints[@]}"; do
    IFS=':' read -r endpoint_url endpoint_name <<< "$endpoint_info"
    if check_endpoint "$endpoint_url" "$endpoint_name"; then
        ((endpoint_ok++))
    fi
done

echo ""
echo -e "${BLUE}📚 Verifying documentation files...${NC}"

# Critical documentation files
docs_files=(
    "$PROJECT_ROOT/visor-urbano-docs/docs/development/api-integration.md"
    "$PROJECT_ROOT/visor-urbano-docs/docs/development/generated-api-integration.md"
    "$PROJECT_ROOT/visor-urbano-docs/docs/development/setup-integration.md"
    "$PROJECT_ROOT/visor-urbano-docs/docs/development/README.md"
)

docs_ok=0
for doc_file in "${docs_files[@]}"; do
    filename=$(basename "$doc_file")
    echo -n "   Verifying $filename... "
    
    if [[ -f "$doc_file" ]]; then
        # Verify that the file is not empty and has valid content
        if [[ -s "$doc_file" ]] && grep -q "^#" "$doc_file"; then
            echo -e "${GREEN}✅ OK${NC}"
            ((docs_ok++))
        else
            echo -e "${YELLOW}⚠️ EMPTY${NC}"
        fi
    else
        echo -e "${RED}❌ NO EXISTE${NC}"
    fi
done

echo ""
echo -e "${BLUE}🔗 Verifying links in documentation...${NC}"

# Verify that internal links work
doc_main="$PROJECT_ROOT/visor-urbano-docs/docs/development/api-integration.md"
if [[ -f "$doc_main" ]]; then
    # Extract localhost links from file
    localhost_links=$(grep -oE "http://localhost:[0-9]{4}[^)]*" "$doc_main" 2>/dev/null || true)
    
    if [[ -n "$localhost_links" ]]; then
        link_ok=0
        total_links=0
        
        while IFS= read -r link; do
            if [[ -n "$link" ]]; then
                ((total_links++))
                echo -n "   Verifying link $(echo "$link" | cut -d'/' -f3)... "
                
                if curl -s --max-time 3 "$link" > /dev/null 2>&1; then
                    echo -e "${GREEN}✅ OK${NC}"
                    ((link_ok++))
                else
                    echo -e "${RED}❌ FAILED${NC}"
                fi
            fi
        done <<< "$localhost_links"
        
        echo "   Working links: $link_ok/$total_links"
    else
        echo "   No localhost links found to verify"
    fi
else
    echo -e "   ${RED}❌ Main documentation file not found${NC}"
fi

echo ""
echo -e "${BLUE}📁 Verifying file structure...${NC}"

# Verify critical structure
structure_items=(
    "$PROJECT_ROOT/scripts/generate-api-docs.sh:Generation script"
    "$PROJECT_ROOT/visor-urbano-docs/src/components/ApiIntegrationTable.tsx:Integration component"
    "$PROJECT_ROOT/apps/frontend/app/routes:Frontend routes"
    "$PROJECT_ROOT/apps/backend/app/routers:Backend routers"
)

structure_ok=0
for item_info in "${structure_items[@]}"; do
    IFS=':' read -r item_path item_name <<< "$item_info"
    echo -n "   Verifying $item_name... "
    
    if [[ -e "$item_path" ]]; then
        echo -e "${GREEN}✅ OK${NC}"
        ((structure_ok++))
    else
        echo -e "${RED}❌ DOES NOT EXIST${NC}"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}📊 Validation Summary${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Calculate general percentage
total_checks=$((services_ok + endpoint_ok + docs_ok + structure_ok))
max_checks=$((total_services + ${#endpoints[@]} + ${#docs_files[@]} + ${#structure_items[@]}))
percentage=$((total_checks * 100 / max_checks))

echo "🔧 Working services: $services_ok/$total_services"
echo "🛣️ Working endpoints: $endpoint_ok/${#endpoints[@]}"
echo "📚 Valid documents: $docs_ok/${#docs_files[@]}"
echo "📁 Correct structure: $structure_ok/${#structure_items[@]}"
echo ""
echo -n "🎯 General status: "

if [[ $percentage -ge 90 ]]; then
    echo -e "${GREEN}$percentage% - ✅ EXCELLENT${NC}"
elif [[ $percentage -ge 75 ]]; then
    echo -e "${YELLOW}$percentage% - ⚠️ GOOD (some improvements needed)${NC}"
elif [[ $percentage -ge 50 ]]; then
    echo -e "${YELLOW}$percentage% - ⚠️ PARTIAL (requires attention)${NC}"
else
    echo -e "${RED}$percentage% - ❌ CRITICAL (requires immediate solution)${NC}"
fi

echo ""
echo -e "${BLUE}🔗 Quick links:${NC}"
echo "   🎨 Storybook: $STORYBOOK_URL"
echo "   📡 Swagger: $SWAGGER_URL"
echo "   📖 Documentation: $DOCS_URL"
echo "   🚀 Frontend: $FRONTEND_URL"

echo ""
if [[ $percentage -ge 90 ]]; then
    echo -e "${GREEN}🎉 All ready for development!${NC}"
else
    echo -e "${YELLOW}💡 Run './scripts/setup-dev-environment.sh' to fix issues${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
