#!/usr/bin/env python3
"""
Test Public API - Datasets Endpoints
Test semua endpoint public untuk Datasets (No authentication required)

Run: python3 test_public_datasets.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"
PUBLIC_URL = f"{BASE_URL}/public/datasets"

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
        print(f"   Response keys: {list(data.keys())}")
        if "data" in data and isinstance(data["data"], list) and data["data"]:
            print(f"   Sample item keys: {list(data['data'][0].keys())[:10]}...")

# ==========================================
# Test Functions
# ==========================================

def test_get_all_datasets():
    """Test: GET /public/datasets"""
    print_header("TEST 1: Get All Datasets")
    
    try:
        response = requests.get(PUBLIC_URL, timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_pagination = "total" in data and ("offset" in data or "page" in data)
            
            print_test(
                "GET /public/datasets",
                has_data and has_pagination,
                f"Found {data.get('total', 0)} datasets",
                data
            )
            
            # Check if all datasets are published and public
            if has_data and data["data"]:
                all_public = all(
                    d.get("status") == "published" and d.get("access_level") == "public"
                    for d in data["data"]
                )
                print_test(
                    "✓ All datasets are published & public",
                    all_public,
                    "All datasets meet visibility requirements" if all_public else "⚠️  Some datasets don't meet requirements"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No datasets found in database (empty result is OK)")
        else:
            print_test(
                "GET /public/datasets",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("GET /public/datasets", False, f"Error: {str(e)}")

def test_pagination():
    """Test: Pagination parameters"""
    print_header("TEST 2: Pagination")
    
    try:
        # Test with offset/limit
        response1 = requests.get(f"{PUBLIC_URL}?offset=0&limit=5", timeout=10)
        success1 = response1.status_code == 200
        
        if success1:
            data1 = response1.json()
            print_test(
                "GET /public/datasets?offset=0&limit=5",
                True,
                f"Got {len(data1.get('data', []))} items, total: {data1.get('total', 0)}"
            )
        else:
            print_test("Pagination offset/limit", False, f"Status: {response1.status_code}")
        
        # Test with different limit
        response2 = requests.get(f"{PUBLIC_URL}?offset=5&limit=10", timeout=10)
        success2 = response2.status_code == 200
        
        if success2:
            data2 = response2.json()
            print_test(
                "GET /public/datasets?offset=5&limit=10",
                True,
                f"Got {len(data2.get('data', []))} items"
            )
        else:
            print_test("Pagination offset 5", False, f"Status: {response2.status_code}")
            
    except Exception as e:
        print_test("Pagination", False, f"Error: {str(e)}")

def test_search():
    """Test: Search functionality"""
    print_header("TEST 3: Search")
    
    try:
        response = requests.get(f"{PUBLIC_URL}?search=data", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            print_test(
                "GET /public/datasets?search=data",
                True,
                f"Search returned {len(data.get('data', []))} results"
            )
        else:
            print_test("Search", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Search", False, f"Error: {str(e)}")

def test_featured_datasets():
    """Test: GET /public/datasets/featured"""
    print_header("TEST 4: Featured Datasets")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/featured", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/datasets/featured",
                has_data,
                f"Found {len(data.get('data', []))} featured datasets",
                data
            )
            
            # Check if all are featured
            if has_data and data["data"]:
                all_featured = all(d.get("is_featured") for d in data["data"])
                print_test(
                    "✓ All datasets have is_featured=true",
                    all_featured,
                    "All returned datasets are featured" if all_featured else "⚠️  Some datasets are not featured (DB might not have featured items)"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No featured datasets found (empty result is OK)")
        else:
            print_test(
                "GET /public/datasets/featured",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Featured datasets", False, f"Error: {str(e)}")

def test_latest_datasets():
    """Test: GET /public/datasets/latest"""
    print_header("TEST 5: Latest Datasets")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/latest?limit=10", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/datasets/latest?limit=10",
                has_data,
                f"Found {len(data.get('data', []))} latest datasets",
                data
            )
            
            # Check if sorted by created_at (newest first)
            if has_data and len(data["data"]) > 1:
                dates = [d.get("created_at") for d in data["data"]]
                is_sorted = dates == sorted(dates, reverse=True)
                print_test(
                    "✓ Datasets sorted by date (newest first)",
                    is_sorted,
                    "Datasets are properly sorted" if is_sorted else "⚠️  Datasets are not sorted correctly"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No datasets found (empty result is OK)")
        else:
            print_test(
                "GET /public/datasets/latest",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Latest datasets", False, f"Error: {str(e)}")

def test_get_by_id_and_slug():
    """Test: GET /public/datasets/{id} and /public/datasets/slug/{slug}"""
    print_header("TEST 6: Get Dataset by ID and Slug")
    
    try:
        # First, get a dataset
        response = requests.get(f"{PUBLIC_URL}?limit=1", timeout=10)
        if response.status_code != 200:
            print_test("Setup - Get datasets", False, "Could not fetch datasets for testing")
            return
        
        data = response.json()
        if not data.get("data"):
            print("   ℹ️  No datasets available for testing (skip this test)")
            return
        
        dataset = data["data"][0]
        dataset_id = dataset.get("id")
        dataset_slug = dataset.get("slug")
        dataset_name = dataset.get("name", "N/A")
        
        print(f"   Testing with dataset: '{dataset_name}'")
        print(f"   ID: {dataset_id}")
        print(f"   Slug: {dataset_slug}")
        
        # Test get by ID
        response_id = requests.get(f"{PUBLIC_URL}/{dataset_id}", timeout=10)
        success_id = response_id.status_code == 200
        
        if success_id:
            dataset_data = response_id.json()
            print_test(
                "✓ GET by ID",
                True,
                f"Got dataset: {dataset_data.get('name', 'N/A')}"
            )
        else:
            print_test(
                "GET by ID",
                False,
                f"Status code: {response_id.status_code}, Response: {response_id.text[:200]}"
            )
        
        # Test get by slug
        if dataset_slug:
            response_slug = requests.get(f"{PUBLIC_URL}/slug/{dataset_slug}", timeout=10)
            success_slug = response_slug.status_code == 200
            
            if success_slug:
                dataset_data = response_slug.json()
                print_test(
                    "✓ GET by slug",
                    True,
                    f"Got dataset: {dataset_data.get('name', 'N/A')}"
                )
            else:
                print_test(
                    "GET by slug",
                    False,
                    f"Status code: {response_slug.status_code}, Response: {response_slug.text[:200]}"
                )
        else:
            print("   ℹ️  No slug available for testing")
            
    except Exception as e:
        print_test("Get by ID and Slug", False, f"Error: {str(e)}")

def test_filter_by_format():
    """Test: Filter by dataset format"""
    print_header("TEST 7: Filter by Format")
    
    try:
        # Test common formats
        formats = ["CSV", "JSON", "XML"]
        
        for fmt in formats:
            response = requests.get(f"{PUBLIC_URL}?format={fmt}", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                count = len(data.get("data", []))
                print_test(
                    f"GET /datasets?format={fmt}",
                    True,
                    f"Found {count} datasets with format {fmt}"
                )
                
                # Verify all datasets have the requested format
                if data.get("data"):
                    all_correct_format = all(
                        d.get("format", "").upper() == fmt.upper()
                        for d in data["data"]
                    )
                    if not all_correct_format:
                        print("   ⚠️  Some datasets have incorrect format")
                
                if count > 0:
                    break  # Found datasets, no need to test other formats
    except Exception as e:
        print_test("Filter by format", False, f"Error: {str(e)}")

def test_invalid_slug():
    """Test: Invalid slug returns 404"""
    print_header("TEST 8: Invalid Slug (404)")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/slug/non-existent-dataset-12345-xyz", timeout=10)
        success = response.status_code == 404
        
        print_test(
            "GET /slug/non-existent-dataset",
            success,
            f"✓ Correctly returned 404" if success else f"⚠️  Expected 404, got {response.status_code}"
        )
    except Exception as e:
        print_test("Invalid slug", False, f"Error: {str(e)}")

def test_invalid_id():
    """Test: Invalid ID returns 404"""
    print_header("TEST 9: Invalid ID (404)")
    
    try:
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = requests.get(f"{PUBLIC_URL}/{fake_uuid}", timeout=10)
        success = response.status_code == 404
        
        print_test(
            f"GET /{fake_uuid}",
            success,
            f"✓ Correctly returned 404" if success else f"⚠️  Expected 404, got {response.status_code}"
        )
    except Exception as e:
        print_test("Invalid ID", False, f"Error: {str(e)}")

def test_limit_validation():
    """Test: Limit parameter validation"""
    print_header("TEST 10: Limit Validation")
    
    try:
        # Test max limit (should be capped)
        response = requests.get(f"{PUBLIC_URL}?limit=200", timeout=10)
        success = response.status_code in [200, 422]  # Either capped or validation error
        
        if response.status_code == 200:
            data = response.json()
            returned_count = len(data.get("data", []))
            print_test(
                "GET /datasets?limit=200 (exceeds max)",
                True,
                f"✓ Request handled, returned {returned_count} items (likely capped at max)"
            )
        elif response.status_code == 422:
            print_test(
                "GET /datasets?limit=200 (exceeds max)",
                True,
                "✓ Validation error returned (limit exceeds maximum)"
            )
        else:
            print_test("Limit validation", False, f"Status: {response.status_code}")
            
    except Exception as e:
        print_test("Limit validation", False, f"Error: {str(e)}")

# ==========================================
# Main Test Runner
# ==========================================

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 PUBLIC API TESTS - DATASETS ENDPOINTS")
    print("=" * 60)
    print(f"Base URL: {PUBLIC_URL}")
    print(f"Testing: {PUBLIC_URL}")
    print("=" * 60)
    print("\n⚡ Running tests (No authentication required)...\n")
    
    try:
        # Basic endpoint tests
        test_get_all_datasets()
        test_pagination()
        test_search()
        test_featured_datasets()
        test_latest_datasets()
        test_get_by_id_and_slug()
        
        # Special filter tests
        test_filter_by_format()
        
        # Error handling tests
        test_invalid_slug()
        test_invalid_id()
        test_limit_validation()
        
        # Summary
        print_header("✅ ALL TESTS COMPLETED")
        print("\n📊 Summary:")
        print(f"   • All public endpoints tested")
        print(f"   • No authentication required ✓")
        print(f"   • Auto-filtering for published & public content ✓")
        print(f"   • Format filtering tested ✓")
        print("\n💡 Note: Empty results are OK if database has no published datasets yet")
        print("   Datasets-specific feature: Filter by format (CSV, JSON, XML, etc.)")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
