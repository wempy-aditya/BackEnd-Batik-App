"""
Pydantic schemas for Gallery model (matching existing database structure)
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GalleryBase(BaseModel):
    prompt: Annotated[str | None, Field(examples=["Generate a beautiful landscape"], default=None)]
    image_url: Annotated[str | None, Field(examples=["https://example.com/images/generated1.jpg"], default=None)]
    extra_metadata: dict | None = Field(examples=[{"parameters": {"steps": 20, "guidance": 7.5}}], default=None)
    model_id: UUID | None = None


class GalleryCreate(GalleryBase):
    model_config = ConfigDict(extra="forbid")


class GalleryUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str | None = None
    image_url: str | None = None
    extra_metadata: dict | None = None
    model_id: UUID | None = None


class GalleryUpdateInternal(GalleryUpdate):
    updated_at: datetime


class GalleryRead(GalleryBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None


# Schema for reading gallery with related data
class GalleryReadWithRelations(GalleryRead):
    # Will be populated via relationships
    categories: list[str] = []  # Category names
    creator_name: str | None = None  # User name
    model_name: str | None = None  # AI Model name


# Schema for category assignment
class GalleryCategoryAssignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_ids: list[UUID] = Field(examples=[["uuid1", "uuid2"]], description="List of category UUIDs to assign")


# Schema for bulk operations
class GalleryBulkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gallery_ids: list[UUID]
    updates: GalleryUpdate
