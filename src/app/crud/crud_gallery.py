"""
CRUD operations for Gallery model using FastCRUD
"""

from typing import Any
from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.gallery import Gallery
from ..schemas.gallery import GalleryCreate, GalleryUpdate


class CRUDGallery(FastCRUD):
    def __init__(self):
        super().__init__(Gallery)

    async def create_with_categories(
        self, db: AsyncSession, *, obj_in: GalleryCreate, created_by: UUID, category_ids: list[UUID] | None = None
    ) -> dict:
        """Create a gallery item with optional categories"""

        # Create the gallery item with created_by using direct SQLAlchemy
        from datetime import UTC, datetime

        from sqlalchemy import insert
        from uuid6 import uuid7

        # Get data as dict and add required fields
        gallery_data = obj_in.model_dump(exclude={"created_by"})
        gallery_data["id"] = uuid7()  # Generate UUID manually
        gallery_data["created_by"] = created_by
        gallery_data["created_at"] = datetime.now(UTC)  # Set timestamp

        # Insert directly using SQLAlchemy
        stmt = insert(Gallery).values(**gallery_data).returning(Gallery)
        result = await db.execute(stmt)
        gallery = result.scalar_one()
        await db.commit()
        await db.refresh(gallery)

        # Add categories if provided
        if category_ids:
            from ..models.categories import GalleryCategory

            for category_id in category_ids:
                # Check if category exists
                category_exists = await db.get(GalleryCategory, category_id)
                if category_exists:
                    # Create the link
                    link_stmt = text("""
                    INSERT INTO gallery_category_links (id, gallery_id, category_id, created_at)
                    VALUES (:id, :gallery_id, :category_id, :created_at)
                    ON CONFLICT (gallery_id, category_id) DO NOTHING
                    """)
                    await db.execute(
                        link_stmt,
                        {
                            "id": uuid7(),
                            "gallery_id": gallery.id,
                            "category_id": category_id,
                            "created_at": datetime.now(UTC),
                        },
                    )

            await db.commit()
            await db.refresh(gallery)

        # Convert to dict for return
        return {
            "id": gallery.id,
            "prompt": gallery.prompt,
            "image_url": gallery.image_url,
            "extra_metadata": gallery.extra_metadata,
            "model_id": gallery.model_id,
            "created_by": gallery.created_by,
            "created_at": gallery.created_at,
            "updated_at": gallery.updated_at,
        }

    async def get_with_relations(self, db: AsyncSession, id: UUID) -> dict | None:
        """Get gallery item with all related data (creator, categories)"""

        from sqlalchemy import select

        # Use direct SQLAlchemy query to properly load relationships
        from ..models.categories import GalleryCategoryLink

        stmt = (
            select(Gallery)
            .where(Gallery.id == id)
            .options(
                selectinload(Gallery.created_by_user),
                selectinload(Gallery.model),
                selectinload(Gallery.category_links).selectinload(GalleryCategoryLink.category),
            )
        )

        result = await db.execute(stmt)
        gallery = result.scalar_one_or_none()

        if not gallery:
            return None

        # Convert to dict and add categories manually
        gallery_dict = {
            "id": gallery.id,
            "prompt": gallery.prompt,
            "image_url": gallery.image_url,
            "extra_metadata": gallery.extra_metadata,
            "model_id": gallery.model_id,
            "created_by": gallery.created_by,
            "created_at": gallery.created_at,
            "updated_at": gallery.updated_at,
            "creator_name": gallery.created_by_user.name if gallery.created_by_user else None,
            "model_name": gallery.model.name if gallery.model else None,
            "categories": [link.category.name for link in gallery.category_links],
        }

        return gallery_dict

    async def get_by_creator(
        self, db: AsyncSession, creator_id: UUID, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get gallery items by creator with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, created_by=creator_id, schema_to_select=Gallery)

    async def get_by_access_level(
        self, db: AsyncSession, access_level: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get gallery items by access level with pagination"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, access_level=access_level, schema_to_select=Gallery
        )

    async def get_by_status(self, db: AsyncSession, status: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get gallery items by status with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, status=status, schema_to_select=Gallery)

    async def get_by_media_type(
        self, db: AsyncSession, media_type: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get gallery items by media type with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, media_type=media_type, schema_to_select=Gallery)

    async def get_featured_gallery(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get featured gallery items"""

        return await self.get_multi(db=db, offset=skip, limit=limit, is_featured=True, schema_to_select=Gallery)

    async def search_gallery(self, db: AsyncSession, query: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Search gallery items by title or description"""

        return await self.get_multi(db=db, offset=skip, limit=limit, title__icontains=query, schema_to_select=Gallery)

    async def update_with_categories(
        self,
        db: AsyncSession,
        *,
        gallery_item: dict,  # Changed from db_obj: Gallery
        obj_in: GalleryUpdate,
        category_ids: list[UUID] | None = None,
    ) -> dict:
        """Update gallery item and optionally update categories"""

        # Update the gallery item fields using direct UPDATE and fetch
        from datetime import UTC, datetime

        from sqlalchemy import select, update

        # Get update data excluding unset fields
        gallery_data = obj_in.model_dump(exclude={"category_ids"}, exclude_unset=True)

        if gallery_data:
            gallery_data["updated_at"] = datetime.now(UTC)

            # Update using SQLAlchemy update
            stmt = update(Gallery).where(Gallery.id == gallery_item["id"]).values(**gallery_data)
            await db.execute(stmt)
            await db.commit()

        # Fetch updated gallery
        select_stmt = select(Gallery).where(Gallery.id == gallery_item["id"])
        result = await db.execute(select_stmt)
        updated_gallery = result.scalar_one()

        # Update categories if provided
        if category_ids is not None:
            # Remove all existing category links
            delete_stmt = text("DELETE FROM gallery_category_links WHERE gallery_id = :gallery_id")
            await db.execute(delete_stmt, {"gallery_id": gallery_item["id"]})

            # Add new category links
            for category_id in category_ids:
                # Check if category exists
                from ..models.categories import GalleryCategory

                category_exists = await db.get(GalleryCategory, category_id)
                if category_exists:
                    from datetime import UTC, datetime

                    from uuid6 import uuid7

                    link_stmt = text("""
                    INSERT INTO gallery_category_links (id, gallery_id, category_id, created_at)
                    VALUES (:id, :gallery_id, :category_id, :created_at)
                    """)
                    await db.execute(
                        link_stmt,
                        {
                            "id": uuid7(),
                            "gallery_id": gallery_item["id"],
                            "category_id": category_id,
                            "created_at": datetime.now(UTC),
                        },
                    )

            await db.commit()
            await db.refresh(updated_gallery)

        # Convert to dict for return
        return {
            "id": updated_gallery.id,
            "prompt": updated_gallery.prompt,
            "image_url": updated_gallery.image_url,
            "extra_metadata": updated_gallery.extra_metadata,
            "model_id": updated_gallery.model_id,
            "created_by": updated_gallery.created_by,
            "created_at": updated_gallery.created_at,
            "updated_at": updated_gallery.updated_at,
        }

    async def assign_categories(self, db: AsyncSession, *, gallery_id: UUID, category_ids: list[UUID]) -> dict:
        """Assign categories to existing gallery item"""

        from datetime import UTC, datetime

        from sqlalchemy import select, text
        from uuid6 import uuid7

        # Get the gallery item first
        select_stmt = select(Gallery).where(Gallery.id == gallery_id)
        result = await db.execute(select_stmt)
        gallery = result.scalar_one_or_none()

        if not gallery:
            return None

        # Remove all existing category links for this gallery
        delete_stmt = text("DELETE FROM gallery_category_links WHERE gallery_id = :gallery_id")
        await db.execute(delete_stmt, {"gallery_id": gallery_id})

        # Add new category links
        for category_id in category_ids:
            # Check if category exists
            from ..models.categories import GalleryCategory

            category_exists = await db.get(GalleryCategory, category_id)
            if category_exists:
                link_stmt = text("""
                INSERT INTO gallery_category_links (id, gallery_id, category_id, created_at)
                VALUES (:id, :gallery_id, :category_id, :created_at)
                """)
                await db.execute(
                    link_stmt,
                    {
                        "id": uuid7(),
                        "gallery_id": gallery_id,
                        "category_id": category_id,
                        "created_at": datetime.now(UTC),
                    },
                )

        await db.commit()
        await db.refresh(gallery)

        # Convert to dict for return
        return {
            "id": gallery.id,
            "prompt": gallery.prompt,
            "image_url": gallery.image_url,
            "extra_metadata": gallery.extra_metadata,
            "model_id": gallery.model_id,
            "created_by": gallery.created_by,
            "created_at": gallery.created_at,
            "updated_at": gallery.updated_at,
        }

    async def delete_with_cascade(self, db: AsyncSession, *, id: UUID) -> bool:
        """Delete gallery item with cascade delete of foreign key references"""
        from sqlalchemy import select, text

        # Get the gallery item first
        select_stmt = select(Gallery).where(Gallery.id == id)
        result = await db.execute(select_stmt)
        gallery = result.scalar_one_or_none()

        if not gallery:
            return False

        # Delete category links first to avoid foreign key constraint
        delete_links_stmt = text("DELETE FROM gallery_category_links WHERE gallery_id = :gallery_id")
        await db.execute(delete_links_stmt, {"gallery_id": id})

        # Now delete the gallery item
        await db.delete(gallery)
        await db.commit()

        return True


# Create an instance
crud_gallery = CRUDGallery()
