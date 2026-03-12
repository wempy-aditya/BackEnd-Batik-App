"""
AI Model and Gallery schemas for request/response models
"""

from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..models.enums import AccessLevel, ContentStatus


# AI Model Schemas
class AIModelBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255, examples=["ResNet-50 Image Classifier"])]
    slug: Annotated[
        str, Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", examples=["resnet-50-image-classifier"])
    ]
    description: Annotated[
        str | None, Field(max_length=5000, examples=["A deep residual network for image classification"], default=None)
    ]
    architecture: Annotated[str | None, Field(max_length=255, examples=["ResNet"], default=None)]
    dataset_used: Annotated[str | None, Field(max_length=255, examples=["ImageNet"], default=None)]
    metrics: Annotated[
        dict[str, Any] | None,
        Field(
            examples=[
                {
                    # Classification metrics
                    "accuracy": 0.95,
                    "precision": 0.93,
                    "recall": 0.94,
                    "f1_score": 0.92,
                    "loss": 0.05,
                    # Regression metrics
                    "mae": 0.15,
                    "mse": 0.023,
                    "rmse": 0.152,
                    "r2_score": 0.89,
                    # Object detection metrics
                    "map": 0.78,
                    "iou": 0.85,
                    # Generative model metrics
                    "fid": 12.5,
                    "inception_score": 8.3,
                    # Custom metrics
                    "training_time": "2.5 hours",
                    "inference_time_ms": 45,
                }
            ],
            description=(
                "Flexible metrics object - can contain any metric name with numeric or string values. "
                "Examples: accuracy, precision, recall, f1_score, loss, mae, mse, rmse, r2_score, map, iou, "
                "fid, inception_score, etc."
            ),
            default=None,
        ),
    ]
    model_file_url: Annotated[str | None, Field(examples=["https://example.com/model.pt"], default=None)]
    access_level: AccessLevel = AccessLevel.public
    status: ContentStatus = ContentStatus.draft


class AIModelCreate(AIModelBase):
    model_config = ConfigDict(extra="forbid")


class AIModelUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=1, max_length=255, default=None)]
    slug: Annotated[str | None, Field(min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$", default=None)]
    description: Annotated[str | None, Field(max_length=5000, default=None)]
    architecture: Annotated[str | None, Field(max_length=255, default=None)]
    dataset_used: Annotated[str | None, Field(max_length=255, default=None)]
    metrics: Annotated[dict[str, Any] | None, Field(default=None)]
    model_file_url: Annotated[str | None, Field(default=None)]
    access_level: AccessLevel | None = None
    status: ContentStatus | None = None


class AIModelUpdateInternal(AIModelUpdate):
    updated_at: datetime


class AIModelRead(AIModelBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None


class AIModelReadWithRelations(AIModelRead):
    categories: list[str] = []
    creator_name: str | None = None
    gallery_count: int = 0  # Count of generated images


class AIModelCategoryAssignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_ids: list[UUID] = Field(description="List of category UUIDs to assign")


# Gallery Schemas
class GalleryBase(BaseModel):
    prompt: Annotated[str | None, Field(max_length=1000, examples=["A beautiful sunset over mountains"], default=None)]
    image_url: Annotated[str | None, Field(examples=["https://example.com/generated-image.jpg"], default=None)]
    extra_metadata: Annotated[
        dict[str, Any] | None, Field(examples=[{"steps": 50, "cfg_scale": 7.5, "seed": 123456}], default=None)
    ]
    model_id: UUID | None = None  # Optional - can be None for user uploads


class GalleryCreate(GalleryBase):
    model_config = ConfigDict(extra="forbid")


class GalleryUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: Annotated[str | None, Field(max_length=1000, default=None)]
    image_url: Annotated[str | None, Field(default=None)]
    extra_metadata: Annotated[dict[str, Any] | None, Field(default=None)]
    model_id: UUID | None = None


class GalleryUpdateInternal(GalleryUpdate):
    updated_at: datetime


class GalleryRead(GalleryBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None


class GalleryReadWithRelations(GalleryRead):
    categories: list[str] = []
    creator_name: str | None = None
    model_name: str | None = None  # Name of the AI model used


class GalleryCategoryAssignment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category_ids: list[UUID] = Field(description="List of category UUIDs to assign")


# Bulk Operations
class AIModelBulkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_ids: list[UUID]
    updates: AIModelUpdate


class GalleryBulkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gallery_ids: list[UUID]
    updates: GalleryUpdate
