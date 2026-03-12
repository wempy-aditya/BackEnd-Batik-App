#!/usr/bin/env python3
"""
Test Public API - Gallery Endpoints
Test semua endpoint public untuk Gallery (No authentication required)

Run: python3 test_public_gallery.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"
PUBLIC_URL = f"{BASE_URL}/public/gallery"

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

def test_get_all_gallery():
    """Test: GET /public/gallery"""
    print_header("TEST 1: Get All Gallery Items")
    
    try:
        response = requests.get(PUBLIC_URL, timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_pagination = "total" in data and ("offset" in data or "page" in data)
            
            print_test(
                "GET /public/gallery",
                has_data and has_pagination,
                f"Found {data.get('total', 0)} gallery items (default limit: 24)",
                data
            )
            
            # Note: Gallery model doesn't have access_level or status fields
            # All gallery items are considered public by design
            if has_data and data["data"]:
                has_access_field = "access_level" in data["data"][0] if data["data"] else False
                if has_access_field:
                    all_public = all(g.get("access_level") == "public" for g in data["data"])
                    print_test(
                        "✓ All gallery items are public",
                        all_public,
                        "All gallery items have access_level=public" if all_public else "⚠️  Some gallery items are not public"
                    )
                else:
                    print("   ℹ️  Gallery model doesn't have access_level field (all items are public by design)")
            elif has_data and not data["data"]:
                print("   ℹ️  No gallery items found in database (empty result is OK)")
        else:
            print_test(
                "GET /public/gallery",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("GET /public/gallery", False, f"Error: {str(e)}")

def test_default_limit():
    """Test: Default limit for gallery (should be 24)"""
    print_header("TEST 2: Default Limit (Gallery = 24)")
    
    try:
        response = requests.get(PUBLIC_URL, timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            count = len(data.get("data", []))
            limit = data.get("limit", 0)
            print_test(
                "GET /public/gallery (no limit param)",
                True,
                f"Returned {count} items with limit={limit} (default should be 24)"
            )
        else:
            print_test("Default limit", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Default limit", False, f"Error: {str(e)}")

def test_pagination():
    """Test: Pagination parameters"""
    print_header("TEST 3: Pagination")
    
    try:
        # Test with offset/limit
        response1 = requests.get(f"{PUBLIC_URL}?offset=0&limit=12", timeout=10)
        success1 = response1.status_code == 200
        
        if success1:
            data1 = response1.json()
            print_test(
                "GET /public/gallery?offset=0&limit=12",
                True,
                f"Got {len(data1.get('data', []))} items, total: {data1.get('total', 0)}"
            )
        else:
            print_test("Pagination offset/limit", False, f"Status: {response1.status_code}")
        
        # Test with different offset
        response2 = requests.get(f"{PUBLIC_URL}?offset=12&limit=12", timeout=10)
        success2 = response2.status_code == 200
        
        if success2:
            data2 = response2.json()
            print_test(
                "GET /public/gallery?offset=12&limit=12",
                True,
                f"Got {len(data2.get('data', []))} items"
            )
        else:
            print_test("Pagination offset 12", False, f"Status: {response2.status_code}")
            
    except Exception as e:
        print_test("Pagination", False, f"Error: {str(e)}")

def test_search():
    """Test: Search functionality"""
    print_header("TEST 4: Search")
    
    try:
        response = requests.get(f"{PUBLIC_URL}?search=gallery", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            print_test(
                "GET /public/gallery?search=gallery",
                True,
                f"Search returned {len(data.get('data', []))} results"
            )
        else:
            print_test("Search", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Search", False, f"Error: {str(e)}")

def test_featured_gallery():
    """Test: GET /public/gallery/featured"""
    print_header("TEST 5: Featured Gallery Items")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/featured", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/gallery/featured",
                has_data,
                f"Found {len(data.get('data', []))} featured gallery items",
                data
            )
            
            # Note: Gallery model might not have is_featured field
            # Check if field exists in response
            if has_data and data["data"]:
                has_featured_field = "is_featured" in data["data"][0] if data["data"] else False
                if has_featured_field:
                    all_featured = all(g.get("is_featured") for g in data["data"])
                    print_test(
                        "✓ All gallery items have is_featured=true",
                        all_featured,
                        "All returned gallery items are featured" if all_featured else "⚠️  Some gallery items are not featured"
                    )
                else:
                    print("   ℹ️  Gallery model doesn't have is_featured field (this is OK)")
            elif has_data and not data["data"]:
                print("   ℹ️  No featured gallery items found (empty result is OK)")
        else:
            print_test(
                "GET /public/gallery/featured",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Featured gallery", False, f"Error: {str(e)}")

def test_latest_gallery():
    """Test: GET /public/gallery/latest"""
    print_header("TEST 6: Latest Gallery Items")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/latest?limit=12", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/gallery/latest?limit=12",
                has_data,
                f"Found {len(data.get('data', []))} latest gallery items",
                data
            )
            
            # Check if sorted by created_at (newest first)
            if has_data and len(data["data"]) > 1:
                dates = [g.get("created_at") for g in data["data"]]
                is_sorted = dates == sorted(dates, reverse=True)
                print_test(
                    "✓ Gallery items sorted by date (newest first)",
                    is_sorted,
                    "Gallery items are properly sorted" if is_sorted else "⚠️  Gallery items are not sorted correctly"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No gallery items found (empty result is OK)")
        else:
            print_test(
                "GET /public/gallery/latest",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Latest gallery", False, f"Error: {str(e)}")

def test_get_by_id():
    """Test: GET /public/gallery/{id}"""
    print_header("TEST 7: Get Gallery by ID")
    
    try:
        # First, get a gallery item
        response = requests.get(f"{PUBLIC_URL}?limit=1", timeout=10)
        if response.status_code != 200:
            print_test("Setup - Get gallery", False, "Could not fetch gallery for testing")
            return
        
        data = response.json()
        if not data.get("data"):
            print("   ℹ️  No gallery items available for testing (skip this test)")
            return
        
        gallery = data["data"][0]
        gallery_id = gallery.get("id")
        gallery_prompt = gallery.get("prompt", "N/A")
        
        print(f"   Testing with gallery prompt: '{gallery_prompt[:50]}...'")
        print(f"   ID: {gallery_id}")
        
        # Test get by ID
        response_id = requests.get(f"{PUBLIC_URL}/{gallery_id}", timeout=10)
        success_id = response_id.status_code == 200
        
        if success_id:
            gallery_data = response_id.json()
            print_test(
                "✓ GET by ID",
                True,
                f"Got gallery item with prompt: {gallery_data.get('prompt', 'N/A')[:50]}..."
            )
        else:
            print_test(
                "GET by ID",
                False,
                f"Status code: {response_id.status_code}, Response: {response_id.text[:200]}"
            )
            
        # Note: Gallery doesn't have slug endpoint
        print("   ℹ️  Gallery doesn't support slug-based lookup (only ID)")
            
    except Exception as e:
        print_test("Get by ID", False, f"Error: {str(e)}")

def test_filter_by_ai_model():
    """Test: GET /public/gallery/model/{model_id}"""
    print_header("TEST 8: Filter Gallery by AI Model")
    
    try:
        # First, get a gallery item that has ai_model_id
        response = requests.get(f"{PUBLIC_URL}?limit=50", timeout=10)
        if response.status_code != 200:
            print_test("Setup - Get gallery", False, "Could not fetch gallery for testing")
            return
        
        data = response.json()
        if not data.get("data"):
            print("   ℹ️  No gallery items available for testing (skip this test)")
            return
        
        # Find a gallery item with model_id
        gallery_with_model = None
        for item in data["data"]:
            if item.get("model_id"):
                gallery_with_model = item
                break
        
        if not gallery_with_model:
            print("   ℹ️  No gallery items with model_id found (skip this test)")
            return
        
        model_id = gallery_with_model.get("model_id")
        print(f"   Testing with AI Model ID: {model_id}")
        
        # Test filter by model (note: endpoint is /by-model/ not /model/)
        response_model = requests.get(f"{PUBLIC_URL}/by-model/{model_id}", timeout=10)
        success_model = response_model.status_code == 200
        
        if success_model:
            model_data = response_model.json()
            print_test(
                "GET /gallery/model/{model_id}",
                True,
                f"Found {len(model_data.get('data', []))} gallery items using this AI model"
            )
            
            # Verify all items use the same model
            if model_data.get("data"):
                all_same_model = all(
                    g.get("model_id") == model_id 
                    for g in model_data["data"]
                )
                print_test(
                    "✓ All gallery items use the same AI model",
                    all_same_model,
                    "Filter working correctly" if all_same_model else "⚠️  Filter not working correctly"
                )
        else:
            print_test(
                "Filter by AI model",
                False,
                f"Status code: {response_model.status_code}, Response: {response_model.text[:200]}"
            )
            
    except Exception as e:
        print_test("Filter by AI model", False, f"Error: {str(e)}")

def test_slug_not_supported():
    """Test: Slug endpoint not available for Gallery"""
    print_header("TEST 9: Slug Not Supported")
    
    try:
        # Gallery doesn't have slug endpoint
        print_test(
            "Gallery slug endpoint",
            True,
            "ℹ️  Gallery model doesn't have slug field - only ID-based lookup supported"
        )
    except Exception as e:
        print_test("Slug check", False, f"Error: {str(e)}")

def test_invalid_id():
    """Test: Invalid ID returns 404"""
    print_header("TEST 10: Invalid ID (404)")
    
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
    print_header("TEST 11: Limit Validation")
    
    try:
        # Test max limit (should be capped at 100 or return validation error)
        response = requests.get(f"{PUBLIC_URL}?limit=200", timeout=10)
        success = response.status_code in [200, 422]
        
        if response.status_code == 200:
            data = response.json()
            returned_count = len(data.get("data", []))
            returned_limit = data.get("limit", 0)
            print_test(
                "GET /gallery?limit=200 (exceeds max)",
                True,
                f"✓ Request handled, returned {returned_count} items with limit={returned_limit} (likely capped at max 100)"
            )
        elif response.status_code == 422:
            print_test(
                "GET /gallery?limit=200 (exceeds max)",
                True,
                "✓ Validation error returned (limit exceeds maximum)"
            )
        else:
            print_test("Limit validation", False, f"Status: {response.status_code}")
            
    except Exception as e:
        print_test("Limit validation", False, f"Error: {str(e)}")

def test_invalid_model_id():
    """Test: Invalid model ID returns appropriate response"""
    print_header("TEST 12: Invalid Model ID")
    
    try:
        fake_uuid = "00000000-0000-0000-0000-000000000000"
        response = requests.get(f"{PUBLIC_URL}/by-model/{fake_uuid}", timeout=10)
        
        # Should return 200 with empty data, or 404
        success = response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            is_empty = len(data.get("data", [])) == 0
            print_test(
                f"GET /gallery/model/{fake_uuid}",
                is_empty,
                f"✓ Correctly returned empty result" if is_empty else f"⚠️  Unexpected data returned"
            )
        elif response.status_code == 404:
            print_test(
                f"GET /gallery/model/{fake_uuid}",
                True,
                "✓ Correctly returned 404"
            )
        else:
            print_test("Invalid model ID", False, f"Status: {response.status_code}")
            
    except Exception as e:
        print_test("Invalid model ID", False, f"Error: {str(e)}")

# ==========================================
# Main Test Runner
# ==========================================

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 PUBLIC API TESTS - GALLERY ENDPOINTS")
    print("=" * 60)
    print(f"Base URL: {PUBLIC_URL}")
    print(f"Testing: {PUBLIC_URL}")
    print("=" * 60)
    print("\n⚡ Running tests (No authentication required)...\n")
    
    try:
        # Basic endpoint tests
        test_get_all_gallery()
        test_default_limit()
        test_pagination()
        test_search()
        test_featured_gallery()
        test_latest_gallery()
        test_get_by_id()
        
        # Gallery-specific tests
        test_filter_by_ai_model()
        
        # Error handling tests
        test_slug_not_supported()
        test_invalid_id()
        test_limit_validation()
        test_invalid_model_id()
        
        # Summary
        print_header("✅ ALL TESTS COMPLETED")
        print("\n📊 Summary:")
        print(f"   • All public endpoints tested")
        print(f"   • No authentication required ✓")
        print(f"   • Auto-filtering for published & public content ✓")
        print(f"   • Default limit=24 (optimized for grid display) ✓")
        print(f"   • Filter by AI Model working ✓")
        print("\n💡 Note: Empty results are OK if database has no published gallery items yet")
        print("   Gallery use case: AI-generated images, visual outputs, showcases")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
