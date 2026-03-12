"""
API endpoints for Gallery
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_current_user, get_optional_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ....crud.crud_gallery import crud_gallery
from ....schemas.gallery import (
    GalleryBulkUpdate,
    GalleryCategoryAssignment,
    GalleryCreate,
    GalleryRead,
    GalleryReadWithRelations,
    GalleryUpdate,
)

router = APIRouter()


@router.post("/", response_model=GalleryRead, status_code=status.HTTP_201_CREATED)
async def create_gallery_item(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    gallery_in: GalleryCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Create new gallery item
    """
    gallery_item = await crud_gallery.create_with_categories(
        db=db, obj_in=gallery_in, created_by=current_user["id"], category_ids=category_ids
    )

    return gallery_item


@router.get("/", response_model=dict)
async def read_gallery(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(max_length=255)] = None,
    status_filter: Annotated[str | None, Query()] = None,
    media_type_filter: Annotated[str | None, Query()] = None,
) -> Any:
    """
    Retrieve gallery items with filtering and pagination
    """
    # Build filters
    filters = {}
    if search:
        filters["title__icontains"] = search
    if status_filter:
        filters["status"] = status_filter
    if media_type_filter:
        filters["media_type"] = media_type_filter

    # Add access level filtering for non-superusers
    if not current_user["is_superuser"]:
        # Show only public content and user's own content
        filters["or"] = [{"access_level": "public"}, {"created_by": current_user["id"]}]

    gallery_items = await crud_gallery.get_multi(db=db, offset=offset, limit=limit, **filters)

    total_count = await crud_gallery.count(db=db, **filters)

    return {"data": gallery_items, "total_count": total_count, "offset": offset, "limit": limit}


@router.get("/{gallery_id}", response_model=GalleryReadWithRelations)
async def read_gallery_item(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    gallery_id: UUID,
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
) -> Any:
    """
    Get gallery item by ID with all relations
    """
    gallery_item = await crud_gallery.get_with_relations(db=db, id=gallery_id)

    if not gallery_item:
        raise NotFoundException(f"Gallery item with id {gallery_id} not found")

    # Check access permissions - gallery_item is a dictionary
    if gallery_item.get("access_level") == "private":
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        if current_user["id"] != gallery_item["created_by"] and not current_user["is_superuser"]:
            raise ForbiddenException()

    return gallery_item


@router.put("/{gallery_id}", response_model=GalleryRead)
async def update_gallery_item(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    gallery_id: UUID,
    gallery_in: GalleryUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Update gallery item
    """
    gallery_item = await crud_gallery.get(db=db, id=gallery_id)

    if not gallery_item:
        raise NotFoundException(f"Gallery item with id {gallery_id} not found")

    # Check permissions: only creator or superuser can update
    if current_user["id"] != gallery_item["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_gallery_item = await crud_gallery.update_with_categories(
        db=db, gallery_item=gallery_item, obj_in=gallery_in, category_ids=category_ids
    )

    return updated_gallery_item


@router.delete("/{gallery_id}")
async def delete_gallery_item(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    gallery_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Delete gallery item with cascade delete
    """
    gallery_item = await crud_gallery.get(db=db, id=gallery_id)

    if not gallery_item:
        raise NotFoundException(f"Gallery item with id {gallery_id} not found")

    # Check permissions: only creator or superuser can delete
    if current_user["id"] != gallery_item["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    # Use cascade delete to remove category links first
    await crud_gallery.delete_with_cascade(db=db, id=gallery_id)

    return {"message": "Gallery item deleted successfully"}


@router.post("/{gallery_id}/categories", response_model=GalleryRead)
async def assign_categories_to_gallery_item(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    gallery_id: UUID,
    assignment: GalleryCategoryAssignment,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Assign categories to gallery item
    """
    gallery_item = await crud_gallery.get(db=db, id=gallery_id)

    if not gallery_item:
        raise NotFoundException(f"Gallery item with id {gallery_id} not found")

    # Check permissions
    if current_user["id"] != gallery_item["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_gallery_item = await crud_gallery.assign_categories(
        db=db, gallery_id=gallery_id, category_ids=assignment.category_ids
    )

    return updated_gallery_item


@router.patch("/bulk-update", response_model=dict)
async def bulk_update_gallery(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    bulk_update: GalleryBulkUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Bulk update gallery items
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException("Only superusers can perform bulk operations")

    result = await crud_gallery.bulk_update(
        db=db, ids=bulk_update.ids, update_data=bulk_update.update_data.model_dump(exclude_unset=True)
    )

    return {"detail": f"Successfully updated {result} gallery items", "updated_count": result}
