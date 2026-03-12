"""
Public API endpoints for Categories
Frontend/Homepage endpoints - No authentication required
Get categories for filtering and navigation
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ....core.db.database import async_get_db
from ....crud.crud_categories import (
    crud_dataset_category,
    crud_gallery_category,
    crud_model_category,
    crud_news_category,
    crud_project_category,
    crud_publication_category,
)

router = APIRouter()


@router.get("/projects", response_model=dict)
async def get_project_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> Any:
    """
    Get all project categories for filtering

    - No authentication required
    - Returns all active project categories
    - Useful for category filter dropdowns
    """
    categories = await crud_project_category.get_multi(
        db=db,
        offset=0,
        limit=limit,
    )

    return {"data": categories.get("data", []), "total": len(categories.get("data", []))}


@router.get("/datasets", response_model=dict)
async def get_dataset_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> Any:
    """Get all dataset categories"""
    categories = await crud_dataset_category.get_multi(
        db=db,
        offset=0,
        limit=limit,
    )

    return {"data": categories.get("data", []), "total": len(categories.get("data", []))}


@router.get("/publications", response_model=dict)
async def get_publication_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> Any:
    """Get all publication categories"""
    categories = await crud_publication_category.get_multi(
        db=db,
        offset=0,
        limit=limit,
    )

    return {"data": categories.get("data", []), "total": len(categories.get("data", []))}


@router.get("/news", response_model=dict)
async def get_news_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> Any:
    """Get all news categories"""
    categories = await crud_news_category.get_multi(
        db=db,
        offset=0,
        limit=limit,
    )

    return {"data": categories.get("data", []), "total": len(categories.get("data", []))}


@router.get("/models", response_model=dict)
async def get_model_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> Any:
    """Get all AI model categories"""
    categories = await crud_model_category.get_multi(
        db=db,
        offset=0,
        limit=limit,
    )

    return {"data": categories.get("data", []), "total": len(categories.get("data", []))}


@router.get("/gallery", response_model=dict)
async def get_gallery_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> Any:
    """Get all gallery categories"""
    categories = await crud_gallery_category.get_multi(
        db=db,
        offset=0,
        limit=limit,
    )

    return {"data": categories.get("data", []), "total": len(categories.get("data", []))}


@router.get("/all", response_model=dict)
async def get_all_categories(
    *,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> Any:
    """
    Get all categories grouped by type

    - Useful for initializing frontend category filters
    - Returns all category types in one call
    """
    result = {
        "projects": (await crud_project_category.get_multi(db=db, offset=0, limit=50)).get("data", []),
        "datasets": (await crud_dataset_category.get_multi(db=db, offset=0, limit=50)).get("data", []),
        "publications": (await crud_publication_category.get_multi(db=db, offset=0, limit=50)).get("data", []),
        "news": (await crud_news_category.get_multi(db=db, offset=0, limit=50)).get("data", []),
        "models": (await crud_model_category.get_multi(db=db, offset=0, limit=50)).get("data", []),
        "gallery": (await crud_gallery_category.get_multi(db=db, offset=0, limit=50)).get("data", []),
    }

    return result
