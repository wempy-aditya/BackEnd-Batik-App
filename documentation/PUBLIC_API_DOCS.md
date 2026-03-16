# Public API Documentation

Public endpoints untuk halaman frontend/homepage yang tidak memerlukan autentikasi. Semua endpoint ini hanya menampilkan konten dengan `status="published"` dan `access_level="public"`.

## Base URL

```
/api/v1/public
```

## Endpoint Structure

Semua endpoint public mengikuti pola yang konsisten:

- `GET /` - List semua items dengan pagination
- `GET /featured` - Items yang di-featured (untuk homepage highlights)
- `GET /latest` - Items terbaru (untuk "Latest Updates" section)
- `GET /{id}` - Get item by UUID
- `GET /slug/{slug}` - Get item by slug (SEO-friendly)

---

## 1. Projects

Base: `/api/v1/public/projects`

### Get All Projects
```http
GET /api/v1/public/projects
```

**Authentication (optional):**
- Tanpa token: hanya konten `access_level=public`
- User `registered`: konten `public` + `registered`
- User `premium`: konten `public` + `registered` + `premium`
- User `admin` / `is_superuser=true`: semua level (`public`, `registered`, `premium`)

Gunakan header berikut jika ingin hasil sesuai role user:
```http
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (int, default: 1) - Halaman
- `items_per_page` (int, default: 10, max: 100) - Items per halaman
- `search` (string, optional) - Pencarian di title & description

**Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "title": "Project Title",
      "slug": "project-title",
      "description": "Description",
      "image_url": "https://...",
      "status": "published",
      "access_level": "public",
      "is_featured": false,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10,
  "pages": 5
}
```

### Get Featured Projects
```http
GET /api/v1/public/projects/featured
```

**Query Parameters:**
- `limit` (int, default: 6, max: 20) - Jumlah featured projects

**Use Case:** Homepage "Featured Projects" section

### Get Latest Projects
```http
GET /api/v1/public/projects/latest
```

**Query Parameters:**
- `limit` (int, default: 10, max: 50) - Jumlah latest projects

**Use Case:** Homepage "Latest Projects" section

### Get Project by ID
```http
GET /api/v1/public/projects/{project_id}
```

**Use Case:** Detail page

### Get Project by Slug
```http
GET /api/v1/public/projects/slug/{slug}
```

**Example:** `/api/v1/public/projects/slug/my-awesome-project`

**Use Case:** SEO-friendly URL untuk detail page

### Get Projects by Category
```http
GET /api/v1/public/projects/category/{category_id}
```

**Query Parameters:**
- `page` (int)
- `items_per_page` (int)

**Use Case:** Filter projects by category

---

## 2. Datasets

Base: `/api/v1/public/datasets`

### Access Behavior (Get All Datasets)
- Tanpa token: hanya konten `access_level=public`
- User `registered`: konten `public` + `registered`
- User `premium`: konten `public` + `registered` + `premium`
- User `admin` / `is_superuser=true`: semua level (`public`, `registered`, `premium`)

Untuk mengaktifkan hasil berbasis role, kirim header berikut:
```http
Authorization: Bearer <access_token>
```

### Endpoints
- `GET /api/v1/public/datasets` - All datasets
- `GET /api/v1/public/datasets/featured` - Featured datasets
- `GET /api/v1/public/datasets/latest` - Latest datasets
- `GET /api/v1/public/datasets/{id}` - Get by ID
- `GET /api/v1/public/datasets/slug/{slug}` - Get by slug

**Same structure as Projects**

---

## 3. AI Models

Base: `/api/v1/public/ai-models`

### Access Behavior (Get All AI Models)
- Tanpa token: hanya konten `access_level=public`
- User `registered`: konten `public` + `registered`
- User `premium`: konten `public` + `registered` + `premium`
- User `admin` / `is_superuser=true`: semua level (`public`, `registered`, `premium`)

Untuk mengaktifkan hasil berbasis role, kirim header berikut:
```http
Authorization: Bearer <access_token>
```

### Endpoints
- `GET /api/v1/public/ai-models` - All AI models
- `GET /api/v1/public/ai-models/featured` - Featured models
- `GET /api/v1/public/ai-models/latest` - Latest models
- `GET /api/v1/public/ai-models/{id}` - Get by ID
- `GET /api/v1/public/ai-models/slug/{slug}` - Get by slug

### Get Models by Framework
```http
GET /api/v1/public/ai-models/framework/{framework}
```

**Example:** `/api/v1/public/ai-models/framework/TensorFlow`

**Query Parameters:**
- `page` (int)
- `items_per_page` (int)

