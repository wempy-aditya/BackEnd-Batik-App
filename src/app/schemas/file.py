"""
Pydantic schemas for File operations
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class FileBase(BaseModel):
    """Base schema for File"""

    description: Optional[str] = Field(None, max_length=1000)


class FileCreate(FileBase):
    """Schema for creating a file (internal use after upload)"""

    original_filename: str
    filename: str
    file_path: str
    file_url: str
    file_type: str
    mime_type: str
    file_size: int
    uploaded_by: Optional[UUID] = None
    file_metadata: Optional[str] = None


class FileUpdate(BaseModel):
    """Schema for updating file metadata"""

    description: Optional[str] = Field(None, max_length=1000)
    file_metadata: Optional[str] = None


class FileRead(FileBase):
    """Schema for reading file data"""

    id: UUID
    original_filename: str
    filename: str
    file_path: str
    file_url: str
    file_type: str
    mime_type: str
    file_size: int
    uploaded_by: Optional[UUID] = None
    file_metadata: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FileUploadResponse(BaseModel):
    """Response after successful file upload"""

    id: UUID
    original_filename: str
    filename: str
    file_url: str
    file_type: str
    mime_type: str
    file_size: int
    message: str = "File uploaded successfully"
