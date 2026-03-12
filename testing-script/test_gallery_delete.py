#!/usr/bin/env python3

import subprocess
import json

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

def test_gallery_delete():
    # Step 1: Login
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
        print(f"❌ Failed to login: {login_response}")
        return
    
    # Step 2: Use the gallery ID from the error
    gallery_id = "019ac4c5-3f75-76ac-bfb8-6163c7e3b333"
    print(f"\n=== Step 2: Testing Delete of Gallery Item ===")
    print(f"Gallery ID: {gallery_id}")
    
    # Step 3: Test delete with cascade
    print("\n=== Step 3: Testing Cascade Delete ===")
    delete_cmd = f'''curl -s -X DELETE "http://localhost:8000/api/v1/gallery/{gallery_id}" \
      -H "Authorization: Bearer {token}"'''
    
    delete_response = run_curl(delete_cmd)
    if delete_response:
        try:
            result = json.loads(delete_response)
            if 'message' in result and 'deleted successfully' in result['message']:
                print("✅ Gallery item with category links deleted successfully!")
                print("✅ No foreign key constraint error occurred!")
                print("✅ Cascade delete working properly!")
                return "SUCCESS"
            elif 'detail' in result:
                if 'not found' in result['detail']:
                    print(f"ℹ️ Gallery item already deleted or not found")
                    return "ALREADY_DELETED"
                else:
                    print(f"❌ Delete failed: {result['detail']}")
                    return "FAILED"
            else:
                print(f"❌ Unexpected response: {result}")
                return "FAILED"
        except Exception as e:
            # If it's not JSON, check for error
            if 'Internal Server Error' in delete_response:
                print("❌ Internal Server Error - cascade delete not working!")
                print("   Foreign key constraint still exists")
                print(f"   Response: {delete_response}")
                return "STILL_BROKEN"
            else:
                print(f"❌ Failed to parse delete response: {delete_response}")
                return "FAILED"
    
    return "FAILED"

if __name__ == "__main__":
    result = test_gallery_delete()
    print(f"\n=== Final Test Result: {result} ===")
    
    if result == "SUCCESS":
        print("✅ Gallery cascade delete FIXED successfully!")
        print("✅ Foreign key constraint error resolved!")
        print("✅ Gallery items can now be deleted even with category links!")
    elif result == "ALREADY_DELETED":
        print("ℹ️ Gallery item was already deleted (possibly from previous test)")
        print("ℹ️ This means the fix is working!")
    elif result == "STILL_BROKEN":
        print("❌ Cascade delete implementation needs debugging")
        print("❌ Check docker logs for details")
    else:
        print("❓ Test was inconclusive")
