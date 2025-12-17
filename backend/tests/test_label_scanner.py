#!/usr/bin/env python3
"""
Specific tests for the Label Scanner API endpoint improvements
Tests the robustness enhancements made to /api/scan-label
"""

import requests
import json
import base64
import sys
from typing import Dict, Any

class LabelScannerTester:
    def __init__(self, base_url="https://persist-data-2.preview.emergentagent.com"):
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

    def make_request(self, data: Dict, expected_status: int = 200) -> tuple[bool, Dict]:
        """Make POST request to scan-label endpoint"""
        url = f"{self.api_url}/scan-label"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
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

    def validate_response_structure(self, response: Dict) -> tuple[bool, str]:
        """Validate that response matches LabelScanResponse model"""
        required_fields = ['name', 'type']
        optional_fields = ['region', 'year', 'grape', 'notes']
        
        # Check required fields
        for field in required_fields:
            if field not in response:
                return False, f"Missing required field: {field}"
            if not isinstance(response[field], str):
                return False, f"Field {field} must be string, got {type(response[field])}"
        
        # Check optional fields types
        for field in optional_fields:
            if field in response and response[field] is not None:
                if field == 'year':
                    if not isinstance(response[field], int):
                        return False, f"Field {field} must be int or null, got {type(response[field])}"
                else:
                    if not isinstance(response[field], str):
                        return False, f"Field {field} must be string or null, got {type(response[field])}"
        
        # Validate wine type
        valid_types = ['rot', 'weiss', 'rose', 'schaumwein']
        if response['type'] not in valid_types:
            return False, f"Invalid wine type: {response['type']}, expected one of {valid_types}"
        
        return True, "Valid structure"

    def test_valid_image(self):
        """Test with a valid small image"""
        # Small valid PNG image (1x1 pixel)
        valid_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        
        data = {"image_base64": valid_image}
        success, response = self.make_request(data)
        
        if success:
            valid_structure, structure_msg = self.validate_response_structure(response)
            if valid_structure:
                self.log_test("Valid Image Processing", True, f"Name: {response['name']}, Type: {response['type']}")
            else:
                self.log_test("Valid Image Processing", False, structure_msg)
                return False
        else:
            self.log_test("Valid Image Processing", False, str(response))
            return False
        
        return True

    def test_empty_image(self):
        """Test with empty image_base64"""
        data = {"image_base64": ""}
        success, response = self.make_request(data)
        
        if success:
            # Should handle gracefully, not crash
            expected_names = ["Kein Bild", "Nicht erkannt", "Ungültiges Bild"]
            if response.get('name') in expected_names:
                self.log_test("Empty Image Handling", True, f"Gracefully handled: {response['name']}")
            else:
                self.log_test("Empty Image Handling", False, f"Unexpected response: {response}")
                return False
        else:
            self.log_test("Empty Image Handling", False, str(response))
            return False
        
        return True

    def test_invalid_base64(self):
        """Test with invalid base64 data"""
        data = {"image_base64": "this_is_not_valid_base64!@#$%"}
        success, response = self.make_request(data)
        
        if success:
            # Should handle gracefully
            expected_names = ["Ungültiges Bild", "Nicht erkannt", "Bildformat nicht unterstützt"]
            if response.get('name') in expected_names:
                self.log_test("Invalid Base64 Handling", True, f"Gracefully handled: {response['name']}")
            else:
                self.log_test("Invalid Base64 Handling", False, f"Unexpected response: {response}")
                return False
        else:
            self.log_test("Invalid Base64 Handling", False, str(response))
            return False
        
        return True

    def test_missing_field(self):
        """Test with missing image_base64 field"""
        data = {}
        success, response = self.make_request(data, expected_status=422)
        
        if success:
            self.log_test("Missing Field Validation", True, "Correctly rejected missing field")
        else:
            # Check if it's handled gracefully with 200 status
            if response.get('status_code') == 200:
                self.log_test("Missing Field Validation", True, "Handled missing field gracefully")
                return True
            else:
                self.log_test("Missing Field Validation", False, str(response))
                return False
        
        return True

    def test_null_image(self):
        """Test with null image_base64"""
        data = {"image_base64": None}
        success, response = self.make_request(data, expected_status=422)
        
        if success:
            self.log_test("Null Image Validation", True, "Correctly rejected null field")
        else:
            # Check if handled gracefully
            if response.get('status_code') == 200:
                expected_names = ["Kein Bild", "Nicht erkannt", "Ungültiges Bild"]
                if response.get('name') in expected_names:
                    self.log_test("Null Image Validation", True, f"Handled null gracefully: {response['name']}")
                    return True
            
            self.log_test("Null Image Validation", False, str(response))
            return False
        
        return True

    def test_very_large_base64(self):
        """Test with very large base64 string (simulating large image)"""
        # Create a large base64 string (not a valid image, but tests size handling)
        large_data = "A" * 10000  # 10KB of 'A' characters
        data = {"image_base64": large_data}
        success, response = self.make_request(data)
        
        if success:
            # Should handle gracefully, likely as invalid format
            expected_names = ["Ungültiges Bild", "Nicht erkannt", "Bildformat nicht unterstützt"]
            if response.get('name') in expected_names:
                self.log_test("Large Base64 Handling", True, f"Handled large data: {response['name']}")
            else:
                # If it processes it, that's also acceptable
                self.log_test("Large Base64 Handling", True, f"Processed large data: {response['name']}")
        else:
            # Should not crash with 500 error
            if response.get('status_code') == 500:
                self.log_test("Large Base64 Handling", False, "Server error on large data")
                return False
            else:
                self.log_test("Large Base64 Handling", True, "Handled large data appropriately")
        
        return True

    def test_data_url_format(self):
        """Test with data URL format (data:image/png;base64,...)"""
        # Valid PNG with data URL prefix
        base64_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        data_url = f"data:image/png;base64,{base64_data}"
        
        data = {"image_base64": data_url}
        success, response = self.make_request(data)
        
        if success:
            valid_structure, structure_msg = self.validate_response_structure(response)
            if valid_structure:
                self.log_test("Data URL Format", True, f"Processed data URL: {response['name']}")
            else:
                self.log_test("Data URL Format", False, structure_msg)
                return False
        else:
            self.log_test("Data URL Format", False, str(response))
            return False
        
        return True

    def run_all_tests(self):
        """Run all label scanner tests"""
        print("🏷️  Starting Label Scanner API Robustness Tests")
        print("=" * 60)
        
        # Test various scenarios
        self.test_valid_image()
        self.test_empty_image()
        self.test_invalid_base64()
        self.test_missing_field()
        self.test_null_image()
        self.test_very_large_base64()
        self.test_data_url_format()
        
        # Print results
        print("\n" + "=" * 60)
        print(f"🏷️  Label Scanner Test Results")
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = LabelScannerTester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())