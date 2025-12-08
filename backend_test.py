#!/usr/bin/env python3
"""
Wine Pairing App Backend API Testing
Tests all API endpoints for the Wine Pairing application
"""

import requests
import sys
import json
import base64
from datetime import datetime
from typing import Dict, Any, Optional

class WinePairingAPITester:
    def __init__(self, base_url="https://palate-translator.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_wine_id = None
        self.session_id = None

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

    def test_root_endpoint(self):
        """Test API root endpoint"""
        success, response = self.make_request('GET', '', expected_status=200)
        self.log_test("API Root Endpoint", success, 
                     f"Response: {response.get('message', 'No message')}" if success else str(response))
        return success

    def test_get_wines_empty(self):
        """Test getting wines when cellar is empty"""
        success, response = self.make_request('GET', 'wines', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            self.log_test("Get Wines (Empty Cellar)", True, f"Found {len(wines)} wines")
        else:
            self.log_test("Get Wines (Empty Cellar)", False, str(response))
        return success

    def test_create_wine(self):
        """Test creating a new wine"""
        wine_data = {
            "name": "Test Bordeaux 2020",
            "type": "rot",
            "region": "Bordeaux",
            "year": 2020,
            "grape": "Cabernet Sauvignon",
            "notes": "Test wine for API testing"
        }
        
        success, response = self.make_request('POST', 'wines', data=wine_data, expected_status=200)
        if success and 'id' in response:
            self.test_wine_id = response['id']
            self.log_test("Create Wine", True, f"Created wine with ID: {self.test_wine_id}")
        else:
            self.log_test("Create Wine", False, str(response))
        return success

    def test_get_wine_by_id(self):
        """Test getting a specific wine by ID"""
        if not self.test_wine_id:
            self.log_test("Get Wine by ID", False, "No wine ID available")
            return False
            
        success, response = self.make_request('GET', f'wines/{self.test_wine_id}', expected_status=200)
        if success:
            self.log_test("Get Wine by ID", True, f"Retrieved wine: {response.get('name', 'Unknown')}")
        else:
            self.log_test("Get Wine by ID", False, str(response))
        return success

    def test_get_wines_with_data(self):
        """Test getting wines when cellar has data"""
        success, response = self.make_request('GET', 'wines', expected_status=200)
        if success:
            wines = response if isinstance(response, list) else []
            self.log_test("Get Wines (With Data)", True, f"Found {len(wines)} wines")
        else:
            self.log_test("Get Wines (With Data)", False, str(response))
        return success

    def test_toggle_favorite(self):
        """Test toggling wine favorite status"""
        if not self.test_wine_id:
            self.log_test("Toggle Favorite", False, "No wine ID available")
            return False
            
        success, response = self.make_request('POST', f'wines/{self.test_wine_id}/favorite', expected_status=200)
        if success:
            is_favorite = response.get('is_favorite', False)
            self.log_test("Toggle Favorite", True, f"Favorite status: {is_favorite}")
        else:
            self.log_test("Toggle Favorite", False, str(response))
        return success

    def test_wine_pairing_basic(self):
        """Test basic wine pairing without cellar"""
        pairing_data = {
            "dish": "Gegrilltes Rinderfilet mit Rosmarin",
            "use_cellar": False
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if success:
            recommendation = response.get('recommendation', '')[:100] + '...' if len(response.get('recommendation', '')) > 100 else response.get('recommendation', '')
            self.log_test("Wine Pairing (Basic)", True, f"Got recommendation: {recommendation}")
        else:
            self.log_test("Wine Pairing (Basic)", False, str(response))
        return success

    def test_wine_pairing_with_cellar(self):
        """Test wine pairing using cellar wines"""
        pairing_data = {
            "dish": "Pasta mit Tomatensauce",
            "use_cellar": True,
            "wine_type_filter": "rot"
        }
        
        success, response = self.make_request('POST', 'pairing', data=pairing_data, expected_status=200)
        if success:
            recommendation = response.get('recommendation', '')[:100] + '...' if len(response.get('recommendation', '')) > 100 else response.get('recommendation', '')
            cellar_matches = response.get('cellar_matches', [])
            self.log_test("Wine Pairing (With Cellar)", True, 
                         f"Got recommendation with {len(cellar_matches)} cellar matches")
        else:
            self.log_test("Wine Pairing (With Cellar)", False, str(response))
        return success

    def test_pairing_history(self):
        """Test getting pairing history"""
        success, response = self.make_request('GET', 'pairings', expected_status=200)
        if success:
            pairings = response if isinstance(response, list) else []
            self.log_test("Pairing History", True, f"Found {len(pairings)} pairing records")
        else:
            self.log_test("Pairing History", False, str(response))
        return success

    def test_sommelier_chat(self):
        """Test sommelier chat functionality"""
        chat_data = {
            "message": "Was ist der Unterschied zwischen Bordeaux und Burgunder?",
            "session_id": None
        }
        
        success, response = self.make_request('POST', 'chat', data=chat_data, expected_status=200)
        if success:
            chat_response = response.get('response', '')[:100] + '...' if len(response.get('response', '')) > 100 else response.get('response', '')
            self.session_id = response.get('session_id')
            self.log_test("Sommelier Chat", True, f"Got response: {chat_response}")
        else:
            self.log_test("Sommelier Chat", False, str(response))
        return success

    def test_chat_history(self):
        """Test getting chat history"""
        if not self.session_id:
            self.log_test("Chat History", False, "No session ID available")
            return False
            
        success, response = self.make_request('GET', f'chat/{self.session_id}', expected_status=200)
        if success:
            messages = response if isinstance(response, list) else []
            self.log_test("Chat History", True, f"Found {len(messages)} chat messages")
        else:
            self.log_test("Chat History", False, str(response))
        return success

    def test_label_scan_basic(self):
        """Test wine label scanning with a simple test image"""
        # Create a simple test image (1x1 pixel PNG in base64)
        test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        scan_data = {
            "image_base64": test_image_base64
        }
        
        success, response = self.make_request('POST', 'scan-label', data=scan_data, expected_status=200)
        if success:
            # Validate response structure matches LabelScanResponse model
            required_fields = ['name', 'type']
            optional_fields = ['region', 'year', 'grape', 'notes']
            
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_test("Label Scanner (Basic)", False, f"Missing required fields: {missing_fields}")
                return False
            
            # Validate wine type is one of the allowed values
            valid_types = ['rot', 'weiss', 'rose', 'schaumwein']
            wine_type = response.get('type')
            if wine_type not in valid_types:
                self.log_test("Label Scanner (Basic)", False, f"Invalid wine type: {wine_type}, expected one of {valid_types}")
                return False
            
            wine_name = response.get('name', 'Unknown')
            self.log_test("Label Scanner (Basic)", True, f"Detected: {wine_name} ({wine_type})")
        else:
            self.log_test("Label Scanner (Basic)", False, str(response))
        return success

    def test_label_scan_empty_image(self):
        """Test label scanner with empty image data"""
        scan_data = {
            "image_base64": ""
        }
        
        success, response = self.make_request('POST', 'scan-label', data=scan_data, expected_status=200)
        if success:
            # Should handle empty image gracefully
            wine_name = response.get('name', 'Unknown')
            wine_type = response.get('type', 'Unknown')
            self.log_test("Label Scanner (Empty Image)", True, f"Handled empty image: {wine_name} ({wine_type})")
        else:
            self.log_test("Label Scanner (Empty Image)", False, str(response))
        return success

    def test_label_scan_invalid_base64(self):
        """Test label scanner with invalid base64 data"""
        scan_data = {
            "image_base64": "invalid_base64_data_here"
        }
        
        success, response = self.make_request('POST', 'scan-label', data=scan_data, expected_status=200)
        if success:
            # Should handle invalid base64 gracefully
            wine_name = response.get('name', 'Unknown')
            wine_type = response.get('type', 'Unknown')
            self.log_test("Label Scanner (Invalid Base64)", True, f"Handled invalid base64: {wine_name} ({wine_type})")
        else:
            self.log_test("Label Scanner (Invalid Base64)", False, str(response))
        return success

    def test_label_scan_missing_field(self):
        """Test label scanner with missing image_base64 field"""
        scan_data = {}
        
        success, response = self.make_request('POST', 'scan-label', data=scan_data, expected_status=422)
        if success:
            self.log_test("Label Scanner (Missing Field)", True, "Correctly rejected missing image_base64 field")
        else:
            # If it doesn't return 422, check if it handles it gracefully
            if response.get('status_code') == 200:
                self.log_test("Label Scanner (Missing Field)", True, "Handled missing field gracefully")
                return True
            else:
                self.log_test("Label Scanner (Missing Field)", False, str(response))
        return success

    def test_label_scan_wine_bottle_image(self):
        """Test label scanner with a more realistic wine bottle image"""
        # This is a small JPEG image encoded in base64 (wine bottle silhouette)
        wine_bottle_base64 = "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/wA=="
        
        scan_data = {
            "image_base64": wine_bottle_base64
        }
        
        success, response = self.make_request('POST', 'scan-label', data=scan_data, expected_status=200)
        if success:
            wine_name = response.get('name', 'Unknown')
            wine_type = response.get('type', 'Unknown')
            
            # Validate response structure
            required_fields = ['name', 'type']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                self.log_test("Label Scanner (Wine Bottle)", False, f"Missing required fields: {missing_fields}")
                return False
            
            # Check if year is properly handled (should be int or null)
            year = response.get('year')
            if year is not None and not isinstance(year, int):
                self.log_test("Label Scanner (Wine Bottle)", False, f"Year should be int or null, got: {type(year)}")
                return False
            
            self.log_test("Label Scanner (Wine Bottle)", True, f"Processed wine bottle image: {wine_name} ({wine_type})")
        else:
            self.log_test("Label Scanner (Wine Bottle)", False, str(response))
        return success

    def test_label_scan_response_structure(self):
        """Test that label scanner response matches expected LabelScanResponse model"""
        test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        scan_data = {
            "image_base64": test_image_base64
        }
        
        success, response = self.make_request('POST', 'scan-label', data=scan_data, expected_status=200)
        if success:
            # Validate complete response structure
            expected_structure = {
                'name': str,
                'type': str,
                'region': (str, type(None)),
                'year': (int, type(None)),
                'grape': (str, type(None)),
                'notes': (str, type(None))
            }
            
            validation_errors = []
            for field, expected_type in expected_structure.items():
                if field not in response:
                    validation_errors.append(f"Missing field: {field}")
                    continue
                
                value = response[field]
                if isinstance(expected_type, tuple):
                    # Field can be multiple types (e.g., str or None)
                    if not any(isinstance(value, t) for t in expected_type):
                        validation_errors.append(f"Field {field} has wrong type: expected {expected_type}, got {type(value)}")
                else:
                    # Field must be specific type
                    if not isinstance(value, expected_type):
                        validation_errors.append(f"Field {field} has wrong type: expected {expected_type}, got {type(value)}")
            
            # Validate wine type values
            valid_types = ['rot', 'weiss', 'rose', 'schaumwein']
            wine_type = response.get('type')
            if wine_type not in valid_types:
                validation_errors.append(f"Invalid wine type: {wine_type}, expected one of {valid_types}")
            
            if validation_errors:
                self.log_test("Label Scanner (Response Structure)", False, "; ".join(validation_errors))
                return False
            else:
                self.log_test("Label Scanner (Response Structure)", True, "Response structure matches LabelScanResponse model")
        else:
            self.log_test("Label Scanner (Response Structure)", False, str(response))
        return success

    def test_get_favorites(self):
        """Test getting favorite wines"""
        success, response = self.make_request('GET', 'favorites', expected_status=200)
        if success:
            favorite_wines = response.get('wines', []) if isinstance(response, dict) else []
            self.log_test("Get Favorites", True, f"Found {len(favorite_wines)} favorite wines")
        else:
            self.log_test("Get Favorites", False, str(response))
        return success

    def test_delete_wine(self):
        """Test deleting a wine"""
        if not self.test_wine_id:
            self.log_test("Delete Wine", False, "No wine ID available")
            return False
            
        success, response = self.make_request('DELETE', f'wines/{self.test_wine_id}', expected_status=200)
        if success:
            message = response.get('message', 'Deleted successfully')
            self.log_test("Delete Wine", True, message)
        else:
            self.log_test("Delete Wine", False, str(response))
        return success

    def run_all_tests(self):
        """Run all API tests"""
        print("🍷 Starting Wine Pairing API Tests")
        print("=" * 50)
        
        # Basic API tests
        self.test_root_endpoint()
        
        # Wine CRUD operations
        self.test_get_wines_empty()
        self.test_create_wine()
        self.test_get_wine_by_id()
        self.test_get_wines_with_data()
        self.test_toggle_favorite()
        
        # AI-powered features
        self.test_wine_pairing_basic()
        self.test_wine_pairing_with_cellar()
        self.test_pairing_history()
        
        # Sommelier chat
        self.test_sommelier_chat()
        self.test_chat_history()
        
        # Label scanning - comprehensive tests for robustness improvements
        self.test_label_scan_basic()
        self.test_label_scan_empty_image()
        self.test_label_scan_invalid_base64()
        self.test_label_scan_missing_field()
        self.test_label_scan_wine_bottle_image()
        self.test_label_scan_response_structure()
        
        # Favorites
        self.test_get_favorites()
        
        # Cleanup
        self.test_delete_wine()
        
        # Print results
        print("\n" + "=" * 50)
        print(f"🍷 Wine Pairing API Test Results")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = WinePairingAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())