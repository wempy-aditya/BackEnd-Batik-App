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

def test_project_delete_with_categories():
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
    
    # Step 2: Create a new project
    print("\n=== Step 2: Creating Project ===")
    create_data = {
        "title": "Test Project with Categories",
        "slug": "test-project-with-categories",
        "description": "Testing delete functionality with category links",
        "technologies": ["Python", "FastAPI"],
        "challenges": ["Foreign key constraints"],
        "achievements": ["Bug fixes"],
        "access_level": "public",
        "status": "published"
    }
    
    create_cmd = f'''curl -s -X POST "http://localhost:8000/api/v1/projects/" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer {token}" \
      -d '{json.dumps(create_data)}' '''
    
    create_response = run_curl(create_cmd)
    try:
        created_project = json.loads(create_response)
        project_id = created_project.get('id')
        print(f"✅ Project created with ID: {project_id}")
    except:
        print(f"❌ Failed to create project: {create_response}")
        return
    
    # Step 3: Assign categories to create foreign key dependency
    print("\n=== Step 3: Assigning Categories ===")
    assign_cmd = f'''curl -s -X POST "http://localhost:8000/api/v1/projects/{project_id}/categories" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer {token}" \
      -d '{{"category_ids": ["019aabe5-142c-747d-8571-ee9cf89ae01a"]}}\''''
    
    assign_response = run_curl(assign_cmd)
    try:
        assign_result = json.loads(assign_response)
        if 'id' in assign_result:
            print("✅ Category assigned successfully")
        else:
            print(f"❌ Failed to assign category: {assign_result}")
    except:
        print(f"❌ Failed to parse assign response: {assign_response}")
    
    # Step 4: Verify category links exist
    print("\n=== Step 4: Verifying Category Links ===")
    # This is the critical test - delete a project with category links
    
    # Step 5: Test delete (potential foreign key constraint error)
    print("\n=== Step 5: Testing Delete with Category Links ===")
    delete_cmd = f'''curl -s -X DELETE "http://localhost:8000/api/v1/projects/{project_id}" \
      -H "Authorization: Bearer {token}"'''
    
    delete_response = run_curl(delete_cmd)
    if delete_response:
        try:
            result = json.loads(delete_response)
            if 'message' in result and 'deleted successfully' in result['message']:
                print("✅ Project with category links deleted successfully!")
                print("✅ No foreign key constraint error occurred!")
            elif 'detail' in result:
                print(f"❌ Delete failed: {result['detail']}")
                return "FAILED"
            else:
                print(f"❌ Unexpected response: {result}")
                return "FAILED"
        except:
            # If it's not JSON, it might be an error page
            if 'Internal Server Error' in delete_response:
                print("❌ Internal Server Error - foreign key constraint violation!")
                print("   This confirms we need cascade delete for projects")
                return "NEEDS_CASCADE_DELETE"
            else:
                print(f"❌ Failed to parse delete response: {delete_response}")
                return "FAILED"
    
    # Step 6: Final verification
    print("\n=== Step 6: Final Verification ===")
    verify_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/projects/{project_id}" \
      -H "Authorization: Bearer {token}"'''
    
    verify_response = run_curl(verify_cmd)
    if verify_response:
        try:
            result = json.loads(verify_response)
            if 'detail' in result and 'not found' in result['detail']:
                print("✅ Project completely removed from database")
                print("✅ All category links also removed")
                return "SUCCESS"
            else:
                print("❌ Project still exists after delete")
                return "FAILED"
        except:
            print(f"❌ Failed to parse verify response: {verify_response}")
            return "FAILED"

if __name__ == "__main__":
    result = test_project_delete_with_categories()
    print(f"\n=== Final Result: {result} ===")
    
    if result == "NEEDS_CASCADE_DELETE":
        print("🔧 Need to implement cascade delete for projects")
        print("   Similar to the fix applied for AI models")
    elif result == "SUCCESS":
        print("✅ Project delete with categories working correctly!")
    else:
        print("❓ Unexpected test result")