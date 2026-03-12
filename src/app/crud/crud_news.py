"""
CRUD operations for News model using FastCRUD
"""

from typing import Any
from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.news import News
from ..schemas.news import NewsCreate, NewsUpdate


class CRUDNews(FastCRUD):
    def __init__(self):
        super().__init__(News)

    async def create_with_categories(
        self, db: AsyncSession, *, obj_in: NewsCreate, created_by: UUID, category_ids: list[UUID] | None = None
    ) -> News:
        """Create news with optional categories"""

        # Create the news with created_by using direct SQLAlchemy
        from datetime import UTC, datetime

        from sqlalchemy import insert
        from uuid6 import uuid7

        # Get data as dict and add required fields
        news_data = obj_in.model_dump()
        news_data["id"] = uuid7()  # Generate UUID manually
        news_data["created_by"] = created_by
        news_data["created_at"] = datetime.now(UTC)  # Set timestamp

        # Insert directly using SQLAlchemy
        stmt = insert(News).values(**news_data).returning(News)
        result = await db.execute(stmt)
        news = result.scalar_one()
        await db.commit()
        await db.refresh(news)

        # Add categories if provided
        if category_ids:
            from ..models.categories import NewsCategory

            for category_id in category_ids:
                # Check if category exists
                category_exists = await db.get(NewsCategory, category_id)
                if category_exists:
                    # Create the link
                    link_stmt = text("""
                    INSERT INTO news_category_links (id, news_id, category_id, created_at)
                    VALUES (:id, :news_id, :category_id, :created_at)
                    ON CONFLICT (news_id, category_id) DO NOTHING
                    """)
                    await db.execute(
                        link_stmt,
                        {
                            "id": uuid7(),
                            "news_id": news.id,
                            "category_id": category_id,
                            "created_at": datetime.now(UTC),
                        },
                    )

            await db.commit()
            await db.refresh(news)

        return news

    async def get_with_relations(self, db: AsyncSession, id: UUID) -> dict | None:
        """Get news with all related data (creator, categories)"""

        from sqlalchemy import select

        # Use direct SQLAlchemy query to properly load relationships
        stmt = (
            select(News)
            .where(News.id == id)
            .options(
                selectinload(News.creator),
                selectinload(News.category_links).selectinload(News.category_links.property.mapper.class_.category),
            )
        )

        result = await db.execute(stmt)
        news = result.scalar_one_or_none()

        if not news:
            return None

        # Convert to dict and add categories manually
        news_dict = {
            "id": news.id,
            "title": news.title,
            "slug": news.slug,
            "content": news.content,
            "thumbnail_url": news.thumbnail_url,
            "tags": news.tags,
            "access_level": news.access_level.value if hasattr(news.access_level, "value") else news.access_level,
            "status": news.status.value if hasattr(news.status, "value") else news.status,
            "created_by": news.created_by,
            "created_at": news.created_at,
            "updated_at": news.updated_at,
            "creator_name": news.creator.name if news.creator else None,
            "categories": [link.category.name for link in news.category_links],
        }

        return news_dict

    async def get_by_creator(
        self, db: AsyncSession, creator_id: UUID, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get news by creator with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, created_by=creator_id, schema_to_select=News)

    async def get_by_access_level(
        self, db: AsyncSession, access_level: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get news by access level with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, access_level=access_level, schema_to_select=News)

    async def get_by_status(self, db: AsyncSession, status: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get news by status with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, status=status, schema_to_select=News)

    async def get_published_news(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get published news ordered by publication date"""

        return await self.get_multi(
            db=db,
            offset=skip,
            limit=limit,
            status="published",
            schema_to_select=News,
            # Note: You might need to handle ordering differently with FastCRUD
        )

    async def get_by_author(
        self, db: AsyncSession, author_name: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get news by author name (contains search)"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, author__icontains=author_name, schema_to_select=News
        )

    async def search_news(self, db: AsyncSession, query: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Search news by title or content"""

        return await self.get_multi(db=db, offset=skip, limit=limit, title__icontains=query, schema_to_select=News)

    async def update_with_categories(
        self,
        db: AsyncSession,
        *,
        news: dict,  # Changed from db_obj: News
        obj_in: NewsUpdate,
        category_ids: list[UUID] | None = None,
    ) -> dict:
        """Update news and optionally update categories"""

        # Update the news fields using direct UPDATE and fetch
        from datetime import UTC, datetime

        from sqlalchemy import select, update

        # Get update data excluding unset fields
        news_data = obj_in.model_dump(exclude={"category_ids"}, exclude_unset=True)

        if news_data:
            news_data["updated_at"] = datetime.now(UTC)

            # Update using SQLAlchemy update
            stmt = update(News).where(News.id == news["id"]).values(**news_data)
            await db.execute(stmt)
            await db.commit()

        # Fetch updated news
        select_stmt = select(News).where(News.id == news["id"])
        result = await db.execute(select_stmt)
        updated_news = result.scalar_one()

        # Update categories if provided
        if category_ids is not None:
            # Remove all existing category links
            delete_stmt = text("DELETE FROM news_category_links WHERE news_id = :news_id")
            await db.execute(delete_stmt, {"news_id": news["id"]})

            # Add new category links
            for category_id in category_ids:
                # Check if category exists
                from ..models.categories import NewsCategory

                category_exists = await db.get(NewsCategory, category_id)
                if category_exists:
                    from datetime import UTC, datetime

                    from uuid6 import uuid7

                    link_stmt = text("""
                    INSERT INTO news_category_links (id, news_id, category_id, created_at)
                    VALUES (:id, :news_id, :category_id, :created_at)
                    """)
                    await db.execute(
                        link_stmt,
                        {
                            "id": uuid7(),
                            "news_id": news["id"],
                            "category_id": category_id,
                            "created_at": datetime.now(UTC),
                        },
                    )

            await db.commit()
            await db.refresh(updated_news)

        return updated_news

    async def assign_categories(self, db: AsyncSession, *, news_id: UUID, category_ids: list[UUID]) -> dict:
        """Assign categories to a news item"""

        from datetime import UTC, datetime

        from uuid6 import uuid7

        # First, remove all existing category links
        delete_stmt = text("DELETE FROM news_category_links WHERE news_id = :news_id")
        await db.execute(delete_stmt, {"news_id": news_id})

        # Add new category links
        for category_id in category_ids:
            # Check if category exists
            from ..models.categories import NewsCategory

            category_exists = await db.get(NewsCategory, category_id)
            if category_exists:
                link_stmt = text("""
                INSERT INTO news_category_links (id, news_id, category_id, created_at)
                VALUES (:id, :news_id, :category_id, :created_at)
                ON CONFLICT (news_id, category_id) DO NOTHING
                """)
                await db.execute(
                    link_stmt,
                    {"id": uuid7(), "news_id": news_id, "category_id": category_id, "created_at": datetime.now(UTC)},
                )

        await db.commit()

        # Return the updated news
        updated_news = await self.get(db=db, id=news_id)
        return updated_news

    async def delete(self, db: AsyncSession, *, id: UUID, **kwargs) -> None:
        """
        Delete news with cascade delete for category links

        First removes all category links, then deletes the news item
        """
        # Delete all category links first
        delete_links_stmt = text("DELETE FROM news_category_links WHERE news_id = :news_id")
        await db.execute(delete_links_stmt, {"news_id": id})

        # Now delete the news directly using SQLAlchemy DELETE statement
        from sqlalchemy import delete as sa_delete

        delete_stmt = sa_delete(News).where(News.id == id)
        await db.execute(delete_stmt)

        await db.commit()


# Create an instance
crud_news = CRUDNews()
