#!/usr/bin/env python3
"""
Multi-User Wine Cellar Implementation Test
Tests the critical feature that ensures each user has their own private wine cellar.
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class MultiUserCellarTester:
    def __init__(self, base_url="https://wine-user-isolation.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.user_a_session = requests.Session()
        self.user_b_session = requests.Session()
        self.user_a_wine_id = None
        self.user_b_wine_id = None

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        if details and success:
            print(f"   Details: {details}")

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    expected_status: int = 200, session: Optional[requests.Session] = None) -> tuple[bool, Dict]:
        """Make HTTP request with optional session for authentication"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        # Use provided session or default requests
        req_session = session or requests
        
        try:
            if method == 'GET':
                response = req_session.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = req_session.post(url, json=data, headers=headers, timeout=30)
            elif method == 'PUT':
                response = req_session.put(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = req_session.delete(url, headers=headers, timeout=30)
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

    def register_user(self, email: str, password: str, name: str, session: requests.Session) -> bool:
        """Register a new user and login with session to get cookies"""
        register_data = {
            "email": email,
            "password": password,
            "name": name
        }
        
        success, response = self.make_request('POST', 'auth/register', data=register_data, expected_status=200, session=session)
        if success and 'user_id' in response:
            # Now login to get session cookie
            login_data = {
                "email": email,
                "password": password
            }
            login_success, login_response = self.make_request('POST', 'auth/login', data=login_data, expected_status=200, session=session)
            if login_success:
                # Cookie should now be set in the session
                return True
        
        return False

    def test_1_authentication_required(self):
        """Test that wine endpoints require authentication"""
        print("\n=== TEST 1: Authentication Required ===")
        
        # Test GET /api/wines without auth - should return 401
        success, response = self.make_request('GET', 'wines', expected_status=401)
        self.log_test("GET /api/wines without auth returns 401", success, 
                     f"Status: {response.get('status_code', 'unknown')}")
        
        # Test POST /api/wines without auth - should return 401
        wine_data = {
            "name": "Test Wine",
            "type": "rot",
            "region": "Test Region"
        }
        success, response = self.make_request('POST', 'wines', data=wine_data, expected_status=401)
        self.log_test("POST /api/wines without auth returns 401", success,
                     f"Status: {response.get('status_code', 'unknown')}")
        
        # Test DELETE /api/wines/{id} without auth - should return 401
        success, response = self.make_request('DELETE', 'wines/test-id', expected_status=401)
        self.log_test("DELETE /api/wines/{id} without auth returns 401", success,
                     f"Status: {response.get('status_code', 'unknown')}")
        
        return True

    def test_2_user_registration(self):
        """Test user registration for both test users"""
        print("\n=== TEST 2: User Registration ===")
        
        # Register User A
        timestamp = int(datetime.now().timestamp())
        user_a_email = f"multitest_a_{timestamp}@test.com"
        success_a = self.register_user(user_a_email, "password123", "Multi Test User A", self.user_a_session)
        
        if success_a:
            self.log_test("Register User A", True, f"Email: {user_a_email}")
        else:
            self.log_test("Register User A", False, "Registration failed")
            return False
        
        # Register User B
        user_b_email = f"multitest_b_{timestamp}@test.com"
        success_b = self.register_user(user_b_email, "password123", "Multi Test User B", self.user_b_session)
        
        if success_b:
            self.log_test("Register User B", True, f"Email: {user_b_email}")
        else:
            self.log_test("Register User B", False, "Registration failed")
            return False
        
        return True

    def test_3_user_isolation_empty_cellars(self):
        """Test that new users see empty cellars"""
        print("\n=== TEST 3: User Isolation - Empty Cellars ===")
        
        # User A should see empty cellar
        success, response = self.make_request('GET', 'wines', auth_token=self.user_a_token)
        if success:
            wines_a = response if isinstance(response, list) else []
            self.log_test("User A sees empty cellar initially", len(wines_a) == 0,
                         f"Found {len(wines_a)} wines (expected 0)")
        else:
            self.log_test("User A sees empty cellar initially", False, str(response))
            return False
        
        # User B should see empty cellar
        success, response = self.make_request('GET', 'wines', auth_token=self.user_b_token)
        if success:
            wines_b = response if isinstance(response, list) else []
            self.log_test("User B sees empty cellar initially", len(wines_b) == 0,
                         f"Found {len(wines_b)} wines (expected 0)")
        else:
            self.log_test("User B sees empty cellar initially", False, str(response))
            return False
        
        return True

    def test_4_add_wine_user_a(self):
        """Test adding a wine to User A's cellar"""
        print("\n=== TEST 4: Add Wine to User A's Cellar ===")
        
        wine_data = {
            "name": "Château Margaux 2015",
            "type": "rot",
            "region": "Bordeaux",
            "year": 2015,
            "grape": "Cabernet Sauvignon",
            "notes": "User A's premium Bordeaux"
        }
        
        success, response = self.make_request('POST', 'wines', data=wine_data, auth_token=self.user_a_token)
        if success and 'id' in response:
            self.user_a_wine_id = response['id']
            user_id = response.get('user_id')
            self.log_test("User A adds wine to cellar", True, 
                         f"Wine ID: {self.user_a_wine_id}, User ID: {user_id}")
        else:
            self.log_test("User A adds wine to cellar", False, str(response))
            return False
        
        return True

    def test_5_user_isolation_after_wine_added(self):
        """Test that User B still sees empty cellar after User A adds wine"""
        print("\n=== TEST 5: User Isolation - After Wine Added ===")
        
        # User A should see their wine
        success, response = self.make_request('GET', 'wines', auth_token=self.user_a_token)
        if success:
            wines_a = response if isinstance(response, list) else []
            if len(wines_a) == 1 and wines_a[0].get('name') == "Château Margaux 2015":
                self.log_test("User A sees their wine", True, f"Found wine: {wines_a[0].get('name')}")
            else:
                self.log_test("User A sees their wine", False, f"Expected 1 wine, found {len(wines_a)}")
                return False
        else:
            self.log_test("User A sees their wine", False, str(response))
            return False
        
        # User B should still see empty cellar (CRITICAL TEST)
        success, response = self.make_request('GET', 'wines', auth_token=self.user_b_token)
        if success:
            wines_b = response if isinstance(response, list) else []
            self.log_test("User B sees EMPTY cellar (not User A's wines)", len(wines_b) == 0,
                         f"Found {len(wines_b)} wines (expected 0) - CRITICAL ISOLATION TEST")
        else:
            self.log_test("User B sees EMPTY cellar (not User A's wines)", False, str(response))
            return False
        
        return True

    def test_6_user_b_cannot_access_user_a_wine(self):
        """Test that User B cannot access or delete User A's wine"""
        print("\n=== TEST 6: User B Cannot Access User A's Wine ===")
        
        if not self.user_a_wine_id:
            self.log_test("User B cannot access User A's wine", False, "No User A wine ID available")
            return False
        
        # User B tries to get User A's wine by ID - should return 404
        success, response = self.make_request('GET', f'wines/{self.user_a_wine_id}', 
                                            expected_status=404, auth_token=self.user_b_token)
        self.log_test("User B cannot GET User A's wine (404)", success,
                     f"Status: {response.get('status_code', 'unknown')}")
        
        # User B tries to delete User A's wine - should return 404
        success, response = self.make_request('DELETE', f'wines/{self.user_a_wine_id}', 
                                            expected_status=404, auth_token=self.user_b_token)
        self.log_test("User B cannot DELETE User A's wine (404)", success,
                     f"Status: {response.get('status_code', 'unknown')}")
        
        return True

    def test_7_user_b_adds_own_wine(self):
        """Test that User B can add their own wine"""
        print("\n=== TEST 7: User B Adds Own Wine ===")
        
        wine_data = {
            "name": "Barolo Brunate 2018",
            "type": "rot",
            "region": "Piemonte",
            "year": 2018,
            "grape": "Nebbiolo",
            "notes": "User B's Italian treasure"
        }
        
        success, response = self.make_request('POST', 'wines', data=wine_data, auth_token=self.user_b_token)
        if success and 'id' in response:
            self.user_b_wine_id = response['id']
            user_id = response.get('user_id')
            self.log_test("User B adds wine to cellar", True, 
                         f"Wine ID: {self.user_b_wine_id}, User ID: {user_id}")
        else:
            self.log_test("User B adds wine to cellar", False, str(response))
            return False
        
        return True

    def test_8_final_isolation_verification(self):
        """Final verification that both users only see their own wines"""
        print("\n=== TEST 8: Final Isolation Verification ===")
        
        # User A should only see their wine
        success, response = self.make_request('GET', 'wines', auth_token=self.user_a_token)
        if success:
            wines_a = response if isinstance(response, list) else []
            if len(wines_a) == 1 and wines_a[0].get('name') == "Château Margaux 2015":
                self.log_test("User A sees only their wine", True, 
                             f"Sees: {wines_a[0].get('name')} (correct)")
            else:
                self.log_test("User A sees only their wine", False, 
                             f"Expected 1 wine (Château Margaux), found {len(wines_a)}")
                return False
        else:
            self.log_test("User A sees only their wine", False, str(response))
            return False
        
        # User B should only see their wine
        success, response = self.make_request('GET', 'wines', auth_token=self.user_b_token)
        if success:
            wines_b = response if isinstance(response, list) else []
            if len(wines_b) == 1 and wines_b[0].get('name') == "Barolo Brunate 2018":
                self.log_test("User B sees only their wine", True, 
                             f"Sees: {wines_b[0].get('name')} (correct)")
            else:
                self.log_test("User B sees only their wine", False, 
                             f"Expected 1 wine (Barolo Brunate), found {len(wines_b)}")
                return False
        else:
            self.log_test("User B sees only their wine", False, str(response))
            return False
        
        return True

    def test_9_cellar_limits_freemium(self):
        """Test cellar limits for basic users (10 wines max)"""
        print("\n=== TEST 9: Cellar Limits (Freemium) ===")
        
        # Add 9 more wines to User A (already has 1, so total will be 10)
        wines_added = 0
        for i in range(9):
            wine_data = {
                "name": f"Test Wine {i+2}",
                "type": "rot",
                "region": "Test Region",
                "notes": f"Test wine number {i+2}"
            }
            
            success, response = self.make_request('POST', 'wines', data=wine_data, auth_token=self.user_a_token)
            if success:
                wines_added += 1
            else:
                break
        
        self.log_test("Add wines up to limit (10 total)", wines_added == 9,
                     f"Added {wines_added}/9 additional wines")
        
        # Try to add 11th wine - should fail with 403
        wine_data = {
            "name": "Wine Over Limit",
            "type": "rot",
            "region": "Should Fail"
        }
        
        success, response = self.make_request('POST', 'wines', data=wine_data, 
                                            expected_status=403, auth_token=self.user_a_token)
        self.log_test("11th wine rejected (403 Forbidden)", success,
                     f"Status: {response.get('status_code', 'unknown')}")
        
        return True

    def test_10_pairing_with_cellar_isolation(self):
        """Test wine pairing with use_cellar=true respects user isolation"""
        print("\n=== TEST 10: Pairing with Cellar (use_cellar) ===")
        
        # User A requests pairing with their cellar
        pairing_data = {
            "dish": "Rinderfilet mit Rosmarin",
            "use_cellar": True,
            "language": "de"
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, auth_token=self.user_a_token)
        if success:
            cellar_matches = response.get('cellar_matches', [])
            recommendation = response.get('recommendation', '')
            
            # Should find wines from User A's cellar
            if len(cellar_matches) > 0:
                self.log_test("User A pairing uses their cellar", True,
                             f"Found {len(cellar_matches)} cellar matches")
            else:
                self.log_test("User A pairing uses their cellar", False,
                             "No cellar matches found")
                return False
        else:
            self.log_test("User A pairing uses their cellar", False, str(response))
            return False
        
        # User B requests pairing with their cellar (should only see their 1 wine)
        success, response = self.make_request('POST', 'pairing', data=pairing_data, auth_token=self.user_b_token)
        if success:
            cellar_matches = response.get('cellar_matches', [])
            
            # Should only find User B's wine, not User A's wines
            if len(cellar_matches) == 1:
                wine_name = cellar_matches[0].get('name', '')
                if 'Barolo' in wine_name:
                    self.log_test("User B pairing uses only their cellar", True,
                                 f"Found only their wine: {wine_name}")
                else:
                    self.log_test("User B pairing uses only their cellar", False,
                                 f"Wrong wine found: {wine_name}")
                    return False
            else:
                self.log_test("User B pairing uses only their cellar", False,
                             f"Expected 1 cellar match, found {len(cellar_matches)}")
                return False
        else:
            self.log_test("User B pairing uses only their cellar", False, str(response))
            return False
        
        return True

    def run_all_tests(self):
        """Run all multi-user cellar tests"""
        print("🍷 MULTI-USER WINE CELLAR IMPLEMENTATION TEST")
        print("=" * 60)
        print("Testing critical feature: Each user has their own private wine cellar")
        print()
        
        tests = [
            self.test_1_authentication_required,
            self.test_2_user_registration,
            self.test_3_user_isolation_empty_cellars,
            self.test_4_add_wine_user_a,
            self.test_5_user_isolation_after_wine_added,
            self.test_6_user_b_cannot_access_user_a_wine,
            self.test_7_user_b_adds_own_wine,
            self.test_8_final_isolation_verification,
            self.test_9_cellar_limits_freemium,
            self.test_10_pairing_with_cellar_isolation
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ {test.__name__} - ERROR: {str(e)}")
                self.tests_run += 1
        
        print("\n" + "=" * 60)
        print(f"🍷 MULTI-USER CELLAR TEST SUMMARY")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "0%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED - Multi-User Wine Cellar is working correctly!")
            return True
        else:
            print("⚠️  SOME TESTS FAILED - Multi-User isolation may have issues")
            return False

if __name__ == "__main__":
    tester = MultiUserCellarTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)