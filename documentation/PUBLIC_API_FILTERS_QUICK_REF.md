# Public API Filters - Quick Reference

## 🎯 All Endpoints Support

✅ **Pagination** - `offset` & `limit`  
✅ **Search** - Case-insensitive partial matching  
✅ **Category Filter** - `category_id` (UUID)  
✅ **Featured Filter** - `is_featured` (boolean)  
✅ **Sorting** - `sort_by` (varies by endpoint)

---

## 📊 Filter Cheat Sheet

### Projects
```
GET /api/v1/public/projects/
  ?search=<text>           # Search in title & description
  &category_id=<uuid>      # Filter by category
  &is_featured=<bool>      # Featured only
  &sort_by=latest|oldest|title
  &offset=0&limit=12
```

### Datasets
```
GET /api/v1/public/datasets/
  ?search=<text>           # Search in name & description
  &format=<text>           # CSV, JSON, Parquet, etc
  &license=<text>          # MIT, Apache, GPL, etc
  &version=<text>          # Dataset version
  &category_id=<uuid>      # Filter by category
  &is_featured=<bool>      # Featured only
  &sort_by=latest|oldest|name|downloads
  &offset=0&limit=12
```

### Publications
```
GET /api/v1/public/publications/
  ?search=<text>           # Search in title, authors, abstract
  &year=<int>              # Publication year (1900-2100)
  &author=<text>           # Filter by author name
  &category_id=<uuid>      # Filter by category
  &is_featured=<bool>      # Featured only
  &sort_by=latest|oldest|title|year|views
  &offset=0&limit=12
```

### AI Models
```
GET /api/v1/public/ai-models/
  ?search=<text>           # Search in name & description
  &architecture=<text>     # CNN, RNN, Transformer, etc
  &dataset_used=<text>     # ImageNet, COCO, etc
  &category_id=<uuid>      # Filter by category
  &is_featured=<bool>      # Featured only
  &sort_by=latest|oldest|name
  &offset=0&limit=12
```

### News
```
GET /api/v1/public/news/
  ?search=<text>           # Search in title & content
  &category_id=<uuid>      # Filter by category
  &is_featured=<bool>      # Featured only
  &sort_by=latest|oldest|title
  &offset=0&limit=12
```

### Gallery
```
GET /api/v1/public/gallery/
  ?search=<text>           # Search in prompt
  &ai_model_id=<uuid>      # Filter by AI model
  &category_id=<uuid>      # Filter by category
  &sort_by=latest|oldest
  &offset=0&limit=24       # Default 24 for grid
```

---

## 🚀 Common Usage Patterns

### Simple Search
```bash
curl "http://localhost:8000/api/v1/public/projects/?search=machine+learning"
```

### Pagination
```bash
# Page 1
curl "http://localhost:8000/api/v1/public/datasets/?offset=0&limit=12"

# Page 2
curl "http://localhost:8000/api/v1/public/datasets/?offset=12&limit=12"

# Page 3
curl "http://localhost:8000/api/v1/public/datasets/?offset=24&limit=12"
```

### Multiple Filters
```bash
curl "http://localhost:8000/api/v1/public/datasets/?format=JSON&license=MIT&is_featured=true&limit=10"
```

### Category Filter
```bash
# Get category ID first
curl "http://localhost:8000/api/v1/public/categories/projects" | jq '.[0].id'

# Then filter
curl "http://localhost:8000/api/v1/public/projects/?category_id=<uuid>&limit=20"
```

### Sorting
```bash
# Latest first (default)
curl "http://localhost:8000/api/v1/public/projects/?sort_by=latest"

# Most downloaded datasets
curl "http://localhost:8000/api/v1/public/datasets/?sort_by=downloads"

# Most viewed publications
curl "http://localhost:8000/api/v1/public/publications/?sort_by=views"
```

---

## 💡 JavaScript Examples

### React/Vue/Angular
```javascript
// Build query dynamically
const params = new URLSearchParams({
  search: 'machine learning',
  category_id: '019ae4b2-d4c7-7a18-890d-80db7143746a',
  is_featured: 'true',
  sort_by: 'latest',
  offset: '0',
  limit: '12'
});

const response = await fetch(`/api/v1/public/projects/?${params}`);
const data = await response.json();

console.log(`Found ${data.total} projects`);
console.log(`Showing ${data.data.length} items`);
console.log(`Has more: ${data.has_more}`);
```

### Pagination Helper
```javascript
function getPaginationParams(page, itemsPerPage = 12) {
  return {
    offset: (page - 1) * itemsPerPage,
    limit: itemsPerPage
  };
}

// Get page 3 with 20 items per page
const { offset, limit } = getPaginationParams(3, 20);
// offset = 40, limit = 20
```

---

## 📝 Response Format

All endpoints return:
```json
{
  "data": [...],        // Array of items
  "total": 150,        // Total items matching filters
  "offset": 0,         // Current offset
  "limit": 12,         // Items per page
  "has_more": true     // More items available
}
```

---

## ⚡ Performance Tips

1. **Use appropriate limits**
   - List view: `limit=10-12`
   - Grid view: `limit=24-48`
   - Don't use `limit=100` unless necessary

2. **Combine filters in one request**
   ```bash
   # ✅ Good - one request
   ?format=JSON&license=MIT&is_featured=true
   
   # ❌ Bad - three requests
   ?format=JSON
   ?license=MIT
   ?is_featured=true
   ```

3. **URL encode search queries**
   ```javascript
   const query = encodeURIComponent("machine learning & AI");
   ```

4. **Cache category IDs**
   - Fetch categories once, store in state/localStorage
   - Reuse for filtering

---

## 🔍 Search Behavior

- **Case-insensitive**: `search=AI` matches "ai", "AI", "Ai"
- **Partial match**: `search=learn` matches "learning", "learner", "learned"
- **Multiple words**: Use `+` or `%20` for spaces
  - `?search=machine+learning`
  - `?search=machine%20learning`

---

## 📚 Full Documentation

See `PUBLIC_API_FILTERS_GUIDE.md` for:
- Detailed filter descriptions
- More examples
- Error handling
- Testing strategies
- Frontend implementation patterns

---

**Updated:** December 2025  
**Version:** 1.0  
**All filters tested and working** ✅
