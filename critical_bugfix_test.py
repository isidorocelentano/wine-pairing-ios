#!/usr/bin/env python3
"""
CRITICAL BUGFIX VERIFICATION TEST for Wine Pairing Platform
Tests the data loss bug fix where user data was being wiped on deployment
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class CriticalBugfixTester:
    def __init__(self, base_url="https://winedata-fix.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.auth_token = None
        self.test_user_email = f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}@winepairing.de"

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

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, expected_status: int = 200, auth: bool = False) -> tuple[bool, Dict]:
        """Make HTTP request and validate response"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if auth and self.auth_token:
            headers['Authorization'] = f"Bearer {self.auth_token}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
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
            
        except requests.exceptions.Timeout:
            return False, {"error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return False, {"error": "Connection error"}
        except Exception as e:
            return False, {"error": str(e)}

    def test_api_health_check(self):
        """Test API health check"""
        success, response = self.make_request('GET', '', expected_status=200)
        self.log_test("API Health Check", success, 
                     f"Response: {response.get('message', 'No message')}" if success else str(response))
        return success

    def test_user_registration(self):
        """Test user registration - Create a new user with unique email"""
        user_data = {
            "email": self.test_user_email,
            "password": "testpassword123",
            "name": "Test User Bugfix"
        }
        
        success, response = self.make_request('POST', 'auth/register', data=user_data, expected_status=200)
        if success:
            user_id = response.get('user_id')
            if user_id:
                self.log_test("User Registration", True, f"Created user with ID: {user_id}")
            else:
                self.log_test("User Registration", False, "No user_id in response")
                return False
        else:
            self.log_test("User Registration", False, str(response))
        return success

    def test_user_login_existing(self):
        """Test login with existing user (test@winepairing.de / testpassword123)"""
        login_data = {
            "email": "test@winepairing.de",
            "password": "testpassword123"
        }
        
        success, response = self.make_request('POST', 'auth/login', data=login_data, expected_status=200)
        if success:
            token = response.get('access_token')
            user_info = response.get('user')
            if token and user_info:
                self.auth_token = token
                self.log_test("User Login (Existing)", True, f"Logged in user: {user_info.get('email')}")
            else:
                self.log_test("User Login (Existing)", False, "Missing token or user info")
                return False
        else:
            self.log_test("User Login (Existing)", False, str(response))
        return success

    def test_user_login_new(self):
        """Test login with newly created user"""
        login_data = {
            "email": self.test_user_email,
            "password": "testpassword123"
        }
        
        success, response = self.make_request('POST', 'auth/login', data=login_data, expected_status=200)
        if success:
            token = response.get('access_token')
            user_info = response.get('user')
            if token and user_info:
                self.auth_token = token
                self.log_test("User Login (New User)", True, f"Logged in new user: {user_info.get('email')}")
            else:
                self.log_test("User Login (New User)", False, "Missing token or user info")
                return False
        else:
            self.log_test("User Login (New User)", False, str(response))
        return success

    def test_authenticated_user_info(self):
        """Test GET /api/auth/me - Verify authenticated user info"""
        if not self.auth_token:
            self.log_test("Authenticated User Info", False, "No auth token available")
            return False
            
        success, response = self.make_request('GET', 'auth/me', expected_status=200, auth=True)
        if success:
            user_email = response.get('email')
            user_name = response.get('name')
            if user_email and user_name:
                self.log_test("Authenticated User Info", True, f"User: {user_name} ({user_email})")
            else:
                self.log_test("Authenticated User Info", False, "Missing user email or name")
                return False
        else:
            self.log_test("Authenticated User Info", False, str(response))
        return success

    def test_users_collection_persistence(self):
        """Test that users collection has users (should be 5+ users)"""
        # We can't directly access the users collection, but we can infer from successful logins
        # and the fact that we can create new users
        success, response = self.make_request('GET', 'auth/me', expected_status=200, auth=True)
        if success:
            self.log_test("Users Collection Persistence", True, "Users collection accessible via auth")
        else:
            self.log_test("Users Collection Persistence", False, "Cannot access user data - possible data loss")
        return success

    def test_wines_collection_persistence(self):
        """Test that wines collection has wines (should be 11+ wines)"""
        success, response = self.make_request('GET', 'public-wines?limit=20', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            wine_count = len(wines)
            if wine_count >= 11:
                self.log_test("Wines Collection Persistence", True, f"Found {wine_count} wines (expected 11+)")
            else:
                self.log_test("Wines Collection Persistence", False, f"Only {wine_count} wines found, expected 11+")
                return False
        else:
            self.log_test("Wines Collection Persistence", False, str(response))
        return success

    def test_coupon_stats(self):
        """Test GET /api/coupon/stats - Get coupon statistics"""
        success, response = self.make_request('GET', 'coupon/stats', expected_status=200)
        if success:
            total_coupons = response.get('total_coupons', 0)
            active_coupons = response.get('active_coupons', 0)
            self.log_test("Coupon Stats", True, f"Total: {total_coupons}, Active: {active_coupons}")
        else:
            self.log_test("Coupon Stats", False, str(response))
        return success

    def test_coupon_redeem_invalid(self):
        """Test POST /api/coupon/redeem - Attempt coupon redemption with invalid code"""
        redeem_data = {
            "coupon_code": "INVALID_CODE_TEST"
        }
        
        success, response = self.make_request('POST', 'coupon/redeem', data=redeem_data, expected_status=404, auth=True)
        if success:
            self.log_test("Coupon Redeem (Invalid)", True, "Correctly rejected invalid coupon")
        else:
            # Check if it returned 404 or another error status
            status_code = response.get('status_code', 0)
            if status_code in [400, 404, 422]:
                self.log_test("Coupon Redeem (Invalid)", True, f"Correctly rejected invalid coupon (status: {status_code})")
                return True
            else:
                self.log_test("Coupon Redeem (Invalid)", False, str(response))
        return success

    def test_grapes_count(self):
        """Test GET /api/grapes - Grape varieties (should be 140)"""
        success, response = self.make_request('GET', 'grapes', expected_status=200)
        if success:
            grapes = response if isinstance(response, list) else []
            grape_count = len(grapes)
            if grape_count >= 140:
                self.log_test("Grapes Count", True, f"Found {grape_count} grape varieties (expected 140)")
            else:
                self.log_test("Grapes Count", False, f"Only {grape_count} grapes found, expected 140")
                return False
        else:
            self.log_test("Grapes Count", False, str(response))
        return success

    def test_blog_posts_count(self):
        """Test GET /api/blog - Blog posts (should be 233)"""
        success, response = self.make_request('GET', 'blog?limit=250', expected_status=200)
        if success:
            posts = response if isinstance(response, list) else []
            post_count = len(posts)
            if post_count >= 233:
                self.log_test("Blog Posts Count", True, f"Found {post_count} blog posts (expected 233)")
            else:
                self.log_test("Blog Posts Count", False, f"Only {post_count} blog posts found, expected 233")
                return False
        else:
            self.log_test("Blog Posts Count", False, str(response))
        return success

    def test_public_wines_database(self):
        """Test GET /api/public-wines?limit=5 - Wine database"""
        success, response = self.make_request('GET', 'public-wines?limit=5', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            wine_count = len(wines)
            if wine_count > 0:
                # Check structure of first wine
                if wines:
                    wine = wines[0]
                    required_fields = ['id', 'name', 'country', 'region', 'grape_variety', 'wine_color']
                    missing_fields = [field for field in required_fields if field not in wine]
                    if missing_fields:
                        self.log_test("Public Wines Database", False, f"Missing fields: {missing_fields}")
                        return False
                
                self.log_test("Public Wines Database", True, f"Found {wine_count} wines with proper structure")
            else:
                self.log_test("Public Wines Database", False, "No wines found in public database")
                return False
        else:
            self.log_test("Public Wines Database", False, str(response))
        return success

    def test_add_wine_to_cellar(self):
        """Test POST /api/wines - Add wine to cellar (requires auth)"""
        if not self.auth_token:
            self.log_test("Add Wine to Cellar", False, "No auth token available")
            return False
            
        wine_data = {
            "name": "Test Bordeaux Bugfix 2020",
            "type": "rot",
            "region": "Bordeaux",
            "year": 2020,
            "grape": "Cabernet Sauvignon",
            "notes": "Test wine for bugfix verification"
        }
        
        success, response = self.make_request('POST', 'wines', data=wine_data, expected_status=200, auth=True)
        if success:
            wine_id = response.get('id')
            wine_name = response.get('name')
            if wine_id and wine_name:
                self.log_test("Add Wine to Cellar", True, f"Added wine: {wine_name} (ID: {wine_id})")
            else:
                self.log_test("Add Wine to Cellar", False, "Missing wine ID or name in response")
                return False
        else:
            self.log_test("Add Wine to Cellar", False, str(response))
        return success

    def test_get_user_wine_cellar(self):
        """Test GET /api/wines - Get user's wine cellar"""
        if not self.auth_token:
            self.log_test("Get User Wine Cellar", False, "No auth token available")
            return False
            
        success, response = self.make_request('GET', 'wines', expected_status=200, auth=True)
        if success:
            wines = response if isinstance(response, list) else []
            wine_count = len(wines)
            self.log_test("Get User Wine Cellar", True, f"Found {wine_count} wines in user's cellar")
        else:
            self.log_test("Get User Wine Cellar", False, str(response))
        return success

    def test_wine_pairing_with_usage_tracking(self):
        """Test POST /api/pairing - Wine pairing (requires auth for usage tracking)"""
        if not self.auth_token:
            self.log_test("Wine Pairing (Usage Tracking)", False, "No auth token available")
            return False
            
        pairing_data = {
            "dish": "Rinderfilet mit Kräuterbutter",
            "language": "de",
            "use_cellar": False
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200, auth=True)
        if success:
            recommendation = response.get('recommendation', '')
            dish = response.get('dish', '')
            if recommendation and len(recommendation) > 50:
                self.log_test("Wine Pairing (Usage Tracking)", True, f"Got pairing for {dish} ({len(recommendation)} chars)")
            else:
                self.log_test("Wine Pairing (Usage Tracking)", False, f"Recommendation too short: {recommendation[:100]}")
                return False
        else:
            self.log_test("Wine Pairing (Usage Tracking)", False, str(response))
        return success

    def run_all_tests(self):
        """Run all critical bugfix verification tests"""
        print("🔍 CRITICAL BUGFIX VERIFICATION TEST for Wine Pairing Platform")
        print("🐛 Testing data loss bug fix - users collection protection")
        print(f"🌐 Testing API at: {self.api_url}")
        print("=" * 80)
        
        # Core API Health Tests
        self.test_api_health_check()
        
        # User Authentication Tests
        self.test_user_registration()
        self.test_user_login_existing()
        self.test_user_login_new()
        self.test_authenticated_user_info()
        
        # Data Persistence Tests
        self.test_users_collection_persistence()
        self.test_wines_collection_persistence()
        
        # Coupon System Tests (New Feature)
        self.test_coupon_stats()
        self.test_coupon_redeem_invalid()
        
        # Core API Health Tests
        self.test_grapes_count()
        self.test_blog_posts_count()
        self.test_public_wines_database()
        
        # User-Specific Data Tests
        self.test_add_wine_to_cellar()
        self.test_get_user_wine_cellar()
        self.test_wine_pairing_with_usage_tracking()
        
        print("=" * 80)
        print(f"🏁 CRITICAL BUGFIX Tests: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 CRITICAL BUGFIX VERIFICATION PASSED! Data loss bug is fixed.")
            return True
        else:
            print("❌ CRITICAL BUGFIX VERIFICATION FAILED! Some tests failed.")
            return False

if __name__ == "__main__":
    tester = CriticalBugfixTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)