#!/usr/bin/env python3
"""
Debug session cookies for Wine API
"""

import requests
import json
from datetime import datetime

def test_session_debug():
    base_url = "https://playpub-helper.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    # Create a fresh session
    session = requests.Session()
    
    print("1. Initial cookies:", dict(session.cookies))
    
    print("\n2. Testing GET /wines without authentication...")
    response = session.get(f"{api_url}/wines")
    print(f"   Status: {response.status_code}")
    print(f"   Cookies after request:", dict(session.cookies))
    
    print("\n3. Registering test user...")
    timestamp = int(datetime.now().timestamp())
    test_email = f"debugtest2_{timestamp}@test.com"
    
    register_data = {
        "email": test_email,
        "password": "TestPass123!",
        "name": "Debug Test User 2"
    }
    
    response = session.post(f"{api_url}/auth/register", json=register_data)
    print(f"   Status: {response.status_code}")
    print(f"   Cookies after register:", dict(session.cookies))
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        
        print("\n4. Testing GET /wines with Bearer token...")
        headers = {'Authorization': f'Bearer {token}'}
        response = session.get(f"{api_url}/wines", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Cookies after authenticated request:", dict(session.cookies))
        
        print("\n5. Testing GET /wines without token (new session)...")
        new_session = requests.Session()
        response = new_session.get(f"{api_url}/wines")
        print(f"   Status: {response.status_code}")
        print(f"   New session cookies:", dict(new_session.cookies))
        
        print("\n6. Testing GET /wines without token (same session)...")
        response = session.get(f"{api_url}/wines")
        print(f"   Status: {response.status_code}")
        print(f"   Same session cookies:", dict(session.cookies))

if __name__ == "__main__":
    test_session_debug()