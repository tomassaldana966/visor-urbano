#!/bin/bash
# Test script for procedures API# Extract Historical Procedure ID from the list
# Note: We need to use a valid historical procedure ID from the historical_procedures table
# The regular procedures table may have HIST- folios but they're not the same as historical procedures
HIST_ID=7 # Use the first historical procedure ID from historical_procedures table
echo -e "${GREEN}Using historical procedure ID: ${HIST_ID}${NC}"
# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Base URL
BASE_URL="http://localhost:8000/v1/procedures"

# Print header
echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}       TESTING PROCEDURES API ENDPOINTS       ${NC}"
echo -e "${BLUE}===============================================${NC}"

# Function to encode a string to base64
encode_base64() {
  echo -n "$1" | base64
}

# Function to test an endpoint
test_endpoint() {
  local endpoint=$1
  local method=${2:-GET}
  local data=$3
  local expected_status=${4:-200}
  
  echo -e "\n${YELLOW}Testing ${method} ${endpoint}${NC}"
  
  if [ "$method" = "GET" ]; then
    response=$(curl -s -o response.json -w "%{http_code}" -X ${method} "${BASE_URL}${endpoint}")
  else
    if [ -n "$data" ]; then
      response=$(curl -s -o response.json -w "%{http_code}" -X ${method} "${BASE_URL}${endpoint}" -H "Content-Type: application/json" -d "${data}")
    else
      response=$(curl -s -o response.json -w "%{http_code}" -X ${method} "${BASE_URL}${endpoint}")
    fi
  fi
  
  if [ "$response" -eq "$expected_status" ]; then
    echo -e "${GREEN}✓ Success (HTTP ${response})${NC}"
    echo -e "${BLUE}Response:${NC}"
    cat response.json | jq . || cat response.json
  else
    echo -e "${RED}✗ Failed (Expected HTTP ${expected_status}, got ${response})${NC}"
    echo -e "${RED}Response:${NC}"
    cat response.json | jq . || cat response.json
  fi
}

# 1. List procedures
test_endpoint "/list"

# 2. List procedures with folio filter
test_endpoint "/list?folio=TEST-00"

# 3. List procedures for director review
test_endpoint "/director-review"

# 4. List procedures for window
test_endpoint "/window-list"

# 5. List solvency procedures
test_endpoint "/solvency"

# 6. List license procedures
test_endpoint "/licenses"

# 7. Get procedure history
test_endpoint "/history"

# 8. Get procedure history with folio filter
test_endpoint "/history?folio=TEST-00"

# Get procedure ids from the database first to use in later requests
echo -e "\\n${YELLOW}Fetching procedure IDs for tests...${NC}"
# Fetch all procedures and extract TEST-001 and TEST-003 IDs
echo "Fetching all procedures to extract IDs..."
PROCEDURES_JSON=$(curl -s -X GET "${BASE_URL}/list" -H "accept: application/json")

# Debug: Print the raw JSON output from the curl command
echo "Raw PROCEDURES_JSON output: $PROCEDURES_JSON"

# Extract procedure IDs using jq
# PROCEDURE_IDS=$(echo "$PROCEDURES_JSON" | jq -r '.[] | select(.folio | startswith("TEST-")) | "\\(.folio)=\\(.id)"')
PROCEDURE_IDS=$(echo "$PROCEDURES_JSON" | jq -r '.[] | select(.folio | startswith("TEST-")) | "\(.folio)=\(.id)"')
echo "Raw PROCEDURE_IDS output: $PROCEDURE_IDS" # Keep this for debugging
TEST_001_ID=$(echo "$PROCEDURE_IDS" | grep "TEST-001" | cut -d'=' -f2 | head -n 1)
TEST_003_ID=$(echo "$PROCEDURE_IDS" | grep "TEST-003" | cut -d'=' -f2 | head -n 1)

if [ -z "$TEST_001_ID" ]; then
  echo -e "${RED}Warning: TEST-001 procedure not found in database. Some tests may fail.${NC}"
  TEST_001_ID=1 # Fallback ID
fi

if [ -z "$TEST_003_ID" ]; then
  echo -e "${RED}Warning: TEST-003 procedure not found in database. Some tests may fail.${NC}"
  TEST_003_ID=3 # Fallback ID
fi

echo -e "${GREEN}Using procedure IDs: TEST-001=$TEST_001_ID, TEST-003=$TEST_003_ID${NC}"

# 9. Get applicant name
test_endpoint "/applicant-name/TEST-001" 

# 10. Get applicant name for renewal
test_endpoint "/applicant-name-renewal/TEST-003"

# 11. Get owner name
test_endpoint "/owner-name/TEST-001"

# 12. Get owner data
test_endpoint "/owner-data/TEST-001"

# 13. Get owner data for renewal
test_endpoint "/owner-data-renewal/TEST-003"

# 14. Get procedure answer
test_endpoint "/answer/${TEST_001_ID}/construction_type"

# 15. Continue procedure (using base64 encoded folio)
ENCODED_FOLIO=$(encode_base64 "TEST-001")
test_endpoint "/continue/${ENCODED_FOLIO}" "POST"

# 16. No electronic signature (using base64 encoded folio)
test_endpoint "/no-electronic-signature/${ENCODED_FOLIO}" "POST"

# 17. Copy procedure (using base64 encoded folio)
test_endpoint "/copy/${ENCODED_FOLIO}/1" "POST" "" 201

# 18. Get historical procedure IDs
HIST_IDS=$(curl -s "${BASE_URL}/historical-list" | jq -r '.[] | .id')
echo "Raw HIST_IDS output: $HIST_IDS" # DEBUG LINE
HIST_ID=$(echo "$HIST_IDS" | head -n 1)

if [ -z "$HIST_ID" ]; then
  echo -e "${RED}Warning: No historical procedures found. Using fallback ID.${NC}"
  HIST_ID=1 # Fallback ID
else
  echo -e "${GREEN}Using historical procedure ID: ${HIST_ID}${NC}"
fi

# Copy historical procedure
test_endpoint "/copy-historical/${HIST_ID}" "POST" "" 201

# 19. Test entry of a new procedure
NEW_PROCEDURE='{
  "folio": "TEST-NEW-001",
  "status": 1,
  "official_applicant_name": "New Test User",
  "user_id": 1,
  "window_user_id": 2,
  "entry_role": 1,
  "procedure_type": "licencia_construccion",
  "license_status": "en_proceso"
}'
test_endpoint "/entry" "POST" "$NEW_PROCEDURE" 201

# 20. Test renewal entry
RENEWAL_PROCEDURE='{
  "folio": "TEST-NEW-002",
  "status": 1,
  "official_applicant_name": "Renewal Test User",
  "user_id": 2,
  "window_user_id": 3,
  "entry_role": 1,
  "license_status": "en_proceso",
  "renewed_folio": "TEST-002"
}'
test_endpoint "/renewal-entry" "POST" "$RENEWAL_PROCEDURE" 201

echo -e "\n${BLUE}===============================================${NC}"
echo -e "${BLUE}       API ENDPOINT TESTING COMPLETE          ${NC}"
echo -e "${BLUE}===============================================${NC}"

# Clean up
rm -f response.json
