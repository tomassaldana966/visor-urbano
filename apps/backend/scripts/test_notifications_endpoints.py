#!/usr/bin/env python3
"""
Test script for notifications endpoints
Tests all three migrated endpoints with the test data
"""
import requests
import json
import sys
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000/v1/notifications"
API_BASE_URL = "http://localhost:8000"

# Test user credentials (matching test data)
TEST_USER_EMAIL = "test.user29@visorurbano.com" 
TEST_PASSWORD = "testpass123"

def get_auth_token():
    """Get authentication token for test user"""
    print("🔐 Getting authentication token...")
    
    # Try to login with our test user
    login_url = f"{API_BASE_URL}/v1/auth/login"
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Successfully authenticated as {TEST_USER_EMAIL}")
            return token
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        return None

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_result(endpoint, response, expected_status=200):
    """Print test result"""
    status = "✅ PASS" if response.status_code == expected_status else "❌ FAIL"
    print(f"{status} {endpoint}")
    print(f"   Status: {response.status_code}")
    
    try:
        data = response.json()
        if response.status_code < 400:
            if isinstance(data, dict):
                if 'notifications' in data:
                    print(f"   Notifications found: {len(data['notifications'])}")
                    print(f"   Total count: {data.get('total_count', 'N/A')}")
                elif 'message' in data:
                    print(f"   Message: {data['message']}")
                else:
                    print(f"   Response keys: {list(data.keys())}")
            elif isinstance(data, list):
                print(f"   Items returned: {len(data)}")
            else:
                print(f"   Response: {data}")
        else:
            print(f"   Error: {data.get('detail', 'Unknown error')}")
    except:
        print(f"   Response: {response.text[:100]}...")
    
    print()

def get_auth_headers(token):
    """Get authentication headers with JWT token"""
    if not token:
        print("⚠️  No authentication token available - some tests may fail")
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

