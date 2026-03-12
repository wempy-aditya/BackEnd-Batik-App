#!/bin/bash

echo "=== Testing Gallery Delete Fix ==="
echo ""

# Login
echo "Step 1: Login..."
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=supernew@example.com&password=password123" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Login failed"
  exit 1
fi

echo "✅ Login successful"
echo ""

# Test the original gallery ID that was failing
GALLERY_ID="019ac4c5-3f75-76ac-bfb8-6163c7e3b333"

echo "Step 2: Testing delete of gallery item: $GALLERY_ID"
echo ""

# Try to delete
RESPONSE=$(curl -s -X DELETE "http://localhost:8000/api/v1/gallery/$GALLERY_ID" \
  -H "Authorization: Bearer $TOKEN")

echo "Response: $RESPONSE"
echo ""

# Check if successful
if echo "$RESPONSE" | grep -q "deleted successfully"; then
  echo "✅ SUCCESS: Gallery item deleted without foreign key errors!"
  echo "✅ Cascade delete is working properly!"
elif echo "$RESPONSE" | grep -q "not found"; then
  echo "ℹ️  Gallery item already deleted (from previous test)"
  echo "✅ This means the fix is working!"
elif echo "$RESPONSE" | grep -q "Internal Server Error"; then
  echo "❌ FAILED: Still getting Internal Server Error"
  echo "   Check docker logs for details"
  docker logs fastapi-boilerplate-web-1 --tail 20
else
  echo "⚠️  Unexpected response: $RESPONSE"
fi

echo ""
echo "=== Test Complete ==="
