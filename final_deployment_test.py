#!/usr/bin/env python3
"""
FINAL PRE-DEPLOYMENT COMPREHENSIVE TEST for wine-pairing.online
Testing specific endpoints mentioned in the review request
"""

import requests
import sys
import json
from datetime import datetime

class FinalDeploymentTester:
    def __init__(self, base_url="https://wine-user-isolation.preview.emergentagent.com"):
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
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
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

    def test_core_health_endpoints(self):
        """Test Core Health endpoints"""
        print("\n🔥 TESTING CORE HEALTH ENDPOINTS")
        
        # 1. GET /api/ - API health
        success, response = self.make_request('GET', '')
        if success:
            message = response.get('message', '')
            self.log_test("API Root Health", True, f"API message: {message}")
        else:
            self.log_test("API Root Health", False, str(response))
        
        # 2. GET /api/grapes - Should return 140 grape varieties
        success, response = self.make_request('GET', 'grapes')
        if success:
            varieties = response if isinstance(response, list) else []
            expected_count = 140
            if len(varieties) >= 140:
                self.log_test("Grape Varieties (140)", True, f"Found {len(varieties)} grape varieties")
            else:
                self.log_test("Grape Varieties (140)", False, f"Expected 140+, got {len(varieties)}")
        else:
            self.log_test("Grape Varieties (140)", False, str(response))
        
        # 3. GET /api/regional-pairings - Should return 44 pairings
        success, response = self.make_request('GET', 'regional-pairings')
        if success:
            pairings = response if isinstance(response, list) else []
            expected_count = 44
            if len(pairings) >= 44:
                self.log_test("Regional Pairings (44)", True, f"Found {len(pairings)} regional pairings")
            else:
                self.log_test("Regional Pairings (44)", False, f"Expected 44+, got {len(pairings)}")
        else:
            self.log_test("Regional Pairings (44)", False, str(response))

    def test_blog_system_with_search(self):
        """Test Blog System with Search functionality"""
        print("\n🔥 TESTING BLOG SYSTEM WITH SEARCH")
        
        # 1. GET /api/blog?limit=20 - Blog posts pagination
        success, response = self.make_request('GET', 'blog?limit=20')
        if success:
            posts = response if isinstance(response, list) else []
            if len(posts) <= 20 and len(posts) > 0:
                self.log_test("Blog Posts Pagination (limit=20)", True, f"Found {len(posts)} blog posts")
            else:
                self.log_test("Blog Posts Pagination (limit=20)", False, f"Expected ≤20 posts, got {len(posts)}")
        else:
            self.log_test("Blog Posts Pagination (limit=20)", False, str(response))
        
        # 2. GET /api/blog-search?q=Piemont - Full-text search
        success, response = self.make_request('GET', 'blog-search?q=Piemont')
        if success:
            results = response if isinstance(response, list) else []
            self.log_test("Blog Search (Piemont)", True, f"Found {len(results)} results for 'Piemont'")
        else:
            self.log_test("Blog Search (Piemont)", False, str(response))
        
        # 3. GET /api/blog-search?q=Bordeaux - Search test
        success, response = self.make_request('GET', 'blog-search?q=Bordeaux')
        if success:
            results = response if isinstance(response, list) else []
            self.log_test("Blog Search (Bordeaux)", True, f"Found {len(results)} results for 'Bordeaux'")
        else:
            self.log_test("Blog Search (Bordeaux)", False, str(response))
        
        # 4. GET /api/blog-categories - Category list
        success, response = self.make_request('GET', 'blog-categories')
        if success:
            categories = response if isinstance(response, list) else []
            self.log_test("Blog Categories", True, f"Found {len(categories)} blog categories")
        else:
            self.log_test("Blog Categories", False, str(response))

    def test_wine_database(self):
        """Test Wine Database endpoints"""
        print("\n🔥 TESTING WINE DATABASE")
        
        # 1. GET /api/public-wines - Should return 1,751 wines
        success, response = self.make_request('GET', 'public-wines?limit=2000')
        if success:
            wines = response if isinstance(response, list) else []
            expected_count = 1751
            if len(wines) >= 1751:
                self.log_test("Public Wines Total (1,751)", True, f"Found {len(wines)} wines (expected 1,751+)")
            else:
                self.log_test("Public Wines Total (1,751)", False, f"Expected 1,751+, got {len(wines)}")
        else:
            self.log_test("Public Wines Total (1,751)", False, str(response))
        
        # 2. GET /api/public-wines?region=Franken - Region filter (50 wines)
        success, response = self.make_request('GET', 'public-wines?region=Franken')
        if success:
            wines = response if isinstance(response, list) else []
            expected_count = 50
            if len(wines) >= 50:
                self.log_test("Franken Region Wines (50)", True, f"Found {len(wines)} Franken wines")
            else:
                self.log_test("Franken Region Wines (50)", False, f"Expected 50+, got {len(wines)}")
        else:
            self.log_test("Franken Region Wines (50)", False, str(response))
        
        # 3. GET /api/public-wines-filters - Available filters
        success, response = self.make_request('GET', 'public-wines-filters')
        if success:
            filters = response
            countries = filters.get('countries', [])
            regions = filters.get('regions', [])
            colors = filters.get('wine_colors', [])
            prices = filters.get('price_categories', [])
            self.log_test("Wine Database Filters", True, 
                         f"Countries: {len(countries)}, Regions: {len(regions)}, Colors: {len(colors)}, Prices: {len(prices)}")
        else:
            self.log_test("Wine Database Filters", False, str(response))

    def test_ai_features(self):
        """Test AI Features"""
        print("\n🔥 TESTING AI FEATURES")
        
        # 1. POST /api/pairing with Wiener Schnitzel
        pairing_data = {
            "dish": "Wiener Schnitzel",
            "language": "de"
        }
        success, response = self.make_request('POST', 'pairing', data=pairing_data)
        if success:
            recommendation = response.get('recommendation', '')
            if len(recommendation) > 50:
                self.log_test("AI Pairing (Wiener Schnitzel)", True, f"Got recommendation ({len(recommendation)} chars)")
            else:
                self.log_test("AI Pairing (Wiener Schnitzel)", False, f"Recommendation too short: {recommendation}")
        else:
            self.log_test("AI Pairing (Wiener Schnitzel)", False, str(response))
        
        # 2. POST /api/chat with sommelier question
        chat_data = {
            "message": "Was ist der beste Wein zu Käse?",
            "language": "de"
        }
        success, response = self.make_request('POST', 'chat', data=chat_data)
        if success:
            chat_response = response.get('response', '')
            if len(chat_response) > 50:
                self.log_test("Sommelier Chat (Käse)", True, f"Got chat response ({len(chat_response)} chars)")
            else:
                self.log_test("Sommelier Chat (Käse)", False, f"Response too short: {chat_response}")
        else:
            self.log_test("Sommelier Chat (Käse)", False, str(response))

    def test_community_endpoints(self):
        """Test Community endpoints"""
        print("\n🔥 TESTING COMMUNITY ENDPOINTS")
        
        # 1. GET /api/feed - Should return 268 posts
        success, response = self.make_request('GET', 'feed?limit=300')
        if success:
            posts = response if isinstance(response, list) else []
            expected_count = 268
            if len(posts) >= 268:
                self.log_test("Community Feed (268)", True, f"Found {len(posts)} feed posts")
            else:
                self.log_test("Community Feed (268)", False, f"Expected 268+, got {len(posts)}")
        else:
            self.log_test("Community Feed (268)", False, str(response))
        
        # 2. GET /api/dishes - Should return 40 dishes
        success, response = self.make_request('GET', 'dishes')
        if success:
            dishes = response if isinstance(response, list) else []
            expected_count = 40
            if len(dishes) >= 40:
                self.log_test("Dishes Database (40)", True, f"Found {len(dishes)} dishes")
            else:
                self.log_test("Dishes Database (40)", False, f"Expected 40+, got {len(dishes)}")
        else:
            self.log_test("Dishes Database (40)", False, str(response))

    def run_all_tests(self):
        """Run all final deployment tests"""
        print("🚀 FINAL PRE-DEPLOYMENT COMPREHENSIVE TEST")
        print(f"📍 Testing API at: {self.api_url}")
        print("=" * 80)
        
        self.test_core_health_endpoints()
        self.test_blog_system_with_search()
        self.test_wine_database()
        self.test_ai_features()
        self.test_community_endpoints()
        
        print("\n" + "=" * 80)
        print(f"🏁 FINAL DEPLOYMENT Test Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL FINAL DEPLOYMENT TESTS PASSED! API IS PRODUCTION READY!")
            return True
        else:
            failed_count = self.tests_run - self.tests_passed
            print(f"❌ {failed_count} tests failed. Review issues before deployment.")
            return False

if __name__ == "__main__":
    tester = FinalDeploymentTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)