#!/bin/bash

# Provisional Openings API Test Script
# Tests all the endpoints for provisional openings

# Configuration
BASE_URL="http://localhost:8000/v1"
API_ENDPOINT="$BASE_URL/provisional_openings"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Function to test HTTP endpoint
test_endpoint() {
    local method=$1
    local url=$2
    local description=$3
    local data=$4
    local expected_status=${5:-200}
    
    echo ""
    print_status "INFO" "Testing: $description"
    echo "Method: $method | URL: $url"
    
    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            -H "Accept: application/json")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            -H "Accept: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq "$expected_status" ]; then
        print_status "SUCCESS" "HTTP $http_code - $description"
        # Pretty print JSON response (first 500 chars)
        echo "Response: $(echo "$body" | cut -c 1-500)..."
    else
        print_status "ERROR" "Expected HTTP $expected_status, got HTTP $http_code - $description"
        echo "Response: $body"
    fi
    
    echo "----------------------------------------"
}

echo "=================================================="
echo "🧪 PROVISIONAL OPENINGS API TEST SUITE"
echo "=================================================="
echo ""

# Check if server is running
print_status "INFO" "Checking if API server is running..."
if ! curl -s "$BASE_URL/docs" > /dev/null 2>&1; then
    print_status "ERROR" "API server is not running at $BASE_URL"
    print_status "INFO" "Please start the server with: uvicorn app.main:app --reload"
    exit 1
fi
print_status "SUCCESS" "API server is running"

# Test 1: Get all provisional openings (default pagination)
test_endpoint "GET" "$API_ENDPOINT/?municipality_id=1" "Get all provisional openings (page 1, default size)"

# Test 2: Get provisional openings with pagination
test_endpoint "GET" "$API_ENDPOINT/?municipality_id=1&page=1&size=5" "Get provisional openings with pagination (5 per page)"

# Test 3: Filter by municipality
test_endpoint "GET" "$API_ENDPOINT/?municipality_id=1" "Filter by municipality ID 1"

# Test 4: Filter by status (active)
test_endpoint "GET" "$API_ENDPOINT/?municipality_id=1&status=1" "Filter by status (active)"

# Test 5: Filter by status (expired)
test_endpoint "GET" "$API_ENDPOINT/?municipality_id=1&status=0" "Filter by status (expired)"

# Test 6: Search by folio pattern
test_endpoint "GET" "$API_ENDPOINT/?municipality_id=1&search=AOD" "Search by folio pattern 'AOD'"

# Test 7: Filter by date range (last 30 days)
end_date=$(date +%Y-%m-%d)
start_date=$(date -v-30d +%Y-%m-%d)
test_endpoint "GET" "$API_ENDPOINT/?municipality_id=1&start_date=$start_date&end_date=$end_date" "Filter by date range (last 30 days)"

# Test 8: Get by folio (Base64 encoded)
# Using the first test folio: AOD-001-2024 -> QU9ELTAwMS0yMDI0
BASE64_FOLIO="QU9ELTAwMS0yMDI0"
test_endpoint "GET" "$API_ENDPOINT/by_folio/$BASE64_FOLIO" "Get by folio (Base64 encoded)"

# Test 9: Get PDF by folio
test_endpoint "GET" "$API_ENDPOINT/pdf/$BASE64_FOLIO" "Generate PDF by folio"

# Test 10: Create new provisional opening
NEW_OPENING_DATA='{
    "folio": "TEST-2024",
    "procedure_id": 1,
    "counter": 9999,
    "granted_by_user_id": 1,
    "granted_role": 1,
    "start_date": "'$(date +%Y-%m-%d)'T08:00:00",
    "end_date": "'$(date -v+90d +%Y-%m-%d)'T18:00:00",
    "status": 1,
    "municipality_id": 1,
    "created_by": 1
}'

test_endpoint "POST" "$API_ENDPOINT/" "Create new provisional opening" "$NEW_OPENING_DATA" 201

# Test 11: Update provisional opening (get the ID first)
print_status "INFO" "Getting latest provisional opening ID for update test..."
latest_response=$(curl -s "$API_ENDPOINT/?municipality_id=1&size=1" -H "Accept: application/json")
latest_id=$(echo "$latest_response" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)

if [ -n "$latest_id" ]; then
    UPDATE_DATA='{
        "status": 2,
        "end_date": "'$(date -v+120d +%Y-%m-%d)'T20:00:00"
    }'
    test_endpoint "PATCH" "$API_ENDPOINT/$latest_id" "Update provisional opening (ID: $latest_id)" "$UPDATE_DATA"
else
    print_status "WARNING" "Could not find provisional opening ID for update test"
fi

# Test 12: Delete provisional opening (soft delete)
if [ -n "$latest_id" ]; then
    test_endpoint "DELETE" "$API_ENDPOINT/$latest_id" "Delete provisional opening (ID: $latest_id)" "" 204
else
    print_status "WARNING" "Could not find provisional opening ID for delete test"
fi

# Test 13: Error cases
echo ""
print_status "INFO" "Testing error cases..."

# Test invalid folio format
test_endpoint "GET" "$API_ENDPOINT/by_folio/invalid-folio" "Get by invalid folio format" "" 400

# Test non-existent folio
test_endpoint "GET" "$API_ENDPOINT/by_folio/bm9uZXhpc3RlbnQ=" "Get by non-existent folio" "" 404

# Test invalid pagination
test_endpoint "GET" "$API_ENDPOINT/?municipality_id=1&page=0" "Invalid pagination (page 0)" "" 422

# Test create with missing required fields
INVALID_DATA='{"folio": "invalid"}'
test_endpoint "POST" "$API_ENDPOINT/" "Create with missing required fields" "$INVALID_DATA" 422

# Test update non-existent ID
test_endpoint "PATCH" "$API_ENDPOINT/99999" "Update non-existent ID" '{"status": 1}' 404

# Test delete non-existent ID
test_endpoint "DELETE" "$API_ENDPOINT/99999" "Delete non-existent ID" "" 404

echo ""
echo "=================================================="
print_status "SUCCESS" "API TEST SUITE COMPLETED"
echo "=================================================="
echo ""
print_status "INFO" "Summary of tests:"
echo "✅ Basic CRUD operations"
echo "✅ Pagination and filtering"
echo "✅ Search functionality"
echo "✅ Base64 folio handling"
echo "✅ PDF generation"
echo "✅ Error handling"
echo ""
print_status "INFO" "For manual testing, you can use:"
echo "curl $API_ENDPOINT/?municipality_id=1"
echo "curl $API_ENDPOINT/by_folio/$BASE64_FOLIO"
echo ""
