#!/usr/bin/env python3
"""
Test script untuk Public API endpoints
Run: python test_public_api.py
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1/public"

def print_test(name: str, success: bool, details: str = ""):
    """Print test result"""
    status = "✅" if success else "❌"
    print(f"{status} {name}")
    if details:
        print(f"   {details}")

def test_endpoint(endpoint: str, expected_status: int = 200) -> Dict[str, Any]:
    """Test an endpoint and return response"""
    try:
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, timeout=5)
        success = response.status_code == expected_status
        return {
            "success": success,
            "status_code": response.status_code,
            "data": response.json() if success else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def main():
    print("=" * 60)
    print("PUBLIC API ENDPOINT TESTS")
    print("=" * 60)
    print()
    
    # Test Projects endpoints
    print("📁 PROJECTS")
    print("-" * 40)
    
    result = test_endpoint("/projects")
    print_test("GET /projects", result["success"])
    
    result = test_endpoint("/projects/featured")
    print_test("GET /projects/featured", result["success"])
    
    result = test_endpoint("/projects/latest")
    print_test("GET /projects/latest", result["success"])
    
    result = test_endpoint("/projects?search=test")
    print_test("GET /projects?search=test", result["success"])
    
    print()
    
    # Test Datasets endpoints
    print("📊 DATASETS")
    print("-" * 40)
    
    result = test_endpoint("/datasets")
    print_test("GET /datasets", result["success"])
    
    result = test_endpoint("/datasets/featured")
    print_test("GET /datasets/featured", result["success"])
    
    result = test_endpoint("/datasets/latest")
    print_test("GET /datasets/latest", result["success"])
    
    print()
    
    # Test AI Models endpoints
    print("🤖 AI MODELS")
    print("-" * 40)
    
    result = test_endpoint("/ai-models")
    print_test("GET /ai-models", result["success"])
    
    result = test_endpoint("/ai-models/featured")
    print_test("GET /ai-models/featured", result["success"])
    
    result = test_endpoint("/ai-models/latest")
    print_test("GET /ai-models/latest", result["success"])
    
    print()
    
    # Test Publications endpoints
    print("📚 PUBLICATIONS")
    print("-" * 40)
    
    result = test_endpoint("/publications")
    print_test("GET /publications", result["success"])
    
    result = test_endpoint("/publications/featured")
    print_test("GET /publications/featured", result["success"])
    
    result = test_endpoint("/publications/latest")
    print_test("GET /publications/latest", result["success"])
    
    result = test_endpoint("/publications/year/2024")
    print_test("GET /publications/year/2024", result["success"])
    
    print()
    
    # Test News endpoints
    print("📰 NEWS")
    print("-" * 40)
    
    result = test_endpoint("/news")
    print_test("GET /news", result["success"])
    
    result = test_endpoint("/news/featured")
    print_test("GET /news/featured", result["success"])
    
    result = test_endpoint("/news/latest")
    print_test("GET /news/latest", result["success"])
    
    print()
    
    # Test Gallery endpoints
    print("🖼️ GALLERY")
    print("-" * 40)
    
    result = test_endpoint("/gallery")
    print_test("GET /gallery", result["success"])
    
    result = test_endpoint("/gallery/featured")
    print_test("GET /gallery/featured", result["success"])
    
    result = test_endpoint("/gallery/latest")
    print_test("GET /gallery/latest", result["success"])
    
    print()
    
    # Test Categories endpoints
    print("🏷️ CATEGORIES")
    print("-" * 40)
    
    result = test_endpoint("/categories/projects")
    print_test("GET /categories/projects", result["success"])
    
    result = test_endpoint("/categories/datasets")
    print_test("GET /categories/datasets", result["success"])
    
    result = test_endpoint("/categories/publications")
    print_test("GET /categories/publications", result["success"])
    
    result = test_endpoint("/categories/news")
    print_test("GET /categories/news", result["success"])
    
    result = test_endpoint("/categories/models")
    print_test("GET /categories/models", result["success"])
    
    result = test_endpoint("/categories/gallery")
    print_test("GET /categories/gallery", result["success"])
    
    result = test_endpoint("/categories/all")
    print_test("GET /categories/all", result["success"])
    if result["success"] and result["data"]:
        categories = result["data"]
        print(f"   Found {len(categories)} category types")
    
    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