**Use Case:** Filter AI models by framework (TensorFlow, PyTorch, etc.)

### Response Example
```json
{
  "id": "uuid",
  "name": "Model Name",
  "slug": "model-name",
  "description": "Description",
  "framework": "TensorFlow",
  "model_type": "Classification",
  "version": "1.0.0",
  "metrics": {
    "accuracy": 0.95,
    "loss": 0.05,
    "f1_score": 0.93,
    "custom_metric": 0.88
  },
  "image_url": "https://...",
  "is_featured": true
}
```

**Note:** Field `metrics` adalah JSONB yang fleksibel, bisa menyimpan metric apa saja.

---

## 4. Publications

Base: `/api/v1/public/publications`

### Access Behavior (Get All Publications)
- Tanpa token: hanya konten `access_level=public`
- User `registered`: konten `public` + `registered`
- User `premium`: konten `public` + `registered` + `premium`
- User `admin` / `is_superuser=true`: semua level (`public`, `registered`, `premium`)

Untuk mengaktifkan hasil berbasis role, kirim header berikut:
```http
Authorization: Bearer <access_token>
```

### Endpoints
- `GET /api/v1/public/publications` - All publications
- `GET /api/v1/public/publications/featured` - Featured publications
- `GET /api/v1/public/publications/latest` - Latest publications
- `GET /api/v1/public/publications/{id}` - Get by ID
- `GET /api/v1/public/publications/slug/{slug}` - Get by slug

### Get Publications by Year
```http
GET /api/v1/public/publications/year/{year}
```

**Example:** `/api/v1/public/publications/year/2024`

**Query Parameters:**
- `page` (int)
- `items_per_page` (int)

**Use Case:** Filter publications by publication year

### Response Example
```json
{
  "id": "uuid",
  "title": "Publication Title",
  "slug": "publication-title",
  "authors": "John Doe, Jane Smith",
  "abstract": "Abstract...",
  "publication_year": 2024,
  "journal": "Journal Name",
  "doi": "10.1234/example",
  "pdf_url": "https://...",
  "is_featured": false
}
```

---

## 5. News

Base: `/api/v1/public/news`

### Access Behavior (Get All News)
- Tanpa token: hanya konten `access_level=public`
- User `registered`: konten `public` + `registered`
- User `premium`: konten `public` + `registered` + `premium`
- User `admin` / `is_superuser=true`: semua level (`public`, `registered`, `premium`)

Untuk mengaktifkan hasil berbasis role, kirim header berikut:
```http
Authorization: Bearer <access_token>
```

### Endpoints
- `GET /api/v1/public/news` - All news
- `GET /api/v1/public/news/featured` - Featured news
- `GET /api/v1/public/news/latest` - Latest news (default: 10)
- `GET /api/v1/public/news/{id}` - Get by ID
- `GET /api/v1/public/news/slug/{slug}` - Get by slug

**Same structure as Projects**

**Use Case:** News section di homepage, blog posts

---

## 6. Gallery

Base: `/api/v1/public/gallery`

### Endpoints
- `GET /api/v1/public/gallery` - All gallery items (limit default: 24)
- `GET /api/v1/public/gallery/featured` - Featured gallery items
- `GET /api/v1/public/gallery/latest` - Latest gallery items
- `GET /api/v1/public/gallery/{id}` - Get by ID
- `GET /api/v1/public/gallery/slug/{slug}` - Get by slug

### Get Gallery by AI Model
```http
GET /api/v1/public/gallery/model/{model_id}
```

**Query Parameters:**
- `page` (int)
- `items_per_page` (int, max: 100)

**Use Case:** Tampilkan semua gallery items yang menggunakan AI model tertentu

### Response Example
```json
{
  "id": "uuid",
  "title": "Gallery Title",
  "slug": "gallery-title",
  "description": "Description",
  "image_url": "https://...",
  "thumbnail_url": "https://...",
  "ai_model_id": "uuid",
  "ai_model": {
    "id": "uuid",
    "name": "Model Name"
  },
  "is_featured": true
}
```

**Note:** Gallery default limit = 24 (optimal untuk grid display)

---

## 7. Categories

Base: `/api/v1/public/categories`

### Get Project Categories
```http
GET /api/v1/public/categories/projects
```

### Get Dataset Categories
```http
GET /api/v1/public/categories/datasets
```

### Get Publication Categories
```http
GET /api/v1/public/categories/publications
```

### Get News Categories
```http
GET /api/v1/public/categories/news
```

### Get AI Model Categories
```http
GET /api/v1/public/categories/models
```

### Get Gallery Categories
```http
GET /api/v1/public/categories/gallery
```

