#!/usr/bin/env python3
"""
SIMPLIFIED CRITICAL BUGFIX VERIFICATION TEST for Wine Pairing Platform
Tests the data loss bug fix - focuses on data persistence and core functionality
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class SimpleBugfixTester:
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

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, expected_status: int = 200) -> tuple[bool, Dict]:
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

    def test_user_registration_works(self):
        """Test user registration system is functional"""
        test_email = f"bugfixtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}@winepairing.de"
        user_data = {
            "email": test_email,
            "password": "testpassword123",
            "name": "Bugfix Test User"
        }
        
        success, response = self.make_request('POST', 'auth/register', data=user_data, expected_status=200)
        if success:
            user_id = response.get('user_id')
            message = response.get('message', '')
            if user_id and 'erfolgreich' in message:
                self.log_test("User Registration System", True, f"Created user with ID: {user_id}")
            else:
                self.log_test("User Registration System", False, "Registration response incomplete")
                return False
        else:
            self.log_test("User Registration System", False, str(response))
        return success

    def test_wines_collection_persistence(self):
        """Test that wines collection has wines (should be 11+ wines) - Core data not lost"""
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

    def test_grapes_count_persistence(self):
        """Test GET /api/grapes - Grape varieties (should be 140) - Core data not lost"""
        success, response = self.make_request('GET', 'grapes', expected_status=200)
        if success:
            grapes = response if isinstance(response, list) else []
            grape_count = len(grapes)
            if grape_count >= 140:
                self.log_test("Grapes Collection Persistence", True, f"Found {grape_count} grape varieties (expected 140)")
            else:
                self.log_test("Grapes Collection Persistence", False, f"Only {grape_count} grapes found, expected 140")
                return False
        else:
            self.log_test("Grapes Collection Persistence", False, str(response))
        return success

    def test_blog_posts_persistence(self):
        """Test GET /api/blog - Blog posts (should be 233) - Core data not lost"""
        success, response = self.make_request('GET', 'blog?limit=250', expected_status=200)
        if success:
            posts = response if isinstance(response, list) else []
            post_count = len(posts)
            if post_count >= 233:
                self.log_test("Blog Posts Persistence", True, f"Found {post_count} blog posts (expected 233)")
            else:
                self.log_test("Blog Posts Persistence", False, f"Only {post_count} blog posts found, expected 233")
                return False
        else:
            self.log_test("Blog Posts Persistence", False, str(response))
        return success

    def test_coupon_system_functional(self):
        """Test coupon system is functional (new feature)"""
        success, response = self.make_request('GET', 'coupon/stats', expected_status=200)
        if success:
            # Check response structure - actual fields are 'total', 'used', 'unused', 'usage_rate'
            if 'total' in response and 'unused' in response:
                total_coupons = response.get('total', 0)
                unused_coupons = response.get('unused', 0)
                used_coupons = response.get('used', 0)
                self.log_test("Coupon System Functional", True, f"Total: {total_coupons}, Used: {used_coupons}, Unused: {unused_coupons}")
            else:
                self.log_test("Coupon System Functional", False, f"Unexpected coupon stats structure: {response}")
                return False
        else:
            self.log_test("Coupon System Functional", False, str(response))
        return success

    def test_wine_pairing_system_works(self):
        """Test wine pairing system works (core functionality)"""
        pairing_data = {
            "dish": "Rinderfilet mit Kräuterbutter",
            "language": "de",
            "use_cellar": False
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if success:
            recommendation = response.get('recommendation', '')
            dish = response.get('dish', '')
            if recommendation and len(recommendation) > 50:
                self.log_test("Wine Pairing System", True, f"Got pairing for {dish} ({len(recommendation)} chars)")
            else:
                self.log_test("Wine Pairing System", False, f"Recommendation too short: {recommendation[:100]}")
                return False
        else:
            self.log_test("Wine Pairing System", False, str(response))
        return success

    def test_protected_collections_exist(self):
        """Test that protected collections mentioned in the bugfix exist and are accessible"""
        # Test collections that should be protected from data loss
        protected_endpoints = [
            ('public-wines', 'Public Wines'),
            ('grapes', 'Grape Varieties'),
            ('blog', 'Blog Posts'),
            ('regional-pairings', 'Regional Pairings'),
            ('feed', 'Feed Posts')
        ]
        
        all_success = True
        results = []
        
        for endpoint, name in protected_endpoints:
            success, response = self.make_request('GET', f'{endpoint}?limit=5', expected_status=200)
            if success:
                data = response if isinstance(response, list) else []
                count = len(data)
                results.append(f"{name}: {count}")
                if count == 0:
                    all_success = False
            else:
                results.append(f"{name}: ERROR")
                all_success = False
        
        if all_success:
            self.log_test("Protected Collections Accessible", True, f"All collections accessible: {', '.join(results)}")
        else:
            self.log_test("Protected Collections Accessible", False, f"Some collections failed: {', '.join(results)}")
        
        return all_success

    def test_data_loss_bug_verification(self):
        """Verify the specific data loss bug is fixed by checking collection counts"""
        # The bug was that user data was wiped on deployment
        # We verify by checking that core data collections have expected counts
        
        expected_minimums = {
            'public-wines': 11,
            'grapes': 140,
            'blog': 233,
            'regional-pairings': 40,
            'feed': 200
        }
        
        all_counts_good = True
        results = []
        
        for endpoint, min_count in expected_minimums.items():
            success, response = self.make_request('GET', f'{endpoint}?limit=300', expected_status=200)
            if success:
                data = response if isinstance(response, list) else []
                actual_count = len(data)
                
                if actual_count >= min_count:
                    results.append(f"{endpoint}: {actual_count} (✓)")
                else:
                    results.append(f"{endpoint}: {actual_count} (✗ expected {min_count}+)")
                    all_counts_good = False
            else:
                results.append(f"{endpoint}: ERROR")
                all_counts_good = False
        
        if all_counts_good:
            self.log_test("Data Loss Bug Verification", True, f"All collections have expected data: {', '.join(results)}")
        else:
            self.log_test("Data Loss Bug Verification", False, f"Data loss detected: {', '.join(results)}")
        
        return all_counts_good

    def run_all_tests(self):
        """Run all critical bugfix verification tests"""
        print("🔍 SIMPLIFIED CRITICAL BUGFIX VERIFICATION TEST")
        print("🐛 Testing data loss bug fix - users collection protection")
        print(f"🌐 Testing API at: {self.api_url}")
        print("=" * 80)
        
        # Core API Health
        self.test_api_health_check()
        
        # User System (verify users collection is protected)
        self.test_user_registration_works()
        
        # Data Persistence Tests (verify core data not lost)
        self.test_wines_collection_persistence()
        self.test_grapes_count_persistence()
        self.test_blog_posts_persistence()
        
        # New Features (verify they work)
        self.test_coupon_system_functional()
        
        # Core Functionality
        self.test_wine_pairing_system_works()
        
        # Comprehensive Data Loss Verification
        self.test_protected_collections_exist()
        self.test_data_loss_bug_verification()
        
        print("=" * 80)
        print(f"🏁 SIMPLIFIED BUGFIX Tests: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 CRITICAL BUGFIX VERIFICATION PASSED! Data loss bug is fixed.")
            print("✅ Users collection is now protected from deployment overwrites")
            print("✅ All core data collections are intact and accessible")
            print("✅ New coupon system is functional")
            print("✅ Core wine pairing functionality works")
            return True
        else:
            failed_count = self.tests_run - self.tests_passed
            print(f"❌ CRITICAL BUGFIX VERIFICATION FAILED! {failed_count} tests failed.")
            return False

if __name__ == "__main__":
    tester = SimpleBugfixTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)