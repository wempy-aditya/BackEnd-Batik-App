"""
Dashboard summary endpoint for admin users.
Returns aggregated statistics across all content tables.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import ForbiddenException
from ...models.ai_models import AIModel
from ...models.categories import (
    DatasetCategory,
    GalleryCategory,
    ModelCategory,
    NewsCategory,
    ProjectCategory,
    PublicationCategory,
)
from ...models.contributor import Contributor
from ...models.dataset import Dataset
from ...models.enums import AccessLevel, ContentStatus
from ...models.file import File
from ...models.gallery import Gallery
from ...models.news import News
from ...models.project import Project
from ...models.publication import Publication
from ...models.user import User, UserRole

router = APIRouter(tags=["dashboard"])


async def _count(db: AsyncSession, model: Any, **filters: Any) -> int:
    """Helper: count rows with optional filters."""
    stmt = select(func.count()).select_from(model)
    for col, val in filters.items():
        stmt = stmt.where(getattr(model, col) == val)
    result = await db.execute(stmt)
    return result.scalar_one()


async def _sum(db: AsyncSession, model: Any, column: str) -> int:
    """Helper: sum a numeric column."""
    stmt = select(func.coalesce(func.sum(getattr(model, column)), 0)).select_from(model)
    result = await db.execute(stmt)
    return result.scalar_one()


@router.get("/dashboard/summary")
async def get_dashboard_summary(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, Any]:
    """
    Dashboard summary statistics — hanya bisa diakses oleh admin atau superuser.
    Mengembalikan ringkasan data dari seluruh tabel di sistem.
    """
    # Hanya admin role atau superuser yang boleh akses
    user_role = current_user.get("role")
    is_superuser = current_user.get("is_superuser", False)
    if user_role not in ("admin", UserRole.admin) and not is_superuser:
        raise ForbiddenException("Only admin users can access the dashboard.")

    # ── USERS ────────────────────────────────────────────────
    total_users = await _count(db, User, is_deleted=False)
    active_users = await _count(db, User, is_deleted=False, is_active=True)
    inactive_users = await _count(db, User, is_deleted=False, is_active=False)
    admin_users = await _count(db, User, is_deleted=False, role=UserRole.admin)
    registered_users = await _count(db, User, is_deleted=False, role=UserRole.registered)
    premium_users = await _count(db, User, is_deleted=False, role=UserRole.premium)
    superusers = await _count(db, User, is_deleted=False, is_superuser=True)

    # New users this month
    new_users_month_result = await db.execute(
        text(
            "SELECT COUNT(*) FROM users WHERE is_deleted = false "
            "AND DATE_TRUNC('month', created_at) = DATE_TRUNC('month', NOW())"
        )
    )
    new_users_this_month = new_users_month_result.scalar_one()

    # ── PROJECTS ─────────────────────────────────────────────
    total_projects = await _count(db, Project)
    projects_published = await _count(db, Project, status=ContentStatus.published)
    projects_draft = await _count(db, Project, status=ContentStatus.draft)
    projects_public = await _count(db, Project, access_level=AccessLevel.public)
    projects_private = await _count(db, Project, access_level=AccessLevel.registered)

    # ── DATASETS ─────────────────────────────────────────────
    total_datasets = await _count(db, Dataset)
    datasets_published = await _count(db, Dataset, status=ContentStatus.published)
    datasets_draft = await _count(db, Dataset, status=ContentStatus.draft)
    total_dataset_views = await _sum(db, Dataset, "view_count")
    total_dataset_downloads = await _sum(db, Dataset, "download_count")

    # ── PUBLICATIONS ─────────────────────────────────────────
    total_publications = await _count(db, Publication)
    publications_published = await _count(db, Publication, status=ContentStatus.published)
    publications_draft = await _count(db, Publication, status=ContentStatus.draft)
    total_citations = await _sum(db, Publication, "citations")
    total_publication_views = await _sum(db, Publication, "view_count")
    total_publication_downloads = await _sum(db, Publication, "download_count")

    # ── NEWS ─────────────────────────────────────────────────
    total_news = await _count(db, News)
    news_published = await _count(db, News, status=ContentStatus.published)
    news_draft = await _count(db, News, status=ContentStatus.draft)

    # ── AI MODELS ────────────────────────────────────────────
    total_ai_models = await _count(db, AIModel)
    ai_models_published = await _count(db, AIModel, status=ContentStatus.published)
    ai_models_draft = await _count(db, AIModel, status=ContentStatus.draft)
    ai_models_public = await _count(db, AIModel, access_level=AccessLevel.public)
    ai_models_private = await _count(db, AIModel, access_level=AccessLevel.registered)

    # ── GALLERY ──────────────────────────────────────────────
    total_gallery = await _count(db, Gallery)

    # ── CONTRIBUTORS ─────────────────────────────────────────
    total_contributors = await _count(db, Contributor)

    # ── FILES ────────────────────────────────────────────────
    total_files = await _count(db, File)
    total_file_size_result = await db.execute(
        select(func.coalesce(func.sum(File.file_size), 0))
    )
    total_file_size_bytes = total_file_size_result.scalar_one()

    # ── CATEGORIES (total per domain) ────────────────────────
    total_project_categories = await _count(db, ProjectCategory)
    total_dataset_categories = await _count(db, DatasetCategory)
    total_publication_categories = await _count(db, PublicationCategory)
    total_news_categories = await _count(db, NewsCategory)
    total_model_categories = await _count(db, ModelCategory)
    total_gallery_categories = await _count(db, GalleryCategory)

    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "inactive": inactive_users,
            "new_this_month": new_users_this_month,
            "by_role": {
                "admin": admin_users,
                "registered": registered_users,
                "premium": premium_users,
                "superuser": superusers,
            },
        },
        "projects": {
            "total": total_projects,
            "by_status": {
                "published": projects_published,
                "draft": projects_draft,
            },
            "by_access": {
                "public": projects_public,
                "restricted": projects_private,
            },
        },
        "datasets": {
            "total": total_datasets,
            "by_status": {
                "published": datasets_published,
                "draft": datasets_draft,
            },
            "total_views": total_dataset_views,
            "total_downloads": total_dataset_downloads,
        },
        "publications": {
            "total": total_publications,
            "by_status": {
                "published": publications_published,
                "draft": publications_draft,
            },
            "total_citations": total_citations,
            "total_views": total_publication_views,
            "total_downloads": total_publication_downloads,
        },
        "news": {
            "total": total_news,
            "by_status": {
                "published": news_published,
                "draft": news_draft,
            },
        },
        "ai_models": {
            "total": total_ai_models,
            "by_status": {
                "published": ai_models_published,
                "draft": ai_models_draft,
            },
            "by_access": {
                "public": ai_models_public,
                "restricted": ai_models_private,
            },
        },
        "gallery": {
            "total": total_gallery,
        },
        "contributors": {
            "total": total_contributors,
        },
        "files": {
            "total": total_files,
            "total_size_bytes": total_file_size_bytes,
            "total_size_mb": round(total_file_size_bytes / (1024 * 1024), 2),
        },
        "categories": {
            "projects": total_project_categories,
            "datasets": total_dataset_categories,
            "publications": total_publication_categories,
            "news": total_news_categories,
            "ai_models": total_model_categories,
            "gallery": total_gallery_categories,
        },
    }
