"""
Public API endpoints for Datasets
Frontend/Homepage endpoints - No authentication required
Only shows published and public datasets
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_optional_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import NotFoundException
from ....crud.crud_datasets import crud_dataset
from ....schemas.dataset import DatasetReadWithRelations

router = APIRouter()


@router.get("/", response_model=dict)
async def get_public_datasets(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 12,
    search: Annotated[str | None, Query(max_length=255, description="Search in name and description")] = None,
    format: Annotated[str | None, Query(description="Filter by format (CSV, JSON, Parquet, etc)")] = None,
    license: Annotated[str | None, Query(description="Filter by license (MIT, Apache, etc)")] = None,
    version: Annotated[str | None, Query(description="Filter by version")] = None,
    category_id: Annotated[UUID | None, Query(description="Filter by category UUID")] = None,
    sort_by: Annotated[str | None, Query(description="Sort by: latest, oldest, name")] = "latest",
) -> Any:
    """
    Get public datasets for homepage/frontend

        - Authentication optional (Bearer token)
        - Access level by role:
            - Guest: public
            - registered: public + registered
            - premium/admin/superuser: public + registered + premium
    - Supports multiple filters and sorting

    Filters:
    - search: Search in name and description
    - format: CSV, JSON, Parquet, HDF5, etc
    - license: MIT, Apache-2.0, GPL, etc
    - version: Dataset version (e.g., "1.0", "2.1")
    - category_id: Filter by category UUID
    - sort_by: latest, oldest, name
    """
    from sqlalchemy import asc, desc, func, or_, select

    from ....models.categories import DatasetCategoryLink
    from ....models.dataset import Dataset
    from ....models.enums import AccessLevel, ContentStatus
    from ....models.user import UserRole

    allowed_access_levels = [AccessLevel.public]
    if current_user:
        role = current_user.get("role")
        role_value = role.value if hasattr(role, "value") else str(role).lower()

        if current_user.get("is_superuser") or role_value in {UserRole.admin.value, UserRole.premium.value}:
            allowed_access_levels = [AccessLevel.public, AccessLevel.registered, AccessLevel.premium]
        elif role_value == UserRole.registered.value:
            allowed_access_levels = [AccessLevel.public, AccessLevel.registered]

    # Build base query
    stmt = select(Dataset).where(
        Dataset.status == ContentStatus.published,
        Dataset.access_level.in_(allowed_access_levels),
    )

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        stmt = stmt.where(or_(Dataset.name.ilike(search_pattern), Dataset.description.ilike(search_pattern)))

    # Apply format filter
    if format:
        stmt = stmt.where(Dataset.format.ilike(f"%{format}%"))

    # Apply license filter
    if license:
        stmt = stmt.where(Dataset.license.ilike(f"%{license}%"))

    # Apply version filter
    if version:
        stmt = stmt.where(Dataset.version == version)

    # Apply category filter
    if category_id:
        stmt = stmt.join(DatasetCategoryLink, Dataset.id == DatasetCategoryLink.dataset_id).where(
            DatasetCategoryLink.category_id == category_id
        )

    # Apply sorting
    if sort_by == "oldest":
        stmt = stmt.order_by(asc(Dataset.created_at))
    elif sort_by == "name":
        stmt = stmt.order_by(asc(Dataset.name))
    else:  # latest (default)
        stmt = stmt.order_by(desc(Dataset.created_at))

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.alias())
    total_result = await db.execute(count_stmt)
    total_count = total_result.scalar() or 0

    # Apply pagination
    stmt = stmt.offset(offset).limit(limit)

    # Execute query
    result = await db.execute(stmt)
    datasets = result.scalars().all()

    # Convert to dict
    from sqlalchemy.inspection import inspect

    datasets_data = [
        {c.key: getattr(dataset, c.key) for c in inspect(dataset).mapper.column_attrs} for dataset in datasets
    ]

    return {
        "data": datasets_data,
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "has_more": (offset + limit) < total_count,
    }


@router.get("/featured", response_model=dict)
async def get_featured_datasets(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """Get featured datasets for homepage"""
    datasets = await crud_dataset.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
        is_featured=True,
    )

    return {"data": datasets.get("data", []), "total": len(datasets.get("data", []))}


@router.get("/latest", response_model=dict)
async def get_latest_datasets(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """Get latest datasets"""
    datasets = await crud_dataset.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
    )

    return {"data": datasets.get("data", []), "total": len(datasets.get("data", []))}


@router.get("/{dataset_id}", response_model=DatasetReadWithRelations)
async def get_public_dataset(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dataset_id: UUID,
) -> Any:
    """Get single dataset details"""
    dataset = await crud_dataset.get_with_relations(db=db, id=dataset_id)

    if not dataset:
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    if dataset.get("status") != "published" or dataset.get("access_level") != "public":
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    return dataset


@router.get("/slug/{slug}", response_model=DatasetReadWithRelations)
async def get_public_dataset_by_slug(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    slug: str,
) -> Any:
    """Get dataset by slug for SEO-friendly URLs"""
    from sqlalchemy import select

    from ....models.dataset import Dataset

    stmt = select(Dataset).where(Dataset.slug == slug, Dataset.status == "published", Dataset.access_level == "public")

    result = await db.execute(stmt)
    dataset_obj = result.scalar_one_or_none()

    if not dataset_obj:
        raise NotFoundException(f"Dataset with slug '{slug}' not found")

    dataset = await crud_dataset.get_with_relations(db=db, id=dataset_obj.id)
    return dataset


@router.post("/{dataset_id}/view")
async def increment_dataset_view(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dataset_id: UUID,
) -> Any:
    """
    Increment view count for a dataset

    - No authentication required
    - Only increments for published and public datasets
    - Returns updated view count
    """
    # First verify the dataset exists and is public/published
    dataset = await crud_dataset.get(db=db, id=dataset_id)

    if not dataset:
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    # Check if dataset is published and public (handle both string and enum)
    status = dataset.get("status")
    access_level = dataset.get("access_level")

    # Convert enum to string if needed
    if hasattr(status, "value"):
        status = status.value
    if hasattr(access_level, "value"):
        access_level = access_level.value

    if status != "published" or access_level != "public":
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    # Increment the view count
    success = await crud_dataset.increment_view_count(db=db, dataset_id=dataset_id)

    if not success:
        raise NotFoundException(f"Failed to increment view count for dataset {dataset_id}")

    # Get updated dataset to return new count
    updated_dataset = await crud_dataset.get(db=db, id=dataset_id)

    return {
        "detail": "View count incremented",
        "dataset_id": dataset_id,
        "view_count": updated_dataset.get("view_count", 0),
    }


@router.post("/{dataset_id}/download")
async def increment_dataset_download(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dataset_id: UUID,
) -> Any:
    """
    Increment download count for a dataset

    - No authentication required
    - Only increments for published and public datasets
    - Returns updated download count
    """
    # First verify the dataset exists and is public/published
    dataset = await crud_dataset.get(db=db, id=dataset_id)

    if not dataset:
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    # Check if dataset is published and public (handle both string and enum)
    status = dataset.get("status")
    access_level = dataset.get("access_level")

    # Convert enum to string if needed
    if hasattr(status, "value"):
        status = status.value
    if hasattr(access_level, "value"):
        access_level = access_level.value

    if status != "published" or access_level != "public":
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    # Increment the download count
    success = await crud_dataset.increment_download_count(db=db, dataset_id=dataset_id)

    if not success:
        raise NotFoundException(f"Failed to increment download count for dataset {dataset_id}")

    # Get updated dataset to return new count
    updated_dataset = await crud_dataset.get(db=db, id=dataset_id)

    return {
        "detail": "Download count incremented",
        "dataset_id": dataset_id,
        "download_count": updated_dataset.get("download_count", 0),
    }