"""
API endpoints for Projects
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_current_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ....crud.crud_projects import crud_project
from ....schemas.project import (
    ProjectBulkUpdate,
    ProjectCategoryAssignment,
    ProjectCreate,
    ProjectRead,
    ProjectReadWithRelations,
    ProjectUpdate,
)

router = APIRouter()


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    project_in: ProjectCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Create new project
    """
    # current_user is now guaranteed to exist (not None)
    # Add creator to the project data (handled in CRUD layer)

    project = await crud_project.create_with_categories(
        db=db, obj_in=project_in, created_by=current_user["id"], category_ids=category_ids
    )

    return project


@router.get("/", response_model=dict[str, Any])
async def read_projects(
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    creator_id: Annotated[UUID | None, Query(description="Filter by creator")] = None,
    access_level: Annotated[str | None, Query(description="Filter by access level")] = None,
    status: Annotated[str | None, Query(description="Filter by status")] = None,
    search: Annotated[str | None, Query(description="Search in title")] = None,
) -> Any:
    """
    Retrieve projects with filtering and pagination
    """

    # Apply filters based on parameters
    if search:
        return await crud_project.search_projects(db=db, query=search, skip=skip, limit=limit)
    elif creator_id:
        return await crud_project.get_by_creator(db=db, creator_id=creator_id, skip=skip, limit=limit)
    elif access_level:
        # For private projects, user must be authenticated
        if access_level == "private" and not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required for private content"
            )
        return await crud_project.get_by_access_level(db=db, access_level=access_level, skip=skip, limit=limit)
    elif status:
        return await crud_project.get_by_status(db=db, status=status, skip=skip, limit=limit)
    else:
        # Default: get all projects (might want to filter by public for unauthenticated users)
        return await crud_project.get_multi(db=db, offset=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectReadWithRelations)
async def read_project(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    project_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Get project by ID with all relations
    """
    project = await crud_project.get_with_relations(db=db, id=project_id)

    if not project:
        raise NotFoundException(f"Project with id {project_id} not found")

    # Check access permissions
    if project.access_level.value == "private":
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        if current_user["id"] != project.created_by and not current_user["is_superuser"]:
            raise ForbiddenException()

    # Convert SQLAlchemy object to Pydantic with relationships
    project_dict = {
        "id": project.id,
        "title": project.title,
        "slug": project.slug,
        "description": project.description,
        "full_description": project.full_description,
        "technologies": project.technologies,
        "challenges": project.challenges,
        "achievements": project.achievements,
        "future_work": project.future_work,
        "thumbnail_url": project.thumbnail_url,
        "demo_url": project.demo_url,
        "tags": project.tags,
        "complexity": project.complexity,
        "start_at": project.start_at,
        "access_level": project.access_level,
        "status": project.status,
        "created_by": project.created_by,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "categories": [link.category.name for link in project.category_links] if project.category_links else [],
        "creator_name": project.creator.name if project.creator else None,
    }

    return ProjectReadWithRelations(**project_dict)


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    project_id: UUID,
    project_in: ProjectUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Update project
    """
    project = await crud_project.get(db=db, id=project_id)

    if not project:
        raise NotFoundException(f"Project with id {project_id} not found")

    # Check permissions: only creator or superuser can update
    if current_user["id"] != project["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_project = await crud_project.update_with_categories(
        db=db, db_obj=project, obj_in=project_in, category_ids=category_ids
    )

    return updated_project


@router.delete("/{project_id}")
async def delete_project(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    project_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict[str, Any]:
    """
    Delete project with proper cascade handling
    """
    project = await crud_project.get(db=db, id=project_id)

    if not project:
        raise NotFoundException(f"Project with id {project_id} not found")

    # Check permissions: only creator or superuser can delete
    if current_user["id"] != project["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    # Use cascade delete to remove category links first
    deleted = await crud_project.delete_with_cascade(db=db, id=project_id)

    if deleted:
        return {"message": "Project deleted successfully"}
    else:
        raise NotFoundException(f"Project with id {project_id} not found")


@router.post("/{project_id}/categories", response_model=ProjectRead)
async def assign_project_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    project_id: UUID,
    assignment: ProjectCategoryAssignment,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Assign categories to project
    """
    project = await crud_project.get(db=db, id=project_id)

    if not project:
        raise NotFoundException(f"Project with id {project_id} not found")

    # Check permissions
    if current_user["id"] != project["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_project = await crud_project.update_with_categories(
        db=db, db_obj=project, obj_in=ProjectUpdate(), category_ids=assignment.category_ids
    )

    return updated_project


@router.patch("/bulk-update", response_model=dict[str, Any])
async def bulk_update_projects(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    bulk_update: ProjectBulkUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Bulk update projects (superuser only)
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_count = 0
    for project_id in bulk_update.project_ids:
        project = await crud_project.get(db=db, id=project_id)
        if project:
            await crud_project.update(db=db, object=bulk_update.updates.model_dump(exclude_unset=True), id=project_id)
            updated_count += 1

    return {"message": f"Updated {updated_count} projects"}
