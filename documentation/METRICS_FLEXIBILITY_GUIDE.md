# AI Model Metrics - Flexible Structure Guide

## 📊 Overview

Field `metrics` di AI Model menggunakan **JSONB** di PostgreSQL dan **Dict[str, Any]** di Pydantic, sehingga **100% fleksibel** untuk menampung metric jenis apapun.

## ✅ Supported Metric Types

### 1. Classification Metrics
```json
{
  "accuracy": 0.95,
  "precision": 0.93,
  "recall": 0.94,
  "f1_score": 0.92,
  "loss": 0.05,
  "auc_roc": 0.96,
  "log_loss": 0.15,
  "confusion_matrix": [[50, 2], [1, 47]]
}
```

### 2. Regression Metrics
```json
{
  "mae": 0.15,
  "mse": 0.023,
  "rmse": 0.152,
  "r2_score": 0.89,
  "mape": 5.2,
  "explained_variance": 0.91
}
```

### 3. Object Detection Metrics
```json
{
  "map": 0.78,
  "map_50": 0.85,
  "map_75": 0.72,
  "iou": 0.85,
  "precision": 0.82,
  "recall": 0.79
}
```

### 4. Segmentation Metrics
```json
{
  "dice_coefficient": 0.88,
  "iou": 0.82,
  "pixel_accuracy": 0.94,
  "mean_iou": 0.76
}
```

### 5. Generative Model Metrics
```json
{
  "fid": 12.5,
  "inception_score": 8.3,
  "lpips": 0.15,
  "ssim": 0.92,
  "psnr": 28.5
}
```

### 6. NLP Metrics
```json
{
  "bleu": 0.45,
  "rouge_1": 0.52,
  "rouge_2": 0.38,
  "rouge_l": 0.48,
  "perplexity": 15.2,
  "meteor": 0.42
}
```

### 7. Custom / Performance Metrics
```json
{
  "training_time": "2.5 hours",
  "training_time_seconds": 9000,
  "inference_time_ms": 45,
  "model_size_mb": 250,
  "parameters_count": 25000000,
  "flops": 4000000000,
  "gpu_memory_mb": 8192
}
```

### 8. Multi-Class Metrics
```json
{
  "accuracy": 0.92,
  "macro_precision": 0.89,
  "macro_recall": 0.87,
  "macro_f1": 0.88,
  "weighted_f1": 0.91,
  "per_class_accuracy": {
    "class_0": 0.95,
    "class_1": 0.89,
    "class_2": 0.92
  }
}
```

## 🚀 Usage Examples

### Create Model with Classification Metrics
```bash
curl -X POST "http://localhost:8000/api/v1/ai-models" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "BERT Text Classifier",
    "slug": "bert-text-classifier",
    "description": "BERT model for sentiment analysis",
    "architecture": "BERT",
    "dataset_used": "IMDB Reviews",
    "metrics": {
      "accuracy": 0.94,
      "precision": 0.93,
      "recall": 0.95,
      "f1_score": 0.94,
      "auc_roc": 0.97,
      "training_time": "3 hours",
      "inference_time_ms": 120
    },
    "model_file_url": "https://example.com/bert-classifier.pt",
    "access_level": "public",
    "status": "published"
  }'
```

### Create Model with Generative Metrics
```bash
curl -X POST "http://localhost:8000/api/v1/ai-models" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Stable Diffusion v2",
    "slug": "stable-diffusion-v2",
    "description": "Text-to-image diffusion model",
    "architecture": "Latent Diffusion",
    "dataset_used": "LAION-5B",
    "metrics": {
      "fid": 8.2,
      "inception_score": 9.1,
      "clip_score": 0.32,
      "lpips": 0.12,
      "inference_steps": 50,
      "inference_time_seconds": 4.5,
      "model_size_gb": 2.1
    },
    "model_file_url": "https://example.com/sd-v2.ckpt",
    "access_level": "public",
    "status": "published"
  }'
```

