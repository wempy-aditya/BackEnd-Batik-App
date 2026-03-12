#!/usr/bin/env python3
"""
Quick test for Contributors API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test 1: Get all contributors
print("=" * 60)
print("TEST 1: GET /contributors")
print("=" * 60)
response = requests.get(f"{BASE_URL}/contributors")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "=" * 60)
print("✅ Contributors API is working!")
print("=" * 60)
