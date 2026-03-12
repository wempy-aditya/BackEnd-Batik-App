"""
Category schemas for all content types
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# Base category schema
class CategoryBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255, examples=["Machine Learning"])]
    slug: Annotated[str, Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", examples=["machine-learning"])]
    description: Annotated[
        str | None, Field(max_length=1000, examples=["Category for machine learning related content"], default=None)
    ]


class CategoryCreate(CategoryBase):
    model_config = ConfigDict(extra="forbid")


class CategoryUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=1, max_length=255, default=None)]
    slug: Annotated[str | None, Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", default=None)]
    description: Annotated[str | None, Field(max_length=1000, default=None)]


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class CategoryReadWithCount(CategoryRead):
    content_count: int = 0  # Number of content items in this category


# Specific category types (same schema, different endpoints)
class ProjectCategoryCreate(CategoryCreate):
    pass


class ProjectCategoryUpdate(CategoryUpdate):
    pass


class ProjectCategoryRead(CategoryRead):
    pass


class ProjectCategoryReadWithCount(CategoryReadWithCount):
    pass


class DatasetCategoryCreate(CategoryCreate):
    pass


class DatasetCategoryUpdate(CategoryUpdate):
    pass


class DatasetCategoryRead(CategoryRead):
    pass


class DatasetCategoryReadWithCount(CategoryReadWithCount):
    pass


class PublicationCategoryCreate(CategoryCreate):
    pass


class PublicationCategoryUpdate(CategoryUpdate):
    pass


class PublicationCategoryRead(CategoryRead):
    pass


class PublicationCategoryReadWithCount(CategoryReadWithCount):
    pass


class NewsCategoryCreate(CategoryCreate):
    pass


class NewsCategoryUpdate(CategoryUpdate):
    pass


class NewsCategoryRead(CategoryRead):
    pass


class NewsCategoryReadWithCount(CategoryReadWithCount):
    pass


class ModelCategoryCreate(CategoryCreate):
    pass


class ModelCategoryUpdate(CategoryUpdate):
    pass


class ModelCategoryRead(CategoryRead):
    pass


class ModelCategoryReadWithCount(CategoryReadWithCount):
    pass


class GalleryCategoryCreate(CategoryCreate):
    pass


class GalleryCategoryUpdate(CategoryUpdate):
    pass


class GalleryCategoryRead(CategoryRead):
    pass


class GalleryCategoryReadWithCount(CategoryReadWithCount):
    pass


# Bulk operations
class CategoryBulkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    categories: list[CategoryCreate]


class CategoryBulkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_ids: list[UUID]
    updates: CategoryUpdate
