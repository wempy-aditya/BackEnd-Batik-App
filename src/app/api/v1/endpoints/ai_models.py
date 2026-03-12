"""
API endpoints for AI Models
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_current_user, get_optional_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ....crud.crud_ai_models import crud_ai_model
from ....schemas.ai_models import (
    AIModelBulkUpdate,
    AIModelCategoryAssignment,
    AIModelCreate,
    AIModelRead,
    AIModelReadWithRelations,
    AIModelUpdate,
)

router = APIRouter()


@router.post("/", response_model=AIModelRead, status_code=status.HTTP_201_CREATED)
async def create_ai_model(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    ai_model_in: AIModelCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Create new AI model
    """
    ai_model = await crud_ai_model.create_with_categories(
        db=db, obj_in=ai_model_in, created_by=current_user["id"], category_ids=category_ids
    )

    return ai_model


@router.get("/", response_model=dict)
async def read_ai_models(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    search: Annotated[str | None, Query(max_length=255)] = None,
    status_filter: Annotated[str | None, Query()] = None,
    model_type_filter: Annotated[str | None, Query()] = None,
    framework_filter: Annotated[str | None, Query()] = None,
) -> Any:
    """
    Retrieve AI models with filtering and pagination
    """
    # Build filters
    filters = {}
    if search:
        filters["name__icontains"] = search
    if status_filter:
        filters["status"] = status_filter
    if model_type_filter:
        filters["model_type"] = model_type_filter
    if framework_filter:
        filters["framework__icontains"] = framework_filter

    # Add access level filtering for non-superusers
    if not current_user["is_superuser"]:
        # Show only public content and user's own content
        filters["or"] = [{"access_level": "public"}, {"created_by": current_user["id"]}]

    ai_models = await crud_ai_model.get_multi(db=db, offset=offset, limit=limit, **filters)

    total_count = await crud_ai_model.count(db=db, **filters)

    return {"data": ai_models, "total_count": total_count, "offset": offset, "limit": limit}


@router.get("/{ai_model_id}", response_model=AIModelReadWithRelations)
async def read_ai_model(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    ai_model_id: UUID,
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
) -> Any:
    """
    Get AI model by ID with all relations
    """
    ai_model = await crud_ai_model.get_with_relations(db=db, id=ai_model_id)

    if not ai_model:
        raise NotFoundException(f"AI Model with id {ai_model_id} not found")

    # Check access permissions
    if ai_model["access_level"] == "private":
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        if current_user["id"] != ai_model["created_by"] and not current_user["is_superuser"]:
            raise ForbiddenException()

    return ai_model


@router.put("/{ai_model_id}", response_model=AIModelRead)
async def update_ai_model(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    ai_model_id: UUID,
    ai_model_in: AIModelUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    category_ids: Annotated[list[UUID] | None, Query(description="Category IDs to assign")] = None,
) -> Any:
    """
    Update AI model
    """
    ai_model = await crud_ai_model.get(db=db, id=ai_model_id)

    if not ai_model:
        raise NotFoundException(f"AI Model with id {ai_model_id} not found")

    # Check permissions: only creator or superuser can update
    if current_user["id"] != ai_model["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_ai_model = await crud_ai_model.update_with_categories(
        db=db,
        ai_model=ai_model,  # Changed from db_obj
        obj_in=ai_model_in,
        category_ids=category_ids,
    )

    return updated_ai_model


@router.delete("/{ai_model_id}")
async def delete_ai_model(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    ai_model_id: UUID,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Delete AI model with proper cascade handling
    """
    ai_model = await crud_ai_model.get(db=db, id=ai_model_id)

    if not ai_model:
        raise NotFoundException(f"AI Model with id {ai_model_id} not found")

    # Check permissions: only creator or superuser can delete
    if current_user["id"] != ai_model["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    # Use cascade delete to remove category links and gallery items first
    deleted = await crud_ai_model.delete_with_cascade(db=db, id=ai_model_id)

    if deleted:
        return {"detail": "AI Model deleted successfully"}
    else:
        raise NotFoundException(f"AI Model with id {ai_model_id} not found")


@router.post("/{ai_model_id}/categories", response_model=AIModelRead)
async def assign_categories_to_ai_model(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    ai_model_id: UUID,
    assignment: AIModelCategoryAssignment,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Assign categories to AI model
    """
    ai_model = await crud_ai_model.get(db=db, id=ai_model_id)

    if not ai_model:
        raise NotFoundException(f"AI Model with id {ai_model_id} not found")

    # Check permissions - ai_model is already a dictionary
    if current_user["id"] != ai_model["created_by"] and not current_user["is_superuser"]:
        raise ForbiddenException()

    updated_ai_model = await crud_ai_model.assign_categories(
        db=db, ai_model_id=ai_model_id, category_ids=assignment.category_ids
    )

    return updated_ai_model


@router.patch("/bulk-update", response_model=dict)
async def bulk_update_ai_models(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    bulk_update: AIModelBulkUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Bulk update AI models
    """
    if not current_user["is_superuser"]:
        raise ForbiddenException("Only superusers can perform bulk operations")

    result = await crud_ai_model.bulk_update(
        db=db, ids=bulk_update.ids, update_data=bulk_update.update_data.model_dump(exclude_unset=True)
    )

    return {"detail": f"Successfully updated {result} AI models", "updated_count": result}
