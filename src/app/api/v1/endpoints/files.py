"""
File management endpoints - upload, list, get, delete files
"""

import mimetypes
import shutil
from datetime import datetime
from pathlib import Path
from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_current_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ....crud.crud_file import crud_file
from ....schemas.file import FileCreate, FileRead, FileUpdate, FileUploadResponse

router = APIRouter(prefix="/files", tags=["files"])

# Upload directory configuration
UPLOAD_DIR = Path("/app/uploads")
ALLOWED_EXTENSIONS = {
    "image": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "document": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"],
    "archive": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "video": [".mp4", ".avi", ".mov", ".wmv", ".flv"],
    "other": [],
}

# Max file size: 50MB
MAX_FILE_SIZE = 50 * 1024 * 1024


def get_file_type(filename: str) -> str:
    """Determine file type category from extension"""
    ext = Path(filename).suffix.lower()

    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type

    return "other"


def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    ext = Path(original_filename).suffix
    name = Path(original_filename).stem
    # Clean filename
    clean_name = "".join(c for c in name if c.isalnum() or c in ("-", "_"))[:50]
    return f"{clean_name}_{timestamp}{ext}"


@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    file: UploadFile = File(...),
    description: Annotated[str | None, Query(max_length=1000)] = None,
    current_user: Annotated[dict | None, Depends(get_current_user)] = None,
) -> Any:
    """
    Upload a file
    - Supports images, documents, archives, videos
    - Max size: 50MB
    - Returns file URL and metadata
    """

    # Validate file
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided")

    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB",
        )

    if file_size == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")

    # Determine file type and mime type
    file_type = get_file_type(file.filename)
    mime_type = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"

    # Generate unique filename
    unique_filename = generate_unique_filename(file.filename)

    # Create directory structure: uploads/YYYY/MM/
    now = datetime.now()
    year_month_dir = UPLOAD_DIR / str(now.year) / f"{now.month:02d}"
    year_month_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    file_path = year_month_dir / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error saving file: {str(e)}")

    # Create file URL (relative path from /api/v1/uploads)
    relative_path = f"{now.year}/{now.month:02d}/{unique_filename}"
    file_url = f"/api/v1/uploads/{relative_path}"

    # Save to database
    file_data = FileCreate(
        original_filename=file.filename,
        filename=unique_filename,
        file_path=relative_path,
        file_url=file_url,
        file_type=file_type,
        mime_type=mime_type,
        file_size=file_size,
        uploaded_by=current_user["id"] if current_user else None,
        description=description,
    )

    db_file = await crud_file.create(db=db, object=file_data)

    return FileUploadResponse(
        id=db_file.id,
        original_filename=db_file.original_filename,
        filename=db_file.filename,
        file_url=db_file.file_url,
        file_type=db_file.file_type,
        mime_type=db_file.mime_type,
        file_size=db_file.file_size,
    )


@router.get("/", response_model=dict)
async def list_files(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    file_type: Annotated[str | None, Query()] = None,
    search: Annotated[str | None, Query(max_length=255)] = None,
) -> Any:
    """
    Get all files with pagination
    - Filter by file_type: image, document, archive, video, other
    - Search by filename
    - Public endpoint
    """

    if file_type:
        files = await crud_file.get_files_by_type(db=db, file_type=file_type, offset=offset, limit=limit)
        total = await crud_file.count(db=db, file_type=file_type)
    elif search:
        files = await crud_file.search_files(db=db, search=search, offset=offset, limit=limit)
        total = await crud_file.count(db=db, original_filename__icontains=search)
    else:
        files = await crud_file.get_multi(db=db, offset=offset, limit=limit)
        total = await crud_file.count(db=db)

    return {"data": files.get("data", []), "total": total, "offset": offset, "limit": limit}


@router.get("/stats")
async def get_storage_stats(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Get storage statistics for current user
    - Total files count
    - Total storage used (bytes)
    """

    user_id = current_user["id"]

    total_files = await crud_file.count(db=db, uploaded_by=user_id)
    total_size = await crud_file.get_total_storage_size(db=db, user_id=user_id)

    return {
        "total_files": total_files,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / 1024 / 1024, 2),
    }


@router.get("/{file_id}", response_model=FileRead)
async def get_file(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    file_id: UUID,
) -> Any:
    """
    Get file metadata by ID
    Public endpoint
    """

    file = await crud_file.get(db=db, id=file_id)

    if not file:
        raise NotFoundException(f"File with id {file_id} not found")

    return file


@router.get("/download/{file_id}")
async def download_file(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    file_id: UUID,
) -> FileResponse:
    """
    Download file by ID
    Public endpoint
    """

    file = await crud_file.get(db=db, id=file_id)

    if not file:
        raise NotFoundException(f"File with id {file_id} not found")

    # Construct full file path
    file_path = UPLOAD_DIR / file["file_path"]

    if not file_path.exists():
        raise NotFoundException("File not found on server")

    return FileResponse(path=file_path, filename=file["original_filename"], media_type=file["mime_type"])


@router.put("/{file_id}", response_model=FileRead)
async def update_file_metadata(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    file_id: UUID,
    file_in: FileUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Update file metadata (description, etc)
    Only file uploader or superuser can update
    """

    file = await crud_file.get(db=db, id=file_id)

    if not file:
        raise NotFoundException(f"File with id {file_id} not found")

    # Check permission
    if file["uploaded_by"] != current_user["id"] and not current_user["is_superuser"]:
        raise ForbiddenException("You can only update your own files")

    await crud_file.update(db=db, object=file_in, id=file_id)

    updated_file = await crud_file.get(db=db, id=file_id)

    return updated_file


@router.delete("/{file_id}")
async def delete_file(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    file_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Delete file (both from database and filesystem)
    Only file uploader or superuser can delete
    """

    file = await crud_file.get(db=db, id=file_id)

    if not file:
        raise NotFoundException(f"File with id {file_id} not found")

    # Check permission
    if file["uploaded_by"] != current_user["id"] and not current_user["is_superuser"]:
        raise ForbiddenException("You can only delete your own files")

    # Delete from filesystem
    file_path = UPLOAD_DIR / file["file_path"]

    if file_path.exists():
        try:
            file_path.unlink()
        except Exception as e:
            # Log error but continue with database deletion
            print(f"Error deleting file from filesystem: {e}")

    # Delete from database
    await crud_file.delete(db=db, id=file_id)

    return {"detail": "File deleted successfully"}
