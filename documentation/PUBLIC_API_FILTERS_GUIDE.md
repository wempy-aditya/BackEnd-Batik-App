# Public API Filters & Search Guide

Panduan lengkap untuk menggunakan fitur **Filter** dan **Search** di semua Public API endpoints.

## 📋 Table of Contents

1. [Projects Filters](#1-projects-filters)
2. [Datasets Filters](#2-datasets-filters)
3. [Publications Filters](#3-publications-filters)
4. [AI Models Filters](#4-ai-models-filters)
5. [News Filters](#5-news-filters)
6. [Gallery Filters](#6-gallery-filters)
7. [Common Filters](#common-filters)
8. [Usage Examples](#usage-examples)

---

## 1. Projects Filters

**Endpoint:** `GET /api/v1/public/projects/`

### Available Filters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search in title and description | `?search=machine learning` |
| `category_id` | UUID | Filter by category UUID | `?category_id=019ae...` |
| `is_featured` | boolean | Show only featured projects | `?is_featured=true` |
| `sort_by` | string | Sort order: `latest`, `oldest`, `title` | `?sort_by=latest` |
| `offset` | integer | Pagination offset (default: 0) | `?offset=0` |
| `limit` | integer | Items per page (1-100, default: 12) | `?limit=20` |

### Sort Options

- `latest` - Newest first (default)
- `oldest` - Oldest first
- `title` - Alphabetical A-Z

### Examples

```bash
# Search projects
GET /api/v1/public/projects/?search=computer+vision

# Filter by category
GET /api/v1/public/projects/?category_id=019ae4b2-d4c7-7a18-890d-80db7143746a

# Get featured projects
GET /api/v1/public/projects/?is_featured=true

# Combine filters
GET /api/v1/public/projects/?search=AI&is_featured=true&sort_by=latest&limit=10

# Pagination
GET /api/v1/public/projects/?offset=20&limit=10  # Page 3
```

---

## 2. Datasets Filters

**Endpoint:** `GET /api/v1/public/datasets/`

### Available Filters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search in name and description | `?search=CIFAR` |
| `format` | string | Filter by format | `?format=CSV` |
| `license` | string | Filter by license | `?license=MIT` |
| `version` | string | Filter by version | `?version=2.0` |
| `category_id` | UUID | Filter by category UUID | `?category_id=019ae...` |
| `is_featured` | boolean | Show only featured datasets | `?is_featured=true` |
| `sort_by` | string | Sort order | `?sort_by=downloads` |
| `offset` | integer | Pagination offset | `?offset=0` |
| `limit` | integer | Items per page (1-100, default: 12) | `?limit=24` |

### Format Options

Common values: `CSV`, `JSON`, `Parquet`, `HDF5`, `TFRecord`, `Arrow`, `Avro`, `XML`

### License Options

Common values: `MIT`, `Apache-2.0`, `GPL-3.0`, `BSD`, `CC-BY-4.0`, `Public Domain`

### Sort Options

- `latest` - Newest first (default)
- `oldest` - Oldest first
- `name` - Alphabetical A-Z
- `downloads` - Most downloaded first

### Examples

```bash
# Search datasets
GET /api/v1/public/datasets/?search=image+classification

# Filter by format
GET /api/v1/public/datasets/?format=JSON

# Filter by license
GET /api/v1/public/datasets/?license=MIT

# Filter by version
GET /api/v1/public/datasets/?version=1.0

# Combine filters
GET /api/v1/public/datasets/?format=CSV&license=MIT&is_featured=true

# Sort by downloads
GET /api/v1/public/datasets/?sort_by=downloads&limit=20

# Filter by category
GET /api/v1/public/datasets/?category_id=019ae4b2-d4c7-7a18-890d-80db7143746a
```

---

## 3. Publications Filters

**Endpoint:** `GET /api/v1/public/publications/`

### Available Filters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search in title, authors, abstract | `?search=deep+learning` |
| `year` | integer | Filter by publication year (1900-2100) | `?year=2024` |
| `category_id` | UUID | Filter by category UUID | `?category_id=019ae...` |
| `author` | string | Filter by author name (partial) | `?author=Smith` |
| `is_featured` | boolean | Show only featured publications | `?is_featured=true` |
| `sort_by` | string | Sort order | `?sort_by=year` |
| `offset` | integer | Pagination offset | `?offset=0` |
| `limit` | integer | Items per page (1-100, default: 12) | `?limit=15` |

### Sort Options

- `latest` - Newest created first (default)
- `oldest` - Oldest created first
- `title` - Alphabetical A-Z
- `year` - Publication year (newest first)
- `views` - Most viewed first

### Examples

```bash
# Search publications
GET /api/v1/public/publications/?search=neural+networks

# Filter by year
GET /api/v1/public/publications/?year=2024

# Filter by author
GET /api/v1/public/publications/?author=John+Doe

# Combine filters
GET /api/v1/public/publications/?year=2024&author=Smith&is_featured=true

# Sort by views
GET /api/v1/public/publications/?sort_by=views&limit=10

# Filter by category
GET /api/v1/public/publications/?category_id=019ae4b2-d4c7-7a18-890d-80db7143746a
```

---

## 4. AI Models Filters

**Endpoint:** `GET /api/v1/public/ai-models/`

### Available Filters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search in name and description | `?search=ResNet` |
| `architecture` | string | Filter by architecture | `?architecture=CNN` |
| `dataset_used` | string | Filter by dataset used | `?dataset_used=ImageNet` |
| `category_id` | UUID | Filter by category UUID | `?category_id=019ae...` |
| `is_featured` | boolean | Show only featured models | `?is_featured=true` |
| `sort_by` | string | Sort order | `?sort_by=latest` |
| `offset` | integer | Pagination offset | `?offset=0` |
| `limit` | integer | Items per page (1-100, default: 12) | `?limit=20` |

### Architecture Options

Common values: `CNN`, `RNN`, `Transformer`, `ResNet`, `YOLO`, `U-Net`, `GAN`, `VAE`, `BERT`, `GPT`, `VGG`, `MobileNet`

### Dataset Used Options

Common values: `ImageNet`, `COCO`, `CIFAR-10`, `MNIST`, `Pascal VOC`, `Custom Dataset`

### Sort Options

- `latest` - Newest first (default)
- `oldest` - Oldest first
- `name` - Alphabetical A-Z

### Examples

```bash
# Search models
GET /api/v1/public/ai-models/?search=image+classification

# Filter by architecture
GET /api/v1/public/ai-models/?architecture=CNN

# Filter by dataset used
GET /api/v1/public/ai-models/?dataset_used=ImageNet

# Combine filters
GET /api/v1/public/ai-models/?architecture=Transformer&dataset_used=COCO

# Filter by category
GET /api/v1/public/ai-models/?category_id=019ae4b2-d4c7-7a18-890d-80db7143746a

# Featured CNN models
GET /api/v1/public/ai-models/?architecture=CNN&is_featured=true
```

---

## 5. News Filters

**Endpoint:** `GET /api/v1/public/news/`

### Available Filters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search in title and content | `?search=breakthrough` |
| `category_id` | UUID | Filter by category UUID | `?category_id=019ae...` |
| `is_featured` | boolean | Show only featured news | `?is_featured=true` |
| `sort_by` | string | Sort order | `?sort_by=latest` |
| `offset` | integer | Pagination offset | `?offset=0` |
| `limit` | integer | Items per page (1-100, default: 12) | `?limit=10` |

### Sort Options

- `latest` - Newest first (default)
- `oldest` - Oldest first
- `title` - Alphabetical A-Z

### Examples

```bash
# Search news
GET /api/v1/public/news/?search=AI+research

# Filter by category
GET /api/v1/public/news/?category_id=019ae4b2-d4c7-7a18-890d-80db7143746a

# Get featured news
GET /api/v1/public/news/?is_featured=true

# Latest 5 news
GET /api/v1/public/news/?sort_by=latest&limit=5

# Combine filters
GET /api/v1/public/news/?search=machine+learning&is_featured=true&limit=10
```

---

## 6. Gallery Filters

**Endpoint:** `GET /api/v1/public/gallery/`

### Available Filters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Search in prompt text | `?search=sunset` |
| `ai_model_id` | UUID | Filter by AI model UUID | `?ai_model_id=019ae...` |
| `category_id` | UUID | Filter by category UUID | `?category_id=019ae...` |
| `sort_by` | string | Sort order | `?sort_by=latest` |
| `offset` | integer | Pagination offset | `?offset=0` |
| `limit` | integer | Items per page (1-100, default: 24) | `?limit=48` |

### Sort Options

- `latest` - Newest first (default)
- `oldest` - Oldest first

### Examples

```bash
# Search gallery
GET /api/v1/public/gallery/?search=landscape

# Filter by AI model
GET /api/v1/public/gallery/?ai_model_id=019ae4b2-d4c7-7a18-890d-80db7143746a

# Filter by category
GET /api/v1/public/gallery/?category_id=019ae4b2-d4c7-7a18-890d-80db7143746a

# Combine filters
GET /api/v1/public/gallery/?ai_model_id=019ae...&search=portrait&limit=24

# Grid display (6x4)
GET /api/v1/public/gallery/?limit=24
```

---

## Common Filters

### Pagination

Semua endpoint mendukung pagination dengan 2 parameter:

```bash
# Page 1 (first 12 items)
GET /endpoint/?offset=0&limit=12

# Page 2 (items 13-24)
GET /endpoint/?offset=12&limit=12

# Page 3 (items 25-36)
GET /endpoint/?offset=24&limit=12

# Custom page size
GET /endpoint/?offset=0&limit=20
```

**Formula:** `offset = (page - 1) * limit`

### Search

Search menggunakan **case-insensitive** partial matching:

```bash
# Finds: "Machine Learning", "machine learning basics", "Deep Machine Learning"
GET /endpoint/?search=machine+learning

# URL encoding for spaces
GET /endpoint/?search=computer%20vision
```

### Boolean Filters

```bash
# Show only featured items
GET /endpoint/?is_featured=true

# Show non-featured items
GET /endpoint/?is_featured=false
```

### Category Filters

Semua content types mendukung filter by category:

```bash
# Get category ID first
GET /api/v1/public/categories/projects

# Then filter
GET /api/v1/public/projects/?category_id=019ae4b2-d4c7-7a18-890d-80db7143746a
```

---

## Usage Examples

### 1. Frontend Search Bar

```javascript
// Real-time search in projects
const searchProjects = async (query) => {
  const response = await fetch(
    `/api/v1/public/projects/?search=${encodeURIComponent(query)}&limit=10`
  );
  return await response.json();
};

// Usage
const results = await searchProjects("machine learning");
```

### 2. Category Filter Dropdown

```javascript
// Get categories first
const categories = await fetch('/api/v1/public/categories/datasets');
const categoryData = await categories.json();

// Filter by selected category
const filterByCategory = async (categoryId) => {
  const response = await fetch(
    `/api/v1/public/datasets/?category_id=${categoryId}&limit=20`
  );
  return await response.json();
};
```

### 3. Advanced Multi-Filter Form

```javascript
// Build query from form inputs
const filterDatasets = async (filters) => {
  const params = new URLSearchParams();
  
  if (filters.search) params.append('search', filters.search);
  if (filters.format) params.append('format', filters.format);
  if (filters.license) params.append('license', filters.license);
  if (filters.categoryId) params.append('category_id', filters.categoryId);
  if (filters.isFeatured !== null) params.append('is_featured', filters.isFeatured);
  
  params.append('sort_by', filters.sortBy || 'latest');
  params.append('offset', filters.offset || 0);
  params.append('limit', filters.limit || 12);
  
  const response = await fetch(`/api/v1/public/datasets/?${params}`);
  return await response.json();
};

// Usage
const results = await filterDatasets({
  search: 'image classification',
  format: 'JSON',
  license: 'MIT',
  isFeatured: true,
  sortBy: 'downloads',
  limit: 20
});
```

### 4. Pagination Component

```javascript
const PaginationExample = async (page = 1, itemsPerPage = 12) => {
  const offset = (page - 1) * itemsPerPage;
  
  const response = await fetch(
    `/api/v1/public/projects/?offset=${offset}&limit=${itemsPerPage}`
  );
  const data = await response.json();
  
  return {
    items: data.data,
    total: data.total,
    currentPage: page,
    totalPages: Math.ceil(data.total / itemsPerPage),
    hasMore: data.has_more
  };
};
```

### 5. Sort Dropdown

```javascript
const sortProjects = async (sortBy) => {
  const response = await fetch(
    `/api/v1/public/projects/?sort_by=${sortBy}&limit=20`
  );
  return await response.json();
};

// Usage
await sortProjects('latest');  // Newest first
await sortProjects('oldest');  // Oldest first
await sortProjects('title');   // A-Z
```

### 6. Filter Gallery by AI Model

```javascript
// Show all images generated by specific model
const getModelGallery = async (modelId) => {
  const response = await fetch(
    `/api/v1/public/gallery/?ai_model_id=${modelId}&limit=24`
  );
  return await response.json();
};
```

### 7. Publications by Year

```javascript
// Filter publications by year
const getPublicationsByYear = async (year) => {
  const response = await fetch(
    `/api/v1/public/publications/?year=${year}&sort_by=year`
  );
  return await response.json();
};

// Get 2024 publications
const pubs2024 = await getPublicationsByYear(2024);
```

### 8. Combined Filters Example

```javascript
// Complex filter: CNN models trained on ImageNet
const response = await fetch(
  '/api/v1/public/ai-models/?' + new URLSearchParams({
    architecture: 'CNN',
    dataset_used: 'ImageNet',
    is_featured: 'true',
    sort_by: 'latest',
    limit: '10'
  })
);
const models = await response.json();
```

---

## Filter Summary Table

| Content Type | Search Fields | Unique Filters | Category | Featured | Sort Options |
|--------------|---------------|----------------|----------|----------|--------------|
| **Projects** | title, description | - | ✅ | ✅ | latest, oldest, title |
| **Datasets** | name, description | format, license, version | ✅ | ✅ | latest, oldest, name, downloads |
| **Publications** | title, authors, abstract | year, author | ✅ | ✅ | latest, oldest, title, year, views |
| **AI Models** | name, description | architecture, dataset_used | ✅ | ✅ | latest, oldest, name |
| **News** | title, content | - | ✅ | ✅ | latest, oldest, title |
| **Gallery** | prompt | ai_model_id | ✅ | ❌ | latest, oldest |

---

## Response Format

Semua endpoint mengembalikan format yang konsisten:

```json
{
  "data": [...],           // Array of items
  "total": 150,           // Total items matching filters
  "offset": 0,            // Current offset
  "limit": 12,            // Items per page
  "has_more": true        // Has more items to load
}
```

---

## Best Practices

### 1. Always Use Pagination

```bash
# ✅ Good
GET /api/v1/public/projects/?limit=20

# ❌ Avoid loading all items
GET /api/v1/public/projects/?limit=100
```

### 2. URL Encode Search Queries

```javascript
// ✅ Correct
const query = encodeURIComponent("machine learning & AI");
fetch(`/api/v1/public/projects/?search=${query}`);

// ❌ Incorrect
fetch(`/api/v1/public/projects/?search=machine learning & AI`);
```

### 3. Combine Filters Efficiently

```bash
# ✅ One request with multiple filters
GET /api/v1/public/datasets/?format=JSON&license=MIT&is_featured=true

# ❌ Multiple separate requests
GET /api/v1/public/datasets/?format=JSON
GET /api/v1/public/datasets/?license=MIT
GET /api/v1/public/datasets/?is_featured=true
```

### 4. Use Appropriate Limits

```bash
# List view - smaller limit
GET /api/v1/public/news/?limit=10

# Grid view - larger limit for better UX
GET /api/v1/public/gallery/?limit=24
```

---

## Error Handling

### Invalid Parameters

```json
{
  "detail": [
    {
      "loc": ["query", "year"],
      "msg": "ensure this value is greater than or equal to 1900",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

### No Results

```json
{
  "data": [],
  "total": 0,
  "offset": 0,
  "limit": 12,
  "has_more": false
}
```

---

## Testing Filters

### Using cURL

```bash
# Test search
curl "http://localhost:8000/api/v1/public/projects/?search=AI"

# Test multiple filters
curl "http://localhost:8000/api/v1/public/datasets/?format=JSON&license=MIT&limit=5"

# Test pagination
curl "http://localhost:8000/api/v1/public/publications/?offset=10&limit=10"

# Test sort
curl "http://localhost:8000/api/v1/public/ai-models/?sort_by=latest"
```

### Using JavaScript Fetch

```javascript
// Test search
const testSearch = async () => {
  const response = await fetch('/api/v1/public/projects/?search=machine+learning');
  const data = await response.json();
  console.log(`Found ${data.total} projects`);
};

// Test filters
const testFilters = async () => {
  const params = new URLSearchParams({
    format: 'CSV',
    license: 'MIT',
    is_featured: 'true',
    limit: '10'
  });
  
  const response = await fetch(`/api/v1/public/datasets/?${params}`);
  const data = await response.json();
  console.log(data);
};
```

---

## Summary

### ✅ All Public Endpoints Support

1. **Pagination** - offset & limit
2. **Search** - Case-insensitive partial matching
3. **Category Filtering** - Filter by category UUID
4. **Featured Filtering** - Show only featured items
5. **Sorting** - Multiple sort options
6. **Custom Filters** - Specific to each content type

### 📊 Total Filter Options

- **Projects:** 6 filters
- **Datasets:** 9 filters (most comprehensive)
- **Publications:** 8 filters
- **AI Models:** 7 filters
- **News:** 5 filters
- **Gallery:** 5 filters

### 🚀 Frontend Implementation

All filters are **query parameters** - easy to implement in any frontend framework (React, Vue, Angular, Svelte, etc).

---

**Happy Filtering! 🎯**
