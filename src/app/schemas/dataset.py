"""
Dataset schemas for request/response models
"""

from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..models.enums import AccessLevel, ContentStatus


class DatasetBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255, examples=["CIFAR-10 Dataset"])]
    slug: Annotated[str, Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", examples=["cifar-10-dataset"])]
    description: Annotated[
        str | None, Field(max_length=5000, examples=["A collection of 60,000 images in 10 classes"], default=None)
    ]

    # Enhanced Core Info fields
    tagline: Annotated[
        str | None, Field(max_length=500, examples=["High-quality computer vision dataset"], default=None)
    ]
    samples: Annotated[int | None, Field(ge=0, examples=[60000], description="Number of samples", default=0)]
    view_count: Annotated[int, Field(ge=0, examples=[250], description="Visitor counter", default=0)]
    download_count: Annotated[int, Field(ge=0, examples=[1500], description="Download counter", default=0)]
    gradient: Annotated[
        str | None, Field(max_length=100, examples=["#FF6B6B,#4ECDC4"], description="UI gradient colors", default=None)
    ]
    version: Annotated[str | None, Field(max_length=50, examples=["2.1"], default="1.0")]
    format: Annotated[str | None, Field(max_length=100, examples=["JSON"], default=None)]
    license: Annotated[str | None, Field(max_length=255, examples=["MIT"], default=None)]
    citation: Annotated[
        str | None, Field(examples=["@dataset{cifar10, author={Krizhevsky}, title={CIFAR-10}}"], default=None)
    ]

    # Key Features & Use Cases (arrays)
    key_features: Annotated[
        list[str] | None, Field(examples=[["High resolution", "Balanced classes", "Quality annotations"]], default=None)
    ]
    use_cases: Annotated[
        list[str] | None,
        Field(examples=[["Image classification", "Computer vision research", "Deep learning"]], default=None),
    ]

    # Technical Specifications (JSON object)
    technical_specs: Annotated[
        dict[str, Any] | None,
        Field(
            examples=[
                {
                    "format": "JSON",
                    "type": "supervised",
                    "license": "MIT",
                    "access": "public",
                    "lastUpdate": "2024-01-15",
                    "version": "2.1",
                }
            ],
            default=None,
        ),
    ]

    # Statistics (JSON object)
    statistics: Annotated[
        dict[str, Any] | None,
        Field(
            examples=[
                {
                    "avgImagesPerCategory": 6000,
                    "minImagesPerCategory": 5000,
                    "maxImagesPerCategory": 7000,
                    "avgImageSize": "32x32",
                    "totalAnnotations": 60000,
                    "qualityScore": 9.2,
                }
            ],
            default=None,
        ),
    ]

    # Sample Images (array of URLs)
    sample_images: Annotated[
        list[str] | None,
        Field(examples=[["https://example.com/sample1.jpg", "https://example.com/sample2.jpg"]], default=None),
    ]

    # Original fields
    sample_image_url: Annotated[str | None, Field(examples=["https://example.com/sample.jpg"], default=None)]
    file_url: Annotated[str | None, Field(examples=["https://example.com/dataset.zip"], default=None)]
    source: Annotated[str | None, Field(max_length=255, examples=["Stanford University"], default=None)]
    size: Annotated[int | None, Field(ge=0, examples=[1024000], description="Size in bytes", default=None)]
    access_level: AccessLevel = AccessLevel.public
    status: ContentStatus = ContentStatus.draft


class DatasetCreate(DatasetBase):
    model_config = ConfigDict(extra="forbid")


class DatasetUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=1, max_length=255, examples=["Updated Dataset Name"], default=None)]
    slug: Annotated[
        str | None,
        Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", examples=["updated-dataset-slug"], default=None),
    ]
    description: Annotated[str | None, Field(max_length=5000, default=None)]

    # Enhanced Core Info fields
    tagline: Annotated[str | None, Field(max_length=500, default=None)]
    samples: Annotated[int | None, Field(ge=0, default=None)]
    view_count: Annotated[int | None, Field(ge=0, default=None)]
    download_count: Annotated[int | None, Field(ge=0, default=None)]
    gradient: Annotated[str | None, Field(max_length=100, default=None)]
    version: Annotated[str | None, Field(max_length=50, default=None)]
    format: Annotated[str | None, Field(max_length=100, default=None)]
    license: Annotated[str | None, Field(max_length=255, default=None)]
    citation: Annotated[str | None, Field(default=None)]

    # Key Features & Use Cases (arrays)
    key_features: Annotated[list[str] | None, Field(default=None)]
    use_cases: Annotated[list[str] | None, Field(default=None)]

    # Technical Specifications & Statistics (JSON objects)
    technical_specs: Annotated[dict[str, Any] | None, Field(default=None)]
    statistics: Annotated[dict[str, Any] | None, Field(default=None)]

    # Sample Images (array of URLs)
    sample_images: Annotated[list[str] | None, Field(default=None)]

    # Original fields
    sample_image_url: Annotated[str | None, Field(default=None)]
    file_url: Annotated[str | None, Field(default=None)]
    source: Annotated[str | None, Field(max_length=255, default=None)]
    size: Annotated[int | None, Field(ge=0, default=None)]
    access_level: AccessLevel | None = None
    status: ContentStatus | None = None


class DatasetUpdateInternal(DatasetUpdate):
    updated_at: datetime


class DatasetRead(DatasetBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None


class DatasetReadWithRelations(DatasetRead):
    categories: list[str] = []
    creator_name: str | None = None


class DatasetCategoryAssignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_ids: list[UUID] = Field(description="List of category UUIDs to assign")


class DatasetBulkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dataset_ids: list[UUID]
    updates: DatasetUpdate
