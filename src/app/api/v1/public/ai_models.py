"""
Public API endpoints for AI Models
Frontend/Homepage endpoints - No authentication required
Only shows published and public AI models
"""

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....api.dependencies import get_optional_user
from ....core.db.database import async_get_db
from ....core.exceptions.http_exceptions import NotFoundException
from ....crud.crud_ai_models import crud_ai_model
from ....schemas.ai_models import AIModelReadWithRelations

router = APIRouter()


@router.get("/", response_model=dict)
async def get_public_ai_models(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    current_user: Annotated[dict | None, Depends(get_optional_user)] = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 12,
    search: Annotated[str | None, Query(max_length=255, description="Search in name and description")] = None,
    architecture: Annotated[
        str | None, Query(description="Filter by architecture (CNN, RNN, Transformer, etc)")
    ] = None,
    dataset_used: Annotated[str | None, Query(description="Filter by dataset used")] = None,
    category_id: Annotated[UUID | None, Query(description="Filter by category UUID")] = None,
    sort_by: Annotated[str | None, Query(description="Sort by: latest, oldest, name")] = "latest",
) -> Any:
    """
    Get public AI models for homepage/frontend

        - Authentication optional (Bearer token)
        - Access level by role:
            - Guest: public
            - registered: public + registered
            - premium/admin/superuser: public + registered + premium
    - Supports multiple filters

    Filters:
    - search: Search in name and description
    - architecture: CNN, RNN, Transformer, ResNet, YOLO, etc
    - dataset_used: Filter by dataset used for training
    - category_id: Filter by category UUID
    - sort_by: latest, oldest, name
    """
    from sqlalchemy import asc, desc, func, or_, select

    from ....models.ai_models import AIModel
    from ....models.categories import ModelCategoryLink
    from ....models.enums import AccessLevel, ContentStatus
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
    stmt = select(AIModel).where(
        AIModel.status == ContentStatus.published,
        AIModel.access_level.in_(allowed_access_levels),
    )

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        stmt = stmt.where(or_(AIModel.name.ilike(search_pattern), AIModel.description.ilike(search_pattern)))

    # Apply architecture filter
    if architecture:
        stmt = stmt.where(AIModel.architecture.ilike(f"%{architecture}%"))

    # Apply dataset filter
    if dataset_used:
        stmt = stmt.where(AIModel.dataset_used.ilike(f"%{dataset_used}%"))

    # Apply category filter
    if category_id:
        stmt = stmt.join(ModelCategoryLink, AIModel.id == ModelCategoryLink.model_id).where(
            ModelCategoryLink.category_id == category_id
        )

    # Apply sorting
    if sort_by == "oldest":
        stmt = stmt.order_by(asc(AIModel.created_at))
    elif sort_by == "name":
        stmt = stmt.order_by(asc(AIModel.name))
    else:  # latest (default)
        stmt = stmt.order_by(desc(AIModel.created_at))

    # Get total count
    count_stmt = select(func.count()).select_from(stmt.alias())
    total_result = await db.execute(count_stmt)
    total_count = total_result.scalar() or 0

    # Apply pagination
    stmt = stmt.offset(offset).limit(limit)

    # Execute query
    result = await db.execute(stmt)
    models = result.scalars().all()

    # Convert to dict
    from sqlalchemy.inspection import inspect

    models_data = [{c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs} for model in models]

    return {
        "data": models_data,
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "has_more": (offset + limit) < total_count,
    }


@router.get("/featured", response_model=dict)
async def get_featured_ai_models(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """Get featured AI models for homepage"""
    models = await crud_ai_model.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
    )

    return {"data": models.get("data", []), "total": len(models.get("data", []))}


@router.get("/latest", response_model=dict)
async def get_latest_ai_models(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
) -> Any:
    """Get latest AI models"""
    models = await crud_ai_model.get_multi(
        db=db,
        offset=0,
        limit=limit,
        status="published",
        access_level="public",
    )

    return {"data": models.get("data", []), "total": len(models.get("data", []))}


@router.get("/{model_id}", response_model=AIModelReadWithRelations)
async def get_public_ai_model(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    model_id: UUID,
) -> Any:
    """Get single AI model details"""
    model = await crud_ai_model.get_with_relations(db=db, id=model_id)

    if not model:
        raise NotFoundException(f"AI Model with id {model_id} not found")

    if model.get("status") != "published" or model.get("access_level") != "public":
        raise NotFoundException(f"AI Model with id {model_id} not found")

    return model


@router.get("/slug/{slug}", response_model=AIModelReadWithRelations)
async def get_public_ai_model_by_slug(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    slug: str,
) -> Any:
    """Get AI model by slug for SEO-friendly URLs"""
    from sqlalchemy import select

    from ....models.ai_models import AIModel

    stmt = select(AIModel).where(AIModel.slug == slug, AIModel.status == "published", AIModel.access_level == "public")

    result = await db.execute(stmt)
    model_obj = result.scalar_one_or_none()

    if not model_obj:
        raise NotFoundException(f"AI Model with slug '{slug}' not found")

    model = await crud_ai_model.get_with_relations(db=db, id=model_obj.id)
    return model