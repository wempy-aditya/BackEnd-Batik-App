# File Management System Documentation

## Overview
Sistem File Manager untuk mengelola upload dan penyimpanan file (gambar, dokumen, arsip, video) yang dapat digunakan untuk thumbnail project/dataset/publication atau file dataset (ZIP, dll).

## Database Structure

### Table: `files`
Master table untuk menyimpan metadata file yang di-upload.

**Fields:**
- `id` (UUID) - Primary key
- `original_filename` (String) - Nama file asli dari user
- `filename` (String) - Nama file yang disimpan (unique, auto-generated)
- `file_path` (Text) - Path relatif dari upload root (YYYY/MM/filename.ext)
- `file_url` (Text) - URL publik untuk akses file
- `file_type` (String) - Kategori file: `image`, `document`, `archive`, `video`, `other`
- `mime_type` (String) - MIME type (image/png, application/pdf, dll)
- `file_size` (Integer) - Ukuran file dalam bytes
- `uploaded_by` (UUID) - Foreign key ke `users.id` (nullable, SET NULL on delete)
- `file_metadata` (Text) - Metadata tambahan dalam format JSON (optional)
- `description` (Text) - Deskripsi/alt text untuk file (optional)
- `created_at` (DateTime) - Timestamp upload
- `updated_at` (DateTime) - Timestamp update terakhir

**Indexes:**
- `ix_files_filename` - Index pada filename untuk pencarian cepat
- `ix_files_file_type` - Index pada file_type untuk filtering
- `ix_files_uploaded_by` - Index pada uploaded_by untuk query per user
- `ix_files_created_at` - Index pada created_at untuk sorting

## File Storage

### Directory Structure
```
/app/uploads/
  ├── 2025/
  │   ├── 01/
  │   │   ├── image_20250115_103045_123456.png
  │   │   └── dataset_20250115_104512_789012.zip
  │   ├── 02/
  │   │   └── document_20250220_091234_456789.pdf
  │   └── 12/
  │       └── thumbnail_20251217_043358_328189.jpg
```

Files disimpan dengan struktur `YYYY/MM/` untuk organisasi yang lebih baik.

### File Naming Convention
Format: `{clean_original_name}_{timestamp}.{extension}`
- `clean_original_name`: Nama asli file (hanya alphanumeric, -, _)
- `timestamp`: Format `YYYYMMDD_HHMMSS_microseconds`
- `extension`: Extension file asli

Contoh: `research_paper_20251217_103045_123456.pdf`

### Supported File Types

#### Image
Extensions: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.svg`

#### Document
Extensions: `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.txt`

#### Archive
Extensions: `.zip`, `.tar`, `.gz`, `.rar`, `.7z`

#### Video
Extensions: `.mp4`, `.avi`, `.mov`, `.wmv`, `.flv`

#### Other
Semua extension lain yang tidak masuk kategori di atas.

### File Size Limit
**Maximum:** 50 MB per file

## API Endpoints

### 1. Upload File

**Endpoint:** `POST /api/v1/files/upload`

**Authentication:** Optional (jika authenticated, `uploaded_by` akan tercatat)

**Content-Type:** `multipart/form-data`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.png" \
  -F "description=Project thumbnail image"
```

**Request Body:**
- `file` (file, required) - File yang akan di-upload
- `description` (string, optional) - Deskripsi file

**Response:** `201 Created`
```json
{
  "id": "019b2a96-1839-76b9-896d-23801a0f06d4",
  "original_filename": "image.png",
  "filename": "image_20251217_043358_328189.png",
  "file_url": "/uploads/2025/12/image_20251217_043358_328189.png",
  "file_type": "image",
  "mime_type": "image/png",
  "file_size": 245678,
  "message": "File uploaded successfully"
}
```

**Validations:**
- File tidak boleh kosong (0 bytes)
- File size max 50MB
- Filename harus ada

### 2. Get All Files (Public)

**Endpoint:** `GET /api/v1/files/`

**Authentication:** None (public)

**Query Parameters:**
- `offset` (int, default: 0) - Pagination offset
- `limit` (int, default: 50, max: 100) - Items per page
- `file_type` (string, optional) - Filter by: `image`, `document`, `archive`, `video`, `other`
- `search` (string, optional) - Search by filename

**Examples:**
```bash
# Get all files
GET /api/v1/files/?offset=0&limit=20

# Filter images only
GET /api/v1/files/?file_type=image

# Search files
GET /api/v1/files/?search=dataset

# Pagination
GET /api/v1/files/?offset=20&limit=10
```

