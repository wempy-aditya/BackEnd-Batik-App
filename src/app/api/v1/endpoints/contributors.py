"""
API endpoints for Contributors
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_current_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ....crud.crud_contributor import crud_contributor
from ....schemas.contributor import ContributorAssignment, ContributorCreate, ContributorRead, ContributorUpdate

router = APIRouter()


@router.post("/", response_model=ContributorRead, status_code=status.HTTP_201_CREATED)
async def create_contributor(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    contributor_in: ContributorCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Create new contributor
    Only superusers can create contributors
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException("Only superusers can create contributors")

    contributor = await crud_contributor.create(db=db, object=contributor_in)
    return contributor


@router.get("/", response_model=dict)
async def read_contributors(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    search: Annotated[str | None, Query(max_length=255)] = None,
) -> Any:
    """
    Get all contributors with pagination
    Public endpoint - no authentication required
    """
    filters = {}
    if search:
        filters["name__icontains"] = search

    contributors = await crud_contributor.get_multi(db=db, offset=offset, limit=limit, **filters)

    total_count = await crud_contributor.count(db=db, **filters)

    return {"data": contributors.get("data", []), "total": total_count, "offset": offset, "limit": limit}


@router.get("/{contributor_id}", response_model=dict)
async def read_contributor(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    contributor_id: UUID,
) -> Any:
    """
    Get contributor by ID with contribution stats
    Public endpoint
    """
    contributor = await crud_contributor.get_with_stats(db=db, id=contributor_id)

    if not contributor:
        raise NotFoundException(f"Contributor with id {contributor_id} not found")

    return contributor


@router.put("/{contributor_id}", response_model=ContributorRead)
async def update_contributor(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    contributor_id: UUID,
    contributor_in: ContributorUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Update contributor
    Only superusers can update
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException("Only superusers can update contributors")

    contributor = await crud_contributor.get(db=db, id=contributor_id)

    if not contributor:
        raise NotFoundException(f"Contributor with id {contributor_id} not found")

    await crud_contributor.update(db=db, object=contributor_in, id=contributor_id)

    # Get the updated contributor to return
    updated_contributor = await crud_contributor.get(db=db, id=contributor_id)

    return updated_contributor


@router.delete("/{contributor_id}")
async def delete_contributor(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    contributor_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Delete contributor
    Only superusers can delete
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException("Only superusers can delete contributors")

    contributor = await crud_contributor.get(db=db, id=contributor_id)

    if not contributor:
        raise NotFoundException(f"Contributor with id {contributor_id} not found")

    await crud_contributor.delete(db=db, id=contributor_id)

    return {"detail": "Contributor deleted successfully"}


# Assignment endpoints
@router.post("/assign/project/{project_id}")
async def assign_to_project(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    project_id: UUID,
    assignment: ContributorAssignment,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """Assign contributors to a project"""

    if not current_user["is_superuser"]:
        raise ForbiddenException("Only superusers can assign contributors")

    for i, contributor_id in enumerate(assignment.contributor_ids):
        role = None
        if assignment.roles and i < len(assignment.roles):
            role = assignment.roles[i]

        await crud_contributor.assign_to_project(
            db=db, project_id=project_id, contributor_id=contributor_id, role_in_project=role
        )

    return {"detail": f"Assigned {len(assignment.contributor_ids)} contributors to project"}


@router.get("/project/{project_id}/contributors")
async def get_project_contributors(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    project_id: UUID,
) -> Any:
    """Get all contributors for a project - Public endpoint"""

    contributors = await crud_contributor.get_project_contributors(db=db, project_id=project_id)

    return {"data": contributors, "total": len(contributors)}