def test_endpoints():
    """Test all notification endpoints"""
    
    print_header("NOTIFICATIONS ENDPOINTS TESTING")
    print(f"🎯 Base URL: {BASE_URL}")
    print(f"📧 Test Email: {TEST_USER_EMAIL}")
    
    # Get authentication token
    auth_token = get_auth_token()
    if not auth_token:
        print("❌ Cannot proceed without authentication")
        return
    
    headers = get_auth_headers(auth_token)
    
    # Test 1: GET /notifications/ - List notifications (new endpoint)
    print_header("Test 1: List Notifications (New Endpoint)")
    try:
        response = requests.get(f"{BASE_URL}/", headers=headers, params={
            "page": 1,
            "per_page": 10
        })
        print_result("GET /notifications/", response)
    except Exception as e:
        print(f"❌ FAIL GET /notifications/ - Error: {e}")
    
    # Test 2: GET /notifications/listadoNotificaciones - List notifications (legacy)
    print_header("Test 2: List Notifications (Legacy Endpoint)")
    try:
        response = requests.get(f"{BASE_URL}/listadoNotificaciones", headers=headers, params={
            "page": 1,
            "per_page": 10
        })
        print_result("GET /notifications/listadoNotificaciones", response)
    except Exception as e:
        print(f"❌ FAIL GET /notifications/listadoNotificaciones - Error: {e}")
    
    # Test 3: PATCH /notifications/{id}/read - Mark notification as read (new)
    print_header("Test 3: Mark Notification as Read (New Endpoint)")
    notification_id = 1  # Test with notification ID 1
    try:
        response = requests.patch(f"{BASE_URL}/{notification_id}/read", headers=headers)
        print_result(f"PATCH /notifications/{notification_id}/read", response, 200)
    except Exception as e:
        print(f"❌ FAIL PATCH /notifications/{notification_id}/read - Error: {e}")
    
    # Test 4: GET /notifications/updateNotificacion/{id} - Mark notification as read (legacy)
    print_header("Test 4: Mark Notification as Read (Legacy Endpoint)")
    notification_id = 3  # Test with notification ID 3
    try:
        response = requests.get(f"{BASE_URL}/updateNotificacion/{notification_id}", headers=headers)
        print_result(f"GET /notifications/updateNotificacion/{notification_id}", response, 200)
    except Exception as e:
        print(f"❌ FAIL GET /notifications/updateNotificacion/{notification_id} - Error: {e}")
    
    # Test 5: GET /notifications/procedure/{id}/files - Get procedure files (new)
    print_header("Test 5: Get Procedure Files (New Endpoint)")
    procedure_id = 1  # Test with procedure ID 1
    try:
        response = requests.get(f"{BASE_URL}/procedure/{procedure_id}/files", headers=headers)
        print_result(f"GET /notifications/procedure/{procedure_id}/files", response)
    except Exception as e:
        print(f"❌ FAIL GET /notifications/procedure/{procedure_id}/files - Error: {e}")
    
    # Test 6: GET /notifications/getFileTipo/{id} - Get file type (legacy)
    print_header("Test 6: Get File Type (Legacy Endpoint)")
    procedure_id = 1  # Test with procedure ID 1
    try:
        response = requests.get(f"{BASE_URL}/getFileTipo/{procedure_id}", headers=headers)
        print_result(f"GET /notifications/getFileTipo/{procedure_id}", response)
    except Exception as e:
        print(f"❌ FAIL GET /notifications/getFileTipo/{procedure_id} - Error: {e}")
    
    # Test 7: Error cases - Non-existent notification
    print_header("Test 7: Error Handling - Non-existent Notification")
    try:
        response = requests.patch(f"{BASE_URL}/999/read", headers=headers)
        print_result("PATCH /notifications/999/read", response, 404)
    except Exception as e:
        print(f"❌ FAIL Error test - Error: {e}")
    
    # Test 8: Error cases - Non-existent procedure files
    print_header("Test 8: Error Handling - Non-existent Procedure Files")
    try:
        response = requests.get(f"{BASE_URL}/procedure/999/files", headers=headers)
        print_result("GET /notifications/procedure/999/files", response, 404)
    except Exception as e:
        print(f"❌ FAIL Error test - Error: {e}")
    
    # Test 9: Pagination test
    print_header("Test 9: Pagination Test")
    try:
        response = requests.get(f"{BASE_URL}/", headers=headers, params={
            "page": 1,
            "per_page": 2
        })
        print_result("GET /notifications/ (page=1, per_page=2)", response)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('has_next'):
                # Test next page
                response2 = requests.get(f"{BASE_URL}/", headers=headers, params={
                    "page": 2,
                    "per_page": 2
                })
                print_result("GET /notifications/ (page=2, per_page=2)", response2)
    except Exception as e:
        print(f"❌ FAIL Pagination test - Error: {e}")

def test_api_health():
    """Test if the API is running"""
    print_header("API Health Check")
    try:
        response = requests.get(f"{API_BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API is running and accessible")
            assert True  # API is accessible
        else:
            print(f"❌ API health check failed: {response.status_code}")
            assert False, f"API health check failed with status code: {response.status_code}"
    except Exception as e:
        print(f"❌ API is not accessible: {e}")
        assert False, f"API is not accessible: {e}"

def main():
    """Main test function"""
    print("🚀 Starting Notifications Endpoints Test Suite")
    print(f"📅 Time: {__import__('datetime').datetime.now()}")
    
    # Check API health
    if not test_api_health():
        print("\n❌ Cannot proceed with tests - API is not accessible")
        print("💡 Make sure the FastAPI server is running on http://localhost:8000")
        sys.exit(1)
    
    # Run endpoint tests
    test_endpoints()
    
    print_header("TESTING COMPLETED")
    print("🎉 All tests have been executed!")
    print("\n📝 Notes:")
    print("- Make sure test data was created using: python scripts/test_notifications_data.py")
    print("- Endpoints are available at /v1/notifications/*")
    print("- Legacy endpoints maintain backward compatibility")
    print("- Check server logs for any internal errors")
    
    print("\n🔧 Next steps:")
    print("1. Add authentication to test requests")
    print("2. Verify database constraints and relationships")
    print("3. Test with different user permissions")
    print("4. Performance testing with larger datasets")

if __name__ == "__main__":
    main()