**Response:** `200 OK`
```json
{
  "data": [
    {
      "id": "019b2a96-1839-76b9-896d-23801a0f06d4",
      "original_filename": "image.png",
      "filename": "image_20251217_043358_328189.png",
      "file_path": "2025/12/image_20251217_043358_328189.png",
      "file_url": "/uploads/2025/12/image_20251217_043358_328189.png",
      "file_type": "image",
      "mime_type": "image/png",
      "file_size": 245678,
      "uploaded_by": "019aac02-ac77-7338-ac5b-3a8446f4a76d",
      "file_metadata": null,
      "description": "Project thumbnail image",
      "created_at": "2025-12-17T04:33:58.328189Z",
      "updated_at": null
    }
  ],
  "total": 15,
  "offset": 0,
  "limit": 50
}
```

### 3. Get File by ID (Public)

**Endpoint:** `GET /api/v1/files/{file_id}`

**Authentication:** None (public)

**Response:** `200 OK`
```json
{
  "id": "019b2a96-1839-76b9-896d-23801a0f06d4",
  "original_filename": "image.png",
  "filename": "image_20251217_043358_328189.png",
  "file_path": "2025/12/image_20251217_043358_328189.png",
  "file_url": "/uploads/2025/12/image_20251217_043358_328189.png",
  "file_type": "image",
  "mime_type": "image/png",
  "file_size": 245678,
  "uploaded_by": "019aac02-ac77-7338-ac5b-3a8446f4a76d",
  "file_metadata": null,
  "description": "Project thumbnail image",
  "created_at": "2025-12-17T04:33:58.328189Z",
  "updated_at": null
}
```

### 4. Download File (Public)

**Endpoint:** `GET /api/v1/files/download/{file_id}`

**Authentication:** None (public)

**Response:** `200 OK` with file binary data

**Headers:**
- `Content-Type`: Sesuai MIME type file
- `Content-Disposition`: `attachment; filename="original_filename.ext"`

**Example:**
```bash
curl -O -J "http://localhost:8000/api/v1/files/download/019b2a96-1839-76b9-896d-23801a0f06d4"
```

### 5. Get Storage Statistics

**Endpoint:** `GET /api/v1/files/stats`

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "total_files": 25,
  "total_size_bytes": 125678934,
  "total_size_mb": 119.84
}
```

Menampilkan statistik untuk user yang sedang login.

### 6. Update File Metadata

**Endpoint:** `PUT /api/v1/files/{file_id}`

**Authentication:** Required (owner atau superuser)

**Request Body:**
```json
{
  "description": "Updated description for the file",
  "file_metadata": "{\"tags\": [\"project\", \"thumbnail\"]}"
}
```

**Response:** `200 OK`
```json
{
  "id": "019b2a96-1839-76b9-896d-23801a0f06d4",
  "original_filename": "image.png",
  "description": "Updated description for the file",
  "file_metadata": "{\"tags\": [\"project\", \"thumbnail\"]}",
  ...
}
```

### 7. Delete File

**Endpoint:** `DELETE /api/v1/files/{file_id}`

**Authentication:** Required (owner atau superuser)

**Response:** `200 OK`
```json
{
  "detail": "File deleted successfully"
}
```

**Action:**
- Menghapus record dari database
- Menghapus file fisik dari filesystem

## Usage Examples

### Upload Thumbnail untuk Project

```python
import requests

# Login
login_response = requests.post(
    "http://localhost:8000/api/v1/login",
    data={"username": "user@example.com", "password": "password"}
)
token = login_response.json()["access_token"]

# Upload thumbnail
with open("project_thumbnail.png", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/files/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": f},
        data={"description": "Project ABC thumbnail"}
    )

file_data = response.json()
thumbnail_url = file_data["file_url"]
# thumbnail_url = "/uploads/2025/12/project_thumbnail_20251217_103045_123456.png"

# Gunakan URL ini di project
project_data = {
    "title": "Project ABC",
    "thumbnail_url": thumbnail_url,
    ...
}
```

### Upload Dataset ZIP File

```bash
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@dataset.zip" \
  -F "description=MNIST dataset for machine learning"
```

Response:
```json
{
  "id": "019b2a97-2b4c-7d1e-9abc-def123456789",
  "original_filename": "dataset.zip",
  "filename": "dataset_20251217_104512_789012.zip",
  "file_url": "/uploads/2025/12/dataset_20251217_104512_789012.zip",
  "file_type": "archive",
  "mime_type": "application/zip",
  "file_size": 45678901,
  "message": "File uploaded successfully"
}
```

### Get All Images

```bash
curl "http://localhost:8000/api/v1/files/?file_type=image&limit=20"
```

### Search Files by Name

```bash
curl "http://localhost:8000/api/v1/files/?search=dataset"
```

### Access Uploaded File Directly

Setelah upload, file bisa diakses langsung via URL:

```
http://localhost:8000/uploads/2025/12/image_20251217_043358_328189.png
```

URL ini bisa digunakan untuk:
- Thumbnail di card project/dataset/publication
- Preview image
- Download link dataset
- Attachment di publication

## Integration dengan Content Models

### Project Thumbnail
```python
# Upload thumbnail
file_response = upload_file("project_thumb.png")
thumbnail_url = file_response["file_url"]

