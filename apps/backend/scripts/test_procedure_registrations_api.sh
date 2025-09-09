#!/bin/bash

# Procedure Registrations API Test Script
# Tests all endpoints for procedure_registrations

# Configuration
BASE_URL="http://localhost:8000/v1"
API_ENDPOINT="$BASE_URL/procedure_registrations"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored status messages
print_status() {
    local status=$1
    local message=$2
    case $status in
        "SUCCESS") echo -e "${GREEN}✅ SUCCESS:${NC} $message" ;;
        "ERROR") echo -e "${RED}❌ ERROR:${NC} $message" ;;
        "INFO") echo -e "${BLUE}ℹ️  INFO:${NC} $message" ;;
        "WARNING") echo -e "${YELLOW}⚠️  WARNING:${NC} $message" ;;
    esac
}

# Generic endpoint tester
test_endpoint() {
    local method=$1
    local url=$2
    local desc=$3
    local data=${4:-}
    local expected=${5:-200}

    print_status "INFO" "Testing: $desc"
    echo "Method: $method | URL: $url"

    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$url" \
            -H "Content-Type: application/json" \
            -d "$data")
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$url" \
            -H "Accept: application/json")
    fi

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq "$expected" ]; then
        print_status "SUCCESS" "HTTP $http_code - $desc"
        echo "Response: $(echo "$body" | cut -c1-200)..."
    else
        print_status "ERROR" "Expected $expected, got $http_code - $desc"
        echo "Response: $body"
    fi
    echo "----------------------------------------"
}

# Ensure server is running
print_status "INFO" "Checking API server"
if ! curl -s "$BASE_URL/docs" > /dev/null; then
    print_status "ERROR" "Server not running at $BASE_URL"
    exit 1
fi
print_status "SUCCESS" "API server is up"

echo "\n===== PROCEDURE_REGISTRATIONS API TESTS ====="

# 1. List records
test_endpoint GET "$API_ENDPOINT/" "List all records"

# 2. List with geometry
test_endpoint GET "$API_ENDPOINT/geometry" "List records with geometry"

# 3. Get non-existing
test_endpoint GET "$API_ENDPOINT/999999" "Get non-existent record" "" 404

# 4. Create new record
CREATE_PAYLOAD='{"area": 123.45, "reference": "REF-API-1", "business_sector": "Test", "procedure_type": "API", "procedure_origin": "Script", "municipality_id": 1}'
resp=$(curl -s -w "\n%{http_code}" -X POST "$API_ENDPOINT/" \
    -H "Content-Type: application/json" \
    -d "$CREATE_PAYLOAD")
code=$(echo "$resp" | tail -n1)
body=$(echo "$resp" | sed '$d')
if [ "$code" -eq 200 ] || [ "$code" -eq 201 ]; then
    print_status "SUCCESS" "Created record"
    # extract id
    NEW_ID=$(echo "$body" | sed -E 's/.*"id"[[:space:]]*:[[:space:]]*([0-9]+).*/\1/')
    echo "New ID: $NEW_ID"
else
    print_status "ERROR" "Create failed with HTTP $code"
    echo "$body"
    exit 1
fi

echo "----------------------------------------"

# 5. Get created record
test_endpoint GET "$API_ENDPOINT/$NEW_ID" "Get created record"

# 6. Update record
UPDATE_PAYLOAD='{"business_sector": "UpdatedSector"}'
test_endpoint PATCH "$API_ENDPOINT/$NEW_ID" "Update record business_sector" "$UPDATE_PAYLOAD"

# 7. Update geometry properties
GEOM_PAYLOAD='{"properties": {"giro": "GeomSector", "area": 321.0, "folio": "REF-API-1", "municipio": 2}}'
test_endpoint PATCH "$API_ENDPOINT/geometry/$NEW_ID" "Update geometry properties" "$GEOM_PAYLOAD"

# 8. Delete record
test_endpoint DELETE "$API_ENDPOINT/$NEW_ID" "Delete record"

# 9. Confirm deletion
test_endpoint GET "$API_ENDPOINT/$NEW_ID" "Get deleted record" "" 404

echo "All tests completed."