#!/usr/bin/env python3
"""
Critical API Tests for Wine Pairing Application
Tests the specific endpoints mentioned in the review request
"""

import requests
import sys
import json
from datetime import datetime

class CriticalAPITester:
    def __init__(self, base_url="https://cellarmate-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        if details:
            print(f"   Details: {details}")

    def make_request(self, method: str, endpoint: str, data=None, expected_status: int = 200):
        """Make HTTP request and validate response"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                return False, {"error": f"Unsupported method: {method}"}

            success = response.status_code == expected_status
            
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text, "status_code": response.status_code}
            
            if not success:
                response_data["status_code"] = response.status_code
                response_data["expected_status"] = expected_status
            
            return success, response_data
            
        except Exception as e:
            return False, {"error": str(e)}

    def test_api_root(self):
        """Test GET /api/ - Should return API welcome message"""
        success, response = self.make_request('GET', '', expected_status=200)
        if success:
            message = response.get('message', '')
            if 'Wine Pairing API' in message:
                self.log_test("API Root Welcome", True, f"Message: {message}")
            else:
                self.log_test("API Root Welcome", False, f"Unexpected message: {message}")
        else:
            self.log_test("API Root Welcome", False, str(response))
        return success

    def test_blog_endpoint(self):
        """Test GET /api/blog - Should return blog posts"""
        success, response = self.make_request('GET', 'blog', expected_status=200)
        if success:
            if isinstance(response, list):
                self.log_test("Blog Posts API", True, f"Found {len(response)} blog posts")
            else:
                self.log_test("Blog Posts API", False, f"Expected list, got {type(response)}")
        else:
            self.log_test("Blog Posts API", False, str(response))
        return success

    def test_grape_varieties_endpoint(self):
        """Test GET /api/grape-varieties - Should return 140 grape varieties"""
        success, response = self.make_request('GET', 'grapes', expected_status=200)
        if success:
            if isinstance(response, list):
                count = len(response)
                if count >= 140:
                    self.log_test("Grape Varieties API", True, f"Found {count} grape varieties (expected 140)")
                else:
                    self.log_test("Grape Varieties API", False, f"Found only {count} grape varieties, expected 140")
            else:
                self.log_test("Grape Varieties API", False, f"Expected list, got {type(response)}")
        else:
            self.log_test("Grape Varieties API", False, str(response))
        return success

    def test_wiener_schnitzel_pairing(self):
        """Test wine pairing with Wiener Schnitzel"""
        pairing_data = {
            "dish": "Wiener Schnitzel",
            "language": "de"
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if success:
            recommendation = response.get('recommendation', '')
            if len(recommendation) > 100:
                # Check for German language indicators
                german_indicators = ['wein', 'empfehlung', 'passt', 'schnitzel']
                has_german = any(indicator in recommendation.lower() for indicator in german_indicators)
                
                if has_german:
                    self.log_test("Wiener Schnitzel Pairing", True, f"Got German recommendation ({len(recommendation)} chars)")
                else:
                    self.log_test("Wiener Schnitzel Pairing", False, "Response doesn't appear to be in German")
            else:
                self.log_test("Wiener Schnitzel Pairing", False, f"Recommendation too short: {len(recommendation)} chars")
        else:
            self.log_test("Wiener Schnitzel Pairing", False, str(response))
        return success

    def run_critical_tests(self):
        """Run all critical tests mentioned in the review request"""
        print("🍷 CRITICAL API TESTS - Wine Pairing Application")
        print(f"🌐 Testing API at: {self.api_url}")
        print("=" * 60)
        
        # Test the specific endpoints mentioned in the review request
        self.test_api_root()
        self.test_blog_endpoint()
        self.test_grape_varieties_endpoint()
        self.test_wiener_schnitzel_pairing()
        
        print("=" * 60)
        print(f"🏁 Critical Tests: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL CRITICAL API TESTS PASSED!")
            return True
        else:
            print("❌ Some critical tests failed")
            return False

if __name__ == "__main__":
    tester = CriticalAPITester()
    success = tester.run_critical_tests()
    sys.exit(0 if success else 1)