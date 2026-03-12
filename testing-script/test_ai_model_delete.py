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

def test_ai_model_delete():
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
    
    # Step 2: Test delete AI model with cascade delete
    print("\n=== Step 2: Testing AI Model Delete ===")
    ai_model_id = "019ac0fe-3ecf-7d52-8d28-a1a09c23e29a"
    
    delete_cmd = f'''curl -s -X DELETE "http://localhost:8000/api/v1/ai-models/{ai_model_id}" \
      -H "Authorization: Bearer {token}"'''
    
    delete_response = run_curl(delete_cmd)
    if delete_response:
        try:
            result = json.loads(delete_response)
            if 'detail' in result:
                if 'deleted successfully' in result['detail']:
                    print("✅ AI Model deleted successfully!")
                    print(f"   Response: {result['detail']}")
                elif 'not found' in result['detail']:
                    print(f"❌ AI Model not found: {result['detail']}")
                else:
                    print(f"❌ Unexpected response: {result['detail']}")
            else:
                print(f"❌ Unexpected response format: {result}")
        except Exception as e:
            print(f"❌ Failed to parse delete response: {delete_response}")
            print(f"   Error: {e}")
    else:
        print("❌ Delete request failed")
    
    # Step 3: Verify the model was deleted
    print("\n=== Step 3: Verifying Model Deletion ===")
    verify_cmd = f'''curl -s -X GET "http://localhost:8000/api/v1/ai-models/{ai_model_id}" \
      -H "Authorization: Bearer {token}"'''
    
    verify_response = run_curl(verify_cmd)
    if verify_response:
        try:
            result = json.loads(verify_response)
            if 'detail' in result and 'not found' in result['detail']:
                print("✅ Model properly deleted - not found in database")
            else:
                print("❌ Model still exists in database")
                print(f"   Response: {result}")
        except:
            print(f"❌ Failed to parse verify response: {verify_response}")
    
    print("\n=== Test Summary ===")
    print("✅ AI Model delete functionality test completed!")

if __name__ == "__main__":
    test_ai_model_delete()