# Create project dengan thumbnail
project = {
    "title": "Batik Classification",
    "thumbnail_url": thumbnail_url,  # Store URL dari file upload
    ...
}
```

### Dataset Files
```python
# Upload dataset ZIP
file_response = upload_file("dataset.zip", "Complete MNIST dataset")
dataset_file_url = file_response["file_url"]

# Create dataset
dataset = {
    "title": "MNIST Dataset",
    "download_url": dataset_file_url,  # Link ke file ZIP
    "file_size": file_response["file_size"],
    ...
}
```

### Publication PDF
```python
# Upload research paper
file_response = upload_file("research_paper.pdf")

# Create publication
publication = {
    "title": "Deep Learning for Batik",
    "pdf_url": file_response["file_url"],
    ...
}
```

## Features

✅ **File Upload**
- Multi-format support (images, documents, archives, videos)
- Auto file type detection
- Unique filename generation
- Size validation (max 50MB)

✅ **Storage Management**
- Organized directory structure (YYYY/MM/)
- Static file serving
- Physical file deletion

✅ **Query & Filter**
- Pagination support
- Filter by file type
- Search by filename
- Get user statistics

✅ **Security**
- Owner-based permissions for update/delete
- Optional authentication for upload
- Public read access

✅ **Metadata**
- Original filename preservation
- Description/alt text support
- JSON metadata field for custom data
- Upload timestamp tracking

## Error Handling

### 400 Bad Request
```json
{
  "detail": "No filename provided"
}
```
atau
```json
{
  "detail": "Empty file"
}
```

### 413 Payload Too Large
```json
{
  "detail": "File too large. Max size: 50MB"
}
```

### 404 Not Found
```json
{
  "detail": "File with id {file_id} not found"
}
```

### 403 Forbidden
```json
{
  "detail": "You can only delete your own files"
}
```

## Testing

Run comprehensive test suite:
```bash
python3 test_files.py
```

Test coverage:
- ✅ Upload image
- ✅ Upload ZIP archive
- ✅ Get all files (public)
- ✅ Filter by file type
- ✅ Get file by ID
- ✅ Storage statistics
- ✅ Update file metadata
- ✅ Download file
- ✅ Delete file

## Configuration

### Environment Variables
Tidak ada environment variables khusus untuk file upload. Menggunakan konfigurasi default:

- Upload directory: `/app/uploads`
- Max file size: 50 MB
- Allowed extensions: Semua extension (dengan kategorisasi)

### Docker Volume
File uploads dipersist dengan volume mapping:
```yaml
volumes:
  - ./uploads:/app/uploads
```

File yang di-upload akan tersimpan di `./uploads/` di host machine.

## Maintenance

### Cleanup Old Files
Untuk membersihkan file lama, bisa dibuat script cron job:

```python
# cleanup_old_files.py
from datetime import datetime, timedelta
import os
from pathlib import Path

UPLOAD_DIR = Path("/app/uploads")
MAX_AGE_DAYS = 90  # Delete files older than 90 days

def cleanup_old_files():
    cutoff_date = datetime.now() - timedelta(days=MAX_AGE_DAYS)
    
    for file_path in UPLOAD_DIR.rglob("*"):
        if file_path.is_file():
            file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_mtime < cutoff_date:
                print(f"Deleting: {file_path}")
                file_path.unlink()
                
                # Also delete from database
                # ... delete query
```

### Storage Monitoring
Monitor total storage usage per user:
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:8000/api/v1/files/stats"
```

## Best Practices

1. **Gunakan Description:** Selalu isi description untuk accessibility (alt text untuk gambar)

2. **Validate File Type:** Di frontend, validate file type sebelum upload

3. **Compress Images:** Compress gambar sebelum upload untuk menghemat storage

4. **Use CDN:** Untuk production, pertimbangkan menggunakan CDN atau object storage (S3, Cloudinary)

5. **Cleanup:** Hapus file yang tidak terpakai untuk menghemat storage

6. **Backup:** Backup folder `/uploads` secara regular

## Future Enhancements

Possible improvements:
- [ ] Image resizing/optimization otomatis
- [ ] Thumbnail generation untuk images
- [ ] Virus scanning untuk uploaded files
- [ ] Integration dengan S3/cloud storage
- [ ] CDN integration
- [ ] File versioning
- [ ] Batch upload
- [ ] Upload progress tracking
- [ ] File sharing dengan expiry time
- [ ] Storage quota per user
