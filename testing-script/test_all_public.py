#!/usr/bin/env python3
"""Comprehensive test for all public API endpoints"""
import requests
import time

BASE_URL = "http://localhost:8000/api/v1/public"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

passed = 0
failed = 0
warnings = 0

def test(name, url, params=None):
    global passed, failed, warnings
    try:
        start = time.time()
        response = requests.get(url, params=params, timeout=10)
        duration = time.time() - start
        
        if response.status_code != 200:
            print(f"{Colors.RED}✗ {name}: HTTP {response.status_code}{Colors.RESET}")
            failed += 1
            return None
            
        data = response.json()
        count = len(data.get("data", []))
        total = data.get("total_count", count)
        
        print(f"{Colors.GREEN}✓ {name}: {count} items (total: {total}) in {duration:.2f}s{Colors.RESET}")
        passed += 1
        return data
        
    except Exception as e:
        print(f"{Colors.RED}✗ {name}: {str(e)}{Colors.RESET}")
        failed += 1
        return None

def test_consistency(name, url, params=None, trials=3):
    global passed, failed
    results_list = []
    
    for i in range(trials):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                count = len(data.get("data", []))
                results_list.append(count)
            time.sleep(0.3)
        except:
            results_list.append(-1)
    
    if len(set(results_list)) == 1:
        print(f"{Colors.GREEN}✓ {name}: Consistent ({results_list[0]} items){Colors.RESET}")
        passed += 1
    else:
        print(f"{Colors.RED}✗ {name}: INCONSISTENT {results_list}{Colors.RESET}")
        failed += 1

print("\n" + "="*60)
print("TESTING: PROJECTS")
print("="*60)
test("Get all", f"{BASE_URL}/projects/")
test("Search", f"{BASE_URL}/projects/", {"search": "project"})
test("Sort latest", f"{BASE_URL}/projects/", {"sort_by": "latest"})
test("Sort oldest", f"{BASE_URL}/projects/", {"sort_by": "oldest"})
test("Sort title", f"{BASE_URL}/projects/", {"sort_by": "title"})
test_consistency("Consistency", f"{BASE_URL}/projects/")

print("\n" + "="*60)
print("TESTING: DATASETS")
print("="*60)
test("Get all", f"{BASE_URL}/datasets/")
test("Search", f"{BASE_URL}/datasets/", {"search": "data"})
test("Filter JSON", f"{BASE_URL}/datasets/", {"format": "JSON"})
test("Filter CSV", f"{BASE_URL}/datasets/", {"format": "CSV"})
test("Filter MIT", f"{BASE_URL}/datasets/", {"license": "MIT"})
test("Featured", f"{BASE_URL}/datasets/", {"is_featured": "true"})
test("Sort latest", f"{BASE_URL}/datasets/", {"sort_by": "latest"})
test("Sort downloads", f"{BASE_URL}/datasets/", {"sort_by": "downloads"})
test_consistency("Consistency", f"{BASE_URL}/datasets/")

print("\n" + "="*60)
print("TESTING: PUBLICATIONS")
print("="*60)
test("Get all", f"{BASE_URL}/publications/")
test("Search", f"{BASE_URL}/publications/", {"search": "machine"})
test("Year 2024", f"{BASE_URL}/publications/", {"year": 2024})
test("Year 2023", f"{BASE_URL}/publications/", {"year": 2023})
test("Featured", f"{BASE_URL}/publications/", {"is_featured": "true"})
test("Sort latest", f"{BASE_URL}/publications/", {"sort_by": "latest"})
test("Sort views", f"{BASE_URL}/publications/", {"sort_by": "views"})
test_consistency("Consistency", f"{BASE_URL}/publications/")

print("\n" + "="*60)
print("TESTING: AI MODELS")
print("="*60)
test("Get all", f"{BASE_URL}/ai-models/")
test("Search", f"{BASE_URL}/ai-models/", {"search": "model"})
test("Filter CNN", f"{BASE_URL}/ai-models/", {"architecture": "CNN"})
test("Filter RNN", f"{BASE_URL}/ai-models/", {"architecture": "RNN"})
test("Featured", f"{BASE_URL}/ai-models/", {"is_featured": "true"})
test("Sort latest", f"{BASE_URL}/ai-models/", {"sort_by": "latest"})
test_consistency("Consistency", f"{BASE_URL}/ai-models/")

print("\n" + "="*60)
print("TESTING: NEWS")
print("="*60)
test("Get all", f"{BASE_URL}/news/")
test("Search", f"{BASE_URL}/news/", {"search": "news"})
test("Featured", f"{BASE_URL}/news/", {"is_featured": "true"})
test("Sort latest", f"{BASE_URL}/news/", {"sort_by": "latest"})
test_consistency("Consistency", f"{BASE_URL}/news/")

print("\n" + "="*60)
print("TESTING: GALLERY")
print("="*60)
test("Get all", f"{BASE_URL}/gallery/")
test("Search", f"{BASE_URL}/gallery/", {"search": "image"})
test("Sort latest", f"{BASE_URL}/gallery/", {"sort_by": "latest"})
test_consistency("Consistency", f"{BASE_URL}/gallery/")

print("\n" + "="*60)
print("TESTING: CATEGORIES & FILTERING")
print("="*60)
cats = test("Get categories", f"{BASE_URL}/categories/projects")
if cats and cats.get("data"):
    cat_id = cats["data"][0]["id"]
    cat_name = cats["data"][0]["name"]
    print(f"\n{Colors.BLUE}Testing with category: {cat_name}{Colors.RESET}")
    test("  Projects by cat", f"{BASE_URL}/projects/", {"category_id": cat_id})
    test("  Datasets by cat", f"{BASE_URL}/datasets/", {"category_id": cat_id})
    test("  Publications by cat", f"{BASE_URL}/publications/", {"category_id": cat_id})
    test("  AI Models by cat", f"{BASE_URL}/ai-models/", {"category_id": cat_id})
    test("  News by cat", f"{BASE_URL}/news/", {"category_id": cat_id})
    test("  Gallery by cat", f"{BASE_URL}/gallery/", {"category_id": cat_id})

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total: {passed + failed}")
print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
if failed == 0:
    print(f"\n{Colors.GREEN}All tests passed!{Colors.RESET}")
else:
    print(f"\n{Colors.RED}Some tests failed!{Colors.RESET}")
