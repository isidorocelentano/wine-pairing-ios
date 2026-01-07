#!/usr/bin/env python3
"""
Password Reset Email Testing for Wine Pairing Live Site
Tests the password reset email functionality on https://wine-pairing.online
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class PasswordResetTester:
    def __init__(self, base_url="https://wine-pairing.online"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.session = requests.Session()
        self.test_email = "isicel@yahoo.com"

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
                response = self.session.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                response = self.session.post(url, json=data, headers=headers, timeout=30)
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
        """Test 1: Check health endpoint to verify deployment version"""
        print("\n=== TEST 1: Health Endpoint ===")
        success, response = self.make_request('GET', 'health', expected_status=200)
        
        if success:
            version = response.get('version', 'unknown')
            db_status = response.get('database', 'unknown')
            email_configured = response.get('email_configured', False)
            resend_key_prefix = response.get('resend_key_prefix', 'not set')
            sender_email = response.get('sender_email', 'not set')
            frontend_base_url = response.get('frontend_base_url', 'not set')
            
            print(f"   Version: {version}")
            print(f"   Database: {db_status}")
            print(f"   Email configured: {email_configured}")
            print(f"   Resend key prefix: {resend_key_prefix}")
            print(f"   Sender email: {sender_email}")
            print(f"   Frontend base URL: {frontend_base_url}")
            
            self.log_test("Health Check", True, f"Version: {version}, DB: {db_status}, Email: {email_configured}")
            
            # Check if this is the expected version with debug info
            if version == "v4-debug":
                print("   ✅ Found v4-debug version - debug info should be available")
            else:
                print(f"   ⚠️  Version is {version}, expected v4-debug for debug info")
                
        else:
            self.log_test("Health Check", False, str(response))
        
        return success, response

    def test_debug_endpoint(self):
        """Test 2: Test the debug endpoint (this should work)"""
        print("\n=== TEST 2: Debug Endpoint ===")
        endpoint = f"debug/forgot-password-test/{self.test_email}"
        success, response = self.make_request('GET', endpoint, expected_status=200)
        
        if success:
            print(f"   Response: {json.dumps(response, indent=2)}")
            
            # Check for expected fields
            expected_fields = ['success', 'message', 'email_sent', 'version']
            missing_fields = [field for field in expected_fields if field not in response]
            
            if missing_fields:
                self.log_test("Debug Endpoint", False, f"Missing fields: {missing_fields}")
            else:
                email_sent = response.get('email_sent', False)
                version = response.get('version', 'unknown')
                message = response.get('message', '')
                
                self.log_test("Debug Endpoint", True, 
                             f"Email sent: {email_sent}, Version: {version}, Message: {message}")
        else:
            self.log_test("Debug Endpoint", False, str(response))
        
        return success, response

    def test_actual_forgot_password(self):
        """Test 3: Test the actual forgot-password endpoint (this doesn't work)"""
        print("\n=== TEST 3: Actual Forgot Password Endpoint ===")
        
        data = {"email": self.test_email}
        success, response = self.make_request('POST', 'auth/forgot-password', data=data, expected_status=200)
        
        if success:
            print(f"   Response: {json.dumps(response, indent=2)}")
            
            # Check for debug info fields
            debug_fields = ['version', 'email_sent', 'error', 'debug_info']
            found_debug_fields = [field for field in debug_fields if field in response]
            
            if found_debug_fields:
                print(f"   Debug fields found: {found_debug_fields}")
                
                version = response.get('version')
                email_sent = response.get('email_sent')
                error = response.get('error')
                debug_info = response.get('debug_info')
                
                if version:
                    print(f"   Version: {version}")
                if email_sent is not None:
                    print(f"   Email sent: {email_sent}")
                if error:
                    print(f"   Error: {error}")
                if debug_info:
                    print(f"   Debug info: {debug_info}")
                    
                self.log_test("Actual Forgot Password", True, 
                             f"Got debug response - Email sent: {email_sent}, Error: {error}")
            else:
                # Standard response without debug info
                message = response.get('message', '')
                self.log_test("Actual Forgot Password", True, f"Standard response: {message}")
                
        else:
            self.log_test("Actual Forgot Password", False, str(response))
        
        return success, response

    def test_check_token_endpoint(self):
        """Test 4: Check if token is being saved"""
        print("\n=== TEST 4: Check Token Endpoint ===")
        endpoint = f"debug/check-token/{self.test_email}"
        success, response = self.make_request('GET', endpoint, expected_status=200)
        
        if success:
            print(f"   Response: {json.dumps(response, indent=2)}")
            
            has_token = response.get('has_token', False)
            token_preview = response.get('token_preview')
            expiry = response.get('expiry')
            
            if has_token:
                print(f"   ✅ Token found for {self.test_email}")
                if token_preview:
                    print(f"   Token preview: {token_preview}")
                if expiry:
                    print(f"   Token expiry: {expiry}")
            else:
                print(f"   ❌ No token found for {self.test_email}")
                
            self.log_test("Check Token", True, f"Token found: {has_token}")
        else:
            self.log_test("Check Token", False, str(response))
        
        return success, response

    def compare_responses(self, debug_response, actual_response):
        """Test 5: Compare responses from debug and actual endpoints"""
        print("\n=== TEST 5: Response Comparison ===")
        
        if not debug_response or not actual_response:
            print("   ❌ Cannot compare - one or both responses missing")
            return
        
        print("   Comparing debug endpoint vs actual endpoint:")
        
        # Compare email_sent status
        debug_email_sent = debug_response.get('email_sent', 'not_found')
        actual_email_sent = actual_response.get('email_sent', 'not_found')
        
        print(f"   Debug endpoint email_sent: {debug_email_sent}")
        print(f"   Actual endpoint email_sent: {actual_email_sent}")
        
        if debug_email_sent != actual_email_sent:
            print(f"   ⚠️  EMAIL_SENT MISMATCH: Debug={debug_email_sent}, Actual={actual_email_sent}")
        else:
            print(f"   ✅ Email sent status matches: {debug_email_sent}")
        
        # Compare versions
        debug_version = debug_response.get('version', 'not_found')
        actual_version = actual_response.get('version', 'not_found')
        
        print(f"   Debug endpoint version: {debug_version}")
        print(f"   Actual endpoint version: {actual_version}")
        
        if debug_version != actual_version:
            print(f"   ⚠️  VERSION MISMATCH: Debug={debug_version}, Actual={actual_version}")
        else:
            print(f"   ✅ Version matches: {debug_version}")
        
        # Check for errors in actual response
        actual_error = actual_response.get('error')
        if actual_error:
            print(f"   ❌ ACTUAL ENDPOINT ERROR: {actual_error}")
        else:
            print(f"   ✅ No error in actual endpoint")
        
        # Check for debug info
        debug_info = actual_response.get('debug_info')
        if debug_info:
            print(f"   📋 Debug info from actual endpoint: {debug_info}")

    def run_all_tests(self):
        """Run all password reset tests"""
        print("🧪 Starting Password Reset Email Testing on LIVE site")
        print(f"🌐 Testing URL: {self.base_url}")
        print(f"📧 Test email: {self.test_email}")
        print("=" * 60)
        
        # Store responses for comparison
        health_response = None
        debug_response = None
        actual_response = None
        token_response = None
        
        # Test 1: Health check
        try:
            success, health_response = self.test_health_endpoint()
        except Exception as e:
            print(f"❌ Health check failed with exception: {e}")
        
        # Test 2: Debug endpoint
        try:
            success, debug_response = self.test_debug_endpoint()
        except Exception as e:
            print(f"❌ Debug endpoint failed with exception: {e}")
        
        # Test 3: Actual forgot password
        try:
            success, actual_response = self.test_actual_forgot_password()
        except Exception as e:
            print(f"❌ Actual forgot password failed with exception: {e}")
        
        # Test 4: Check token
        try:
            success, token_response = self.test_check_token_endpoint()
        except Exception as e:
            print(f"❌ Check token failed with exception: {e}")
        
        # Test 5: Compare responses
        try:
            self.compare_responses(debug_response, actual_response)
        except Exception as e:
            print(f"❌ Response comparison failed with exception: {e}")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run*100):.1f}%" if self.tests_run > 0 else "0%")
        
        # Analysis
        print("\n🔍 ANALYSIS:")
        
        if debug_response and actual_response:
            debug_email_sent = debug_response.get('email_sent', False)
            actual_email_sent = actual_response.get('email_sent', False)
            
            if debug_email_sent and not actual_email_sent:
                print("❌ CRITICAL ISSUE: Debug endpoint sends emails but actual endpoint doesn't")
                actual_error = actual_response.get('error', 'No error details')
                print(f"   Actual endpoint error: {actual_error}")
            elif debug_email_sent and actual_email_sent:
                print("✅ Both endpoints report successful email sending")
            elif not debug_email_sent and not actual_email_sent:
                print("⚠️  Neither endpoint is sending emails")
            else:
                print("🤔 Unexpected state - actual works but debug doesn't")
        
        if token_response:
            has_token = token_response.get('has_token', False)
            if not has_token:
                print("❌ ISSUE: Password reset token is not being saved to database")
            else:
                print("✅ Password reset token is being saved correctly")
        
        return self.tests_passed == self.tests_run

def main():
    """Main function"""
    tester = PasswordResetTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()