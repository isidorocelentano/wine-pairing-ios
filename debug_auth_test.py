#!/usr/bin/env python3
"""
Debug authentication test for Wine API
"""

import requests
import json
from datetime import datetime

def test_auth_debug():
    base_url = "https://wine-promo-suite.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    # Create a fresh session
    session = requests.Session()
    
    print("1. Testing GET /wines without authentication...")
    response = session.get(f"{api_url}/wines")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")
    
    if response.status_code != 401:
        print("   ❌ ISSUE: Should return 401 but got", response.status_code)
    else:
        print("   ✅ Correctly returned 401")
    
    print("\n2. Registering test user...")
    timestamp = int(datetime.now().timestamp())
    test_email = f"debugtest_{timestamp}@test.com"
    
    register_data = {
        "email": test_email,
        "password": "TestPass123!",
        "name": "Debug Test User"
    }
    
    response = session.post(f"{api_url}/auth/register", json=register_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        print(f"   ✅ User registered, token: {token[:20]}...")
        
        print("\n3. Testing GET /wines with Bearer token...")
        headers = {'Authorization': f'Bearer {token}'}
        response = session.get(f"{api_url}/wines", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
        if response.status_code == 200:
            wines = response.json()
            print(f"   ✅ Got {len(wines)} wines")
        else:
            print(f"   ❌ Expected 200 but got {response.status_code}")
        
        print("\n4. Testing GET /wines without token (should fail)...")
        response = session.get(f"{api_url}/wines")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 401:
            print("   ✅ Correctly returned 401")
        else:
            print(f"   ❌ Expected 401 but got {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    else:
        print(f"   ❌ Registration failed: {response.text}")

if __name__ == "__main__":
    test_auth_debug()