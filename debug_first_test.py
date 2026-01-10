#!/usr/bin/env python3
"""
Debug the first test issue
"""

import requests
import json
from datetime import datetime

def debug_first_test():
    base_url = "https://playpub-helper.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    # Create a fresh session like the test does
    session = requests.Session()
    
    print("Initial session cookies:", dict(session.cookies))
    
    # Clear cookies like the test does
    session.cookies.clear()
    print("After clearing cookies:", dict(session.cookies))
    
    # Test GET wines without auth
    print("\nTesting GET /wines without auth...")
    response = session.get(f"{api_url}/wines")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    print(f"Cookies after request:", dict(session.cookies))

if __name__ == "__main__":
    debug_first_test()