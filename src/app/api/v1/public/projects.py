"""
Public API endpoints for Projects
Frontend/Homepage endpoints - No authentication required
Only shows published and public projects
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_optional_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import NotFoundException
from ....crud.crud_projects import crud_project

router = APIRouter()


@router.get("/", response_model=dict)
async def get_public_projects(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 12,
    search: Annotated[str | None, Query(max_length=255, description="Search in title and description")] = None,
    category_id: Annotated[UUID | None, Query(description="Filter by category UUID")] = None,
    sort_by: Annotated[str | None, Query(description="Sort by: latest, oldest, title")] = "latest",
) -> Any:
    """
    Get public projects for homepage/frontend

        - Authentication optional (Bearer token)
        - Access level by role:
            - Guest: public
            - registered: public + registered
            - premium/admin/superuser: public + registered + premium
    - Supports search, category filter, and sorting
    - Pagination support

    Filters:
    - search: Search in title and description
    - category_id: Filter by category UUID
    - sort_by: latest (newest first), oldest, title (A-Z)
    """
    from sqlalchemy import asc, desc, func, or_, select

    from ....models.categories import ProjectCategoryLink
    from ....models.enums import AccessLevel, ContentStatus
    from ....models.project import Project
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
    stmt = select(Project).where(
        Project.status == ContentStatus.published,
        Project.access_level.in_(allowed_access_levels),
    )

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        stmt = stmt.where(or_(Project.title.ilike(search_pattern), Project.description.ilike(search_pattern)))

    # Apply category filter
    if category_id:
        stmt = stmt.join(ProjectCategoryLink, Project.id == ProjectCategoryLink.project_id).where(
            ProjectCategoryLink.category_id == category_id
        )

    # Apply sorting
    if sort_by == "oldest":
        stmt = stmt.order_by(asc(Project.created_at))
    elif sort_by == "title":
        stmt = stmt.order_by(asc(Project.title))
    else:  # latest (default)
        stmt = stmt.order_by(desc(Project.created_at))

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.alias())
    total_result = await db.execute(count_stmt)
    total_count = total_result.scalar() or 0

    # Apply pagination
    stmt = stmt.offset(offset).limit(limit)

    # Execute query
    result = await db.execute(stmt)
    projects = result.scalars().all()

    # Convert to dict
    from sqlalchemy.inspection import inspect

    projects_data = [
        {c.key: getattr(project, c.key) for c in inspect(project).mapper.column_attrs} for project in projects
    ]

    return {
        "data": projects_data,
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "has_more": (offset + limit) < total_count,
    }


@router.get("/featured", response_model=dict)
async def get_featured_projects(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """
    Get featured projects for homepage hero section

    - No authentication required
    - Shows only featured, published, public projects
    - Limited to small number for hero/featured section
    """
    projects = await crud_project.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
        is_featured=True,
    )

    return {"data": projects.get("data", []), "total": len(projects.get("data", []))}


@router.get("/latest", response_model=dict)
async def get_latest_projects(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """
    Get latest projects for homepage

    - No authentication required
    - Shows latest published public projects
    - Sorted by creation date (newest first)
    """

    # Custom query to get latest projects
    projects = await crud_project.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
    )

    return {"data": projects.get("data", []), "total": len(projects.get("data", []))}


@router.get("/{project_id}")
async def get_public_project(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    project_id: UUID,
) -> Any:
    """
    Get single project details for project detail page

    - No authentication required
    - Only shows published, public projects
    - Returns full project data
    """
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    from ....models.categories import ProjectCategoryLink
    from ....models.project import Project

    # Query with eager loading to avoid lazy load issues
    stmt = (
        select(Project)
        .options(
            selectinload(Project.creator),
            selectinload(Project.category_links).selectinload(ProjectCategoryLink.category),
        )
        .where(Project.id == project_id, Project.status == "published", Project.access_level == "public")
    )

    result = await db.execute(stmt)
    project = result.scalar_one_or_none()

    if not project:
        raise NotFoundException(f"Project with id {project_id} not found")

    # Serialize to dict within async context
    from sqlalchemy.inspection import inspect

    project_dict = {c.key: getattr(project, c.key) for c in inspect(project).mapper.column_attrs}

    # Add relations if loaded
    if project.creator:
        project_dict["creator"] = {
            "id": project.creator.id,
            "name": project.creator.name,
            "username": project.creator.username,
        }

    if project.category_links:
        project_dict["categories"] = [
            {
                "id": link.category.id,
                "name": link.category.name,
                "slug": link.category.slug,
            }
            for link in project.category_links
        ]

    return project_dict


@router.get("/slug/{slug}")
async def get_public_project_by_slug(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    slug: str,
) -> Any:
    """
    Get project by slug for SEO-friendly URLs

    - No authentication required
    - Only shows published, public projects
    - Example: /public/projects/slug/my-awesome-project
    """
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload

    from ....models.categories import ProjectCategoryLink
    from ....models.project import Project

    # Query with eager loading
    stmt = (
        select(Project)
        .options(
            selectinload(Project.creator),
            selectinload(Project.category_links).selectinload(ProjectCategoryLink.category),
        )
        .where(Project.slug == slug, Project.status == "published", Project.access_level == "public")
    )

    result = await db.execute(stmt)
    project = result.scalar_one_or_none()

    if not project:
        raise NotFoundException(f"Project with slug '{slug}' not found")

    # Serialize to dict within async context
    from sqlalchemy.inspection import inspect

    project_dict = {c.key: getattr(project, c.key) for c in inspect(project).mapper.column_attrs}

    # Add relations if loaded
    if project.creator:
        project_dict["creator"] = {
            "id": project.creator.id,
            "name": project.creator.name,
            "username": project.creator.username,
        }

    if project.category_links:
        project_dict["categories"] = [
            {
                "id": link.category.id,
                "name": link.category.name,
                "slug": link.category.slug,
            }
            for link in project.category_links
        ]

    return project_dict


@router.get("/category/{category_name}", response_model=dict)
async def get_projects_by_category(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    category_name: str,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 12,
) -> Any:
    """
    Get projects filtered by category

    - No authentication required
    - Only shows published, public projects
    - Filter by category name
    """
    # This would require a join with category table
    # For now, use the standard get_multi
    projects = await crud_project.get_multi(
        db=db,
        offset=offset,
        limit=limit,
        status="published",
        access_level="public",
    )

    # TODO: Implement proper category filtering with join
    # For now, return all public projects

    total_count = await crud_project.count(
        db=db,
        status="published",
        access_level="public",
    )

    return {
        "data": projects.get("data", []),
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "category": category_name,
    }