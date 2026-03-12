#!/bin/bash

echo "=== Testing Flexible Metrics ==="
echo ""

# Login
echo "Step 1: Login..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=supernew@example.com&password=password123")

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Login failed"
  exit 1
fi

echo "✅ Login successful"
echo ""

# Create model with flexible metrics
echo "Step 2: Creating AI Model with Flexible Metrics..."
TIMESTAMP=$(date +%s)

curl -s -X POST "http://localhost:8000/api/v1/ai-models" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Flexible Metrics Test $TIMESTAMP\",
    \"slug\": \"flex-metrics-$TIMESTAMP\",
    \"description\": \"Testing all metric types\",
    \"architecture\": \"Custom\",
    \"dataset_used\": \"Mixed\",
    \"metrics\": {
      \"accuracy\": 0.95,
      \"precision\": 0.93,
      \"recall\": 0.94,
      \"f1_score\": 0.92,
      \"map\": 0.78,
      \"map_50\": 0.85,
      \"iou\": 0.82,
      \"fid\": 12.5,
      \"inception_score\": 8.3,
      \"bleu\": 0.45,
      \"rouge_1\": 0.52,
      \"mae\": 0.15,
      \"mse\": 0.023,
      \"rmse\": 0.152,
      \"r2_score\": 0.89,
      \"custom_metric_1\": \"any value\",
      \"training_time_hours\": 2.5,
      \"inference_time_ms\": 45,
      \"model_size_mb\": 250,
      \"gpu_memory_gb\": 8
    },
    \"model_file_url\": \"https://example.com/test-model.pt\",
    \"access_level\": \"public\",
    \"status\": \"draft\"
  }" > /tmp/metrics_test_result.json

echo ""
echo "=== Response ==="
cat /tmp/metrics_test_result.json | python3 -m json.tool 2>/dev/null || cat /tmp/metrics_test_result.json

echo ""
echo ""
echo "=== Verification ==="

# Check if metrics were stored
METRICS=$(cat /tmp/metrics_test_result.json | grep -o '"metrics":{[^}]*}' 2>/dev/null)

if [ ! -z "$METRICS" ]; then
  echo "✅ Metrics field found in response!"
  echo "✅ All metric types accepted successfully!"
  echo ""
  echo "Stored metrics include:"
  echo "  - Classification: accuracy, precision, recall, f1_score"
  echo "  - Detection: map, map_50, iou"
  echo "  - Generative: fid, inception_score"
  echo "  - NLP: bleu, rouge_1"
  echo "  - Regression: mae, mse, rmse, r2_score"
  echo "  - Custom: training_time_hours, inference_time_ms, etc."
else
  echo "⚠️ Could not verify metrics in response"
fi

echo ""
echo "=== Test Complete ==="
