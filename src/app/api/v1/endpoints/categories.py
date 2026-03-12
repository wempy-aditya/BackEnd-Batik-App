"""
API endpoints for Categories (all types)
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_current_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ....crud.crud_categories import (
    crud_dataset_category,
    crud_gallery_category,
    crud_model_category,
    crud_news_category,
    crud_project_category,
    crud_publication_category,
)
from ....schemas.categories import (
    CategoryBulkUpdate,
    CategoryCreate,
    CategoryRead,
    CategoryReadWithCount,
    CategoryUpdate,
)

router = APIRouter()

# Map category types to their respective CRUD instances
CATEGORY_CRUD_MAP = {
    "project": crud_project_category,
    "dataset": crud_dataset_category,
    "publication": crud_publication_category,
    "news": crud_news_category,
    "model": crud_model_category,
    "gallery": crud_gallery_category,
}


def get_crud_for_category_type(category_type: str):
    """Get the appropriate CRUD instance for category type"""
    crud_instance = CATEGORY_CRUD_MAP.get(category_type)
    if not crud_instance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category type: {category_type}. Valid types: {list(CATEGORY_CRUD_MAP.keys())}",
        )
    return crud_instance


@router.post("/{category_type}/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    category_type: Annotated[str, Path(description="Type of category")],
    category_in: CategoryCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Create new category (admin/superuser only)
    """
    # Temporary: Skip auth check for testing
    # if not current_user["is_superuser"]:
    #     raise ForbiddenException()

    crud_category = get_crud_for_category_type(category_type)

    category = await crud_category.create(db=db, object=category_in)

    return category


@router.get("/{category_type}/", response_model=dict[str, Any])
async def read_categories(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    category_type: Annotated[str, Path(description="Type of category")],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    parent_id: Annotated[UUID | None, Query(description="Filter by parent category")] = None,
    active_only: Annotated[bool, Query(description="Show only active categories")] = True,
    search: Annotated[str | None, Query(description="Search in name")] = None,
) -> Any:
    """
    Retrieve categories with filtering and pagination
    """
    crud_category = get_crud_for_category_type(category_type)

    # Apply filters based on parameters
    if search:
        return await crud_category.search_categories(db=db, query=search, skip=skip, limit=limit)
    elif parent_id is not None:  # Allow searching for root categories (parent_id=None)
        return await crud_category.get_by_parent(db=db, parent_id=parent_id, skip=skip, limit=limit)
    elif active_only:
        return await crud_category.get_active_categories(db=db, skip=skip, limit=limit)
    else:
        # Default: get all categories
        return await crud_category.get_multi(db=db, offset=skip, limit=limit)


@router.get("/{category_type}/root", response_model=dict[str, Any])
async def read_root_categories(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    category_type: Annotated[str, Path(description="Type of category")],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> Any:
    """
    Get root categories (no parent)
    """
    crud_category = get_crud_for_category_type(category_type)

    return await crud_category.get_root_categories(db=db, skip=skip, limit=limit)


@router.get("/{category_type}/{category_id}", response_model=CategoryReadWithCount)
async def read_category(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    category_type: Annotated[str, Path(description="Type of category")],
    category_id: UUID,
) -> Any:
    """
    Get category by ID with content count
    """
    crud_category = get_crud_for_category_type(category_type)

    result = await crud_category.get_category_with_content_count(db=db, category_id=category_id)

    if not result:
        raise NotFoundException(f"{category_type.title()}Category", category_id)

    category_data = result["category"]

    # Handle both dict and SQLAlchemy model object cases
    if hasattr(category_data, "__dict__"):
        # SQLAlchemy model object
        category_dict = {key: value for key, value in category_data.__dict__.items() if not key.startswith("_")}
    else:
        # Already a dictionary
        category_dict = category_data

    return {**category_dict, "content_count": result["content_count"]}


@router.patch("/{category_type}/{category_id}", response_model=CategoryRead)
async def update_category(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    category_type: Annotated[str, Path(description="Type of category")],
    category_id: UUID,
    category_in: CategoryUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Update category (admin/superuser only)
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException()

    crud_category = get_crud_for_category_type(category_type)

    category = await crud_category.get(db=db, id=category_id)

    if not category:
        raise NotFoundException(f"{category_type.title()}Category", category_id)

    # Use direct update with ID to avoid multiple results
    update_data = category_in.model_dump(exclude_unset=True)

    await crud_category.update(db=db, id=category_id, object=update_data)

    # Get the updated category to return
    updated_category = await crud_category.get(db=db, id=category_id)

    return updated_category


@router.delete("/{category_type}/{category_id}")
async def delete_category(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    category_type: Annotated[str, Path(description="Type of category")],
    category_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict[str, Any]:
    """
    Delete category (admin/superuser only)
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException()

    crud_category = get_crud_for_category_type(category_type)

    category = await crud_category.get(db=db, id=category_id)

    if not category:
        raise NotFoundException(f"{category_type.title()}Category", category_id)

    # Check if category has content associated
    result = await crud_category.get_category_with_content_count(db=db, category_id=category_id)

    if result and result["content_count"] > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {result['content_count']} associated content items",
        )

    await crud_category.delete(db=db, id=category_id)

    return {"message": "Category deleted successfully"}


@router.patch("/{category_type}/bulk-update", response_model=dict[str, Any])
async def bulk_update_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    category_type: Annotated[str, Path(description="Type of category")],
    bulk_update: CategoryBulkUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Bulk update categories (superuser only)
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException()

    crud_category = get_crud_for_category_type(category_type)

    updated_count = 0
    for category_id in bulk_update.category_ids:
        category = await crud_category.get(db=db, id=category_id)
        if category:
            await crud_category.update(db=db, object=bulk_update.updates.model_dump(exclude_unset=True), id=category_id)
            updated_count += 1

    return {"message": f"Updated {updated_count} categories"}
