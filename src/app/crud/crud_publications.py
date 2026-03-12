"""
CRUD operations for Publication model using FastCRUD
"""

from typing import Any
from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.publication import Publication
from ..schemas.publication import PublicationCreate, PublicationUpdate


class CRUDPublication(FastCRUD):
    def __init__(self):
        super().__init__(Publication)

    async def create_with_categories(
        self, db: AsyncSession, *, obj_in: PublicationCreate, created_by: UUID, category_ids: list[UUID] | None = None
    ) -> Publication:
        """Create a publication with optional categories"""

        # Create the publication with created_by using direct SQLAlchemy
        from datetime import UTC, datetime

        from sqlalchemy import insert
        from uuid6 import uuid7

        # Get data as dict and add required fields
        publication_data = obj_in.model_dump()
        publication_data["id"] = uuid7()  # Generate UUID manually
        publication_data["created_by"] = created_by
        publication_data["created_at"] = datetime.now(UTC)  # Set timestamp

        # Insert directly using SQLAlchemy
        stmt = insert(Publication).values(**publication_data).returning(Publication)
        result = await db.execute(stmt)
        publication = result.scalar_one()
        await db.commit()
        await db.refresh(publication)

        # Add categories if provided
        if category_ids:
            from ..core.exceptions.http_exceptions import NotFoundException
            from ..models.categories import PublicationCategory

            # Validate that all categories exist before making any changes
            invalid_categories = []
            for category_id in category_ids:
                category_exists = await db.get(PublicationCategory, category_id)
                if not category_exists:
                    invalid_categories.append(str(category_id))

            # If any categories are invalid, raise an error
            if invalid_categories:
                raise NotFoundException(f"Categories not found: {', '.join(invalid_categories)}")

            # All categories are valid, proceed with assignment
            for category_id in category_ids:
                # Create the link
                link_stmt = text("""
                INSERT INTO publication_category_links (publication_id, category_id)
                VALUES (:publication_id, :category_id)
                ON CONFLICT (publication_id, category_id) DO NOTHING
                """)
                await db.execute(link_stmt, {"publication_id": publication.id, "category_id": category_id})

            await db.commit()
            await db.refresh(publication)

        return publication

    async def get_with_relations(self, db: AsyncSession, id: UUID) -> dict | None:
        """Get publication with all related data (creator, categories)"""

        from sqlalchemy import select

        # Use direct SQLAlchemy query to properly load relationships
        stmt = (
            select(Publication)
            .where(Publication.id == id)
            .options(
                selectinload(Publication.creator),
                selectinload(Publication.category_links).selectinload(
                    Publication.category_links.property.mapper.class_.category
                ),
            )
        )

        result = await db.execute(stmt)
        publication = result.scalar_one_or_none()

        if not publication:
            return None

        # Convert to dict and add categories manually
        publication_dict = {
            "id": publication.id,
            "title": publication.title,
            "slug": publication.slug,
            "abstract": publication.abstract,
            # New Core Info fields
            "authors": publication.authors,
            "venue": publication.venue,
            "citations": publication.citations,
            "doi": publication.doi,
            "keywords": publication.keywords,
            "impact": publication.impact,
            "pages": publication.pages,
            # Journal Specific fields
            "volume": publication.volume,
            "issue": publication.issue,
            "publisher": publication.publisher,
            # Content Sections
            "methodology": publication.methodology,
            "results": publication.results,
            "conclusions": publication.conclusions,
            # Existing fields
            "pdf_url": publication.pdf_url,
            "journal_name": publication.journal_name,
            "year": publication.year,
            "graphical_abstract_url": publication.graphical_abstract_url,
            "view_count": publication.view_count,
            "download_count": publication.download_count,
            "access_level": publication.access_level.value
            if hasattr(publication.access_level, "value")
            else publication.access_level,
            "status": publication.status.value if hasattr(publication.status, "value") else publication.status,
            "created_by": publication.created_by,
            "created_at": publication.created_at,
            "updated_at": publication.updated_at,
            "creator_name": publication.creator.name if publication.creator else None,
            "categories": [link.category.name for link in publication.category_links],
        }

        return publication_dict

    async def increment_view_count(self, db: AsyncSession, publication_id: UUID) -> bool:
        """Increment view count for a publication"""
        from sqlalchemy import update

        stmt = update(Publication).where(Publication.id == publication_id).values(view_count=Publication.view_count + 1)

        result = await db.execute(stmt)
        await db.commit()

        return result.rowcount > 0

    async def increment_download_count(self, db: AsyncSession, publication_id: UUID) -> bool:
        """Increment download count for a publication"""
        from sqlalchemy import update

        stmt = (
            update(Publication)
            .where(Publication.id == publication_id)
            .values(download_count=Publication.download_count + 1)
        )

        result = await db.execute(stmt)
        await db.commit()

        return result.rowcount > 0

    async def get_by_creator(
        self, db: AsyncSession, creator_id: UUID, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get publications by creator with pagination"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, created_by=creator_id, schema_to_select=Publication
        )

    async def get_by_access_level(
        self, db: AsyncSession, access_level: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get publications by access level with pagination"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, access_level=access_level, schema_to_select=Publication
        )

    async def get_by_status(self, db: AsyncSession, status: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get publications by status with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, status=status, schema_to_select=Publication)

    async def get_by_type(
        self, db: AsyncSession, publication_type: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get publications by type with pagination"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, publication_type=publication_type, schema_to_select=Publication
        )

    async def get_by_authors(
        self, db: AsyncSession, author_name: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get publications by author name (contains search)"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, authors__icontains=author_name, schema_to_select=Publication
        )

    async def search_publications(
        self, db: AsyncSession, query: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Search publications by title or abstract"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, title__icontains=query, schema_to_select=Publication
        )

    async def update_with_categories(
        self,
        db: AsyncSession,
        *,
        publication: dict,  # Changed from db_obj: Publication
        obj_in: PublicationUpdate,
        category_ids: list[UUID] | None = None,
    ) -> dict:
        """Update publication and optionally update categories"""

        # Update the publication fields using direct UPDATE and fetch
        from datetime import UTC, datetime

        from sqlalchemy import select, update

        # Get update data excluding unset fields
        publication_data = obj_in.model_dump(exclude={"category_ids"}, exclude_unset=True)

        if publication_data:
            publication_data["updated_at"] = datetime.now(UTC)

            # Update using SQLAlchemy update
            stmt = update(Publication).where(Publication.id == publication["id"]).values(**publication_data)
            await db.execute(stmt)
            await db.commit()

        # Fetch updated publication
        select_stmt = select(Publication).where(Publication.id == publication["id"])
        result = await db.execute(select_stmt)
        updated_publication = result.scalar_one()

        # Update categories if provided
        if category_ids is not None:
            # Validate that all categories exist before making any changes
            from ..core.exceptions.http_exceptions import NotFoundException
            from ..models.categories import PublicationCategory

            invalid_categories = []
            for category_id in category_ids:
                category_exists = await db.get(PublicationCategory, category_id)
                if not category_exists:
                    invalid_categories.append(str(category_id))

            # If any categories are invalid, raise an error
            if invalid_categories:
                raise NotFoundException(f"Categories not found: {', '.join(invalid_categories)}")

            # Remove all existing category links
            delete_stmt = text("DELETE FROM publication_category_links WHERE publication_id = :publication_id")
            await db.execute(delete_stmt, {"publication_id": publication["id"]})

            # Add new category links (all categories are validated at this point)
            for category_id in category_ids:
                link_stmt = text("""
                INSERT INTO publication_category_links (publication_id, category_id)
                VALUES (:publication_id, :category_id)
                """)
                await db.execute(link_stmt, {"publication_id": publication["id"], "category_id": category_id})

            await db.commit()
            await db.refresh(updated_publication)

        return updated_publication

    async def assign_categories(self, db: AsyncSession, *, publication_id: UUID, category_ids: list[UUID]) -> dict:
        """Assign categories to a publication"""

        from datetime import UTC, datetime

        from uuid6 import uuid7

        from ..core.exceptions.http_exceptions import NotFoundException

        # Validate that all categories exist before making any changes
        from ..models.categories import PublicationCategory

        invalid_categories = []
        for category_id in category_ids:
            category_exists = await db.get(PublicationCategory, category_id)
            if not category_exists:
                invalid_categories.append(str(category_id))

        # If any categories are invalid, raise an error
        if invalid_categories:
            raise NotFoundException(f"Categories not found: {', '.join(invalid_categories)}")

        # First, remove all existing category links
        delete_stmt = text("DELETE FROM publication_category_links WHERE publication_id = :publication_id")
        await db.execute(delete_stmt, {"publication_id": publication_id})

        # Add new category links (all categories are validated at this point)
        for category_id in category_ids:
            link_stmt = text("""
            INSERT INTO publication_category_links (id, publication_id, category_id, created_at)
            VALUES (:id, :publication_id, :category_id, :created_at)
            ON CONFLICT (publication_id, category_id) DO NOTHING
            """)
            await db.execute(
                link_stmt,
                {
                    "id": uuid7(),
                    "publication_id": publication_id,
                    "category_id": category_id,
                    "created_at": datetime.now(UTC),
                },
            )

        await db.commit()

        # Return the updated publication
        updated_publication = await self.get(db=db, id=publication_id)
        return updated_publication

    async def delete_with_cascade(self, db: AsyncSession, *, id: UUID) -> bool:
        """Delete publication with proper cascade handling"""

        from sqlalchemy import delete, text

        # First, remove all category links for this publication
        delete_links_stmt = text("DELETE FROM publication_category_links WHERE publication_id = :publication_id")
        await db.execute(delete_links_stmt, {"publication_id": id})

        # Now delete the publication itself
        delete_publication_stmt = delete(Publication).where(Publication.id == id)
        result = await db.execute(delete_publication_stmt)

        await db.commit()

        # Return True if any rows were deleted
        return result.rowcount > 0


# Create an instance
crud_publication = CRUDPublication()
