"""
Public API endpoints for News
Frontend/Homepage endpoints - No authentication required
Only shows published and public news
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_optional_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import NotFoundException
from ....crud.crud_news import crud_news
from ....schemas.news import NewsReadWithRelations

router = APIRouter()


@router.get("/", response_model=dict)
async def get_public_news(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 12,
    search: Annotated[str | None, Query(max_length=255, description="Search in title and content")] = None,
    category_id: Annotated[UUID | None, Query(description="Filter by category UUID")] = None,
    sort_by: Annotated[str | None, Query(description="Sort by: latest, oldest, title")] = "latest",
) -> Any:
    """
    Get public news for homepage/frontend

        - Authentication optional (Bearer token)
        - Access level by role:
            - Guest: public
            - registered: public + registered
            - premium/admin/superuser: public + registered + premium
    - Supports multiple filters

    Filters:
    - search: Search in title and content
    - category_id: Filter by category UUID
    - sort_by: latest (newest first), oldest, title
    """
    from sqlalchemy import asc, desc, func, or_, select

    from ....models.categories import NewsCategoryLink
    from ....models.enums import AccessLevel, ContentStatus
    from ....models.news import News
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
    stmt = select(News).where(
        News.status == ContentStatus.published,
        News.access_level.in_(allowed_access_levels),
    )

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        stmt = stmt.where(or_(News.title.ilike(search_pattern), News.content.ilike(search_pattern)))

    # Apply category filter
    if category_id:
        stmt = stmt.join(NewsCategoryLink, News.id == NewsCategoryLink.news_id).where(
            NewsCategoryLink.category_id == category_id
        )

    # Apply sorting
    if sort_by == "oldest":
        stmt = stmt.order_by(asc(News.created_at))
    elif sort_by == "title":
        stmt = stmt.order_by(asc(News.title))
    else:  # latest (default)
        stmt = stmt.order_by(desc(News.created_at))

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.alias())
    total_result = await db.execute(count_stmt)
    total_count = total_result.scalar() or 0

    # Apply pagination
    stmt = stmt.offset(offset).limit(limit)

    # Execute query
    result = await db.execute(stmt)
    news_items = result.scalars().all()

    # Convert to dict
    from sqlalchemy.inspection import inspect

    news_data = [{c.key: getattr(news, c.key) for c in inspect(news).mapper.column_attrs} for news in news_items]

    return {
        "data": news_data,
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "has_more": (offset + limit) < total_count,
    }


@router.get("/featured", response_model=dict)
async def get_featured_news(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """Get featured news for homepage"""
    news = await crud_news.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
        is_featured=True,
    )

    return {"data": news.get("data", []), "total": len(news.get("data", []))}


@router.get("/latest", response_model=dict)
async def get_latest_news(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """Get latest news - perfect for homepage news section"""
    news = await crud_news.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
    )

    return {"data": news.get("data", []), "total": len(news.get("data", []))}


@router.get("/{news_id}", response_model=NewsReadWithRelations)
async def get_public_news_item(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    news_id: UUID,
) -> Any:
    """Get single news details"""
    news = await crud_news.get_with_relations(db=db, id=news_id)

    if not news:
        raise NotFoundException(f"News with id {news_id} not found")

    if news.get("status") != "published" or news.get("access_level") != "public":
        raise NotFoundException(f"News with id {news_id} not found")

    return news


@router.get("/slug/{slug}", response_model=NewsReadWithRelations)
async def get_public_news_by_slug(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    slug: str,
) -> Any:
    """Get news by slug for SEO-friendly URLs"""
    from sqlalchemy import select

    from ....models.news import News

    stmt = select(News).where(News.slug == slug, News.status == "published", News.access_level == "public")

    result = await db.execute(stmt)
    news_obj = result.scalar_one_or_none()

    if not news_obj:
        raise NotFoundException(f"News with slug '{slug}' not found")

    news = await crud_news.get_with_relations(db=db, id=news_obj.id)
    return news