#!/usr/bin/env python3
"""
Comprehensive Test Script for Files API
Tests file upload, listing, download, update, and delete

Prerequisites:
- Server running on http://localhost:8000
- Admin user credentials

Run: python3 test_files.py
"""

import requests
import json
import io

BASE_URL = "http://localhost:8000/api/v1"
FILES_URL = f"{BASE_URL}/files"

# Admin credentials
ADMIN_EMAIL = "supernew@example.com"
ADMIN_PASSWORD = "password123"

# Global variables
access_token = None
uploaded_file_id = None

def print_header(text: str):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def print_test(name: str, success: bool, details: str = ""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status} - {name}")
    if details:
        print(f"   {details}")

def test_login():
    global access_token
    print_header("SETUP: Admin Login")
    
    try:
        response = requests.post(
            f"{BASE_URL}/login",
            data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            print_test("Admin Login", True, f"Token: {access_token[:20]}...")
            return True
        else:
            print_test("Admin Login", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Admin Login", False, f"Error: {str(e)}")
        return False

def get_headers():
    return {"Authorization": f"Bearer {access_token}"}

def test_upload_image():
    global uploaded_file_id
    print_header("TEST 1: Upload Image")
    
    try:
        fake_image = io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00' * 100)
        files = {'file': ('test_image.png', fake_image, 'image/png')}
        data = {'description': 'Test image upload'}
        
        response = requests.post(f"{FILES_URL}/upload", headers=get_headers(), files=files, data=data)
        
        if response.status_code == 201:
            result = response.json()
            uploaded_file_id = result.get("id")
            print_test("Upload Image", True, 
                      f"ID: {uploaded_file_id}\nURL: {result.get('file_url')}\nSize: {result.get('file_size')} bytes")
            return True
        else:
            print_test("Upload Image", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Upload Image", False, f"Error: {str(e)}")
        return False

def test_upload_zip():
    print_header("TEST 2: Upload ZIP")
    
    try:
        fake_zip = io.BytesIO(b'PK\x03\x04' + b'\x00' * 200)
        files = {'file': ('dataset.zip', fake_zip, 'application/zip')}
        data = {'description': 'Test dataset archive'}
        
        response = requests.post(f"{FILES_URL}/upload", headers=get_headers(), files=files, data=data)
        
        if response.status_code == 201:
            result = response.json()
            print_test("Upload ZIP", True, f"Type: {result.get('file_type')}, MIME: {result.get('mime_type')}")
            return True
        else:
            print_test("Upload ZIP", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Upload ZIP", False, f"Error: {str(e)}")
        return False

def test_get_all_files():
    print_header("TEST 3: Get All Files (Public)")
    
    try:
        response = requests.get(f"{FILES_URL}/?offset=0&limit=10")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", 0)
            print_test("GET /files", True, f"Found {total} files")
            return True
        else:
            print_test("GET /files", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("GET /files", False, f"Error: {str(e)}")
        return False

def test_filter_by_type():
    print_header("TEST 4: Filter by Type")
    
    for file_type in ["image", "archive"]:
        try:
            response = requests.get(f"{FILES_URL}/?file_type={file_type}")
            if response.status_code == 200:
                count = response.json().get("total", 0)
                print_test(f"Filter '{file_type}'", True, f"Found {count} files")
            else:
                print_test(f"Filter '{file_type}'", False, f"Status: {response.status_code}")
        except Exception as e:
            print_test(f"Filter '{file_type}'", False, f"Error: {str(e)}")

def test_get_file_by_id():
    print_header("TEST 5: Get File by ID")
    
    if not uploaded_file_id:
        print("   ⚠️  Skipping")
        return False
    
    try:
        response = requests.get(f"{FILES_URL}/{uploaded_file_id}")
        
        if response.status_code == 200:
            data = response.json()
            print_test("GET by ID", True, f"File: {data.get('original_filename')}, Size: {data.get('file_size')} bytes")
            return True
        else:
            print_test("GET by ID", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("GET by ID", False, f"Error: {str(e)}")
        return False

def test_get_stats():
    print_header("TEST 6: Storage Stats")
    
    try:
        response = requests.get(f"{FILES_URL}/stats", headers=get_headers())
        
        if response.status_code == 200:
            data = response.json()
            print_test("GET stats", True, f"Files: {data.get('total_files')}, Storage: {data.get('total_size_mb')} MB")
            return True
        else:
            print_test("GET stats", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("GET stats", False, f"Error: {str(e)}")
        return False

def test_update_file():
    print_header("TEST 7: Update File")
    
    if not uploaded_file_id:
        print("   ⚠️  Skipping")
        return False
    
    try:
        update_data = {"description": "Updated: Test image for file manager"}
        response = requests.put(
            f"{FILES_URL}/{uploaded_file_id}",
            headers={**get_headers(), "Content-Type": "application/json"},
            json=update_data
        )
        
        if response.status_code == 200:
            print_test("Update file", True, "Description updated")
            return True
        else:
            print_test("Update file", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Update file", False, f"Error: {str(e)}")
        return False

def test_download_file():
    print_header("TEST 8: Download File")
    
    if not uploaded_file_id:
        print("   ⚠️  Skipping")
        return False
    
    try:
        response = requests.get(f"{FILES_URL}/download/{uploaded_file_id}")
        
        if response.status_code == 200:
            size = len(response.content)
            print_test("Download file", True, f"Downloaded {size} bytes")
            return True
        else:
            print_test("Download file", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Download file", False, f"Error: {str(e)}")
        return False

def test_delete_file():
    print_header("TEST 9: Delete File")
    
    if not uploaded_file_id:
        print("   ⚠️  Skipping")
        return False
    
    try:
        response = requests.delete(f"{FILES_URL}/{uploaded_file_id}", headers=get_headers())
        
        if response.status_code == 200:
            print_test("Delete file", True, response.json().get('detail'))
            
            # Verify deletion
            verify = requests.get(f"{FILES_URL}/{uploaded_file_id}")
            if verify.status_code == 404:
                print_test("✓ Deletion verified", True, "File not found")
            return True
        else:
            print_test("Delete file", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Delete file", False, f"Error: {str(e)}")
        return False

def main():
    print("\n" + "=" * 70)
    print("🧪 FILES API - TEST SUITE")
    print("=" * 70)
    
    results = []
    
    if not test_login():
        print("\n❌ FAILED: Cannot login")
        return
    
    results.append(("Upload Image", test_upload_image()))
    results.append(("Upload ZIP", test_upload_zip()))
    results.append(("Get All Files", test_get_all_files()))
    test_filter_by_type()
    results.append(("Get by ID", test_get_file_by_id()))
    results.append(("Storage Stats", test_get_stats()))
    results.append(("Update File", test_update_file()))
    results.append(("Download File", test_download_file()))
    results.append(("Delete File", test_delete_file()))
    
    print_header("📊 SUMMARY")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n{'Test':<40} {'Result'}")
    print("-" * 70)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:<40} {status}")
    
    print("-" * 70)
    print(f"Total: {passed}/{total} passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {total - passed} failed")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