### Create Model with Object Detection Metrics
```bash
curl -X POST "http://localhost:8000/api/v1/ai-models" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "YOLOv8 Large",
    "slug": "yolov8-large",
    "description": "Real-time object detection model",
    "architecture": "YOLOv8",
    "dataset_used": "COCO",
    "metrics": {
      "map": 0.528,
      "map_50": 0.697,
      "map_75": 0.571,
      "precision": 0.682,
      "recall": 0.581,
      "fps": 45,
      "inference_time_ms": 22,
      "model_size_mb": 165
    },
    "model_file_url": "https://example.com/yolov8l.pt",
    "access_level": "public",
    "status": "published"
  }'
```

### Create Model with Regression Metrics
```bash
curl -X POST "http://localhost:8000/api/v1/ai-models" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "House Price Predictor",
    "slug": "house-price-predictor",
    "description": "XGBoost model for house price prediction",
    "architecture": "XGBoost",
    "dataset_used": "California Housing",
    "metrics": {
      "mae": 45000,
      "mse": 3250000000,
      "rmse": 57000,
      "r2_score": 0.82,
      "mape": 8.5,
      "training_time_minutes": 15
    },
    "model_file_url": "https://example.com/house-price.pkl",
    "access_level": "public",
    "status": "published"
  }'
```

## 💡 Best Practices

### 1. **Use Consistent Key Names**
```json
// ✅ Good - lowercase with underscores
{
  "f1_score": 0.92,
  "training_time": "2h"
}

// ❌ Avoid - inconsistent naming
{
  "F1Score": 0.92,
  "TrainingTime": "2h"
}
```

### 2. **Include Units in Key Names**
```json
// ✅ Good - clear what unit is used
{
  "training_time_hours": 2.5,
  "inference_time_ms": 45,
  "model_size_mb": 250
}

// ⚠️ OK but less clear
{
  "training_time": "2.5 hours",
  "inference_time": "45ms"
}
```

### 3. **Group Related Metrics**
```json
{
  // Main metrics
  "accuracy": 0.95,
  "f1_score": 0.92,
  
  // Performance metrics
  "training_time_seconds": 9000,
  "inference_time_ms": 45,
  "model_size_mb": 250,
  
  // Per-class metrics
  "per_class_f1": {
    "cat": 0.94,
    "dog": 0.91,
    "bird": 0.89
  }
}
```

### 4. **Store Both Numeric and Readable Values**
```json
{
  "training_time_seconds": 9000,
  "training_time_readable": "2.5 hours",
  "model_size_bytes": 262144000,
  "model_size_readable": "250 MB"
}
```

## 🔍 Query Examples

### Filter by Specific Metric
```python
# Get models with accuracy > 0.9
models = await crud_ai_model.get_multi(
    db=db,
    # Use JSONB queries for PostgreSQL
    # This would require custom filter in CRUD
)
```

### Sort by Metric Value
```python
# Sort by FID score (lower is better for generative models)
# Would require custom implementation
```

## 📝 Database Structure

```sql
-- The metrics column in the models table
ALTER TABLE models
ADD COLUMN metrics JSONB DEFAULT NULL;

-- Create index for faster JSONB queries (optional)
CREATE INDEX idx_models_metrics ON models USING GIN (metrics);

-- Query examples in SQL
SELECT * FROM models 
WHERE metrics->>'accuracy' > '0.9';

SELECT * FROM models 
WHERE metrics ? 'fid';  -- Check if 'fid' key exists
```

## ✅ Summary

- ✅ **100% Flexible**: Dapat menerima metric apapun
- ✅ **No Schema Changes Needed**: Database sudah menggunakan JSONB
- ✅ **No CRUD Changes Needed**: CRUD sudah support Dict[str, Any]
- ✅ **Type Safe**: Pydantic validation tetap berjalan
- ✅ **Queryable**: Bisa di-query dengan PostgreSQL JSONB operators

**Kesimpulan**: Sistem sudah sepenuhnya fleksibel! Anda bisa langsung menggunakan metric apapun tanpa perubahan code atau migration. 🎉
