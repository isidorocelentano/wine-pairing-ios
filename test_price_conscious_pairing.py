#!/usr/bin/env python3
"""
Price-Conscious Wine Pairing System Testing
Tests the new price-conscious wine pairing recommendation system
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class PriceConsciousPairingTester:
    def __init__(self, base_url="https://grape-encyclopedia.preview.emergentagent.com"):
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

    def test_price_conscious_pairing_german_fondue(self):
        """Test German recommendation for Swiss dish (Fondue) with price tiers"""
        pairing_data = {
            "dish": "Fondue",
            "language": "de"
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if success:
            recommendation = response.get('recommendation', '')
            
            if len(recommendation) < 100:
                self.log_test("Price-Conscious Pairing (German Fondue)", False, f"Recommendation too short: {recommendation}")
                return False
            
            # Check for required price tier structure in German
            required_patterns = [
                "💚 **Preis-Leistung (CHF 10-20):**",
                "💛 **Gehobene Qualität (CHF 20-40):**"
            ]
            
            missing_patterns = []
            for pattern in required_patterns:
                if pattern not in recommendation:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                self.log_test("Price-Conscious Pairing (German Fondue)", False, 
                             f"Missing required price tier patterns: {missing_patterns}")
                print(f"   Full recommendation: {recommendation[:500]}...")
                return False
            
            # Check that affordable wines come first (💚 before 💛)
            green_pos = recommendation.find("💚 **Preis-Leistung")
            yellow_pos = recommendation.find("💛 **Gehobene Qualität")
            
            if green_pos == -1 or yellow_pos == -1:
                self.log_test("Price-Conscious Pairing (German Fondue)", False, "Price tier emojis not found")
                return False
            
            if green_pos > yellow_pos:
                self.log_test("Price-Conscious Pairing (German Fondue)", False, 
                             "Price tiers in wrong order - affordable should come first")
                return False
            
            # Check for at least 2 wines in the Preis-Leistung category
            preis_leistung_section = recommendation[green_pos:yellow_pos]
            wine_count = preis_leistung_section.count('**') // 2  # Each wine has **name**
            
            if wine_count < 2:
                self.log_test("Price-Conscious Pairing (German Fondue)", False, 
                             f"Expected at least 2 wines in Preis-Leistung category, found {wine_count}")
                return False
            
            # Check for CHF price ranges
            if "CHF" not in recommendation:
                self.log_test("Price-Conscious Pairing (German Fondue)", False, "CHF price ranges not visible")
                return False
            
            self.log_test("Price-Conscious Pairing (German Fondue)", True, 
                         f"German Fondue pairing with proper price structure - {wine_count} affordable wines")
        else:
            self.log_test("Price-Conscious Pairing (German Fondue)", False, str(response))
        return success

    def test_price_conscious_pairing_german_meat(self):
        """Test German recommendation for meat dish with price tiers"""
        pairing_data = {
            "dish": "Rindsfilet mit Rotweinsauce",
            "language": "de"
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if success:
            recommendation = response.get('recommendation', '')
            
            if len(recommendation) < 100:
                self.log_test("Price-Conscious Pairing (German Meat)", False, f"Recommendation too short: {recommendation}")
                return False
            
            # Check for price-tiered red wine recommendations
            required_patterns = [
                "💚 **Preis-Leistung (CHF 10-20):**",
                "💛 **Gehobene Qualität (CHF 20-40):**"
            ]
            
            missing_patterns = []
            for pattern in required_patterns:
                if pattern not in recommendation:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                self.log_test("Price-Conscious Pairing (German Meat)", False, 
                             f"Missing required price tier patterns: {missing_patterns}")
                print(f"   Full recommendation: {recommendation[:500]}...")
                return False
            
            # For meat dishes, should recommend red wine
            red_wine_indicators = ['rotwein', 'cabernet', 'merlot', 'pinot noir', 'bordeaux', 'barolo']
            has_red_wine = any(indicator in recommendation.lower() for indicator in red_wine_indicators)
            
            if not has_red_wine:
                self.log_test("Price-Conscious Pairing (German Meat)", False, 
                             "Expected red wine recommendation for meat dish")
                return False
            
            # Check for CHF price ranges
            if "CHF" not in recommendation:
                self.log_test("Price-Conscious Pairing (German Meat)", False, "CHF price ranges not visible")
                return False
            
            self.log_test("Price-Conscious Pairing (German Meat)", True, 
                         "German meat dish pairing with proper price structure and red wine focus")
        else:
            self.log_test("Price-Conscious Pairing (German Meat)", False, str(response))
        return success

    def test_price_conscious_pairing_english(self):
        """Test English recommendation with price tiers"""
        pairing_data = {
            "dish": "Grilled Salmon",
            "language": "en"
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if success:
            recommendation = response.get('recommendation', '')
            
            if len(recommendation) < 100:
                self.log_test("Price-Conscious Pairing (English)", False, f"Recommendation too short: {recommendation}")
                return False
            
            # Check for English price tier structure
            required_patterns = [
                "💚 **Great Value (CHF 10-20):**",
                "💛 **Premium Quality (CHF 20-40):**"
            ]
            
            missing_patterns = []
            for pattern in required_patterns:
                if pattern not in recommendation:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                self.log_test("Price-Conscious Pairing (English)", False, 
                             f"Missing required English price tier patterns: {missing_patterns}")
                print(f"   Full recommendation: {recommendation[:500]}...")
                return False
            
            # Check that affordable wines come first
            green_pos = recommendation.find("💚 **Great Value")
            yellow_pos = recommendation.find("💛 **Premium Quality")
            
            if green_pos == -1 or yellow_pos == -1:
                self.log_test("Price-Conscious Pairing (English)", False, "Price tier emojis not found")
                return False
            
            if green_pos > yellow_pos:
                self.log_test("Price-Conscious Pairing (English)", False, 
                             "Price tiers in wrong order - affordable should come first")
                return False
            
            # Check for CHF price ranges
            if "CHF" not in recommendation:
                self.log_test("Price-Conscious Pairing (English)", False, "CHF price ranges not visible")
                return False
            
            self.log_test("Price-Conscious Pairing (English)", True, 
                         "English salmon pairing with proper price structure")
        else:
            self.log_test("Price-Conscious Pairing (English)", False, str(response))
        return success

    def test_price_conscious_pairing_french(self):
        """Test French recommendation with price tiers"""
        pairing_data = {
            "dish": "Coq au Vin",
            "language": "fr"
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if success:
            recommendation = response.get('recommendation', '')
            
            if len(recommendation) < 100:
                self.log_test("Price-Conscious Pairing (French)", False, f"Recommendation too short: {recommendation}")
                return False
            
            # Check for French price tier structure
            required_patterns = [
                "💚 **Excellent Rapport Qualité-Prix (CHF 10-20):**",
                "💛 **Qualité Supérieure (CHF 20-40):**"
            ]
            
            missing_patterns = []
            for pattern in required_patterns:
                if pattern not in recommendation:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                self.log_test("Price-Conscious Pairing (French)", False, 
                             f"Missing required French price tier patterns: {missing_patterns}")
                print(f"   Full recommendation: {recommendation[:500]}...")
                return False
            
            # Check that affordable wines come first
            green_pos = recommendation.find("💚 **Excellent Rapport")
            yellow_pos = recommendation.find("💛 **Qualité Supérieure")
            
            if green_pos == -1 or yellow_pos == -1:
                self.log_test("Price-Conscious Pairing (French)", False, "Price tier emojis not found")
                return False
            
            if green_pos > yellow_pos:
                self.log_test("Price-Conscious Pairing (French)", False, 
                             "Price tiers in wrong order - affordable should come first")
                return False
            
            # Check for CHF price ranges
            if "CHF" not in recommendation:
                self.log_test("Price-Conscious Pairing (French)", False, "CHF price ranges not visible")
                return False
            
            self.log_test("Price-Conscious Pairing (French)", True, 
                         "French Coq au Vin pairing with proper price structure")
        else:
            self.log_test("Price-Conscious Pairing (French)", False, str(response))
        return success

    def run_all_tests(self):
        """Run all price-conscious pairing tests"""
        print("🍷 Testing Price-Conscious Wine Pairing System...")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🔗 API URL: {self.api_url}")
        print("=" * 60)
        
        # Test all 4 required test cases
        self.test_price_conscious_pairing_german_fondue()
        self.test_price_conscious_pairing_german_meat()
        self.test_price_conscious_pairing_english()
        self.test_price_conscious_pairing_french()
        
        print("=" * 60)
        print(f"🏁 Tests completed: {self.tests_passed}/{self.tests_run} passed")
        
        if self.tests_passed == self.tests_run:
            print("✅ All price-conscious pairing tests PASSED!")
            return True
        else:
            failed = self.tests_run - self.tests_passed
            print(f"❌ {failed} tests FAILED!")
            return False

if __name__ == "__main__":
    tester = PriceConsciousPairingTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)