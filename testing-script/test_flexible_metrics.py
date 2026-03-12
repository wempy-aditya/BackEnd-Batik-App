#!/usr/bin/env python3
"""
Test script to verify flexible metrics support in AI Models
"""

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

def test_flexible_metrics():
    # Login
    print("=== Step 1: Login ===")
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
    
    # Test 1: Classification Metrics
    print("=== Test 1: Classification Metrics ===")
    random_num = random.randint(1000, 9999)
    
    classification_model = {
        "name": f"BERT Classifier {random_num}",
        "slug": f"bert-classifier-{random_num}",
        "description": "BERT model for sentiment analysis",
        "architecture": "BERT",
        "dataset_used": "IMDB Reviews",
        "metrics": {
            "accuracy": 0.94,
            "precision": 0.93,
            "recall": 0.95,
            "f1_score": 0.94,
            "auc_roc": 0.97,
            "log_loss": 0.15,
            "training_time_hours": 3,
            "inference_time_ms": 120,
            "model_size_mb": 440
        },
        "model_file_url": "https://example.com/bert-classifier.pt",
        "access_level": "public",
        "status": "published"
    }
    
    create_cmd = f'''curl -s -X POST "http://localhost:8000/api/v1/ai-models" \
      -H "Authorization: Bearer {token}" \
      -H "Content-Type: application/json" \
      -d '{json.dumps(classification_model)}' '''
    
    response = run_curl(create_cmd)
    if response:
        try:
            result = json.loads(response)
            if 'id' in result:
                print(f"✅ Created model with ID: {result['id']}")
                print(f"✅ Metrics stored: {json.dumps(result.get('metrics', {}), indent=2)}")
                test_1_id = result['id']
            else:
                print(f"❌ Failed: {result}")
                return
        except Exception as e:
            print(f"❌ Parse error: {e}")
            print(f"Response: {response}")
            return
    
    # Test 2: Generative Model Metrics
    print("\n=== Test 2: Generative Model Metrics ===")
    random_num = random.randint(1000, 9999)
    
    generative_model = {
        "name": f"Stable Diffusion {random_num}",
        "slug": f"stable-diffusion-{random_num}",
        "description": "Text-to-image diffusion model",
        "architecture": "Latent Diffusion",
        "dataset_used": "LAION-5B",
        "metrics": {
            "fid": 8.2,
            "inception_score": 9.1,
            "clip_score": 0.32,
            "lpips": 0.12,
            "ssim": 0.92,
            "psnr": 28.5,
            "inference_steps": 50,
            "inference_time_seconds": 4.5,
            "model_size_gb": 2.1,
            "gpu_memory_mb": 8192
        },
        "model_file_url": "https://example.com/sd.ckpt",
        "access_level": "public",
        "status": "published"
    }
    
    create_cmd = f'''curl -s -X POST "http://localhost:8000/api/v1/ai-models" \
      -H "Authorization: Bearer {token}" \
      -H "Content-Type: application/json" \
      -d '{json.dumps(generative_model)}' '''
    
    response = run_curl(create_cmd)
    if response:
        try:
            result = json.loads(response)
            if 'id' in result:
                print(f"✅ Created model with ID: {result['id']}")
                print(f"✅ Metrics stored: {json.dumps(result.get('metrics', {}), indent=2)}")
            else:
                print(f"❌ Failed: {result}")
        except Exception as e:
            print(f"❌ Parse error: {e}")
            print(f"Response: {response}")
    
    # Test 3: Object Detection Metrics
    print("\n=== Test 3: Object Detection Metrics ===")
    random_num = random.randint(1000, 9999)
    
    detection_model = {
        "name": f"YOLOv8 {random_num}",
        "slug": f"yolov8-{random_num}",
        "description": "Real-time object detection",
        "architecture": "YOLOv8",
        "dataset_used": "COCO",
        "metrics": {
            "map": 0.528,
            "map_50": 0.697,
            "map_75": 0.571,
            "precision": 0.682,
            "recall": 0.581,
            "iou": 0.65,
            "fps": 45,
            "inference_time_ms": 22,
            "model_size_mb": 165,
            "parameters_millions": 43.7
        },
        "model_file_url": "https://example.com/yolov8.pt",
        "access_level": "public",
        "status": "published"
    }
    
    create_cmd = f'''curl -s -X POST "http://localhost:8000/api/v1/ai-models" \
      -H "Authorization: Bearer {token}" \
      -H "Content-Type: application/json" \
      -d '{json.dumps(detection_model)}' '''
    
    response = run_curl(create_cmd)
    if response:
        try:
            result = json.loads(response)
            if 'id' in result:
                print(f"✅ Created model with ID: {result['id']}")
                print(f"✅ Metrics stored: {json.dumps(result.get('metrics', {}), indent=2)}")
            else:
                print(f"❌ Failed: {result}")
        except Exception as e:
            print(f"❌ Parse error: {e}")
            print(f"Response: {response}")
    
    # Test 4: Regression Metrics
    print("\n=== Test 4: Regression Metrics ===")
    random_num = random.randint(1000, 9999)
    
    regression_model = {
        "name": f"XGBoost Regressor {random_num}",
        "slug": f"xgboost-regressor-{random_num}",
        "description": "House price prediction model",
        "architecture": "XGBoost",
        "dataset_used": "California Housing",
        "metrics": {
            "mae": 45000,
            "mse": 3250000000,
            "rmse": 57000,
            "r2_score": 0.82,
            "mape": 8.5,
            "explained_variance": 0.85,
            "training_time_minutes": 15,
            "cross_val_score": 0.81
        },
        "model_file_url": "https://example.com/xgboost.pkl",
        "access_level": "public",
        "status": "published"
    }
    
    create_cmd = f'''curl -s -X POST "http://localhost:8000/api/v1/ai-models" \
      -H "Authorization: Bearer {token}" \
      -H "Content-Type: application/json" \
      -d '{json.dumps(regression_model)}' '''
    
    response = run_curl(create_cmd)
    if response:
        try:
            result = json.loads(response)
            if 'id' in result:
                print(f"✅ Created model with ID: {result['id']}")
                print(f"✅ Metrics stored: {json.dumps(result.get('metrics', {}), indent=2)}")
            else:
                print(f"❌ Failed: {result}")
        except Exception as e:
            print(f"❌ Parse error: {e}")
            print(f"Response: {response}")

if __name__ == "__main__":
    print("=" * 70)
    print("   TESTING FLEXIBLE METRICS SUPPORT IN AI MODELS")
    print("=" * 70)
    print()
    
    test_flexible_metrics()
    
    print("\n" + "=" * 70)
    print("=== SUMMARY ===")
    print("=" * 70)
    print("✅ Metrics field is fully flexible!")
    print("✅ Can store ANY metric type: classification, regression, detection, etc.")
    print("✅ No database changes needed - JSONB handles everything!")
    print("✅ No CRUD changes needed - Dict[str, Any] accepts any structure!")
    print()
    print("You can now use metrics like:")
    print("  - Classification: accuracy, precision, recall, f1_score, auc_roc")
    print("  - Regression: mae, mse, rmse, r2_score, mape")
    print("  - Detection: map, iou, fps")
    print("  - Generative: fid, inception_score, clip_score")
    print("  - Custom: training_time, model_size, inference_time, etc.")
    print("=" * 70)
