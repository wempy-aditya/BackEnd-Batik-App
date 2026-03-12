# Public API - Quick Reference

## 🚀 Quick Start

All public endpoints: **No authentication required**

Base URL: `/api/v1/public`

---

## 📋 Endpoint Patterns

Every content type has these endpoints:

```
GET /{type}                    # List all (paginated)
GET /{type}/featured           # Featured items
GET /{type}/latest             # Latest items  
GET /{type}/{id}               # Get by UUID
GET /{type}/slug/{slug}        # Get by slug (SEO)
```

---

## 📦 Content Types

| Type | Path | Special Endpoints |
|------|------|-------------------|
| Projects | `/public/projects` | `/category/{id}` |
| Datasets | `/public/datasets` | `/category/{id}` |
| AI Models | `/public/ai-models` | `/framework/{name}` |
| Publications | `/public/publications` | `/year/{year}` |
| News | `/public/news` | - |
| Gallery | `/public/gallery` | `/model/{id}` |
| Categories | `/public/categories` | `/all` |

---

## 🔍 Common Query Parameters

```
?page=1                        # Page number (default: 1)
?items_per_page=10            # Items per page (default: 10)
?search=keyword               # Search in title & description
?limit=6                      # Limit for featured/latest
```

---

## 💡 Quick Examples

### Homepage Featured Section
```javascript
// Get featured content
GET /api/v1/public/projects/featured?limit=6
GET /api/v1/public/ai-models/featured?limit=4
GET /api/v1/public/news/latest?limit=5
GET /api/v1/public/gallery/featured?limit=8
```

### Project Detail Page
```javascript
// SEO-friendly URL
GET /api/v1/public/projects/slug/my-awesome-project
```

### Filter by Category
```javascript
// Get categories first
GET /api/v1/public/categories/projects

// Filter by category
GET /api/v1/public/projects/category/{category_id}
```

### Search
```javascript
GET /api/v1/public/projects?search=machine+learning&page=1
```

### Publications by Year
```javascript
GET /api/v1/public/publications/year/2024
```

### Gallery by AI Model
```javascript
GET /api/v1/public/gallery/model/{model_id}
```

### Get All Categories at Once
```javascript
GET /api/v1/public/categories/all
```

---

## ✅ Auto-filtering

All public endpoints automatically filter:
- ✅ `status = "published"`
- ✅ `access_level = "public"`

---

## 📊 Response Format

### List Response
```json
{
  "data": [...],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

### Single Item Response
```json
{
  "id": "uuid",
  "title": "...",
  "slug": "...",
  ...
}
```

---

## 🎯 Use Cases

| Use Case | Endpoint |
|----------|----------|
| Homepage hero section | `/projects/featured?limit=6` |
| Latest news widget | `/news/latest?limit=5` |
| Project detail page | `/projects/slug/{slug}` |
| Category filter dropdown | `/categories/projects` |
| Search results | `/projects?search=keyword` |
| Publications timeline | `/publications/year/2024` |
| Gallery grid | `/gallery/featured?limit=24` |
| Model showcase | `/ai-models/framework/TensorFlow` |

---

## 🛠️ Testing

```bash
# cURL examples
curl http://localhost:8000/api/v1/public/projects/featured
curl http://localhost:8000/api/v1/public/categories/all
curl "http://localhost:8000/api/v1/public/projects?search=ai"
```

---

## 📝 Notes

- Gallery default limit = 24 (optimal for grid)
- AI Models metrics field is JSONB (flexible)
- All timestamps in ISO 8601 format
- Slug URLs are SEO-friendly
- No rate limiting on public endpoints (currently)

---

## 🔗 Full Documentation

See [PUBLIC_API_DOCS.md](./PUBLIC_API_DOCS.md) for complete details.
