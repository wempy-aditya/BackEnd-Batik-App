# Quick Reference: AI Model Metrics

## TL;DR
✅ **Metrics field is 100% flexible - use ANY metric you want!**

## Common Patterns

### Image Classification
```json
{
  "accuracy": 0.95,
  "precision": 0.93,
  "recall": 0.94,
  "f1_score": 0.92
}
```

### Object Detection
```json
{
  "map": 0.78,
  "map_50": 0.85,
  "iou": 0.82
}
```

### Image Generation
```json
{
  "fid": 12.5,
  "inception_score": 8.3
}
```

### Regression
```json
{
  "mae": 0.15,
  "mse": 0.023,
  "r2_score": 0.89
}
```

### With Performance Metrics
```json
{
  "accuracy": 0.95,
  "training_time_hours": 2.5,
  "inference_time_ms": 45,
  "model_size_mb": 250
}
```

## See METRICS_FLEXIBILITY_GUIDE.md for complete documentation
