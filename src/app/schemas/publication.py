"""
Publication schemas for request/response models
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..models.enums import AccessLevel, ContentStatus


class PublicationBase(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=255, examples=["Deep Learning for Computer Vision"])]
    slug: Annotated[
        str,
        Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", examples=["deep-learning-for-computer-vision"]),
    ]
    abstract: Annotated[
        str | None, Field(max_length=5000, examples=["This paper presents a novel approach to..."], default=None)
    ]

    # New Core Info fields
    authors: Annotated[list[str] | None, Field(examples=[["John Doe", "Jane Smith"]], default=None)]
    venue: Annotated[str | None, Field(max_length=255, examples=["IEEE Conference on Computer Vision"], default=None)]
    citations: Annotated[int | None, Field(ge=0, examples=[42], default=0)]
    doi: Annotated[str | None, Field(max_length=255, examples=["10.1000/182"], default=None)]
    keywords: Annotated[
        list[str] | None, Field(examples=[["machine learning", "deep learning", "computer vision"]], default=None)
    ]
    impact: Annotated[str | None, Field(max_length=50, examples=["2.5"], default=None)]
    pages: Annotated[str | None, Field(max_length=50, examples=["123-145"], default=None)]

    # Journal Specific fields
    volume: Annotated[str | None, Field(max_length=50, examples=["15"], default=None)]
    issue: Annotated[str | None, Field(max_length=50, examples=["3"], default=None)]
    publisher: Annotated[str | None, Field(max_length=255, examples=["IEEE Press"], default=None)]

    # Content Sections
    methodology: Annotated[
        str | None, Field(max_length=10000, examples=["We used a convolutional neural network..."], default=None)
    ]
    results: Annotated[
        str | None, Field(max_length=10000, examples=["Our model achieved 95% accuracy..."], default=None)
    ]
    conclusions: Annotated[
        str | None, Field(max_length=10000, examples=["This work demonstrates that..."], default=None)
    ]

    # Existing fields
    pdf_url: Annotated[str | None, Field(examples=["https://arxiv.org/pdf/example.pdf"], default=None)]
    journal_name: Annotated[str | None, Field(max_length=255, examples=["Nature Machine Intelligence"], default=None)]
    year: Annotated[int | None, Field(ge=1900, le=2100, examples=[2023], default=None)]
    graphical_abstract_url: Annotated[
        str | None, Field(examples=["https://example.com/graphical-abstract.jpg"], default=None)
    ]
    access_level: AccessLevel = AccessLevel.public
    status: ContentStatus = ContentStatus.draft


class PublicationCreate(PublicationBase):
    model_config = ConfigDict(extra="forbid")


class PublicationUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str | None, Field(min_length=1, max_length=255, default=None)]
    slug: Annotated[str | None, Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", default=None)]
    abstract: Annotated[str | None, Field(max_length=5000, default=None)]

    # New Core Info fields
    authors: Annotated[list[str] | None, Field(default=None)]
    venue: Annotated[str | None, Field(max_length=255, default=None)]
    citations: Annotated[int | None, Field(ge=0, default=None)]
    doi: Annotated[str | None, Field(max_length=255, default=None)]
    keywords: Annotated[list[str] | None, Field(default=None)]
    impact: Annotated[str | None, Field(max_length=50, default=None)]
    pages: Annotated[str | None, Field(max_length=50, default=None)]

    # Journal Specific fields
    volume: Annotated[str | None, Field(max_length=50, default=None)]
    issue: Annotated[str | None, Field(max_length=50, default=None)]
    publisher: Annotated[str | None, Field(max_length=255, default=None)]

    # Content Sections
    methodology: Annotated[str | None, Field(max_length=10000, default=None)]
    results: Annotated[str | None, Field(max_length=10000, default=None)]
    conclusions: Annotated[str | None, Field(max_length=10000, default=None)]

    # Existing fields
    pdf_url: Annotated[str | None, Field(default=None)]
    journal_name: Annotated[str | None, Field(max_length=255, default=None)]
    year: Annotated[int | None, Field(ge=1900, le=2100, default=None)]
    graphical_abstract_url: Annotated[str | None, Field(default=None)]
    access_level: AccessLevel | None = None
    status: ContentStatus | None = None


class PublicationUpdateInternal(PublicationUpdate):
    updated_at: datetime


class PublicationRead(PublicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    view_count: int = 0
    download_count: int = 0


class PublicationReadWithRelations(PublicationRead):
    categories: list[str] = []
    creator_name: str | None = None


class PublicationCategoryAssignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_ids: list[UUID] = Field(description="List of category UUIDs to assign")


class PublicationBulkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    publication_ids: list[UUID]
    updates: PublicationUpdate
