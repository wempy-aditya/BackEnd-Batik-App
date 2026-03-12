"""
API endpoints for News
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_current_user, get_optional_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ....crud.crud_news import crud_news
from ....schemas.news import (
    NewsBulkUpdate,
    NewsCategoryAssignment,
    NewsCreate,
    NewsRead,
    NewsReadWithRelations,
    NewsUpdate,
)

router = APIRouter()


@router.post("/", response_model=NewsRead, status_code=status.HTTP_201_CREATED)
async def create_news(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    news_in: NewsCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Create new news
    """
    news = await crud_news.create_with_categories(
        db=db, obj_in=news_in, created_by=current_user["id"], category_ids=category_ids
    )

    return news


@router.get("/", response_model=dict)
async def read_news(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(max_length=255)] = None,
    status_filter: Annotated[str | None, Query()] = None,
    priority_filter: Annotated[str | None, Query()] = None,
) -> Any:
    """
    Retrieve news with filtering and pagination
    """
    # Build filters
    filters = {}
    if search:
        filters["title__icontains"] = search
    if status_filter:
        filters["status"] = status_filter
    if priority_filter:
        filters["priority"] = priority_filter

    # Add access level filtering for non-superusers
    if not current_user["is_superuser"]:
        # Show only public content and user's own content
        filters["or"] = [{"access_level": "public"}, {"created_by": current_user["id"]}]

    news_items = await crud_news.get_multi(db=db, offset=offset, limit=limit, **filters)

    total_count = await crud_news.count(db=db, **filters)

    return {"data": news_items, "total_count": total_count, "offset": offset, "limit": limit}


@router.get("/{news_id}", response_model=NewsReadWithRelations)
async def read_news_item(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    news_id: UUID,
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
) -> Any:
    """
    Get news by ID with all relations
    """
    news = await crud_news.get_with_relations(db=db, id=news_id)

    if not news:
        raise NotFoundException(f"News with id {news_id} not found")

    # Check access permissions
    if news["access_level"] == "private":
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        if current_user["id"] != news["created_by"] and not current_user["is_superuser"]:
            raise ForbiddenException()

    return news


@router.put("/{news_id}", response_model=NewsRead)
async def update_news(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    news_id: UUID,
    news_in: NewsUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Update news
    """
    news = await crud_news.get(db=db, id=news_id)

    if not news:
        raise NotFoundException(f"News with id {news_id} not found")

    # Check permissions: only creator or superuser can update
    if current_user["id"] != news["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_news = await crud_news.update_with_categories(
        db=db,
        news=news,  # Changed from db_obj
        obj_in=news_in,
        category_ids=category_ids,
    )

    return updated_news


@router.delete("/{news_id}")
async def delete_news(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    news_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Delete news (soft delete)
    """
    news = await crud_news.get(db=db, id=news_id)

    if not news:
        raise NotFoundException(f"News with id {news_id} not found")

    # Check permissions: only creator or superuser can delete
    if current_user["id"] != news["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    await crud_news.delete(db=db, id=news["id"], is_deleted_column="is_deleted")

    return {"detail": "News deleted successfully"}


@router.post("/{news_id}/categories", response_model=NewsRead)
async def assign_categories_to_news(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    news_id: UUID,
    assignment: NewsCategoryAssignment,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Assign categories to news
    """
    news = await crud_news.get(db=db, id=news_id)

    if not news:
        raise NotFoundException(f"News with id {news_id} not found")

    # Check permissions
    if current_user["id"] != news["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_news = await crud_news.assign_categories(db=db, news_id=news_id, category_ids=assignment.category_ids)

    return updated_news


@router.patch("/bulk-update", response_model=dict)
async def bulk_update_news(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    bulk_update: NewsBulkUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Bulk update news
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException("Only superusers can perform bulk operations")

    result = await crud_news.bulk_update(
        db=db, ids=bulk_update.ids, update_data=bulk_update.update_data.model_dump(exclude_unset=True)
    )

    return {"detail": f"Successfully updated {result} news items", "updated_count": result}
