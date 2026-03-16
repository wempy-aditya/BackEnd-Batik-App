"""
Project schemas for request/response models
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..models.enums import AccessLevel, ContentStatus, ProjectComplexity


# Base schema with common fields
class ProjectBase(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=255, examples=["My Awesome Project"])]
    slug: Annotated[str, Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", examples=["my-awesome-project"])]
    description: Annotated[str | None, Field(max_length=5000, examples=["This is a short description"], default=None)]
    full_description: Annotated[
        str | None,
        Field(
            max_length=50000,
            examples=["This is a detailed description of my project with all the technical details"],
            default=None,
        ),
    ]

    # Technologies and project arrays
    technologies: Annotated[list[str] | None, Field(examples=[["Python", "FastAPI", "PostgreSQL"]], default=None)]
    challenges: Annotated[
        list[str] | None, Field(examples=[["Database optimization", "Performance tuning"]], default=None)
    ]
    achievements: Annotated[
        list[str] | None, Field(examples=[["99.9% uptime", "50% performance improvement"]], default=None)
    ]
    future_work: Annotated[
        list[str] | None, Field(examples=[["Add machine learning features", "Mobile app development"]], default=None)
    ]

    # Media and metadata
    thumbnail_url: Annotated[str | None, Field(examples=["https://example.com/image.jpg"], default=None)]
    demo_url: Annotated[
        list[str] | None,
        Field(
            examples=[["https://demo.example.com", "https://prototype.example.com"]],
            description="Demo/prototype URLs",
            default=None,
        ),
    ]
    tags: Annotated[list[str] | None, Field(examples=[["ai", "machine-learning", "python"]], default=None)]
    # Project metadata
    complexity: ProjectComplexity | None = None
    start_at: Annotated[datetime | None, Field(examples=["2025-01-15T10:00:00Z"], default=None)]

    # Access control and status
    access_level: AccessLevel = AccessLevel.public
    status: ContentStatus = ContentStatus.draft


# Schema for creating a new project
class ProjectCreate(ProjectBase):
    model_config = ConfigDict(extra="forbid")


# Schema for updating an existing project
class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str | None, Field(min_length=1, max_length=255, examples=["Updated Project Title"], default=None)]
    slug: Annotated[
        str | None,
        Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", examples=["updated-project-slug"], default=None),
    ]
    description: Annotated[str | None, Field(max_length=5000, examples=["Updated short description"], default=None)]
    full_description: Annotated[
        str | None, Field(max_length=50000, examples=["Updated detailed description"], default=None)
    ]

    # Technologies and project arrays
    technologies: Annotated[list[str] | None, Field(examples=[["Python", "FastAPI"]], default=None)]
    challenges: Annotated[list[str] | None, Field(examples=[["Updated challenges"]], default=None)]
    achievements: Annotated[list[str] | None, Field(examples=[["Updated achievements"]], default=None)]
    future_work: Annotated[list[str] | None, Field(examples=[["Updated future work"]], default=None)]

    # Media and metadata
    thumbnail_url: Annotated[str | None, Field(examples=["https://example.com/new-image.jpg"], default=None)]
    demo_url: Annotated[
        list[str] | None,
        Field(examples=[["https://new-demo.example.com"]], description="Demo/prototype URLs", default=None),
    ]
    tags: Annotated[list[str] | None, Field(examples=[["ai", "updated-tag"]], default=None)]
    # Project metadata
    complexity: ProjectComplexity | None = None
    start_at: Annotated[datetime | None, Field(examples=["2025-02-01T10:00:00Z"], default=None)]

    # Access control and status
    access_level: AccessLevel | None = None
    status: ContentStatus | None = None


# Schema for internal updates (includes system fields)
class ProjectUpdateInternal(ProjectUpdate):
    updated_at: datetime


# Schema for reading project data (response)
class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None


# Schema for reading project with related data
class ProjectReadWithRelations(ProjectRead):
    # Will be populated via relationships
    categories: list[str] = []  # Category names
    creator_name: str | None = None  # User name


# Schema for category assignment
class ProjectCategoryAssignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_ids: list[UUID] = Field(examples=[["uuid1", "uuid2"]], description="List of category UUIDs to assign")


# Schema for bulk operations
class ProjectBulkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_ids: list[UUID]
    updates: ProjectUpdate