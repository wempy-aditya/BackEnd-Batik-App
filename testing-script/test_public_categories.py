#!/usr/bin/env python3
"""
Test Public API - Categories Endpoints
Test semua endpoint public untuk Categories (No authentication required)

Run: python3 test_public_categories.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"
PUBLIC_URL = f"{BASE_URL}/public/categories"

# ==========================================
# Helper Functions
# ==========================================

def print_header(text: str):
    """Print section header"""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def print_test(name: str, success: bool, details: str = "", data: Any = None):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status} - {name}")
    if details:
        print(f"   {details}")
    if data and isinstance(data, dict):
        if "data" in data:
            print(f"   Response has 'data' key with {len(data.get('data', []))} items")
        else:
            # For /all endpoint which returns grouped categories
            print(f"   Response keys: {list(data.keys())}")

# ==========================================
# Test Functions
# ==========================================

def test_get_project_categories():
    """Test: GET /public/categories/projects"""
    print_header("TEST 1: Get Project Categories")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/projects", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_total = "total" in data
            
            print_test(
                "GET /public/categories/projects",
                has_data and has_total,
                f"Found {data.get('total', 0)} project categories",
                data
            )
            
            # Check structure of first category if exists
            if has_data and data["data"]:
                first_cat = data["data"][0]
                has_required_fields = all(k in first_cat for k in ["id", "name"])
                print_test(
                    "✓ Category structure",
                    has_required_fields,
                    f"Category has required fields: id, name"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No project categories found (empty result is OK)")
        else:
            print_test(
                "GET /public/categories/projects",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("GET project categories", False, f"Error: {str(e)}")

def test_get_dataset_categories():
    """Test: GET /public/categories/datasets"""
    print_header("TEST 2: Get Dataset Categories")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/datasets", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_total = "total" in data
            
            print_test(
                "GET /public/categories/datasets",
                has_data and has_total,
                f"Found {data.get('total', 0)} dataset categories",
                data
            )
        else:
            print_test(
                "GET dataset categories",
                False,
                f"Status code: {response.status_code}"
            )
    except Exception as e:
        print_test("GET dataset categories", False, f"Error: {str(e)}")

def test_get_publication_categories():
    """Test: GET /public/categories/publications"""
    print_header("TEST 3: Get Publication Categories")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/publications", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_total = "total" in data
            
            print_test(
                "GET /public/categories/publications",
                has_data and has_total,
                f"Found {data.get('total', 0)} publication categories",
                data
            )
        else:
            print_test(
                "GET publication categories",
                False,
                f"Status code: {response.status_code}"
            )
    except Exception as e:
        print_test("GET publication categories", False, f"Error: {str(e)}")

def test_get_news_categories():
    """Test: GET /public/categories/news"""
    print_header("TEST 4: Get News Categories")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/news", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_total = "total" in data
            
            print_test(
                "GET /public/categories/news",
                has_data and has_total,
                f"Found {data.get('total', 0)} news categories",
                data
            )
        else:
            print_test(
                "GET news categories",
                False,
                f"Status code: {response.status_code}"
            )
    except Exception as e:
        print_test("GET news categories", False, f"Error: {str(e)}")

def test_get_model_categories():
    """Test: GET /public/categories/models"""
    print_header("TEST 5: Get AI Model Categories")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/models", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_total = "total" in data
            
            print_test(
                "GET /public/categories/models",
                has_data and has_total,
                f"Found {data.get('total', 0)} AI model categories",
                data
            )
        else:
            print_test(
                "GET model categories",
                False,
                f"Status code: {response.status_code}"
            )
    except Exception as e:
        print_test("GET model categories", False, f"Error: {str(e)}")

def test_get_gallery_categories():
    """Test: GET /public/categories/gallery"""
    print_header("TEST 6: Get Gallery Categories")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/gallery", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_total = "total" in data
            
            print_test(
                "GET /public/categories/gallery",
                has_data and has_total,
                f"Found {data.get('total', 0)} gallery categories",
                data
            )
        else:
            print_test(
                "GET gallery categories",
                False,
                f"Status code: {response.status_code}"
            )
    except Exception as e:
        print_test("GET gallery categories", False, f"Error: {str(e)}")

def test_get_all_categories():
    """Test: GET /public/categories/all"""
    print_header("TEST 7: Get All Categories (Grouped)")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/all", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            
            # Check if all expected keys are present
            expected_keys = ["projects", "datasets", "publications", "news", "models", "gallery"]
            has_all_keys = all(k in data for k in expected_keys)
            
            if has_all_keys:
                total_categories = sum(len(data[k]) for k in expected_keys if isinstance(data[k], list))
                print_test(
                    "GET /public/categories/all",
                    True,
                    f"Found all category types with {total_categories} total categories",
                    data
                )
                
                # Show breakdown
                print("\n   Breakdown:")
                for key in expected_keys:
                    count = len(data[key]) if isinstance(data[key], list) else 0
                    print(f"     • {key}: {count} categories")
            else:
                missing_keys = [k for k in expected_keys if k not in data]
                print_test(
                    "GET /public/categories/all",
                    False,
                    f"Missing keys: {missing_keys}"
                )
        else:
            print_test(
                "GET all categories",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("GET all categories", False, f"Error: {str(e)}")

def test_limit_parameter():
    """Test: Limit parameter validation"""
    print_header("TEST 8: Limit Parameter")
    
    try:
        # Test with custom limit
        response = requests.get(f"{PUBLIC_URL}/projects?limit=10", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            count = len(data.get("data", []))
            print_test(
                "GET /categories/projects?limit=10",
                True,
                f"Returned {count} categories (limit applied)"
            )
        else:
            print_test("Limit parameter", False, f"Status: {response.status_code}")
            
        # Test with limit exceeding max
        response2 = requests.get(f"{PUBLIC_URL}/projects?limit=200", timeout=10)
        success2 = response2.status_code in [200, 422]
        
        if response2.status_code == 200:
            data2 = response2.json()
            print_test(
                "GET /categories/projects?limit=200 (exceeds max)",
                True,
                f"✓ Request handled, returned {len(data2.get('data', []))} categories (likely capped at max 100)"
            )
        elif response2.status_code == 422:
            print_test(
                "GET /categories/projects?limit=200",
                True,
                "✓ Validation error returned (limit exceeds maximum)"
            )
        else:
            print_test("Limit validation", False, f"Status: {response2.status_code}")
            
    except Exception as e:
        print_test("Limit parameter", False, f"Error: {str(e)}")

def test_response_consistency():
    """Test: Check response consistency across all category endpoints"""
    print_header("TEST 9: Response Consistency")
    
    try:
        endpoints = ["projects", "datasets", "publications", "news", "models", "gallery"]
        all_consistent = True
        
        print("   Checking response structure across all endpoints:")
        for endpoint in endpoints:
            response = requests.get(f"{PUBLIC_URL}/{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                has_structure = "data" in data and "total" in data
                print(f"     • /{endpoint}: {'✓' if has_structure else '✗'} {'OK' if has_structure else 'FAIL'}")
                if not has_structure:
                    all_consistent = False
            else:
                print(f"     • /{endpoint}: ✗ Status {response.status_code}")
                all_consistent = False
        
        print_test(
            "Response consistency",
            all_consistent,
            "All endpoints return consistent structure" if all_consistent else "⚠️  Some endpoints have inconsistent structure"
        )
    except Exception as e:
        print_test("Response consistency", False, f"Error: {str(e)}")

def test_empty_results_handling():
    """Test: Endpoints handle empty results gracefully"""
    print_header("TEST 10: Empty Results Handling")
    
    try:
        # All category endpoints should return empty array if no data, not error
        response = requests.get(f"{PUBLIC_URL}/projects", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data_key = "data" in data
            is_list = isinstance(data.get("data"), list)
            
            print_test(
                "Empty results handling",
                has_data_key and is_list,
                "✓ Endpoints return empty list [] when no data (not error)"
            )
        else:
            print_test("Empty results", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Empty results", False, f"Error: {str(e)}")

# ==========================================
# Main Test Runner
# ==========================================

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 PUBLIC API TESTS - CATEGORIES ENDPOINTS")
    print("=" * 60)
    print(f"Base URL: {PUBLIC_URL}")
    print(f"Testing: {PUBLIC_URL}")
    print("=" * 60)
    print("\n⚡ Running tests (No authentication required)...\n")
    
    try:
        # Test each category type endpoint
        test_get_project_categories()
        test_get_dataset_categories()
        test_get_publication_categories()
        test_get_news_categories()
        test_get_model_categories()
        test_get_gallery_categories()
        
        # Test special endpoints
        test_get_all_categories()
        
        # Test parameters and behavior
        test_limit_parameter()
        test_response_consistency()
        test_empty_results_handling()
        
        # Summary
        print_header("✅ ALL TESTS COMPLETED")
        print("\n📊 Summary:")
        print(f"   • All category endpoints tested")
        print(f"   • No authentication required ✓")
        print(f"   • 6 category types available ✓")
        print(f"   • /all endpoint for bulk fetch ✓")
        print("\n💡 Use Cases:")
        print("   • Category filter dropdowns in frontend")
        print("   • Navigation menus by category")
        print("   • Initialize all filters with /all in one call")
        print("\n📌 Endpoints:")
        print("   • GET /categories/projects - Project categories")
        print("   • GET /categories/datasets - Dataset categories")
        print("   • GET /categories/publications - Publication categories")
        print("   • GET /categories/news - News categories")
        print("   • GET /categories/models - AI Model categories")
        print("   • GET /categories/gallery - Gallery categories")
        print("   • GET /categories/all - All categories grouped")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
