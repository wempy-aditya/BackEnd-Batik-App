#!/usr/bin/env python3
"""
Comprehensive Test Script for Contributors API
Tests all endpoints: CRUD operations and assignment functionality

Prerequisites:
- Server running on http://localhost:8000
- Admin user credentials (for creating/updating/deleting contributors)

Run: python3 test_contributors.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"
CONTRIBUTORS_URL = f"{BASE_URL}/contributors"

# Admin credentials - update these with your actual credentials
ADMIN_EMAIL = "supernew@example.com"
ADMIN_PASSWORD = "password123"

# Global variables to store created IDs
access_token = None
contributor1_id = None
contributor2_id = None
contributor3_id = None
project_id = None

# ==========================================
# Helper Functions
# ==========================================

def print_header(text: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def print_test(name: str, success: bool, details: str = "", data: Any = None):
    """Print test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status} - {name}")
    if details:
        print(f"   {details}")
    if data and isinstance(data, dict):
        print(f"   Response: {json.dumps(data, indent=4)[:500]}...")

# ==========================================
# Setup: Authentication
# ==========================================

def test_login():
    """Login and get access token"""
    global access_token
    
    print_header("SETUP: Admin Login")
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            data={
                "username": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            data = response.json()
            access_token = data.get("access_token")
            print_test(
                "Admin Login",
                True,
                f"Access token obtained: {access_token[:20]}..."
            )
            return True
        else:
            print_test(
                "Admin Login",
                False,
                f"Status: {response.status_code}, Error: {response.text[:200]}"
            )
            return False
    except Exception as e:
        print_test("Admin Login", False, f"Error: {str(e)}")
        return False

def get_headers():
    """Get headers with auth token"""
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

# ==========================================
# Test 1: Create Contributors
# ==========================================

def test_create_contributor():
    """Test creating new contributors"""
    global contributor1_id, contributor2_id, contributor3_id
    
    print_header("TEST 1: Create Contributors")
    
    contributors_data = [
        {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "role": "Full Stack Developer",
            "bio": "Experienced developer with 5+ years in web development",
            "github_url": "https://github.com/alice",
            "linkedin_url": "https://linkedin.com/in/alice"
        },
        {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "role": "Data Scientist",
            "bio": "ML engineer specializing in computer vision",
            "github_url": "https://github.com/bob"
        },
        {
            "name": "Charlie Davis",
            "email": "charlie@example.com",
            "role": "UI/UX Designer",
            "bio": "Creative designer with passion for user experience"
        }
    ]
    
    created_ids = []
    
    for i, contrib_data in enumerate(contributors_data, 1):
        try:
            response = requests.post(
                CONTRIBUTORS_URL,
                headers=get_headers(),
                json=contrib_data
            )
            
            if response.status_code == 201:
                data = response.json()
                created_id = data.get("id")
                created_ids.append(created_id)
                print_test(
                    f"Create Contributor {i}: {contrib_data['name']}",
                    True,
                    f"ID: {created_id}, Email: {data.get('email')}"
                )
            else:
                print_test(
                    f"Create Contributor {i}",
                    False,
                    f"Status: {response.status_code}, Error: {response.text[:200]}"
                )
        except Exception as e:
            print_test(f"Create Contributor {i}", False, f"Error: {str(e)}")
    
    # Store IDs for later tests
    if len(created_ids) >= 3:
        contributor1_id = created_ids[0]
        contributor2_id = created_ids[1]
        contributor3_id = created_ids[2]
        return True
    return False

# ==========================================
# Test 2: Get All Contributors (Public)
# ==========================================

def test_get_all_contributors():
    """Test getting all contributors without authentication"""
    print_header("TEST 2: Get All Contributors (Public)")
    
    try:
        response = requests.get(f"{CONTRIBUTORS_URL}?offset=0&limit=10")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            items_count = len(data.get("data", []))
            
            print_test(
                "GET /contributors (No auth required)",
                True,
                f"Found {total} total contributors, showing {items_count}",
                data
            )
            return True
        else:
            print_test(
                "GET /contributors",
                False,
                f"Status: {response.status_code}"
            )
            return False
    except Exception as e:
        print_test("GET /contributors", False, f"Error: {str(e)}")
        return False

# ==========================================
# Test 3: Search Contributors
# ==========================================

def test_search_contributors():
    """Test search functionality"""
    print_header("TEST 3: Search Contributors")
    
    try:
        response = requests.get(f"{CONTRIBUTORS_URL}?search=Alice")
        
        if response.status_code == 200:
            data = response.json()
            results_count = len(data.get("data", []))
            
            print_test(
                "Search contributors by name",
                True,
                f"Search 'Alice' returned {results_count} results"
            )
            
            # Check if Alice is in results
            if results_count > 0:
                names = [item.get("name") for item in data["data"]]
                has_alice = any("Alice" in name for name in names)
                print_test(
                    "✓ Search accuracy",
                    has_alice,
                    f"Found contributors: {names}"
                )
            return True
        else:
            print_test("Search", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Search", False, f"Error: {str(e)}")
        return False

# ==========================================
# Test 4: Get Contributor by ID
# ==========================================

def test_get_contributor_by_id():
    """Test getting contributor details with stats"""
    print_header("TEST 4: Get Contributor by ID (with stats)")
    
    if not contributor1_id:
        print("   ⚠️  Skipping - no contributor ID available")
        return False
    
    try:
        response = requests.get(f"{CONTRIBUTORS_URL}/{contributor1_id}")
        
        if response.status_code == 200:
            data = response.json()
            
            print_test(
                f"GET /contributors/{contributor1_id}",
                True,
                f"Name: {data.get('name')}, Email: {data.get('email')}",
                data
            )
            
            # Check stats
            if "project_count" in data:
                print(f"   📊 Stats:")
                print(f"      - Projects: {data.get('project_count')}")
                print(f"      - Publications: {data.get('publication_count')}")
                print(f"      - Datasets: {data.get('dataset_count')}")
                print(f"      - Total: {data.get('total_contributions')}")
            
            return True
        else:
            print_test(
                "GET by ID",
                False,
                f"Status: {response.status_code}"
            )
            return False
    except Exception as e:
        print_test("GET by ID", False, f"Error: {str(e)}")
        return False

# ==========================================
# Test 5: Update Contributor
# ==========================================

def test_update_contributor():
    """Test updating contributor data"""
    print_header("TEST 5: Update Contributor")
    
    if not contributor1_id:
        print("   ⚠️  Skipping - no contributor ID available")
        return False
    
    try:
        update_data = {
            "bio": "Updated bio: Senior Full Stack Developer with 7+ years experience",
            "website_url": "https://alice-portfolio.com"
        }
        
        response = requests.put(
            f"{CONTRIBUTORS_URL}/{contributor1_id}",
            headers=get_headers(),
            json=update_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test(
                f"PUT /contributors/{contributor1_id}",
                True,
                f"Updated bio and website",
                data
            )
            return True
        else:
            print_test(
                "Update contributor",
                False,
                f"Status: {response.status_code}, Error: {response.text[:200]}"
            )
            return False
    except Exception as e:
        print_test("Update contributor", False, f"Error: {str(e)}")
        return False

# ==========================================
# Test 6: Get or Create Test Project
# ==========================================

def test_get_or_create_project():
    """Get existing project or create one for testing"""
    global project_id
    
    print_header("SETUP: Get/Create Test Project")
    
    try:
        # Try to get existing projects
        response = requests.get(
            f"{BASE_URL}/projects",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                project_id = data["data"][0]["id"]
                print_test(
                    "Using existing project",
                    True,
                    f"Project ID: {project_id}"
                )
                return True
        
        # Create new project if none exists
        project_data = {
            "title": "Contributors Test Project",
            "slug": "contributors-test-project",
            "description": "Test project for contributors assignment",
            "status": "published",
            "access_level": "public"
        }
        
        response = requests.post(
            f"{BASE_URL}/projects",
            headers=get_headers(),
            json=project_data
        )
        
        if response.status_code == 201:
            data = response.json()
            project_id = data.get("id")
            print_test(
                "Created test project",
                True,
                f"Project ID: {project_id}"
            )
            return True
        else:
            print_test(
                "Get/Create project",
                False,
                f"Status: {response.status_code}"
            )
            return False
    except Exception as e:
        print_test("Get/Create project", False, f"Error: {str(e)}")
        return False

# ==========================================
# Test 7: Assign Contributors to Project
# ==========================================

def test_assign_to_project():
    """Test assigning contributors to a project"""
    print_header("TEST 7: Assign Contributors to Project")
    
    if not project_id or not contributor1_id:
        print("   ⚠️  Skipping - no project or contributor ID available")
        return False
    
    try:
        assignment_data = {
            "contributor_ids": [contributor1_id, contributor2_id, contributor3_id],
            "roles": ["Lead Developer", "ML Engineer", "UI/UX Designer"]
        }
        
        response = requests.post(
            f"{CONTRIBUTORS_URL}/assign/project/{project_id}",
            headers=get_headers(),
            json=assignment_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test(
                f"Assign contributors to project",
                True,
                f"Response: {data.get('detail')}",
                data
            )
            return True
        else:
            print_test(
                "Assign to project",
                False,
                f"Status: {response.status_code}, Error: {response.text[:200]}"
            )
            return False
    except Exception as e:
        print_test("Assign to project", False, f"Error: {str(e)}")
        return False

# ==========================================
# Test 8: Get Project Contributors
# ==========================================

def test_get_project_contributors():
    """Test getting all contributors for a project (public endpoint)"""
    print_header("TEST 8: Get Project Contributors (Public)")
    
    if not project_id:
        print("   ⚠️  Skipping - no project ID available")
        return False
    
    try:
        response = requests.get(
            f"{CONTRIBUTORS_URL}/project/{project_id}/contributors"
        )
        
        if response.status_code == 200:
            data = response.json()
            contributors = data.get("data", [])
            total = data.get("total", 0)
            
            print_test(
                f"GET /project/{project_id}/contributors",
                True,
                f"Found {total} contributors for this project"
            )
            
            if contributors:
                print("\n   Project Team:")
                for contrib in contributors:
                    name = contrib.get("name")
                    role = contrib.get("role_in_project") or contrib.get("role", "N/A")
                    print(f"      • {name} - {role}")
            
            return True
        else:
            print_test(
                "Get project contributors",
                False,
                f"Status: {response.status_code}"
            )
            return False
    except Exception as e:
        print_test("Get project contributors", False, f"Error: {str(e)}")
        return False

# ==========================================
# Test 9: Verify Contributor Stats Updated
# ==========================================

def test_verify_contributor_stats():
    """Verify that contributor stats are updated after assignment"""
    print_header("TEST 9: Verify Contributor Stats Updated")
    
    if not contributor1_id:
        print("   ⚠️  Skipping - no contributor ID available")
        return False
    
    try:
        response = requests.get(f"{CONTRIBUTORS_URL}/{contributor1_id}")
        
        if response.status_code == 200:
            data = response.json()
            project_count = data.get("project_count", 0)
            total = data.get("total_contributions", 0)
            
            success = project_count > 0
            print_test(
                "Contributor stats updated",
                success,
                f"Project count: {project_count}, Total contributions: {total}"
            )
            return success
        else:
            print_test("Verify stats", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Verify stats", False, f"Error: {str(e)}")
        return False

# ==========================================
# Test 10: Pagination
# ==========================================

def test_pagination():
    """Test pagination parameters"""
    print_header("TEST 10: Pagination")
    
    try:
        # Test with limit
        response = requests.get(f"{CONTRIBUTORS_URL}?offset=0&limit=2")
        
        if response.status_code == 200:
            data = response.json()
            items_returned = len(data.get("data", []))
            
            print_test(
                "Pagination with limit=2",
                items_returned <= 2,
                f"Returned {items_returned} items (max 2 requested)"
            )
            
            # Test offset
            response2 = requests.get(f"{CONTRIBUTORS_URL}?offset=1&limit=2")
            if response2.status_code == 200:
                data2 = response2.json()
                print_test(
                    "Pagination with offset=1",
                    True,
                    f"Returned {len(data2.get('data', []))} items"
                )
            
            return True
        else:
            print_test("Pagination", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Pagination", False, f"Error: {str(e)}")
        return False

# ==========================================
# Test 11: Delete Contributor
# ==========================================

def test_delete_contributor():
    """Test deleting a contributor"""
    print_header("TEST 11: Delete Contributor")
    
    if not contributor3_id:
        print("   ⚠️  Skipping - no contributor ID available")
        return False
    
    try:
        response = requests.delete(
            f"{CONTRIBUTORS_URL}/{contributor3_id}",
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test(
                f"DELETE /contributors/{contributor3_id}",
                True,
                f"Response: {data.get('detail')}"
            )
            
            # Verify deletion
            verify_response = requests.get(f"{CONTRIBUTORS_URL}/{contributor3_id}")
            if verify_response.status_code == 404:
                print_test(
                    "✓ Deletion verified",
                    True,
                    "Contributor no longer accessible"
                )
            
            return True
        else:
            print_test(
                "Delete contributor",
                False,
                f"Status: {response.status_code}, Error: {response.text[:200]}"
            )
            return False
    except Exception as e:
        print_test("Delete contributor", False, f"Error: {str(e)}")
        return False

# ==========================================
# Main Test Runner
# ==========================================

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🧪 CONTRIBUTORS API - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Contributors URL: {CONTRIBUTORS_URL}")
    print("=" * 70)
    
    results = []
    
    # Setup
    if not test_login():
        print("\n❌ FAILED: Cannot login. Please check credentials.")
        return
    
    # Run tests
    results.append(("Create Contributors", test_create_contributor()))
    results.append(("Get All Contributors", test_get_all_contributors()))
    results.append(("Search Contributors", test_search_contributors()))
    results.append(("Get Contributor by ID", test_get_contributor_by_id()))
    results.append(("Update Contributor", test_update_contributor()))
    results.append(("Get/Create Project", test_get_or_create_project()))
    results.append(("Assign to Project", test_assign_to_project()))
    results.append(("Get Project Contributors", test_get_project_contributors()))
    results.append(("Verify Stats Updated", test_verify_contributor_stats()))
    results.append(("Pagination", test_pagination()))
    results.append(("Delete Contributor", test_delete_contributor()))
    
    # Summary
    print_header("📊 TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n{'Test Name':<40} {'Result'}")
    print("-" * 70)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:<40} {status}")
    
    print("-" * 70)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    print("\n" + "=" * 70)
    print("✅ Test suite completed")
    print("=" * 70)

if __name__ == "__main__":
    main()
