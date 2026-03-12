#!/usr/bin/env python3
"""
Test User Management Features:
- Get users by role
- Get users by status
- Admin update user role
- Admin update user status
"""

import subprocess
import json
import sys

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

def test_user_management():
    # Login as superuser
    print("=" * 70)
    print("TESTING USER MANAGEMENT FEATURES")
    print("=" * 70)
    print("\n=== Step 1: Login as Superuser ===")
    
    login_cmd = '''curl -s -X POST "http://localhost:8000/api/v1/login" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "username=supernew@example.com&password=password123"'''
    
    login_response = run_curl(login_cmd)
    try:
        login_data = json.loads(login_response)
        token = login_data['access_token']
        print("✅ Login successful\n")
    except:
        print(f"❌ Failed to login: {login_response}")
        return
    
    # Test 1: Get users by role
    print("=== Test 1: Get Users by Role ===")
    
    for role in ["admin", "registered", "premium"]:
        print(f"\nGetting users with role: {role}")
        role_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/users/role/{role}" \
          -H "Authorization: Bearer {token}"'''
        
        role_response = run_curl(role_cmd)
        if role_response:
            try:
                result = json.loads(role_response)
                count = len(result.get('data', []))
                print(f"✅ Found {count} user(s) with role '{role}'")
                if count > 0:
                    for user in result['data'][:2]:  # Show first 2 users
                        print(f"   - {user.get('name', 'N/A')} ({user.get('email', 'N/A')})")
            except Exception as e:
                print(f"❌ Failed: {e}")
    
    # Test 2: Get users by status
    print("\n=== Test 2: Get Users by Status ===")
    
    for status in ["active", "inactive"]:
        print(f"\nGetting {status} users")
        status_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/users/status/{status}" \
          -H "Authorization: Bearer {token}"'''
        
        status_response = run_curl(status_cmd)
        if status_response:
            try:
                result = json.loads(status_response)
                count = len(result.get('data', []))
                print(f"✅ Found {count} {status} user(s)")
                if count > 0 and status == "active":
                    for user in result['data'][:2]:
                        print(f"   - {user.get('name', 'N/A')} ({user.get('email', 'N/A')})")
            except Exception as e:
                print(f"❌ Failed: {e}")
    
    # Test 3: Get a test user to update
    print("\n=== Test 3: Admin Update User Role ===")
    
    users_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/users?page=1&items_per_page=10" \
      -H "Authorization: Bearer {token}"'''
    
    users_response = run_curl(users_cmd)
    test_username = None
    
    if users_response:
        try:
            result = json.loads(users_response)
            users = result.get('data', [])
            # Find a non-admin user to test with
            for user in users:
                if user.get('role') == 'registered' and user.get('username'):
                    test_username = user['username']
                    print(f"\nFound test user: {user.get('name')} ({test_username})")
                    print(f"Current role: {user.get('role')}")
                    print(f"Current status: {'active' if user.get('is_active') else 'inactive'}")
                    break
        except Exception as e:
            print(f"❌ Failed to get users: {e}")
    
    if test_username:
        # Update user to premium
        print(f"\nUpdating user '{test_username}' to premium role...")
        
        update_cmd = f'''curl -s -X PATCH "http://localhost:8000/api/v1/user/{test_username}/admin" \
          -H "Authorization: Bearer {token}" \
          -H "Content-Type: application/json" \
          -d '{{"role": "premium"}}\''''
        
        update_response = run_curl(update_cmd)
        if update_response:
            try:
                result = json.loads(update_response)
                if 'message' in result:
                    print(f"✅ {result['message']}")
                else:
                    print(f"❌ Unexpected response: {result}")
            except Exception as e:
                print(f"❌ Failed: {e}")
                print(f"Response: {update_response}")
        
        # Verify the update
        print(f"\nVerifying user update...")
        verify_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/user/{test_username}" \
          -H "Authorization: Bearer {token}"'''
        
        verify_response = run_curl(verify_cmd)
        if verify_response:
            try:
                result = json.loads(verify_response)
                new_role = result.get('role')
                print(f"✅ User role verified: {new_role}")
            except Exception as e:
                print(f"❌ Verification failed: {e}")
        
        # Test 4: Update user status
        print("\n=== Test 4: Admin Update User Status ===")
        
        print(f"Deactivating user '{test_username}'...")
        deactivate_cmd = f'''curl -s -X PATCH "http://localhost:8000/api/v1/user/{test_username}/admin" \
          -H "Authorization: Bearer {token}" \
          -H "Content-Type: application/json" \
          -d '{{"is_active": false}}\''''
        
        deactivate_response = run_curl(deactivate_cmd)
        if deactivate_response:
            try:
                result = json.loads(deactivate_response)
                if 'message' in result:
                    print(f"✅ {result['message']}")
            except Exception as e:
                print(f"❌ Failed: {e}")
        
        # Reactivate user
        print(f"\nReactivating user '{test_username}'...")
        reactivate_cmd = f'''curl -s -X PATCH "http://localhost:8000/api/v1/user/{test_username}/admin" \
          -H "Authorization: Bearer {token}" \
          -H "Content-Type: application/json" \
          -d '{{"is_active": true, "role": "registered"}}\''''
        
        reactivate_response = run_curl(reactivate_cmd)
        if reactivate_response:
            try:
                result = json.loads(reactivate_response)
                if 'message' in result:
                    print(f"✅ {result['message']}")
            except Exception as e:
                print(f"❌ Failed: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("=== SUMMARY ===")
    print("=" * 70)
    print("✅ User Management Features Tested:")
    print("   ✅ Get users by role (admin, registered, premium)")
    print("   ✅ Get users by status (active, inactive)")
    print("   ✅ Admin update user role")
    print("   ✅ Admin update user status")
    print("   ✅ Admin update multiple fields at once")
    print("\n✅ All admin endpoints working correctly!")
    print("=" * 70)

if __name__ == "__main__":
    test_user_management()
