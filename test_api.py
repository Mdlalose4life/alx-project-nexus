#!/usr/bin/env python3
"""
API Testing Script for Local Business Directory

This script demonstrates how to interact with the API endpoints.
Run this after setting up the development server.

Usage:
    python test_api.py

Requirements:
    pip install requests
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000/api/v1"
ADMIN_USERNAME = "admin"  # Change as needed
ADMIN_PASSWORD = "admin"  # Change as needed

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.user_data = None
    
    def print_response(self, response, description=""):
        """Pretty print API response"""
        print(f"\n{'='*60}")
        print(f"Test: {description}")
        print(f"URL: {response.url}")
        print(f"Status: {response.status_code}")
        
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except json.JSONDecodeError:
            print(f"Response: {response.text}")
        print(f"{'='*60}")
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.session.get(f"{self.base_url}/../health/")
        self.print_response(response, "Health Check")
        return response.status_code == 200
    
    def test_user_registration(self):
        """Test user registration"""
        user_data = {
            "username": f"testuser_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "password": "TestPassword123!",
            "password_confirm": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User",
            "user_type": "business_owner",
            "phone_number": "+27812345678"
        }
        
        response = self.session.post(f"{self.base_url}/auth/register/", json=user_data)
        self.print_response(response, "User Registration")
        
        if response.status_code == 201:
            data = response.json()
            self.access_token = data.get('tokens', {}).get('access')
            self.user_data = data.get('user')
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            return True
        return False
    
    def test_user_login(self):
        """Test user login with existing user"""
        if not self.user_data:
            print("No user data available for login test")
            return False
        
        login_data = {
            "username": self.user_data['username'],
            "password": "TestPassword123!"
        }
        
        response = self.session.post(f"{self.base_url}/auth/login/", json=login_data)
        self.print_response(response, "User Login")
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get('tokens', {}).get('access')
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            return True
        return False
    
    def test_user_profile(self):
        """Test getting user profile"""
        response = self.session.get(f"{self.base_url}/auth/me/")
        self.print_response(response, "Get User Profile")
        return response.status_code == 200
    
    def test_business_categories(self):
        """Test business categories endpoint"""
        response = self.session.get(f"{self.base_url}/business-categories/")
        self.print_response(response, "Get Business Categories")
        return response.status_code == 200
    
    def test_product_categories(self):
        """Test product categories endpoint"""
        response = self.session.get(f"{self.base_url}/product-categories/")
        self.print_response(response, "Get Product Categories")
        return response.status_code == 200
    
    def test_create_business(self):
        """Test creating a business"""
        business_data = {
            "name": f"Test Business {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": "A test business for API testing",
            "business_type": "spaza_shop",
            "phone_number": "+27812345678",
            "email": "business@test.com",
            "address": "123 Test Street, Test City",
            "city": "Cape Town",
            "province": "Western Cape",
            "postal_code": "8001",
            "latitude": -33.9249,
            "longitude": 18.4241
        }
        
        response = self.session.post(f"{self.base_url}/businesses/", json=business_data)
        self.print_response(response, "Create Business")
        
        if response.status_code == 201:
            return response.json()
        return None
    
    def test_list_businesses(self):
        """Test listing businesses"""
        response = self.session.get(f"{self.base_url}/businesses/")
        self.print_response(response, "List Businesses")
        return response.status_code == 200
    
    def test_nearby_businesses(self):
        """Test nearby businesses endpoint"""
        params = {
            'lat': -33.9249,
            'lon': 18.4241,
            'radius': 10
        }
        response = self.session.get(f"{self.base_url}/businesses/nearby/", params=params)
        self.print_response(response, "Get Nearby Businesses")
        return response.status_code == 200
    
    def test_featured_businesses(self):
        """Test featured businesses endpoint"""
        response = self.session.get(f"{self.base_url}/businesses/featured/")
        self.print_response(response, "Get Featured Businesses")
        return response.status_code == 200
    
    def test_create_product(self, business_slug=None):
        """Test creating a product"""
        product_data = {
            "name": f"Test Product {datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "description": "A test product for API testing",
            "price": 29.99,
            "original_price": 39.99,
            "stock_quantity": 100,
            "status": "active",
            "is_featured": True
        }
        
        response = self.session.post(f"{self.base_url}/products/", json=product_data)
        self.print_response(response, "Create Product")
        
        if response.status_code == 201:
            return response.json()
        return None
    
    def test_list_products(self):
        """Test listing products"""
        response = self.session.get(f"{self.base_url}/products/")
        self.print_response(response, "List Products")
        return response.status_code == 200
    
    def test_featured_products(self):
        """Test featured products endpoint"""
        response = self.session.get(f"{self.base_url}/products/featured/")
        self.print_response(response, "Get Featured Products")
        return response.status_code == 200
    
    def test_search_products(self):
        """Test product search"""
        params = {'q': 'test'}
        response = self.session.get(f"{self.base_url}/products/search/", params=params)
        self.print_response(response, "Search Products")
        return response.status_code == 200
    
    def test_swagger_docs(self):
        """Test that Swagger documentation is accessible"""
        response = self.session.get(f"{self.base_url}/../docs/")
        print(f"\nSwagger UI: {response.status_code} - {response.url}")
        
        response = self.session.get(f"{self.base_url}/../schema/")
        print(f"OpenAPI Schema: {response.status_code} - {response.url}")
        
        return True
    
    def run_all_tests(self):
        """Run all API tests"""
        print("Starting API Tests...")
        print(f"Base URL: {self.base_url}")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("User Profile", self.test_user_profile),
            ("Business Categories", self.test_business_categories),
            ("Product Categories", self.test_product_categories),
            ("Create Business", self.test_create_business),
            ("List Businesses", self.test_list_businesses),
            ("Nearby Businesses", self.test_nearby_businesses),
            ("Featured Businesses", self.test_featured_businesses),
            ("Create Product", self.test_create_product),
            ("List Products", self.test_list_products),
            ("Featured Products", self.test_featured_products),
            ("Search Products", self.test_search_products),
            ("Swagger Documentation", self.test_swagger_docs),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, "PASS" if result else "FAIL"))
                print(f"✅ {test_name}: {'PASS' if result else 'FAIL'}")
            except Exception as e:
                results.append((test_name, f"ERROR: {str(e)}"))
                print(f"❌ {test_name}: ERROR - {str(e)}")
        
        # Print summary
        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}")
        for test_name, result in results:
            status_icon = "✅" if result == "PASS" else "❌"
            print(f"{status_icon} {test_name}: {result}")
        
        total_tests = len(results)
        passed_tests = len([r for r in results if r[1] == "PASS"])
        print(f"\nTotal: {total_tests}, Passed: {passed_tests}, Failed: {total_tests - passed_tests}")
        
        return results

def main():
    """Main function to run API tests"""
    print("Local Business Directory API Tester")
    print("=" * 60)
    
    tester = APITester(BASE_URL)
    results = tester.run_all_tests()
    
    # Print API endpoints for reference
    print(f"\n{'='*60}")
    print("API ENDPOINTS REFERENCE")
    print(f"{'='*60}")
    print(f"Base URL: {BASE_URL}")
    print(f"Swagger UI: http://127.0.0.1:8000/api/docs/")
    print(f"ReDoc: http://127.0.0.1:8000/api/redoc/")
    print(f"OpenAPI Schema: http://127.0.0.1:8000/api/schema/")
    print(f"Admin Panel: http://127.0.0.1:8000/admin/")
    
    print(f"\nKey Endpoints:")
    endpoints = [
        "POST /api/v1/auth/register/ - User registration",
        "POST /api/v1/auth/login/ - User login",
        "GET /api/v1/auth/me/ - Get user profile",
        "GET /api/v1/businesses/ - List businesses",
        "POST /api/v1/businesses/ - Create business",
        "GET /api/v1/businesses/nearby/ - Find nearby businesses",
        "GET /api/v1/businesses/featured/ - Get featured businesses",
        "GET /api/v1/products/ - List products",
        "POST /api/v1/products/ - Create product",
        "GET /api/v1/products/featured/ - Get featured products",
        "GET /api/v1/products/search/ - Search products",
        "GET /api/v1/business-categories/ - List business categories",
        "GET /api/v1/product-categories/ - List product categories",
    ]
    
    for endpoint in endpoints:
        print(f"  {endpoint}")

if __name__ == "__main__":
    main()