#!/usr/bin/env python3

import subprocess
import json
import sys

def run_curl(cmd):
    """Run curl command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_existing_project_delete():
    # Step 1: Login to get fresh token
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
    
    # Step 2: Use existing project with category links
    project_id = "019aabee-16f0-75e5-827f-33a66e24814c"  # ML Research project
    print(f"\n=== Step 2: Testing Delete of Existing Project ===")
    print(f"Project ID: {project_id} (ML Research with 2 category links)")
    
    # Step 3: Test delete (should work with our new cascade delete)
    print("\n=== Step 3: Testing Cascade Delete ===")
    delete_cmd = f'''curl -s -X DELETE "http://localhost:8000/api/v1/projects/{project_id}" \
      -H "Authorization: Bearer {token}"'''
    
    delete_response = run_curl(delete_cmd)
    if delete_response:
        try:
            result = json.loads(delete_response)
            if 'message' in result and 'deleted successfully' in result['message']:
                print("✅ Project with category links deleted successfully!")
                print("✅ No foreign key constraint error occurred!")
                print("✅ Cascade delete working properly!")
            elif 'detail' in result:
                print(f"❌ Delete failed: {result['detail']}")
                return "FAILED"
            else:
                print(f"❌ Unexpected response: {result}")
                return "FAILED"
        except:
            # If it's not JSON, it might be an error page
            if 'Internal Server Error' in delete_response:
                print("❌ Internal Server Error - cascade delete not working!")
                print("   Foreign key constraint still exists")
                return "STILL_BROKEN"
            else:
                print(f"❌ Failed to parse delete response: {delete_response}")
                return "FAILED"
    
    # Step 4: Verify deletion and category links cleanup
    print("\n=== Step 4: Verifying Complete Deletion ===")
    verify_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/projects/{project_id}" \
      -H "Authorization: Bearer {token}"'''
    
    verify_response = run_curl(verify_cmd)
    if verify_response:
        try:
            result = json.loads(verify_response)
            if 'detail' in result and 'not found' in result['detail']:
                print("✅ Project completely removed from database")
                return "SUCCESS"
            else:
                print("❌ Project still exists after delete")
                return "FAILED"
        except:
            print(f"❌ Failed to parse verify response: {verify_response}")
            return "FAILED"

if __name__ == "__main__":
    result = test_existing_project_delete()
    print(f"\n=== Final Test Result: {result} ===")
    
    if result == "SUCCESS":
        print("✅ Project cascade delete FIXED successfully!")
        print("✅ Foreign key constraint error resolved!")
        print("✅ Projects can now be deleted even with category links!")
    elif result == "STILL_BROKEN":
        print("❌ Cascade delete implementation needs debugging")
    else:
        print("❓ Test was inconclusive")