"""
API endpoints for Publications
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_current_user, get_optional_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ....crud.crud_publications import crud_publication
from ....schemas.publication import (
    PublicationBulkUpdate,
    PublicationCategoryAssignment,
    PublicationCreate,
    PublicationRead,
    PublicationReadWithRelations,
    PublicationUpdate,
)

router = APIRouter()


@router.post("/", response_model=PublicationRead, status_code=status.HTTP_201_CREATED)
async def create_publication(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    publication_in: PublicationCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Create new publication
    """
    publication = await crud_publication.create_with_categories(
        db=db, obj_in=publication_in, created_by=current_user["id"], category_ids=category_ids
    )

    return publication


@router.get("/", response_model=dict)
async def read_publications(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(max_length=255)] = None,
    status_filter: Annotated[str | None, Query()] = None,
    year_filter: Annotated[int | None, Query(ge=1900, le=2100)] = None,
    journal_filter: Annotated[str | None, Query()] = None,
) -> Any:
    """
    Retrieve publications with filtering and pagination
    """
    # Build filters
    filters = {}
    if search:
        filters["title__icontains"] = search
    if status_filter:
        filters["status"] = status_filter
    if year_filter:
        filters["year"] = year_filter
    if journal_filter:
        filters["journal_name__icontains"] = journal_filter

    # Add access level filtering for non-superusers
    if not current_user["is_superuser"]:
        # Show only public content and user's own content
        filters["or"] = [{"access_level": "public"}, {"created_by": current_user["id"]}]

    publications = await crud_publication.get_multi(db=db, offset=offset, limit=limit, **filters)

    total_count = await crud_publication.count(db=db, **filters)

    return {"data": publications, "total_count": total_count, "offset": offset, "limit": limit}


@router.get("/{publication_id}", response_model=PublicationReadWithRelations)
async def read_publication(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    publication_id: UUID,
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
) -> Any:
    """
    Get publication by ID with all relations
    """
    publication = await crud_publication.get_with_relations(db=db, id=publication_id)

    if not publication:
        raise NotFoundException(f"Publication with id {publication_id} not found")

    # Check access permissions
    if publication["access_level"] == "private":
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        if current_user["id"] != publication["created_by"] and not current_user["is_superuser"]:
            raise ForbiddenException()

    return publication


@router.put("/{publication_id}", response_model=PublicationRead)
async def update_publication(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    publication_id: UUID,
    publication_in: PublicationUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Update publication
    """
    publication = await crud_publication.get(db=db, id=publication_id)

    if not publication:
        raise NotFoundException(f"Publication with id {publication_id} not found")

    # Check permissions: only creator or superuser can update
    if current_user["id"] != publication["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_publication = await crud_publication.update_with_categories(
        db=db,
        publication=publication,  # Changed from db_obj
        obj_in=publication_in,
        category_ids=category_ids,
    )

    return updated_publication


@router.delete("/{publication_id}")
async def delete_publication(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    publication_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Delete publication with proper cascade handling
    """
    publication = await crud_publication.get(db=db, id=publication_id)

    if not publication:
        raise NotFoundException(f"Publication with id {publication_id} not found")

    # Check permissions: only creator or superuser can delete
    if current_user["id"] != publication["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    # Use cascade delete to remove category links first
    deleted = await crud_publication.delete_with_cascade(db=db, id=publication_id)

    if deleted:
        return {"detail": "Publication deleted successfully"}
    else:
        raise NotFoundException(f"Publication with id {publication_id} not found")


@router.post("/{publication_id}/categories", response_model=PublicationRead)
async def assign_categories_to_publication(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    publication_id: UUID,
    assignment: PublicationCategoryAssignment,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Assign categories to publication
    """
    publication = await crud_publication.get(db=db, id=publication_id)

    if not publication:
        raise NotFoundException(f"Publication with id {publication_id} not found")

    # Check permissions
    if current_user["id"] != publication["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_publication = await crud_publication.assign_categories(
        db=db, publication_id=publication_id, category_ids=assignment.category_ids
    )

    return updated_publication


@router.patch("/bulk-update", response_model=dict)
async def bulk_update_publications(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    bulk_update: PublicationBulkUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Bulk update publications
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException("Only superusers can perform bulk operations")

    result = await crud_publication.bulk_update(
        db=db, ids=bulk_update.ids, update_data=bulk_update.update_data.model_dump(exclude_unset=True)
    )

    return {"detail": f"Successfully updated {result} publications", "updated_count": result}
