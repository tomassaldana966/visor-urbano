#!/bin/bash

# Comprehensive API Testing Script for Business License Histories
# Tests all endpoints including the newly added ones

BASE_URL="http://localhost:8000/v1/business_license_histories"
MUNICIPALITY_ID=1
LICENSE_ID=1

echo "🧪 Testing Business License Histories API - Complete Suite"
echo "=========================================================="

# Test 1: List business license histories
echo "📋 Test 1: List business license histories"
curl -X GET "${BASE_URL}/?municipality_id=${MUNICIPALITY_ID}&status=1&skip=0&limit=10" \
     -H "accept: application/json" | jq '.'
echo -e "\n"

# Test 2: Get specific business license history
echo "📖 Test 2: Get specific business license history"
curl -X GET "${BASE_URL}/${LICENSE_ID}" \
     -H "accept: application/json" | jq '.'
echo -e "\n"

# Test 3: Create new business license history
echo "➕ Test 3: Create new business license history"
curl -X POST "${BASE_URL}/" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "license_folio": "TEST-2024-001",
       "business_name": "Test Business API",
       "business_line": "Restaurant",
       "business_line_code": "REST001",
       "owner_first_name": "Test",
       "owner_last_name_p": "Owner",
       "owner_email": "test@example.com",
       "municipality_id": '${MUNICIPALITY_ID}',
       "status": 1,
       "license_year": "2024",
       "license_type": "new",
       "license_status": "pending",
       "payment_status": "pending"
     }' | jq '.'
echo -e "\n"

# Test 4: Update business license history
echo "📝 Test 4: Update business license history"
curl -X PATCH "${BASE_URL}/${LICENSE_ID}" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "business_name": "Updated Business Name",
       "owner_phone": "555-1234"
     }' | jq '.'
echo -e "\n"

# Test 5: Update license status (NEW ENDPOINT)
echo "🔄 Test 5: Update license status"
curl -X PATCH "${BASE_URL}/${LICENSE_ID}/status" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "license_status": "approved",
       "reason": "All requirements met",
       "status_change_date": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
     }' | jq '.'
echo -e "\n"

# Test 6: Mark as paid (NEW ENDPOINT)
echo "💰 Test 6: Mark license as paid"
curl -X PATCH "${BASE_URL}/${LICENSE_ID}/paid" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "payment_status": "paid",
       "payment_user_id": 1,
       "payment_date": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"
     }' | jq '.'
echo -e "\n"

# Test 7: Get license files (NEW ENDPOINT)
echo "📁 Test 7: Get license files"
curl -X GET "${BASE_URL}/${LICENSE_ID}/files" \
     -H "accept: application/json" | jq '.'
echo -e "\n"

# Test 8: Create license renewal/refrendo (NEW ENDPOINT)
echo "🔄 Test 8: Create license renewal (refrendo)"
curl -X POST "${BASE_URL}/${LICENSE_ID}/refrendo" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "license_year": "2025",
       "license_type": "refrendo"
     }' | jq '.'
echo -e "\n"

# Test 9: Export business license histories
echo "📤 Test 9: Export business license histories (downloads Excel file)"
curl -X GET "${BASE_URL}/export?municipality_id=${MUNICIPALITY_ID}&status=1" \
     -H "accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
     --output "business_licenses_export_$(date +%Y%m%d).xlsx"
echo "Export saved to business_licenses_export_$(date +%Y%m%d).xlsx"
echo -e "\n"

# Test 10: Generate PDF (existing endpoint with QR code)
echo "📄 Test 10: Generate PDF with QR code"
curl -X GET "${BASE_URL}/pdf/${LICENSE_ID}/2024/original" \
     -H "accept: application/pdf" \
     --output "license_${LICENSE_ID}_2024_original.pdf"
echo "PDF saved to license_${LICENSE_ID}_2024_original.pdf"
echo -e "\n"

# Test 11: Test file deletion (NEW ENDPOINT)
echo "🗑️  Test 11: Delete license file (testing with non-existent file)"
curl -X DELETE "${BASE_URL}/${LICENSE_ID}/files/reason_file" \
     -H "accept: application/json" | jq '.'
echo -e "\n"

# Test 12: Soft delete business license history
echo "❌ Test 12: Soft delete business license history"
curl -X DELETE "${BASE_URL}/${LICENSE_ID}" \
     -H "accept: application/json" | jq '.'
echo -e "\n"

echo "✅ All API tests completed!"
echo "=========================================================="
echo "Summary of tested endpoints:"
echo "- GET    / (list)"
echo "- GET    /{id} (get single)"
echo "- POST   / (create)"
echo "- PATCH  /{id} (update)"
echo "- PATCH  /{id}/status (update status) [NEW]"
echo "- PATCH  /{id}/paid (mark as paid) [NEW]"
echo "- GET    /{id}/files (get files) [NEW]"
echo "- DELETE /{id}/files/{file_type} (delete file) [NEW]"
echo "- POST   /{id}/refrendo (create renewal) [NEW]"
echo "- GET    /export (export Excel)"
echo "- GET    /pdf/{id}/{year}/{type} (generate PDF)"
echo "- DELETE /{id} (soft delete)"
echo "=========================================================="
