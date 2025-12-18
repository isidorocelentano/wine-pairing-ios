#!/usr/bin/env python3
"""
French Wine Data Cleanup Testing
Tests the French wine filters and data cleanup for the Wine Pairing Platform
"""

import requests
import sys
import json
from typing import Dict, Any, Optional

class FrenchWineDataTester:
    def __init__(self, base_url="https://dish-wine-match.preview.emergentagent.com"):
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
        
        if details and success:
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

    def test_french_wine_region_bordeaux(self):
        """Test French Wine Region Filter - Bordeaux"""
        success, response = self.make_request('GET', 'public-wines?region=Bordeaux&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            # Check that we have wines from Bordeaux
            if len(wines) == 0:
                self.log_test("French Region Filter - Bordeaux", False, "No wines found for Bordeaux region")
                return False
            
            # Verify wines are actually from Bordeaux region
            non_bordeaux_wines = []
            for wine in wines:
                region = (wine.get('region') or '').lower()
                appellation = (wine.get('appellation') or '').lower()
                if 'bordeaux' not in region and 'bordeaux' not in appellation:
                    non_bordeaux_wines.append(f"{wine.get('name', 'Unknown')} (region: {wine.get('region')}, appellation: {wine.get('appellation')})")
            
            if non_bordeaux_wines:
                self.log_test("French Region Filter - Bordeaux", False, 
                             f"Found non-Bordeaux wines: {non_bordeaux_wines[:3]}")
                return False
            
            # Check expected count (should be ~1041 wines)
            expected_min = 900  # Allow some variance
            if len(wines) < expected_min:
                self.log_test("French Region Filter - Bordeaux", False, 
                             f"Expected ~1041 Bordeaux wines, got {len(wines)}")
                return False
            
            self.log_test("French Region Filter - Bordeaux", True, 
                         f"Found {len(wines)} Bordeaux wines (expected ~1041)")
        else:
            self.log_test("French Region Filter - Bordeaux", False, str(response))
        return success

    def test_french_wine_region_burgund(self):
        """Test French Wine Region Filter - Burgund"""
        success, response = self.make_request('GET', 'public-wines?region=Burgund&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            if len(wines) == 0:
                self.log_test("French Region Filter - Burgund", False, "No wines found for Burgund region")
                return False
            
            # Verify wines are from Burgund region
            non_burgund_wines = []
            for wine in wines:
                region = (wine.get('region') or '').lower()
                appellation = (wine.get('appellation') or '').lower()
                if 'burgund' not in region and 'bourgogne' not in region and 'burgundy' not in region:
                    non_burgund_wines.append(f"{wine.get('name', 'Unknown')} (region: {wine.get('region')})")
            
            if non_burgund_wines:
                self.log_test("French Region Filter - Burgund", False, 
                             f"Found non-Burgund wines: {non_burgund_wines[:3]}")
                return False
            
            self.log_test("French Region Filter - Burgund", True, 
                         f"Found {len(wines)} Burgund wines")
        else:
            self.log_test("French Region Filter - Burgund", False, str(response))
        return success

    def test_french_wine_region_champagne(self):
        """Test French Wine Region Filter - Champagne"""
        success, response = self.make_request('GET', 'public-wines?region=Champagne&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            if len(wines) == 0:
                self.log_test("French Region Filter - Champagne", False, "No wines found for Champagne region")
                return False
            
            # Verify wines are from Champagne region
            non_champagne_wines = []
            for wine in wines:
                region = (wine.get('region') or '').lower()
                appellation = (wine.get('appellation') or '').lower()
                wine_name = (wine.get('name') or '').lower()
                if 'champagne' not in region and 'champagne' not in appellation and 'champagne' not in wine_name:
                    non_champagne_wines.append(f"{wine.get('name', 'Unknown')} (region: {wine.get('region')})")
            
            if non_champagne_wines:
                self.log_test("French Region Filter - Champagne", False, 
                             f"Found non-Champagne wines: {non_champagne_wines[:3]}")
                return False
            
            # Check expected count (should be ~62 wines)
            expected_min = 50  # Allow some variance
            if len(wines) < expected_min:
                self.log_test("French Region Filter - Champagne", False, 
                             f"Expected ~62 Champagne wines, got {len(wines)}")
                return False
            
            self.log_test("French Region Filter - Champagne", True, 
                         f"Found {len(wines)} Champagne wines (expected ~62)")
        else:
            self.log_test("French Region Filter - Champagne", False, str(response))
        return success

    def test_french_wine_region_rhone(self):
        """Test French Wine Region Filter - Rhône"""
        success, response = self.make_request('GET', 'public-wines?region=Rhône&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            if len(wines) == 0:
                self.log_test("French Region Filter - Rhône", False, "No wines found for Rhône region")
                return False
            
            # Verify wines are from Rhône region
            non_rhone_wines = []
            for wine in wines:
                region = (wine.get('region') or '').lower()
                appellation = (wine.get('appellation') or '').lower()
                if 'rhône' not in region and 'rhone' not in region and 'côtes du rhône' not in appellation:
                    non_rhone_wines.append(f"{wine.get('name', 'Unknown')} (region: {wine.get('region')})")
            
            if non_rhone_wines:
                self.log_test("French Region Filter - Rhône", False, 
                             f"Found non-Rhône wines: {non_rhone_wines[:3]}")
                return False
            
            self.log_test("French Region Filter - Rhône", True, 
                         f"Found {len(wines)} Rhône wines")
        else:
            self.log_test("French Region Filter - Rhône", False, str(response))
        return success

    def test_french_appellation_pauillac(self):
        """Test French Appellation Filter - Pauillac (region OR appellation match)"""
        success, response = self.make_request('GET', 'public-wines?region=Pauillac&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            if len(wines) == 0:
                self.log_test("French Appellation Filter - Pauillac", False, "No wines found for Pauillac")
                return False
            
            # Verify wines have Pauillac in region OR appellation
            non_pauillac_wines = []
            for wine in wines:
                region = (wine.get('region') or '').lower()
                appellation = (wine.get('appellation') or '').lower()
                if 'pauillac' not in region and 'pauillac' not in appellation:
                    non_pauillac_wines.append(f"{wine.get('name', 'Unknown')} (region: {wine.get('region')}, appellation: {wine.get('appellation')})")
            
            if non_pauillac_wines:
                self.log_test("French Appellation Filter - Pauillac", False, 
                             f"Found non-Pauillac wines: {non_pauillac_wines[:3]}")
                return False
            
            self.log_test("French Appellation Filter - Pauillac", True, 
                         f"Found {len(wines)} Pauillac wines")
        else:
            self.log_test("French Appellation Filter - Pauillac", False, str(response))
        return success

    def test_french_appellation_saint_emilion(self):
        """Test French Appellation Filter - Saint-Émilion"""
        success, response = self.make_request('GET', 'public-wines?region=Saint-Émilion&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            if len(wines) == 0:
                self.log_test("French Appellation Filter - Saint-Émilion", False, "No wines found for Saint-Émilion")
                return False
            
            # Verify wines have Saint-Émilion in region OR appellation
            non_saint_emilion_wines = []
            for wine in wines:
                region = (wine.get('region') or '').lower()
                appellation = (wine.get('appellation') or '').lower()
                wine_name = (wine.get('name') or '').lower()
                if ('saint-émilion' not in region and 'saint-emilion' not in region and 
                    'saint-émilion' not in appellation and 'saint-emilion' not in appellation and
                    'saint-émilion' not in wine_name and 'saint-emilion' not in wine_name):
                    non_saint_emilion_wines.append(f"{wine.get('name', 'Unknown')} (region: {wine.get('region')}, appellation: {wine.get('appellation')})")
            
            if non_saint_emilion_wines:
                self.log_test("French Appellation Filter - Saint-Émilion", False, 
                             f"Found non-Saint-Émilion wines: {non_saint_emilion_wines[:3]}")
                return False
            
            self.log_test("French Appellation Filter - Saint-Émilion", True, 
                         f"Found {len(wines)} Saint-Émilion wines")
        else:
            self.log_test("French Appellation Filter - Saint-Émilion", False, str(response))
        return success

    def test_french_appellation_chateauneuf_du_pape(self):
        """Test French Appellation Filter - Châteauneuf-du-Pape"""
        success, response = self.make_request('GET', 'public-wines?region=Châteauneuf-du-Pape&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            if len(wines) == 0:
                self.log_test("French Appellation Filter - Châteauneuf-du-Pape", False, "No wines found for Châteauneuf-du-Pape")
                return False
            
            # Verify wines have Châteauneuf-du-Pape in region OR appellation
            non_chateauneuf_wines = []
            for wine in wines:
                region = (wine.get('region') or '').lower()
                appellation = (wine.get('appellation') or '').lower()
                wine_name = (wine.get('name') or '').lower()
                if ('châteauneuf-du-pape' not in region and 'chateauneuf-du-pape' not in region and 
                    'châteauneuf-du-pape' not in appellation and 'chateauneuf-du-pape' not in appellation and
                    'châteauneuf-du-pape' not in wine_name and 'chateauneuf-du-pape' not in wine_name):
                    non_chateauneuf_wines.append(f"{wine.get('name', 'Unknown')} (region: {wine.get('region')}, appellation: {wine.get('appellation')})")
            
            if non_chateauneuf_wines:
                self.log_test("French Appellation Filter - Châteauneuf-du-Pape", False, 
                             f"Found non-Châteauneuf-du-Pape wines: {non_chateauneuf_wines[:3]}")
                return False
            
            self.log_test("French Appellation Filter - Châteauneuf-du-Pape", True, 
                         f"Found {len(wines)} Châteauneuf-du-Pape wines")
        else:
            self.log_test("French Appellation Filter - Châteauneuf-du-Pape", False, str(response))
        return success

    def test_french_wines_total_count(self):
        """Test total French wines count (should be ~1861)"""
        success, response = self.make_request('GET', 'public-wines?country=Frankreich&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            # Check total count
            expected_count = 1861
            tolerance = 50  # Allow some variance
            
            if len(wines) < (expected_count - tolerance):
                self.log_test("French Wines Total Count", False, 
                             f"Expected ~{expected_count} French wines, got {len(wines)}")
                return False
            
            # Verify all wines are French
            non_french_wines = []
            for wine in wines:
                country = wine.get('country', '')
                if country.lower() not in ['frankreich', 'france', 'französisch']:
                    non_french_wines.append(f"{wine.get('name', 'Unknown')} (country: {country})")
            
            if non_french_wines:
                self.log_test("French Wines Total Count", False, 
                             f"Found non-French wines: {non_french_wines[:3]}")
                return False
            
            self.log_test("French Wines Total Count", True, 
                         f"Found {len(wines)} French wines (expected ~{expected_count})")
        else:
            self.log_test("French Wines Total Count", False, str(response))
        return success

    def test_french_wines_no_empty_regions(self):
        """Test that all French wines have a valid region (no empty regions)"""
        success, response = self.make_request('GET', 'public-wines?country=Frankreich&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            if len(wines) == 0:
                self.log_test("French Wines No Empty Regions", False, "No French wines found")
                return False
            
            # Check for wines with empty or missing regions
            wines_without_region = []
            for wine in wines:
                region = (wine.get('region') or '').strip()
                if not region or region.lower() in ['', 'null', 'none', 'unknown']:
                    wines_without_region.append(f"{wine.get('name', 'Unknown')} (region: '{region}')")
            
            if wines_without_region:
                self.log_test("French Wines No Empty Regions", False, 
                             f"Found {len(wines_without_region)} wines without valid regions: {wines_without_region[:5]}")
                return False
            
            self.log_test("French Wines No Empty Regions", True, 
                         f"All {len(wines)} French wines have valid regions")
        else:
            self.log_test("French Wines No Empty Regions", False, str(response))
        return success

    def test_french_appellations_correct_characters(self):
        """Test that appellations use correct French characters (é, ô, etc.)"""
        success, response = self.make_request('GET', 'public-wines?country=Frankreich&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            if len(wines) == 0:
                self.log_test("French Appellations Correct Characters", False, "No French wines found")
                return False
            
            # Check for specific corrected appellations
            expected_corrections = {
                'Saint-Émilion': ['saint-émilion', 'saint-emilion'],
                'Châteauneuf-du-Pape': ['châteauneuf-du-pape', 'chateauneuf-du-pape'],
                'Côtes du Rhône': ['côtes du rhône', 'cotes du rhone']
            }
            
            found_corrections = {}
            for wine in wines:
                appellation = (wine.get('appellation') or '').strip()
                region = (wine.get('region') or '').strip()
                wine_name = (wine.get('name') or '').strip()
                
                for correct_form, variations in expected_corrections.items():
                    for variation in variations:
                        if (variation in appellation.lower() or 
                            variation in region.lower() or 
                            variation in wine_name.lower()):
                            if correct_form not in found_corrections:
                                found_corrections[correct_form] = 0
                            found_corrections[correct_form] += 1
                            break
            
            if not found_corrections:
                self.log_test("French Appellations Correct Characters", False, 
                             "No corrected French appellations found")
                return False
            
            self.log_test("French Appellations Correct Characters", True, 
                         f"Found corrected appellations: {found_corrections}")
        else:
            self.log_test("French Appellations Correct Characters", False, str(response))
        return success

    def test_no_duplicate_appellations(self):
        """Test that no duplicate appellations exist (like 'Pauillac' and 'Pauillac ')"""
        success, response = self.make_request('GET', 'public-wines?country=Frankreich&limit=2000', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            
            if len(wines) == 0:
                self.log_test("No Duplicate Appellations", False, "No French wines found")
                return False
            
            # Collect all appellations and check for duplicates (with/without trailing spaces)
            appellations = {}
            for wine in wines:
                appellation = (wine.get('appellation') or '').strip()
                if appellation:
                    normalized = appellation.lower().strip()
                    if normalized not in appellations:
                        appellations[normalized] = []
                    appellations[normalized].append(appellation)
            
            # Check for potential duplicates (same normalized form but different original forms)
            duplicates = {}
            for normalized, original_forms in appellations.items():
                unique_forms = list(set(original_forms))
                if len(unique_forms) > 1:
                    duplicates[normalized] = unique_forms
            
            if duplicates:
                self.log_test("No Duplicate Appellations", False, 
                             f"Found potential duplicates: {dict(list(duplicates.items())[:3])}")
                return False
            
            self.log_test("No Duplicate Appellations", True, 
                         f"No duplicate appellations found among {len(appellations)} unique appellations")
        else:
            self.log_test("No Duplicate Appellations", False, str(response))
        return success

    def test_filter_options_french_regions(self):
        """Test GET /api/public-wines-filters?country=Frankreich returns available French regions"""
        success, response = self.make_request('GET', 'public-wines-filters?country=Frankreich', expected_status=200)
        if success:
            regions = response.get('regions', [])
            appellations = response.get('appellations', [])
            
            if not regions:
                self.log_test("Filter Options French Regions", False, "No regions returned for French wines")
                return False
            
            # Check for expected French regions
            expected_regions = ['Bordeaux', 'Champagne', 'Burgund', 'Rhône']
            found_regions = [region for region in expected_regions if region in regions]
            
            if len(found_regions) < 3:
                self.log_test("Filter Options French Regions", False, 
                             f"Missing expected regions. Found: {regions[:10]}")
                return False
            
            # Check for expected appellations
            expected_appellations = ['Pauillac', 'Saint-Émilion', 'Châteauneuf-du-Pape']
            found_appellations = [app for app in expected_appellations if app in appellations]
            
            self.log_test("Filter Options French Regions", True, 
                         f"Found {len(regions)} regions and {len(appellations)} appellations. Expected regions found: {found_regions}")
        else:
            self.log_test("Filter Options French Regions", False, str(response))
        return success

    def run_all_tests(self):
        """Run all French wine data cleanup tests"""
        print("🍷 Starting French Wine Data Cleanup Tests")
        print("=" * 60)
        
        # French Wine Region Filter Tests
        print("\n📍 French Wine Region Filter Tests:")
        self.test_french_wine_region_bordeaux()
        self.test_french_wine_region_burgund()
        self.test_french_wine_region_champagne()
        self.test_french_wine_region_rhone()
        
        # French Wine Appellation Filter Tests
        print("\n🏷️ French Wine Appellation Filter Tests:")
        self.test_french_appellation_pauillac()
        self.test_french_appellation_saint_emilion()
        self.test_french_appellation_chateauneuf_du_pape()
        
        # Data Cleanup Verification Tests
        print("\n🧹 Data Cleanup Verification Tests:")
        self.test_french_wines_total_count()
        self.test_french_wines_no_empty_regions()
        self.test_french_appellations_correct_characters()
        self.test_no_duplicate_appellations()
        
        # Filter Options Test
        print("\n🔍 Filter Options Test:")
        self.test_filter_options_french_regions()
        
        # Summary
        print("\n" + "=" * 60)
        print(f"🏁 French Wine Tests Complete: {self.tests_passed}/{self.tests_run} PASSED")
        
        if self.tests_passed == self.tests_run:
            print("✅ ALL TESTS PASSED - French wine data cleanup is working correctly!")
            return True
        else:
            failed_tests = self.tests_run - self.tests_passed
            print(f"❌ {failed_tests} TESTS FAILED - French wine data cleanup needs attention")
            return False

if __name__ == "__main__":
    tester = FrenchWineDataTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)