### Get All Categories (Grouped)
```http
GET /api/v1/public/categories/all
```

**Response:**
```json
{
  "projects": [...],
  "datasets": [...],
  "publications": [...],
  "news": [...],
  "models": [...],
  "gallery": [...]
}
```

**Use Case:** Inisialisasi filter categories di frontend dalam satu call

---

## Frontend Implementation Examples

### 1. Homepage Featured Section

```javascript
// Fetch featured content for homepage
const fetchHomepageData = async () => {
  const [projects, models, news, gallery] = await Promise.all([
    fetch('/api/v1/public/projects/featured?limit=6'),
    fetch('/api/v1/public/ai-models/featured?limit=4'),
    fetch('/api/v1/public/news/latest?limit=5'),
    fetch('/api/v1/public/gallery/featured?limit=8')
  ]);
  
  return {
    featuredProjects: await projects.json(),
    featuredModels: await models.json(),
    latestNews: await news.json(),
    featuredGallery: await gallery.json()
  };
};
```

### 2. Project Detail Page (SEO-friendly)

```javascript
// Use slug for SEO-friendly URLs
const getProjectDetail = async (slug) => {
  const response = await fetch(`/api/v1/public/projects/slug/${slug}`);
  return await response.json();
};

// URL: /projects/my-awesome-project
```

### 3. Category Filter

```javascript
// Get all categories first
const categories = await fetch('/api/v1/public/categories/projects');

// Then filter by category
const filterByCategory = async (categoryId, page = 1) => {
  const response = await fetch(
    `/api/v1/public/projects/category/${categoryId}?page=${page}&items_per_page=12`
  );
  return await response.json();
};
```

### 4. Search with Pagination

```javascript
const searchProjects = async (query, page = 1) => {
  const response = await fetch(
    `/api/v1/public/projects?search=${query}&page=${page}&items_per_page=10`
  );
  return await response.json();
};
```

### 5. Publications by Year

```javascript
const getPublicationsByYear = async (year) => {
  const response = await fetch(`/api/v1/public/publications/year/${year}`);
  return await response.json();
};
```

### 6. Gallery by AI Model

```javascript
// Show all gallery items using specific AI model
const getModelGallery = async (modelId) => {
  const response = await fetch(`/api/v1/public/gallery/model/${modelId}`);
  return await response.json();
};
```

---

## Key Features

### ✅ No Authentication Required
Semua endpoint public bisa diakses tanpa token atau login

### ✅ Auto-filtering
- Hanya menampilkan `status="published"`
- Hanya menampilkan `access_level="public"`

### ✅ SEO-friendly
- Slug-based URLs untuk detail pages
- Clean URL structure

### ✅ Pagination
- Standard pagination di semua list endpoints
- Customizable `page` dan `items_per_page`

### ✅ Search
- Search di title & description
- Case-insensitive

### ✅ Featured & Latest
- Featured items untuk homepage highlights
- Latest items untuk "What's New" sections

### ✅ Category Filtering
- Filter by category untuk semua content types
- Get all categories in one call

### ✅ Specialized Filters
- **AI Models:** Filter by framework
- **Publications:** Filter by year
- **Gallery:** Filter by AI model

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Project not found or not available"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["query", "page"],
      "msg": "ensure this value is greater than or equal to 1",
      "type": "value_error"
    }
  ]
}
```

---

## API Versioning

Current version: `v1`

Base URL akan selalu: `/api/v1/public/...`

---

## Rate Limiting

Public endpoints mungkin memiliki rate limiting. Cek response headers:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

---

## CORS

Public endpoints support CORS untuk akses dari domain frontend yang berbeda.

---

## Testing

Gunakan curl atau Postman untuk testing:

```bash
# Test featured projects
curl http://localhost:8000/api/v1/public/projects/featured

# Test project detail by slug
curl http://localhost:8000/api/v1/public/projects/slug/my-project

# Test search
curl "http://localhost:8000/api/v1/public/projects?search=machine+learning"

# Test categories
curl http://localhost:8000/api/v1/public/categories/all
```

---

## Summary

| Content Type | Base Path | Special Filters |
|--------------|-----------|-----------------|
| Projects | `/public/projects` | category |
| Datasets | `/public/datasets` | category |
| AI Models | `/public/ai-models` | framework, category |
| Publications | `/public/publications` | year, category |
| News | `/public/news` | category |
| Gallery | `/public/gallery` | ai_model, category |
| Categories | `/public/categories` | by type, all |

**Total Endpoints:** 40+ public endpoints untuk frontend

**Authentication:** None required ✅

**Data Visibility:** Published + Public only ✅