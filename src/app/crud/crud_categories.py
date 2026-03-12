"""
CRUD operations for Category models using FastCRUD
"""

from typing import Any
from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.categories import (
    DatasetCategory,
    GalleryCategory,
    ModelCategory,
    NewsCategory,
    ProjectCategory,
    PublicationCategory,
)


class CRUDCategory(FastCRUD):
    def __init__(self, model: type):
        super().__init__(model)
        self.model = model

    async def get_by_parent(
        self, db: AsyncSession, parent_id: UUID | None = None, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get categories by parent with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, parent_id=parent_id)

    async def get_root_categories(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get root categories (no parent)"""

        return await self.get_multi(db=db, offset=skip, limit=limit, parent_id=None)

    async def get_active_categories(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get active categories only"""

        return await self.get_multi(db=db, offset=skip, limit=limit, is_active=True)

    async def search_categories(self, db: AsyncSession, query: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Search categories by name or description"""

        return await self.get_multi(db=db, offset=skip, limit=limit, name__icontains=query)

    async def get_category_with_content_count(self, db: AsyncSession, category_id: UUID) -> dict[str, Any] | None:
        """Get category with content count"""

        category = await self.get(db=db, id=category_id)

        if not category:
            return None

        # Count content based on category type
        content_count = 0
        table_name = ""

        if isinstance(category, ProjectCategory):
            table_name = "project_category_links"
        elif isinstance(category, DatasetCategory):
            table_name = "dataset_category_links"
        elif isinstance(category, PublicationCategory):
            table_name = "publication_category_links"
        elif isinstance(category, NewsCategory):
            table_name = "news_category_links"
        elif isinstance(category, ModelCategory):
            table_name = "model_category_links"
        elif isinstance(category, GalleryCategory):
            table_name = "gallery_category_links"

        if table_name:
            count_stmt = text(f"""
            SELECT COUNT(*) as count
            FROM {table_name}
            WHERE category_id = :category_id
            """)
            result = await db.execute(count_stmt, {"category_id": category_id})
            row = result.fetchone()
            content_count = row[0] if row else 0

        return {"category": category, "content_count": content_count}


# Create instances for each category type
crud_project_category = CRUDCategory(ProjectCategory)
crud_dataset_category = CRUDCategory(DatasetCategory)
crud_publication_category = CRUDCategory(PublicationCategory)
crud_news_category = CRUDCategory(NewsCategory)
crud_model_category = CRUDCategory(ModelCategory)
crud_gallery_category = CRUDCategory(GalleryCategory)
