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

def test_project_delete():
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
        "title": "Test Project for Delete",
        "slug": "test-project-for-delete",
        "description": "Testing delete functionality with category links",
        "full_description": "This project is created to test the delete functionality",
        "technologies": ["Python", "FastAPI", "PostgreSQL"],
        "challenges": ["Foreign key constraints", "Cascade delete"],
        "achievements": ["Successful implementation", "Bug fixes"],
        "future_work": ["Performance optimization"],
        "tags": ["testing", "backend"],
        "complexity": "medium",
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
    # First check available project categories
    categories_check_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/projects/" \
      -H "Authorization: Bearer {token}"'''
    
    # Let's try to assign some category (we'll need to check what's available)
    # For now, let's try with an existing category if available
    
    # Step 4: Test delete (might fail due to foreign key constraint)
    print("\n=== Step 4: Testing Project Delete ===")
    delete_cmd = f'''curl -s -X DELETE "http://localhost:8000/api/v1/projects/{project_id}" \
      -H "Authorization: Bearer {token}"'''
    
    delete_response = run_curl(delete_cmd)
    if delete_response:
        try:
            result = json.loads(delete_response)
            if 'message' in result and 'deleted successfully' in result['message']:
                print("✅ Project deleted successfully!")
                print(f"   Response: {result['message']}")
            elif 'detail' in result:
                print(f"❌ Delete failed: {result['detail']}")
            else:
                print(f"❌ Unexpected response: {result}")
        except:
            # If it's not JSON, it might be an error page
            if 'Internal Server Error' in delete_response:
                print("❌ Internal Server Error - likely foreign key constraint issue")
                print("   This indicates we need to implement cascade delete for projects")
                return "NEEDS_FIX"
            else:
                print(f"❌ Failed to parse delete response: {delete_response}")
    
    # Step 5: Verify deletion
    print("\n=== Step 5: Verifying Deletion ===")
    verify_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/projects/{project_id}" \
      -H "Authorization: Bearer {token}"'''
    
    verify_response = run_curl(verify_cmd)
    if verify_response:
        try:
            result = json.loads(verify_response)
            if 'detail' in result and 'not found' in result['detail']:
                print("✅ Project properly deleted")
                return "SUCCESS"
            else:
                print("❌ Project still exists after delete")
                return "FAILED"
        except:
            print(f"❌ Failed to parse verify response: {verify_response}")
    
    return "UNKNOWN"

if __name__ == "__main__":
    result = test_project_delete()
    print(f"\n=== Test Result: {result} ===")
    if result == "NEEDS_FIX":
        print("🔧 Project delete needs cascade delete implementation")
    elif result == "SUCCESS":
        print("✅ Project delete working correctly")
    else:
        print("❓ Test result unclear")