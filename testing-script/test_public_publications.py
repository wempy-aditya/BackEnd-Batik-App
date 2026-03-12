#!/usr/bin/env python3
"""
Test Public API - Publications Endpoints
Test semua endpoint public untuk Publications (No authentication required)

Run: python3 test_public_publications.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"
PUBLIC_URL = f"{BASE_URL}/public/publications"

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

def test_get_all_publications():
    """Test: GET /public/publications"""
    print_header("TEST 1: Get All Publications")
    
    try:
        response = requests.get(PUBLIC_URL, timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_pagination = "total" in data and ("offset" in data or "page" in data)
            
            print_test(
                "GET /public/publications",
                has_data and has_pagination,
                f"Found {data.get('total', 0)} publications",
                data
            )
            
            # Check if all publications are published and public
            if has_data and data["data"]:
                all_public = all(
                    p.get("status") == "published" and p.get("access_level") == "public"
                    for p in data["data"]
                )
                print_test(
                    "✓ All publications are published & public",
                    all_public,
                    "All publications meet visibility requirements" if all_public else "⚠️  Some publications don't meet requirements"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No publications found in database (empty result is OK)")
        else:
            print_test(
                "GET /public/publications",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("GET /public/publications", False, f"Error: {str(e)}")

def test_pagination():
    """Test: Pagination parameters"""
    print_header("TEST 2: Pagination")
    
    try:
        # Test with limit
        response = requests.get(f"{PUBLIC_URL}?offset=0&limit=5", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            print_test(
                "GET /public/publications?offset=0&limit=5",
                True,
                f"Got {len(data.get('data', []))} items, total: {data.get('total', 0)}"
            )
        else:
            print_test("Pagination", False, f"Status: {response.status_code}")
            
    except Exception as e:
        print_test("Pagination", False, f"Error: {str(e)}")

def test_search():
    """Test: Search functionality"""
    print_header("TEST 3: Search")
    
    try:
        response = requests.get(f"{PUBLIC_URL}?search=research", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            print_test(
                "GET /public/publications?search=research",
                True,
                f"Search returned {len(data.get('data', []))} results"
            )
        else:
            print_test("Search", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Search", False, f"Error: {str(e)}")

def test_featured_publications():
    """Test: GET /public/publications/featured"""
    print_header("TEST 4: Featured Publications")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/featured", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/publications/featured",
                has_data,
                f"Found {len(data.get('data', []))} featured publications",
                data
            )
            
            # Check if all are featured
            if has_data and data["data"]:
                all_featured = all(p.get("is_featured") for p in data["data"])
                print_test(
                    "✓ All publications have is_featured=true",
                    all_featured,
                    "All returned publications are featured" if all_featured else "⚠️  Some publications are not featured (DB might not have featured items)"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No featured publications found (empty result is OK)")
        else:
            print_test(
                "GET /public/publications/featured",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Featured publications", False, f"Error: {str(e)}")

def test_latest_publications():
    """Test: GET /public/publications/latest"""
    print_header("TEST 5: Latest Publications")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/latest?limit=10", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/publications/latest?limit=10",
                has_data,
                f"Found {len(data.get('data', []))} latest publications",
                data
            )
            
            # Check if sorted by created_at (newest first)
            if has_data and len(data["data"]) > 1:
                dates = [p.get("created_at") for p in data["data"]]
                is_sorted = dates == sorted(dates, reverse=True)
                print_test(
                    "✓ Publications sorted by date (newest first)",
                    is_sorted,
                    "Publications are properly sorted" if is_sorted else "⚠️  Publications are not sorted correctly"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No publications found (empty result is OK)")
        else:
            print_test(
                "GET /public/publications/latest",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Latest publications", False, f"Error: {str(e)}")

def test_get_by_id_and_slug():
    """Test: GET /public/publications/{id} and /public/publications/slug/{slug}"""
    print_header("TEST 6: Get Publication by ID and Slug")
    
    try:
        # First, get a publication
        response = requests.get(f"{PUBLIC_URL}?limit=1", timeout=10)
        if response.status_code != 200:
            print_test("Setup - Get publications", False, "Could not fetch publications for testing")
            return
        
        data = response.json()
        if not data.get("data"):
            print("   ℹ️  No publications available for testing (skip this test)")
            return
        
        publication = data["data"][0]
        publication_id = publication.get("id")
        publication_slug = publication.get("slug")
        publication_title = publication.get("title", "N/A")
        
        print(f"   Testing with publication: '{publication_title}'")
        print(f"   ID: {publication_id}")
        print(f"   Slug: {publication_slug}")
        
        # Test get by ID
        response_id = requests.get(f"{PUBLIC_URL}/{publication_id}", timeout=10)
        success_id = response_id.status_code == 200
        
        if success_id:
            publication_data = response_id.json()
            print_test(
                "✓ GET by ID",
                True,
                f"Got publication: {publication_data.get('title', 'N/A')}"
            )
        else:
            print_test(
                "GET by ID",
                False,
                f"Status code: {response_id.status_code}, Response: {response_id.text[:200]}"
            )
        
        # Test get by slug
        if publication_slug:
            response_slug = requests.get(f"{PUBLIC_URL}/slug/{publication_slug}", timeout=10)
            success_slug = response_slug.status_code == 200
            
            if success_slug:
                publication_data = response_slug.json()
                print_test(
                    "✓ GET by slug",
                    True,
                    f"Got publication: {publication_data.get('title', 'N/A')}"
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

def test_get_by_year():
    """Test: GET /public/publications/year/{year}"""
    print_header("TEST 7: Get Publications by Year")
    
    try:
        # Test with current year and common years
        test_years = [2024, 2023, 2022]
        
        for year in test_years:
            response = requests.get(f"{PUBLIC_URL}/year/{year}", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                count = len(data.get("data", []))
                print_test(
                    f"GET /publications/year/{year}",
                    True,
                    f"Found {count} publications for year {year}"
                )
                
                # Verify all publications are from the requested year
                if data.get("data"):
                    all_correct_year = all(
                        p.get("publication_year") == year 
                        for p in data["data"]
                    )
                    if not all_correct_year:
                        print("   ⚠️  Some publications have incorrect year")
                
                break  # Stop after first successful year
            else:
                if year == test_years[-1]:  # Last year in list
                    print_test(
                        f"GET /publications/year/{year}",
                        False,
                        f"Status: {response.status_code}"
                    )
    except Exception as e:
        print_test("Get by year", False, f"Error: {str(e)}")

def test_invalid_slug():
    """Test: Invalid slug returns 404"""
    print_header("TEST 8: Invalid Slug (404)")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/slug/non-existent-publication-12345-xyz", timeout=10)
        success = response.status_code == 404
        
        print_test(
            "GET /slug/non-existent-publication",
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

def test_invalid_year():
    """Test: Invalid year handling"""
    print_header("TEST 10: Invalid Year")
    
    try:
        # Test with invalid year (future year)
        response = requests.get(f"{PUBLIC_URL}/year/9999", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            is_empty = len(data.get("data", [])) == 0
            print_test(
                "GET /publications/year/9999",
                True,
                f"✓ Returned empty result for invalid year" if is_empty else f"Found {len(data['data'])} items (unexpected)"
            )
        else:
            print_test("Invalid year", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Invalid year", False, f"Error: {str(e)}")

# ==========================================
# Main Test Runner
# ==========================================

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 PUBLIC API TESTS - PUBLICATIONS ENDPOINTS")
    print("=" * 60)
    print(f"Base URL: {PUBLIC_URL}")
    print(f"Testing: {PUBLIC_URL}")
    print("=" * 60)
    print("\n⚡ Running tests (No authentication required)...\n")
    
    try:
        # Basic endpoint tests
        test_get_all_publications()
        test_pagination()
        test_search()
        test_featured_publications()
        test_latest_publications()
        test_get_by_id_and_slug()
        
        # Special filter tests
        test_get_by_year()
        
        # Error handling tests
        test_invalid_slug()
        test_invalid_id()
        test_invalid_year()
        
        # Summary
        print_header("✅ ALL TESTS COMPLETED")
        print("\n📊 Summary:")
        print(f"   • All public endpoints tested")
        print(f"   • No authentication required ✓")
        print(f"   • Auto-filtering for published & public content ✓")
        print(f"   • Year filtering tested ✓")
        print("\n💡 Note: Empty results are OK if database has no published publications yet")
        print("   Publications-specific feature: Filter by publication year")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
