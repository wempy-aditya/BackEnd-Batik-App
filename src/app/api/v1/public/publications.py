"""
Public API endpoints for Publications
Frontend/Homepage endpoints - No authentication required
Only shows published and public publications
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import NotFoundException
from ....crud.crud_publications import crud_publication

router = APIRouter()


@router.get("/", response_model=dict)
async def get_public_publications(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 12,
    search: Annotated[str | None, Query(max_length=255, description="Search in title, authors, and abstract")] = None,
    year: Annotated[int | None, Query(ge=1900, le=2100, description="Filter by publication year")] = None,
    category_id: Annotated[UUID | None, Query(description="Filter by category UUID")] = None,
    author: Annotated[str | None, Query(description="Filter by author name")] = None,
    sort_by: Annotated[str | None, Query(description="Sort by: latest, oldest, title, year")] = "latest",
) -> Any:
    """
    Get public publications for homepage/frontend

    - No authentication required
    - Only shows published publications with public access
    - Supports multiple filters

    Filters:
    - search: Search in title, authors, and abstract
    - year: Publication year (e.g., 2024)
    - category_id: Filter by category UUID
    - author: Filter by author name (partial match)
    - sort_by: latest, oldest, title, year (newest first)
    """
    from sqlalchemy import asc, desc, func, or_, select

    from ....models.categories import PublicationCategoryLink
    from ....models.publication import Publication

    # Build base query
    stmt = select(Publication).where(Publication.status == "published", Publication.access_level == "public")

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        stmt = stmt.where(or_(Publication.title.ilike(search_pattern), Publication.abstract.ilike(search_pattern)))

    # Apply year filter
    if year:
        stmt = stmt.where(Publication.year == year)

    # Apply author filter (search in authors array)
    if author:
        from sqlalchemy import String, cast

        # Use PostgreSQL array operator to search in array
        stmt = stmt.where(cast(Publication.authors, String).ilike(f"%{author}%"))

    # Apply category filter
    if category_id:
        stmt = stmt.join(PublicationCategoryLink, Publication.id == PublicationCategoryLink.publication_id).where(
            PublicationCategoryLink.category_id == category_id
        )

    # Apply sorting
    if sort_by == "oldest":
        stmt = stmt.order_by(asc(Publication.created_at))
    elif sort_by == "title":
        stmt = stmt.order_by(asc(Publication.title))
    elif sort_by == "year":
        stmt = stmt.order_by(desc(Publication.year))
    else:  # latest (default)
        stmt = stmt.order_by(desc(Publication.created_at))

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.alias())
    total_result = await db.execute(count_stmt)
    total_count = total_result.scalar() or 0

    # Apply pagination
    stmt = stmt.offset(offset).limit(limit)

    # Execute query
    result = await db.execute(stmt)
    publications = result.scalars().all()

    # Convert to dict
    from sqlalchemy.inspection import inspect

    publications_data = [{c.key: getattr(pub, c.key) for c in inspect(pub).mapper.column_attrs} for pub in publications]

    return {
        "data": publications_data,
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "has_more": (offset + limit) < total_count,
    }


@router.get("/featured", response_model=dict)
async def get_featured_publications(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """Get featured publications for homepage"""
    publications = await crud_publication.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
        is_featured=True,
    )

    return {"data": publications.get("data", []), "total": len(publications.get("data", []))}


@router.get("/latest", response_model=dict)
async def get_latest_publications(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """Get latest publications"""
    publications = await crud_publication.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
    )

    return {"data": publications.get("data", []), "total": len(publications.get("data", []))}


@router.get("/year/{year}", response_model=dict)
async def get_publications_by_year(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    year: int,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Any:
    """
    Get publications by publication year

    - No authentication required
    - Filter by specific year
    - Example: /public/publications/year/2024
    """
    publications = await crud_publication.get_multi(
        db=db,
        offset=offset,
        limit=limit,
        status="published",
        access_level="public",
        year=year,
    )

    total_count = await crud_publication.count(
        db=db,
        status="published",
        access_level="public",
        year=year,
    )

    return {
        "data": publications.get("data", []),
        "total": total_count,
        "year": year,
        "offset": offset,
        "limit": limit,
        "has_more": (offset + limit) < total_count,
    }


@router.get("/{publication_id}")
async def get_public_publication(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    publication_id: UUID,
) -> Any:
    """Get single publication details"""
    from sqlalchemy import select

    from ....models.publication import Publication

    stmt = select(Publication).where(
        Publication.id == publication_id, Publication.status == "published", Publication.access_level == "public"
    )

    result = await db.execute(stmt)
    publication = result.scalar_one_or_none()

    if not publication:
        raise NotFoundException(f"Publication with id {publication_id} not found")

    # Convert to dict to avoid lazy loading issues
    from sqlalchemy.inspection import inspect

    return {c.key: getattr(publication, c.key) for c in inspect(publication).mapper.column_attrs}


@router.get("/slug/{slug}")
async def get_public_publication_by_slug(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    slug: str,
) -> Any:
    """Get publication by slug for SEO-friendly URLs"""
    from sqlalchemy import select

    from ....models.publication import Publication

    stmt = select(Publication).where(
        Publication.slug == slug, Publication.status == "published", Publication.access_level == "public"
    )

    result = await db.execute(stmt)
    publication = result.scalar_one_or_none()

    if not publication:
        raise NotFoundException(f"Publication with slug '{slug}' not found")

    # Convert to dict to avoid lazy loading issues
    from sqlalchemy.inspection import inspect

    return {c.key: getattr(publication, c.key) for c in inspect(publication).mapper.column_attrs}


@router.post("/{publication_id}/view")
async def increment_publication_view(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    publication_id: UUID,
) -> Any:
    """
    Increment view count for a publication

    - No authentication required
    - Call this when user visits publication detail page
    """
    # Check if publication exists and is public
    from sqlalchemy import select

    from ....models.publication import Publication

    stmt = select(Publication).where(
        Publication.id == publication_id, Publication.status == "published", Publication.access_level == "public"
    )

    result = await db.execute(stmt)
    publication = result.scalar_one_or_none()

    if not publication:
        raise NotFoundException(f"Publication with id {publication_id} not found")

    # Increment view count
    success = await crud_publication.increment_view_count(db, publication_id)

    if success:
        return {
            "detail": "View count incremented",
            "publication_id": publication_id,
            "view_count": publication.view_count + 1,
        }
    else:
        return {"detail": "Failed to increment view count"}


@router.post("/{publication_id}/download")
async def increment_publication_download(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    publication_id: UUID,
) -> Any:
    """
    Increment download count for a publication

    - No authentication required
    - Call this when user downloads publication PDF
    """
    # Check if publication exists and is public
    from sqlalchemy import select

    from ....models.publication import Publication

    stmt = select(Publication).where(
        Publication.id == publication_id, Publication.status == "published", Publication.access_level == "public"
    )

    result = await db.execute(stmt)
    publication = result.scalar_one_or_none()

    if not publication:
        raise NotFoundException(f"Publication with id {publication_id} not found")

    # Increment download count
    success = await crud_publication.increment_download_count(db, publication_id)

    if success:
        return {
            "detail": "Download count incremented",
            "publication_id": publication_id,
            "download_count": publication.download_count + 1,
        }
    else:
        return {"detail": "Failed to increment download count"}
