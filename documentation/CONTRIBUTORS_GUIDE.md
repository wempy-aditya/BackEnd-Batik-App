# Contributors System Documentation

## Overview
Sistem Contributors untuk mengelola data kontributor/team members yang dapat di-assign ke berbagai content (Projects, Publications, Datasets, dll).

## Database Structure

### Table: `contributors`
Master table untuk menyimpan data kontributor.

**Fields:**
- `id` (UUID) - Primary key
- `name` (String) - Nama kontributor (required)
- `email` (String) - Email kontributor (optional)
- `role` (String) - Role umum (e.g., "Developer", "Researcher") (optional)
- `bio` (Text) - Bio/deskripsi singkat (optional)
- `profile_image` (Text) - URL foto profil (optional)
- `github_url` (Text) - GitHub profile link (optional)
- `linkedin_url` (Text) - LinkedIn profile link (optional)
- `website_url` (Text) - Personal website link (optional)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Link Tables

#### `project_contributor_links`
Hubungkan contributors dengan projects.
- `project_id` → `projects.id`
- `contributor_id` → `contributors.id`
- `role_in_project` (String) - Role spesifik di project ini (optional)

#### `publication_contributor_links`
Hubungkan contributors dengan publications.
- `publication_id` → `publications.id`
- `contributor_id` → `contributors.id`
- `role_in_publication` (String) - Role spesifik di publication ini (optional)

#### `dataset_contributor_links`
Hubungkan contributors dengan datasets.
- `dataset_id` → `datasets.id`
- `contributor_id` → `contributors.id`
- `role_in_dataset` (String) - Role spesifik di dataset ini (optional)

## API Endpoints

### Contributor Management (Admin/Superuser only)

#### Create Contributor
```http
POST /api/v1/contributors
Authorization: Bearer <token>

{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "Lead Developer",
  "bio": "Experienced software engineer...",
  "github_url": "https://github.com/johndoe"
}
```

#### Get All Contributors (Public)
```http
GET /api/v1/contributors?offset=0&limit=50&search=john

Response:
{
  "data": [...],
  "total": 10,
  "offset": 0,
  "limit": 50
}
```

#### Get Contributor by ID (Public)
```http
GET /api/v1/contributors/{contributor_id}

Response:
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "Lead Developer",
  ...
  "project_count": 5,
  "publication_count": 3,
  "dataset_count": 2,
  "total_contributions": 10
}
```

#### Update Contributor
```http
PUT /api/v1/contributors/{contributor_id}
Authorization: Bearer <token> (Superuser only)

{
  "name": "John Doe Updated",
  "bio": "Updated bio..."
}
```

#### Delete Contributor
```http
DELETE /api/v1/contributors/{contributor_id}
Authorization: Bearer <token> (Superuser only)
```

### Assignment Endpoints

#### Assign Contributors to Project
```http
POST /api/v1/contributors/assign/project/{project_id}
Authorization: Bearer <token> (Superuser only)

{
  "contributor_ids": ["uuid1", "uuid2", "uuid3"],
  "roles": ["Lead Developer", "Backend Developer", "Frontend Developer"]
}
```

Roles array adalah optional. Jika tidak ada, role_in_project akan null.

#### Get Project Contributors (Public)
```http
GET /api/v1/contributors/project/{project_id}/contributors

Response:
{
  "data": [
    {
      "id": "uuid",
      "name": "John Doe",
      "role": "Lead Developer",
      "role_in_project": "Lead Developer",
      ...
    }
  ],
  "total": 3
}
```

## Usage Examples

### 1. Create Contributors (One-time setup)
```bash
# Create contributor 1
curl -X POST http://localhost:8000/api/v1/contributors \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "role": "Full Stack Developer",
    "github_url": "https://github.com/alice"
  }'

# Create contributor 2
curl -X POST http://localhost:8000/api/v1/contributors \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Smith",
    "email": "bob@example.com",
    "role": "Data Scientist"
  }'
```

### 2. Assign to Project
```bash
curl -X POST http://localhost:8000/api/v1/contributors/assign/project/PROJECT_UUID \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "contributor_ids": ["ALICE_UUID", "BOB_UUID"],
    "roles": ["Lead Developer", "ML Engineer"]
  }'
```

### 3. View Project Team (Public)
```bash
curl http://localhost:8000/api/v1/contributors/project/PROJECT_UUID/contributors
```

## Features

✅ **Master Data Management**
- CRUD operations untuk contributor data
- Search contributors by name
- View contributor stats (total contributions)

✅ **Flexible Assignment**
- Assign ke Projects, Publications, Datasets
- Optional role untuk setiap assignment
- Support multiple contributors per content

✅ **Public Access**
- List all contributors (no auth)
- View contributor details with stats (no auth)
- View content contributors (no auth)

✅ **Admin Control**
- Only superusers can create/update/delete contributors
- Only superusers can assign contributors to content

## Database Relationships

```
Contributor 1 <-----> M ProjectContributorLink M <-----> 1 Project
Contributor 1 <-----> M PublicationContributorLink M <-----> 1 Publication  
Contributor 1 <-----> M DatasetContributorLink M <-----> 1 Dataset
```

Each link can have an optional `role_in_*` field for specific role in that content.

## Next Steps

Jika ingin extend untuk content types lain (News, AI Models, Gallery), tinggal:
1. Buat link table baru (e.g., `news_contributor_links`)
2. Tambahkan relationship di model
3. Tambahkan CRUD methods di `crud_contributor.py`
4. Tambahkan endpoints di `contributors.py`
