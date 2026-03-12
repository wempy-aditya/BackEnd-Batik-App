"""
News schemas for request/response models
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..models.enums import AccessLevel, ContentStatus


class NewsBase(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=255, examples=["Breaking: New AI Breakthrough"])]
    slug: Annotated[str, Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", examples=["new-ai-breakthrough"])]
    content: Annotated[
        str | None, Field(examples=["# Article Title\n\nThis is the content in markdown..."], default=None)
    ]
    thumbnail_url: Annotated[str | None, Field(examples=["https://example.com/news-image.jpg"], default=None)]
    tags: Annotated[list[str] | None, Field(examples=[["ai", "breakthrough", "technology"]], default=None)]
    access_level: AccessLevel = AccessLevel.public
    status: ContentStatus = ContentStatus.draft


class NewsCreate(NewsBase):
    model_config = ConfigDict(extra="forbid")


class NewsUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str | None, Field(min_length=1, max_length=255, default=None)]
    slug: Annotated[str | None, Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", default=None)]
    content: Annotated[str | None, Field(default=None)]
    thumbnail_url: Annotated[str | None, Field(default=None)]
    tags: Annotated[list[str] | None, Field(default=None)]
    access_level: AccessLevel | None = None
    status: ContentStatus | None = None


class NewsUpdateInternal(NewsUpdate):
    updated_at: datetime


class NewsRead(NewsBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None


class NewsReadWithRelations(NewsRead):
    categories: list[str] = []
    creator_name: str | None = None


class NewsCategoryAssignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_ids: list[UUID] = Field(description="List of category UUIDs to assign")


class NewsBulkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    news_ids: list[UUID]
    updates: NewsUpdate
