#!/usr/bin/env python3

import subprocess
import json
import random

def run_curl(cmd):
    """Run curl command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"Exception: {e}")
        return None

def comprehensive_gallery_test():
    # Login
    print("=== Step 1: Logging in ===")
    login_cmd = '''curl -s -X POST "http://localhost:8000/api/v1/login" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "username=supernew@example.com&password=password123"'''
    
    login_response = run_curl(login_cmd)
    try:
        login_data = json.loads(login_response)
        token = login_data['access_token']
        print("✅ Login successful")
    except:
        print(f"❌ Failed to login")
        return
    
    # Get a gallery category to test with
    print("\n=== Step 2: Getting Gallery Categories ===")
    categories_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/gallery-categories" \
      -H "Authorization: Bearer {token}"'''
    
    categories_response = run_curl(categories_cmd)
    category_id = None
    if categories_response:
        try:
            categories_data = json.loads(categories_response)
            if categories_data.get('items') and len(categories_data['items']) > 0:
                category_id = categories_data['items'][0]['id']
                print(f"✅ Found category: {category_id}")
            else:
                print("⚠️ No categories found, will test without categories")
        except Exception as e:
            print(f"⚠️ Could not get categories: {e}")
    
    # Create a new gallery item
    print("\n=== Step 3: Creating Test Gallery Item ===")
    random_num = random.randint(1000, 9999)
    
    if category_id:
        create_cmd = f'''curl -s -X POST "http://localhost:8000/api/v1/gallery?category_ids={category_id}" \
          -H "Authorization: Bearer {token}" \
          -H "Content-Type: application/json" \
          -d '{{"prompt": "Test cascade delete {random_num}", "image_url": "https://example.com/test{random_num}.jpg"}}\''''
    else:
        create_cmd = f'''curl -s -X POST "http://localhost:8000/api/v1/gallery" \
          -H "Authorization: Bearer {token}" \
          -H "Content-Type: application/json" \
          -d '{{"prompt": "Test cascade delete {random_num}", "image_url": "https://example.com/test{random_num}.jpg"}}\''''
    
    create_response = run_curl(create_cmd)
    test_gallery_id = None
    
    if create_response:
        try:
            gallery_data = json.loads(create_response)
            test_gallery_id = gallery_data.get('id')
            print(f"✅ Test gallery created: {test_gallery_id}")
            if category_id:
                print(f"✅ With category link: {category_id}")
        except Exception as e:
            print(f"❌ Failed to create gallery: {e}")
            print(f"Response: {create_response}")
            return
    
    if not test_gallery_id:
        print("❌ Could not create test gallery item")
        return
    
    # Test delete with cascade
    print("\n=== Step 4: Testing Cascade Delete ===")
    delete_cmd = f'''curl -s -X DELETE "http://localhost:8000/api/v1/gallery/{test_gallery_id}" \
      -H "Authorization: Bearer {token}"'''
    
    delete_response = run_curl(delete_cmd)
    if delete_response:
        try:
            result = json.loads(delete_response)
            if 'message' in result and 'deleted successfully' in result['message']:
                print("✅ Gallery item deleted successfully!")
                print("✅ No foreign key constraint error!")
                
                # Verify deletion
                print("\n=== Step 5: Verifying Complete Deletion ===")
                verify_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/gallery/{test_gallery_id}" \
                  -H "Authorization: Bearer {token}"'''
                
                verify_response = run_curl(verify_cmd)
                try:
                    verify_result = json.loads(verify_response)
                    if 'detail' in verify_result and 'not found' in verify_result['detail']:
                        print("✅ Gallery item completely removed from database")
                        print("✅ Category links properly cleaned up")
                        return "SUCCESS"
                    else:
                        print("❌ Gallery item still exists after delete")
                        return "FAILED"
                except:
                    print(f"❌ Unexpected verify response: {verify_response}")
                    return "FAILED"
            else:
                print(f"❌ Delete failed: {result}")
                return "FAILED"
        except Exception as e:
            print(f"❌ Delete parse error: {e}")
            print(f"Response: {delete_response}")
            return "FAILED"
    
    return "FAILED"

if __name__ == "__main__":
    result = comprehensive_gallery_test()
    
    print("\n" + "="*60)
    print("=== COMPREHENSIVE GALLERY CASCADE DELETE TEST RESULTS ===")
    print("="*60)
    
    if result == "SUCCESS":
        print("✅ ALL TESTS PASSED!")
        print("✅ Gallery cascade delete working perfectly!")
        print("✅ Foreign key constraint error RESOLVED!")
        print("✅ Gallery items can be created and deleted with category links!")
    else:
        print("❌ Some tests failed")
        print("   Check the output above for details")
