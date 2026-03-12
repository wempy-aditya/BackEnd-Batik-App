"""
API endpoints for Datasets
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_current_user, get_optional_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ....crud.crud_datasets import crud_dataset
from ....schemas.dataset import (
    DatasetBulkUpdate,
    DatasetCategoryAssignment,
    DatasetCreate,
    DatasetRead,
    DatasetReadWithRelations,
    DatasetUpdate,
)

router = APIRouter()


@router.post("/", response_model=DatasetRead, status_code=status.HTTP_201_CREATED)
async def create_dataset(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dataset_in: DatasetCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Create new dataset
    """
    dataset = await crud_dataset.create_with_categories(
        db=db, obj_in=dataset_in, created_by=current_user["id"], category_ids=category_ids
    )

    return dataset


@router.get("/", response_model=dict[str, Any])
async def read_datasets(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    creator_id: Annotated[UUID | None, Query(description="Filter by creator")] = None,
    access_level: Annotated[str | None, Query(description="Filter by access level")] = None,
    status: Annotated[str | None, Query(description="Filter by status")] = None,
    format_type: Annotated[str | None, Query(description="Filter by format")] = None,
    search: Annotated[str | None, Query(description="Search in title")] = None,
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
) -> Any:
    """
    Retrieve datasets with filtering and pagination
    """

    # Apply filters based on parameters
    if search:
        return await crud_dataset.search_datasets(db=db, query=search, skip=skip, limit=limit)
    elif creator_id:
        return await crud_dataset.get_by_creator(db=db, creator_id=creator_id, skip=skip, limit=limit)
    elif access_level:
        # For private datasets, user must be authenticated
        if access_level == "private" and not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required for private content"
            )
        return await crud_dataset.get_by_access_level(db=db, access_level=access_level, skip=skip, limit=limit)
    elif status:
        return await crud_dataset.get_by_status(db=db, status=status, skip=skip, limit=limit)
    elif format_type:
        return await crud_dataset.get_by_format(db=db, format_type=format_type, skip=skip, limit=limit)
    else:
        # Default: get all datasets
        return await crud_dataset.get_multi(db=db, offset=skip, limit=limit)


@router.get("/{dataset_id}", response_model=DatasetReadWithRelations)
async def read_dataset(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dataset_id: UUID,
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
) -> Any:
    """
    Get dataset by ID with all relations
    """
    dataset = await crud_dataset.get_with_relations(db=db, id=dataset_id)

    if not dataset:
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    # Check access permissions
    if dataset["access_level"] == "private":
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        if current_user["id"] != dataset["created_by"] and not current_user["is_superuser"]:
            raise ForbiddenException()

    return dataset


@router.patch("/{dataset_id}", response_model=DatasetRead)
async def update_dataset(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dataset_id: UUID,
    dataset_in: DatasetUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Update dataset
    """
    dataset = await crud_dataset.get(db=db, id=dataset_id)

    if not dataset:
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    # Check permissions: only creator or superuser can update
    if current_user["id"] != dataset["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_dataset = await crud_dataset.update_with_categories(
        db=db,
        dataset=dataset,  # Changed from db_obj
        obj_in=dataset_in,
        category_ids=category_ids,
    )

    return updated_dataset


@router.delete("/{dataset_id}")
async def delete_dataset(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dataset_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict[str, Any]:
    """
    Delete dataset with proper cascade handling
    """
    dataset = await crud_dataset.get(db=db, id=dataset_id)

    if not dataset:
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    # Check permissions: only creator or superuser can delete
    if current_user["id"] != dataset["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    # Use cascade delete to remove category links first
    deleted = await crud_dataset.delete_with_cascade(db=db, id=dataset_id)

    if deleted:
        return {"message": "Dataset deleted successfully"}
    else:
        raise NotFoundException(f"Dataset with id {dataset_id} not found")


@router.post("/{dataset_id}/categories", response_model=DatasetRead)
async def assign_dataset_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dataset_id: UUID,
    assignment: DatasetCategoryAssignment,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Assign categories to dataset
    """
    dataset = await crud_dataset.get(db=db, id=dataset_id)

    if not dataset:
        raise NotFoundException(f"Dataset with id {dataset_id} not found")

    # Check permissions
    if current_user["id"] != dataset["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_dataset = await crud_dataset.assign_categories(
        db=db, dataset_id=dataset_id, category_ids=assignment.category_ids
    )

    return updated_dataset


@router.patch("/bulk-update", response_model=dict[str, Any])
async def bulk_update_datasets(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    bulk_update: DatasetBulkUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Bulk update datasets (superuser only)
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_count = 0
    for dataset_id in bulk_update.dataset_ids:
        dataset = await crud_dataset.get(db=db, id=dataset_id)
        if dataset:
            await crud_dataset.update(db=db, object=bulk_update.updates.model_dump(exclude_unset=True), id=dataset_id)
            updated_count += 1

    return {"message": f"Updated {updated_count} datasets"}
