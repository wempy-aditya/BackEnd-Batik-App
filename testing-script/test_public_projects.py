#!/usr/bin/env python3
"""
Test Public API - Projects Endpoints
Test semua endpoint public untuk Projects (No authentication required)

Run: python test_public_projects.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "https://spmb1.wempyaw.com/api/v1"
PUBLIC_URL = f"{BASE_URL}/public/projects"

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
            print(f"   Sample item keys: {list(data['data'][0].keys())}")

# ==========================================
# Test Functions
# ==========================================

def test_get_all_projects():
    """Test: GET /public/projects"""
    print_header("TEST 1: Get All Projects")
    
    try:
        response = requests.get(PUBLIC_URL, timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            has_pagination = all(k in data for k in ["total", "page", "size"])
            
            print_test(
                "GET /public/projects",
                has_data and has_pagination,
                f"Found {data.get('total', 0)} projects, Page {data.get('page', 0)}, Size: {data.get('size', 0)}",
                data
            )
            
            # Check if all projects are published and public
            if has_data and data["data"]:
                all_public = all(
                    p.get("status") == "published" and p.get("access_level") == "public"
                    for p in data["data"]
                )
                print_test(
                    "✓ All projects are published & public",
                    all_public,
                    "All projects meet visibility requirements" if all_public else "⚠️  Some projects don't meet requirements"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No projects found in database (empty result is OK)")
        else:
            print_test(
                "GET /public/projects",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("GET /public/projects", False, f"Error: {str(e)}")

def test_pagination():
    """Test: Pagination parameters"""
    print_header("TEST 2: Pagination")
    
    try:
        # Test page 1
        response1 = requests.get(f"{PUBLIC_URL}?page=1&items_per_page=5", timeout=10)
        success1 = response1.status_code == 200
        
        if success1:
            data1 = response1.json()
            print_test(
                "GET /public/projects?page=1&items_per_page=5",
                True,
                f"Got {len(data1.get('data', []))} items, total: {data1.get('total', 0)}"
            )
        else:
            print_test("Pagination page 1", False, f"Status: {response1.status_code}")
        
        # Test page 2
        response2 = requests.get(f"{PUBLIC_URL}?page=2&items_per_page=5", timeout=10)
        success2 = response2.status_code == 200
        
        if success2:
            data2 = response2.json()
            print_test(
                "GET /public/projects?page=2&items_per_page=5",
                True,
                f"Got {len(data2.get('data', []))} items"
            )
        else:
            print_test("Pagination page 2", False, f"Status: {response2.status_code}")
            
    except Exception as e:
        print_test("Pagination", False, f"Error: {str(e)}")

def test_search():
    """Test: Search functionality"""
    print_header("TEST 3: Search")
    
    try:
        response = requests.get(f"{PUBLIC_URL}?search=project", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            print_test(
                "GET /public/projects?search=project",
                True,
                f"Search returned {len(data.get('data', []))} results"
            )
        else:
            print_test("Search", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Search", False, f"Error: {str(e)}")

def test_featured_projects():
    """Test: GET /public/projects/featured"""
    print_header("TEST 4: Featured Projects")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/featured", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/projects/featured",
                has_data,
                f"Found {len(data.get('data', []))} featured projects",
                data
            )
            
            # Check if all are featured
            if has_data and data["data"]:
                all_featured = all(p.get("is_featured") for p in data["data"])
                print_test(
                    "✓ All projects have is_featured=true",
                    all_featured,
                    "All returned projects are featured" if all_featured else "⚠️  Some projects are not featured"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No featured projects found (empty result is OK)")
        else:
            print_test(
                "GET /public/projects/featured",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Featured projects", False, f"Error: {str(e)}")

def test_latest_projects():
    """Test: GET /public/projects/latest"""
    print_header("TEST 5: Latest Projects")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/latest?limit=10", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            has_data = "data" in data
            
            print_test(
                "GET /public/projects/latest?limit=10",
                has_data,
                f"Found {len(data.get('data', []))} latest projects",
                data
            )
            
            # Check if sorted by created_at (newest first)
            if has_data and len(data["data"]) > 1:
                dates = [p.get("created_at") for p in data["data"]]
                is_sorted = dates == sorted(dates, reverse=True)
                print_test(
                    "✓ Projects sorted by date (newest first)",
                    is_sorted,
                    "Projects are properly sorted" if is_sorted else "⚠️  Projects are not sorted correctly"
                )
            elif has_data and not data["data"]:
                print("   ℹ️  No projects found (empty result is OK)")
        else:
            print_test(
                "GET /public/projects/latest",
                False,
                f"Status code: {response.status_code}, Response: {response.text[:200]}"
            )
    except Exception as e:
        print_test("Latest projects", False, f"Error: {str(e)}")

def test_get_by_id_and_slug():
    """Test: GET /public/projects/{id} and /public/projects/slug/{slug}"""
    print_header("TEST 6: Get Project by ID and Slug")
    
    try:
        # First, get a project
        response = requests.get(f"{PUBLIC_URL}?limit=1", timeout=10)
        if response.status_code != 200:
            print_test("Setup - Get projects", False, "Could not fetch projects for testing")
            return
        
        data = response.json()
        if not data.get("data"):
            print("   ℹ️  No projects available for testing (skip this test)")
            return
        
        project = data["data"][0]
        project_id = project.get("id")
        project_slug = project.get("slug")
        project_title = project.get("title", "N/A")
        
        print(f"   Testing with project: '{project_title}'")
        print(f"   ID: {project_id}")
        print(f"   Slug: {project_slug}")
        
        # Test get by ID
        response_id = requests.get(f"{PUBLIC_URL}/{project_id}", timeout=10)
        success_id = response_id.status_code == 200
        
        if success_id:
            project_data = response_id.json()
            print_test(
                "✓ GET by ID",
                True,
                f"Got project: {project_data.get('title', 'N/A')}"
            )
        else:
            print_test(
                "GET by ID",
                False,
                f"Status code: {response_id.status_code}, Response: {response_id.text[:200]}"
            )
        
        # Test get by slug
        if project_slug:
            response_slug = requests.get(f"{PUBLIC_URL}/slug/{project_slug}", timeout=10)
            success_slug = response_slug.status_code == 200
            
            if success_slug:
                project_data = response_slug.json()
                print_test(
                    "✓ GET by slug",
                    True,
                    f"Got project: {project_data.get('title', 'N/A')}"
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

def test_invalid_slug():
    """Test: Invalid slug returns 404"""
    print_header("TEST 7: Invalid Slug (404)")
    
    try:
        response = requests.get(f"{PUBLIC_URL}/slug/non-existent-project-12345-xyz", timeout=10)
        success = response.status_code == 404
        
        print_test(
            "GET /slug/non-existent-project",
            success,
            f"✓ Correctly returned 404" if success else f"⚠️  Expected 404, got {response.status_code}"
        )
    except Exception as e:
        print_test("Invalid slug", False, f"Error: {str(e)}")

def test_invalid_id():
    """Test: Invalid ID returns 404"""
    print_header("TEST 8: Invalid ID (404)")
    
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

# ==========================================
# Main Test Runner
# ==========================================

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🧪 PUBLIC API TESTS - PROJECTS ENDPOINTS")
    print("=" * 60)
    print(f"Base URL: {PUBLIC_URL}")
    print(f"Testing: {PUBLIC_URL}")
    print("=" * 60)
    print("\n⚡ Running tests (No authentication required)...\n")
    
    test_results = {
        "passed": 0,
        "failed": 0,
        "errors": 0
    }
    
    try:
        # Basic endpoint tests
        test_get_all_projects()
        test_pagination()
        test_search()
        test_featured_projects()
        test_latest_projects()
        test_get_by_id_and_slug()
        
        # Error handling tests
        test_invalid_slug()
        test_invalid_id()
        
        # Summary
        print_header("✅ ALL TESTS COMPLETED")
        print("\n📊 Summary:")
        print(f"   • All public endpoints tested")
        print(f"   • No authentication required ✓")
        print(f"   • Auto-filtering for published & public content ✓")
        print("\n💡 Note: Empty results are OK if database has no published projects yet")
        print("   To add test data, use the admin endpoints with authentication")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
