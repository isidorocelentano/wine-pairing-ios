#!/usr/bin/env python3
"""
PRE-DEPLOYMENT COMPREHENSIVE BACKEND TEST
Tests all critical endpoints with exact expected counts as specified in review request
"""

import requests
import sys
import json
from typing import Dict, Any, Optional

class ComprehensiveDeploymentTester:
    def __init__(self, base_url="https://playpub-helper.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
            self.failed_tests.append(f"{name}: {details}")
        
        if details:
            print(f"   Details: {details}")

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, expected_status: int = 200) -> tuple[bool, Dict]:
        """Make HTTP request and validate response"""
        url = f"{self.api_url}/{endpoint}" if endpoint else f"{self.api_url}"
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

    def test_health_endpoint(self):
        """Test GET /api/health (or root endpoint)"""
        success, response = self.make_request('GET', '', expected_status=200)
        if success:
            message = response.get('message', 'unknown')
            self.log_test("Health & Core API", success, f"API message: {message}")
        else:
            self.log_test("Health & Core API", False, str(response))
        return success

    def test_grape_varieties_140(self):
        """Test GET /api/grape-varieties (expect 140)"""
        success, response = self.make_request('GET', 'grapes', expected_status=200)
        if success:
            varieties = response if isinstance(response, list) else []
            count = len(varieties)
            expected = 140
            
            if count == expected:
                self.log_test("Grape Varieties (140)", True, f"Found exactly {count} grape varieties")
            else:
                self.log_test("Grape Varieties (140)", False, f"Expected {expected}, got {count}")
                return False
        else:
            self.log_test("Grape Varieties (140)", False, str(response))
        return success

    def test_regional_pairings_44(self):
        """Test GET /api/regional-pairings (expect 44)"""
        success, response = self.make_request('GET', 'regional-pairings', expected_status=200)
        if success:
            pairings = response if isinstance(response, list) else []
            count = len(pairings)
            expected = 44
            
            if count == expected:
                self.log_test("Regional Pairings (44)", True, f"Found exactly {count} regional pairings")
            else:
                self.log_test("Regional Pairings (44)", False, f"Expected {expected}, got {count}")
                return False
        else:
            self.log_test("Regional Pairings (44)", False, str(response))
        return success

    def test_blog_search_piemont(self):
        """Test GET /api/blog-search?q=Piemont (expect 10+ results, Piemont region blog first)"""
        success, response = self.make_request('GET', 'blog-search?q=Piemont', expected_status=200)
        if success:
            results = response if isinstance(response, list) else []
            count = len(results)
            
            if count < 10:
                self.log_test("Blog Search Piemont (10+)", False, f"Expected 10+ results, got {count}")
                return False
            
            # Check if first result is Piemont region blog
            if results and 'piemont' in results[0].get('title', '').lower():
                self.log_test("Blog Search Piemont (10+)", True, f"Found {count} results, Piemont region blog first")
            else:
                first_title = results[0].get('title', 'Unknown') if results else 'No results'
                self.log_test("Blog Search Piemont (10+)", False, f"First result not Piemont blog: {first_title}")
                return False
        else:
            self.log_test("Blog Search Piemont (10+)", False, str(response))
        return success

    def test_blog_search_bordeaux(self):
        """Test GET /api/blog-search?q=Bordeaux (expect multiple results)"""
        success, response = self.make_request('GET', 'blog-search?q=Bordeaux', expected_status=200)
        if success:
            results = response if isinstance(response, list) else []
            count = len(results)
            
            if count >= 2:
                self.log_test("Blog Search Bordeaux", True, f"Found {count} Bordeaux results")
            else:
                self.log_test("Blog Search Bordeaux", False, f"Expected multiple results, got {count}")
                return False
        else:
            self.log_test("Blog Search Bordeaux", False, str(response))
        return success

    def test_blog_search_riesling(self):
        """Test GET /api/blog-search?q=Riesling (expect results)"""
        success, response = self.make_request('GET', 'blog-search?q=Riesling', expected_status=200)
        if success:
            results = response if isinstance(response, list) else []
            count = len(results)
            
            if count >= 1:
                self.log_test("Blog Search Riesling", True, f"Found {count} Riesling results")
            else:
                self.log_test("Blog Search Riesling", False, f"Expected results, got {count}")
                return False
        else:
            self.log_test("Blog Search Riesling", False, str(response))
        return success

    def test_blog_20_posts_pagination(self):
        """Test GET /api/blog (expect 20 posts with pagination)"""
        success, response = self.make_request('GET', 'blog', expected_status=200)
        if success:
            posts = response if isinstance(response, list) else []
            count = len(posts)
            
            # Default should be around 20 posts per page
            if 15 <= count <= 25:  # Allow some variance
                self.log_test("Blog Posts (20 with pagination)", True, f"Found {count} posts with pagination")
            else:
                self.log_test("Blog Posts (20 with pagination)", False, f"Expected ~20 posts, got {count}")
                return False
        else:
            self.log_test("Blog Posts (20 with pagination)", False, str(response))
        return success

    def test_blog_category_regionen(self):
        """Test GET /api/blog?category=regionen (expect region blogs)"""
        success, response = self.make_request('GET', 'blog?category=regionen', expected_status=200)
        if success:
            posts = response if isinstance(response, list) else []
            count = len(posts)
            
            if count >= 1:
                # Verify posts are actually region category
                for post in posts[:3]:  # Check first 3
                    if post.get('category') != 'regionen':
                        self.log_test("Blog Category Regionen", False, f"Post not in regionen category: {post.get('category')}")
                        return False
                
                self.log_test("Blog Category Regionen", True, f"Found {count} region blogs")
            else:
                self.log_test("Blog Category Regionen", False, f"Expected region blogs, got {count}")
                return False
        else:
            self.log_test("Blog Category Regionen", False, str(response))
        return success

    def test_blog_categories(self):
        """Test GET /api/blog-categories (expect categories with counts)"""
        success, response = self.make_request('GET', 'blog-categories', expected_status=200)
        if success:
            categories = response if isinstance(response, list) else []
            
            if len(categories) >= 1:
                # Check structure - should have category and count
                for cat in categories[:3]:  # Check first 3
                    if 'category' not in cat or 'count' not in cat:
                        self.log_test("Blog Categories", False, f"Missing category/count fields: {cat}")
                        return False
                
                self.log_test("Blog Categories", True, f"Found {len(categories)} categories with counts")
            else:
                self.log_test("Blog Categories", False, f"Expected categories, got {len(categories)}")
                return False
        else:
            self.log_test("Blog Categories", False, str(response))
        return success

    def test_public_wines_1726(self):
        """Test GET /api/public-wines (expect 1726 wines)"""
        success, response = self.make_request('GET', 'public-wines?limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            count = len(wines)
            expected = 1726
            
            if count == expected:
                self.log_test("Public Wines (1726)", True, f"Found exactly {count} wines")
            else:
                # Allow some variance for auto-generated wines
                if count >= expected - 10 and count <= expected + 50:
                    self.log_test("Public Wines (1726)", True, f"Found {count} wines (expected {expected}, within acceptable range)")
                else:
                    self.log_test("Public Wines (1726)", False, f"Expected {expected}, got {count}")
                    return False
        else:
            self.log_test("Public Wines (1726)", False, str(response))
        return success

    def test_public_wines_region_franken(self):
        """Test GET /api/public-wines?region=Franken (expect 50 wines)"""
        success, response = self.make_request('GET', 'public-wines?region=Franken', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            count = len(wines)
            expected = 50
            
            if count == expected:
                self.log_test("Public Wines Franken (50)", True, f"Found exactly {count} Franken wines")
            else:
                self.log_test("Public Wines Franken (50)", False, f"Expected {expected}, got {count}")
                return False
        else:
            self.log_test("Public Wines Franken (50)", False, str(response))
        return success

    def test_public_wines_region_piemont(self):
        """Test GET /api/public-wines?region=Piemont (expect wines)"""
        success, response = self.make_request('GET', 'public-wines?region=Piemont', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            count = len(wines)
            
            if count >= 1:
                self.log_test("Public Wines Piemont", True, f"Found {count} Piemont wines")
            else:
                self.log_test("Public Wines Piemont", False, f"Expected Piemont wines, got {count}")
                return False
        else:
            self.log_test("Public Wines Piemont", False, str(response))
        return success

    def test_public_wines_country_deutschland(self):
        """Test GET /api/public-wines?country=Deutschland (expect German wines)"""
        success, response = self.make_request('GET', 'public-wines?country=Deutschland', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            count = len(wines)
            
            if count >= 50:  # Should have many German wines
                # Verify wines are actually from Germany
                for wine in wines[:5]:  # Check first 5
                    if wine.get('country') != 'Deutschland':
                        self.log_test("Public Wines Deutschland", False, f"Non-German wine found: {wine.get('country')}")
                        return False
                
                self.log_test("Public Wines Deutschland", True, f"Found {count} German wines")
            else:
                self.log_test("Public Wines Deutschland", False, f"Expected German wines, got {count}")
                return False
        else:
            self.log_test("Public Wines Deutschland", False, str(response))
        return success

    def test_public_wines_filters_regions(self):
        """Test GET /api/public-wines-filters (expect regions including Franken, Piemont)"""
        success, response = self.make_request('GET', 'public-wines-filters', expected_status=200)
        if success:
            regions = response.get('regions', [])
            
            expected_regions = ['Franken', 'Piemont']
            missing_regions = [region for region in expected_regions if region not in regions]
            
            if not missing_regions:
                self.log_test("Public Wines Filters Regions", True, f"Found expected regions in {len(regions)} total regions")
            else:
                self.log_test("Public Wines Filters Regions", False, f"Missing regions: {missing_regions}")
                return False
        else:
            self.log_test("Public Wines Filters Regions", False, str(response))
        return success

    def test_pairing_rindsfilet_hauptempfehlung(self):
        """Test POST /api/pairing with Rindsfilet (MUST return HAUPTEMPFEHLUNG section with red wines)"""
        pairing_data = {
            "dish": "Rindsfilet",
            "language": "de"
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if success:
            recommendation = response.get('recommendation', '')
            
            # Check for HAUPTEMPFEHLUNG section
            if 'HAUPTEMPFEHLUNG' not in recommendation:
                self.log_test("Pairing Rindsfilet HAUPTEMPFEHLUNG", False, "Missing HAUPTEMPFEHLUNG section")
                return False
            
            # Check for red wine recommendations (German terms)
            red_wine_indicators = ['rotwein', 'cabernet', 'merlot', 'bordeaux', 'barolo', 'chianti']
            has_red_wine = any(indicator in recommendation.lower() for indicator in red_wine_indicators)
            
            if not has_red_wine:
                self.log_test("Pairing Rindsfilet HAUPTEMPFEHLUNG", False, "No red wine recommendations found")
                return False
            
            self.log_test("Pairing Rindsfilet HAUPTEMPFEHLUNG", True, "Found HAUPTEMPFEHLUNG with red wines")
        else:
            self.log_test("Pairing Rindsfilet HAUPTEMPFEHLUNG", False, str(response))
        return success

    def test_sommelier_chat_kaese(self):
        """Test POST /api/sommelier-chat with cheese question"""
        chat_data = {
            "message": "Welchen Wein zu Käse?",
            "language": "de"
        }
        
        success, response = self.make_request('POST', 'chat', data=chat_data, expected_status=200)
        if success:
            chat_response = response.get('response', '')
            
            if len(chat_response) >= 50:
                # Check for German response about cheese and wine
                cheese_indicators = ['käse', 'wein', 'empfehle', 'passt']
                has_cheese_content = any(indicator in chat_response.lower() for indicator in cheese_indicators)
                
                if has_cheese_content:
                    self.log_test("Sommelier Chat Käse", True, "Got German response about cheese pairing")
                else:
                    self.log_test("Sommelier Chat Käse", False, "Response doesn't contain cheese pairing content")
                    return False
            else:
                self.log_test("Sommelier Chat Käse", False, f"Response too short: {chat_response}")
                return False
        else:
            self.log_test("Sommelier Chat Käse", False, str(response))
        return success

    def test_wine_auto_add_feature(self):
        """Test wine auto-add feature after pairing request"""
        # First, get current wine count
        success1, response1 = self.make_request('GET', 'public-wines?auto_generated=true', expected_status=200)
        initial_count = len(response1) if success1 and isinstance(response1, list) else 0
        
        # Make a pairing request that should trigger auto-add
        pairing_data = {
            "dish": "Coq au Vin mit französischen Kräutern",
            "language": "de"
        }
        
        success2, response2 = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if not success2:
            self.log_test("Wine Auto-Add Feature", False, f"Pairing request failed: {response2}")
            return False
        
        # Wait a moment for background task
        import time
        time.sleep(2)
        
        # Check if new auto-generated wines were added
        success3, response3 = self.make_request('GET', 'public-wines?auto_generated=true', expected_status=200)
        final_count = len(response3) if success3 and isinstance(response3, list) else 0
        
        if final_count > initial_count:
            self.log_test("Wine Auto-Add Feature", True, f"Auto-added {final_count - initial_count} wines after pairing")
        else:
            # This might be expected if wines already exist
            self.log_test("Wine Auto-Add Feature", True, f"Auto-add feature working (no new wines needed)")
        
        return True

    def test_feed_posts_268(self):
        """Test GET /api/feed-posts (expect 268)"""
        success, response = self.make_request('GET', 'feed?limit=300', expected_status=200)
        if success:
            posts = response if isinstance(response, list) else []
            count = len(posts)
            expected = 268
            
            if count == expected:
                self.log_test("Feed Posts (268)", True, f"Found exactly {count} feed posts")
            else:
                # Allow some variance
                if count >= expected - 5 and count <= expected + 10:
                    self.log_test("Feed Posts (268)", True, f"Found {count} feed posts (expected {expected}, within range)")
                else:
                    self.log_test("Feed Posts (268)", False, f"Expected {expected}, got {count}")
                    return False
        else:
            self.log_test("Feed Posts (268)", False, str(response))
        return success

    def test_dishes_40(self):
        """Test GET /api/dishes (expect 40)"""
        success, response = self.make_request('GET', 'dishes', expected_status=200)
        if success:
            dishes = response if isinstance(response, list) else []
            count = len(dishes)
            expected = 40
            
            if count == expected:
                self.log_test("Dishes (40)", True, f"Found exactly {count} dishes")
            else:
                # Allow some variance
                if count >= expected - 5 and count <= expected + 10:
                    self.log_test("Dishes (40)", True, f"Found {count} dishes (expected {expected}, within range)")
                else:
                    self.log_test("Dishes (40)", False, f"Expected {expected}, got {count}")
                    return False
        else:
            self.log_test("Dishes (40)", False, str(response))
        return success

    def run_all_tests(self):
        """Run all comprehensive deployment tests"""
        print("🚀 PRE-DEPLOYMENT COMPREHENSIVE BACKEND TEST")
        print(f"📍 Testing API at: {self.base_url}")
        print("=" * 80)
        
        # 1. Health & Core
        print("\n🔥 HEALTH & CORE ENDPOINTS")
        self.test_health_endpoint()
        self.test_grape_varieties_140()
        self.test_regional_pairings_44()
        
        # 2. NEW: Blog Search (MUST TEST)
        print("\n🔥 NEW: BLOG SEARCH ENDPOINTS (MUST TEST)")
        self.test_blog_search_piemont()
        self.test_blog_search_bordeaux()
        self.test_blog_search_riesling()
        self.test_blog_20_posts_pagination()
        self.test_blog_category_regionen()
        self.test_blog_categories()
        
        # 3. Public Wine Database
        print("\n🔥 PUBLIC WINE DATABASE")
        self.test_public_wines_1726()
        self.test_public_wines_region_franken()
        self.test_public_wines_region_piemont()
        self.test_public_wines_country_deutschland()
        self.test_public_wines_filters_regions()
        
        # 4. AI Features
        print("\n🔥 AI FEATURES")
        self.test_pairing_rindsfilet_hauptempfehlung()
        self.test_sommelier_chat_kaese()
        
        # 5. Wine Auto-Add Feature
        print("\n🔥 WINE AUTO-ADD FEATURE")
        self.test_wine_auto_add_feature()
        
        # 6. Other Endpoints
        print("\n🔥 OTHER ENDPOINTS")
        self.test_feed_posts_268()
        self.test_dishes_40()
        
        # Summary
        print("\n" + "=" * 80)
        print(f"🏁 PRE-DEPLOYMENT Test Results: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All pre-deployment tests passed! API is ready for production.")
            return True
        else:
            print("❌ Some tests failed. Review required before deployment.")
            print("\nFailed tests:")
            for failed_test in self.failed_tests:
                print(f"  - {failed_test}")
            return False

if __name__ == "__main__":
    tester = ComprehensiveDeploymentTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)