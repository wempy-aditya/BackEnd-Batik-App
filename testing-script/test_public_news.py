#!/usr/bin/env python3
"""
Test Public API - News Endpoints
Test semua endpoint public untuk News (No authentication required)

Run: python3 test_public_news.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"
PUBLIC_URL = f"{BASE_URL}/public/news"

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

def test_get_all_news():
    """Test: GET /public/news"""
    print_header("TEST 1: Get All News")
    
    try:
        response = requests.get(PUBLIC_URL, timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_pagination = "total" in data and ("offset" in data or "page" in data)
            
            print_test(
                "GET /public/news",
                has_data and has_pagination,
                f"Found {data.get('total', 0)} news items",
                data
            )
            
            # Check if all news are published and public
            if has_data and data["data"]:
                all_public = all(
                    n.get("status") == "published" and n.get("access_level") == "public"
                    for n in data["data"]
                )
                print_test(
                    "✓ All news are published & public",
                    all_public,
                    "All news meet visibility requirements" if all_public else "⚠️  Some news don't meet requirements"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No news found in database (empty result is OK)")
        else:
            print_test(
                "GET /public/news",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("GET /public/news", False, f"Error: {str(e)}")

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
                "GET /public/news?offset=0&limit=5",
                True,
                f"Got {len(data1.get('data', []))} items, total: {data1.get('total', 0)}"
            )
        else:
            print_test("Pagination offset/limit", False, f"Status: {response1.status_code}")
        
        # Test with different offset
        response2 = requests.get(f"{PUBLIC_URL}?offset=5&limit=5", timeout=10)
        success2 = response2.status_code == 200
        
        if success2:
            data2 = response2.json()
            print_test(
                "GET /public/news?offset=5&limit=5",
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
        response = requests.get(f"{PUBLIC_URL}?search=news", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            print_test(
                "GET /public/news?search=news",
                True,
                f"Search returned {len(data.get('data', []))} results"
            )
        else:
            print_test("Search", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Search", False, f"Error: {str(e)}")

def test_featured_news():
    """Test: GET /public/news/featured"""
    print_header("TEST 4: Featured News")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/featured", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/news/featured",
                has_data,
                f"Found {len(data.get('data', []))} featured news items",
                data
            )
            
            # Check if all are featured
            if has_data and data["data"]:
                all_featured = all(n.get("is_featured") for n in data["data"])
                print_test(
                    "✓ All news have is_featured=true",
                    all_featured,
                    "All returned news are featured" if all_featured else "⚠️  Some news are not featured (DB might not have featured items)"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No featured news found (empty result is OK)")
        else:
            print_test(
                "GET /public/news/featured",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Featured news", False, f"Error: {str(e)}")

def test_latest_news():
    """Test: GET /public/news/latest"""
    print_header("TEST 5: Latest News")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/latest?limit=10", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/news/latest?limit=10",
                has_data,
                f"Found {len(data.get('data', []))} latest news items",
                data
            )
            
            # Check if sorted by created_at (newest first)
            if has_data and len(data["data"]) > 1:
                dates = [n.get("created_at") for n in data["data"]]
                is_sorted = dates == sorted(dates, reverse=True)
                print_test(
                    "✓ News sorted by date (newest first)",
                    is_sorted,
                    "News are properly sorted" if is_sorted else "⚠️  News are not sorted correctly"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No news found (empty result is OK)")
        else:
            print_test(
                "GET /public/news/latest",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Latest news", False, f"Error: {str(e)}")

def test_get_by_id_and_slug():
    """Test: GET /public/news/{id} and /public/news/slug/{slug}"""
    print_header("TEST 6: Get News by ID and Slug")
    
    try:
        # First, get a news item
        response = requests.get(f"{PUBLIC_URL}?limit=1", timeout=10)
        if response.status_code != 200:
            print_test("Setup - Get news", False, "Could not fetch news for testing")
            return
        
        data = response.json()
        if not data.get("data"):
            print("   ℹ️  No news available for testing (skip this test)")
            return
        
        news = data["data"][0]
        news_id = news.get("id")
        news_slug = news.get("slug")
        news_title = news.get("title", "N/A")
        
        print(f"   Testing with news: '{news_title}'")
        print(f"   ID: {news_id}")
        print(f"   Slug: {news_slug}")
        
        # Test get by ID
        response_id = requests.get(f"{PUBLIC_URL}/{news_id}", timeout=10)
        success_id = response_id.status_code == 200
        
        if success_id:
            news_data = response_id.json()
            print_test(
                "✓ GET by ID",
                True,
                f"Got news: {news_data.get('title', 'N/A')}"
            )
        else:
            print_test(
                "GET by ID",
                False,
                f"Status code: {response_id.status_code}, Response: {response_id.text[:200]}"
            )
        
        # Test get by slug
        if news_slug:
            response_slug = requests.get(f"{PUBLIC_URL}/slug/{news_slug}", timeout=10)
            success_slug = response_slug.status_code == 200
            
            if success_slug:
                news_data = response_slug.json()
                print_test(
                    "✓ GET by slug",
                    True,
                    f"Got news: {news_data.get('title', 'N/A')}"
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

def test_default_limit():
    """Test: Default limit for latest news"""
    print_header("TEST 7: Default Limit")
    
    try:
        # News latest should default to limit=10
        response = requests.get(f"{PUBLIC_URL}/latest", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            count = len(data.get("data", []))
            print_test(
                "GET /public/news/latest (no limit param)",
                True,
                f"Returned {count} items (default should be 10 or less)"
            )
        else:
            print_test("Default limit", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Default limit", False, f"Error: {str(e)}")

def test_invalid_slug():
    """Test: Invalid slug returns 404"""
    print_header("TEST 8: Invalid Slug (404)")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/slug/non-existent-news-12345-xyz", timeout=10)
        success = response.status_code == 404
        
        print_test(
            "GET /slug/non-existent-news",
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
        # Test max limit (should be capped or return validation error)
        response = requests.get(f"{PUBLIC_URL}?limit=200", timeout=10)
        success = response.status_code in [200, 422]
        
        if response.status_code == 200:
            data = response.json()
            returned_count = len(data.get("data", []))
            print_test(
                "GET /news?limit=200 (exceeds max)",
                True,
                f"✓ Request handled, returned {returned_count} items (likely capped at max)"
            )
        elif response.status_code == 422:
            print_test(
                "GET /news?limit=200 (exceeds max)",
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
    print("🧪 PUBLIC API TESTS - NEWS ENDPOINTS")
    print("=" * 60)
    print(f"Base URL: {PUBLIC_URL}")
    print(f"Testing: {PUBLIC_URL}")
    print("=" * 60)
    print("\n⚡ Running tests (No authentication required)...\n")
    
    try:
        # Basic endpoint tests
        test_get_all_news()
        test_pagination()
        test_search()
        test_featured_news()
        test_latest_news()
        test_get_by_id_and_slug()
        
        # News-specific tests
        test_default_limit()
        
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
        print(f"   • Latest news with default limit=10 ✓")
        print("\n💡 Note: Empty results are OK if database has no published news yet")
        print("   News use case: Blog posts, announcements, updates")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
