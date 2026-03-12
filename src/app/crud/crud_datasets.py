"""
CRUD operations for Dataset model using FastCRUD
"""

from typing import Any
from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.dataset import Dataset
from ..schemas.dataset import DatasetCreate, DatasetUpdate


class CRUDDataset(FastCRUD):
    def __init__(self):
        super().__init__(Dataset)

    async def create_with_categories(
        self, db: AsyncSession, *, obj_in: DatasetCreate, created_by: UUID, category_ids: list[UUID] | None = None
    ) -> Dataset:
        """Create a dataset with optional categories"""

        # Create the dataset with created_by using direct SQLAlchemy
        from datetime import UTC, datetime

        from sqlalchemy import insert
        from uuid6 import uuid7

        # Get data as dict and add required fields
        dataset_data = obj_in.model_dump()
        dataset_data["id"] = uuid7()  # Generate UUID manually
        dataset_data["created_by"] = created_by
        dataset_data["created_at"] = datetime.now(UTC)  # Set timestamp

        # Insert directly using SQLAlchemy
        stmt = insert(Dataset).values(**dataset_data).returning(Dataset)
        result = await db.execute(stmt)
        dataset = result.scalar_one()
        await db.commit()
        await db.refresh(dataset)

        # Add categories if provided
        if category_ids:
            from ..core.exceptions.http_exceptions import NotFoundException
            from ..models.categories import DatasetCategory

            # Validate that all categories exist before making any changes
            invalid_categories = []
            for category_id in category_ids:
                category_exists = await db.get(DatasetCategory, category_id)
                if not category_exists:
                    invalid_categories.append(str(category_id))

            # If any categories are invalid, raise an error
            if invalid_categories:
                raise NotFoundException(f"Categories not found: {', '.join(invalid_categories)}")

            # All categories are valid, proceed with assignment
            for category_id in category_ids:
                # Create the link
                link_stmt = text("""
                INSERT INTO dataset_category_links (id, dataset_id, category_id, created_at)
                VALUES (:id, :dataset_id, :category_id, :created_at)
                ON CONFLICT (dataset_id, category_id) DO NOTHING
                """)
                await db.execute(
                    link_stmt,
                    {
                        "id": uuid7(),
                        "dataset_id": dataset.id,
                        "category_id": category_id,
                        "created_at": datetime.now(UTC),
                    },
                )

            await db.commit()
            await db.refresh(dataset)

        return dataset

    async def get_with_relations(self, db: AsyncSession, id: UUID) -> dict | None:
        """Get dataset with all related data (creator, categories)"""

        from sqlalchemy import select

        # Use direct SQLAlchemy query to properly load relationships
        stmt = (
            select(Dataset)
            .where(Dataset.id == id)
            .options(
                selectinload(Dataset.creator),
                selectinload(Dataset.category_links).selectinload(
                    Dataset.category_links.property.mapper.class_.category
                ),
            )
        )

        result = await db.execute(stmt)
        dataset = result.scalar_one_or_none()

        if not dataset:
            return None

        # Convert to dict and add categories manually
        dataset_dict = {
            "id": dataset.id,
            "name": dataset.name,
            "slug": dataset.slug,
            "description": dataset.description,
            # Enhanced Core Info fields
            "tagline": dataset.tagline,
            "samples": dataset.samples,
            "view_count": dataset.view_count,
            "download_count": dataset.download_count,
            "gradient": dataset.gradient,
            "version": dataset.version,
            "format": dataset.format,
            "license": dataset.license,
            "citation": dataset.citation,
            # Key Features & Use Cases
            "key_features": dataset.key_features,
            "use_cases": dataset.use_cases,
            # Technical Specifications & Statistics
            "technical_specs": dataset.technical_specs,
            "statistics": dataset.statistics,
            # Sample Images
            "sample_images": dataset.sample_images,
            # Original fields
            "sample_image_url": dataset.sample_image_url,
            "file_url": dataset.file_url,
            "source": dataset.source,
            "size": dataset.size,
            "access_level": dataset.access_level.value
            if hasattr(dataset.access_level, "value")
            else dataset.access_level,
            "status": dataset.status.value if hasattr(dataset.status, "value") else dataset.status,
            "created_by": dataset.created_by,
            "created_at": dataset.created_at,
            "updated_at": dataset.updated_at,
            "creator_name": dataset.creator.name if dataset.creator else None,
            "categories": [link.category.name for link in dataset.category_links],
        }

        return dataset_dict

    async def get_by_creator(
        self, db: AsyncSession, creator_id: UUID, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get datasets by creator with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, created_by=creator_id, schema_to_select=Dataset)

    async def get_by_access_level(
        self, db: AsyncSession, access_level: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get datasets by access level with pagination"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, access_level=access_level, schema_to_select=Dataset
        )

    async def get_by_status(self, db: AsyncSession, status: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get datasets by status with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, status=status, schema_to_select=Dataset)

    async def get_by_format(
        self, db: AsyncSession, format_type: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get datasets by format type with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, format=format_type, schema_to_select=Dataset)

    async def search_datasets(self, db: AsyncSession, query: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Search datasets by title or description"""

        return await self.get_multi(db=db, offset=skip, limit=limit, title__icontains=query, schema_to_select=Dataset)

    async def update_with_categories(
        self,
        db: AsyncSession,
        *,
        dataset: dict,  # Changed from db_obj: Dataset
        obj_in: DatasetUpdate,
        category_ids: list[UUID] | None = None,
    ) -> dict:
        """Update dataset and optionally update categories"""

        # Update the dataset fields using direct UPDATE and fetch
        from datetime import UTC, datetime

        from sqlalchemy import select, update

        # Get update data excluding unset fields
        dataset_data = obj_in.model_dump(exclude={"category_ids"}, exclude_unset=True)

        if dataset_data:
            dataset_data["updated_at"] = datetime.now(UTC)

            # Update using SQLAlchemy update
            stmt = update(Dataset).where(Dataset.id == dataset["id"]).values(**dataset_data)
            await db.execute(stmt)
            await db.commit()

        # Fetch updated dataset
        select_stmt = select(Dataset).where(Dataset.id == dataset["id"])
        result = await db.execute(select_stmt)
        updated_dataset = result.scalar_one()

        # Update categories if provided
        if category_ids is not None:
            # Validate that all categories exist before making any changes
            from ..core.exceptions.http_exceptions import NotFoundException
            from ..models.categories import DatasetCategory

            invalid_categories = []
            for category_id in category_ids:
                category_exists = await db.get(DatasetCategory, category_id)
                if not category_exists:
                    invalid_categories.append(str(category_id))

            # If any categories are invalid, raise an error
            if invalid_categories:
                raise NotFoundException(f"Categories not found: {', '.join(invalid_categories)}")

            # Remove all existing category links
            delete_stmt = text("DELETE FROM dataset_category_links WHERE dataset_id = :dataset_id")
            await db.execute(delete_stmt, {"dataset_id": dataset["id"]})

            # Add new category links (all categories are validated at this point)
            for category_id in category_ids:
                from datetime import UTC, datetime

                from uuid6 import uuid7

                link_stmt = text("""
                INSERT INTO dataset_category_links (id, dataset_id, category_id, created_at)
                VALUES (:id, :dataset_id, :category_id, :created_at)
                """)
                await db.execute(
                    link_stmt,
                    {
                        "id": uuid7(),
                        "dataset_id": dataset["id"],
                        "category_id": category_id,
                        "created_at": datetime.now(UTC),
                    },
                )

            await db.commit()
            await db.refresh(updated_dataset)

        return updated_dataset

    async def assign_categories(self, db: AsyncSession, *, dataset_id: UUID, category_ids: list[UUID]) -> dict:
        """Assign categories to a dataset"""

        from datetime import UTC, datetime

        from uuid6 import uuid7

        from ..core.exceptions.http_exceptions import NotFoundException

        # Validate that all categories exist before making any changes
        from ..models.categories import DatasetCategory

        invalid_categories = []
        for category_id in category_ids:
            category_exists = await db.get(DatasetCategory, category_id)
            if not category_exists:
                invalid_categories.append(str(category_id))

        # If any categories are invalid, raise an error
        if invalid_categories:
            raise NotFoundException(f"Categories not found: {', '.join(invalid_categories)}")

        # First, remove all existing category links
        delete_stmt = text("DELETE FROM dataset_category_links WHERE dataset_id = :dataset_id")
        await db.execute(delete_stmt, {"dataset_id": dataset_id})

        # Add new category links (all categories are validated at this point)
        for category_id in category_ids:
            link_stmt = text("""
            INSERT INTO dataset_category_links (id, dataset_id, category_id, created_at)
            VALUES (:id, :dataset_id, :category_id, :created_at)
            ON CONFLICT (dataset_id, category_id) DO NOTHING
            """)
            await db.execute(
                link_stmt,
                {"id": uuid7(), "dataset_id": dataset_id, "category_id": category_id, "created_at": datetime.now(UTC)},
            )

        await db.commit()

        # Return the updated dataset
        updated_dataset = await self.get(db=db, id=dataset_id)
        return updated_dataset

    async def delete_with_cascade(self, db: AsyncSession, *, id: UUID) -> bool:
        """Delete dataset with proper cascade handling"""

        from sqlalchemy import delete, text

        # First, remove all category links for this dataset
        delete_links_stmt = text("DELETE FROM dataset_category_links WHERE dataset_id = :dataset_id")
        await db.execute(delete_links_stmt, {"dataset_id": id})

        # Now delete the dataset itself
        delete_dataset_stmt = delete(Dataset).where(Dataset.id == id)
        result = await db.execute(delete_dataset_stmt)

        await db.commit()

        # Return True if any rows were deleted
        return result.rowcount > 0

    async def increment_view_count(self, db: AsyncSession, dataset_id: UUID) -> bool:
        """Increment view count for a dataset using atomic SQL update"""
        from sqlalchemy import text

        stmt = text("UPDATE datasets SET view_count = view_count + 1 WHERE id = :id")
        result = await db.execute(stmt, {"id": dataset_id})
        await db.commit()

        return result.rowcount > 0

    async def increment_download_count(self, db: AsyncSession, dataset_id: UUID) -> bool:
        """Increment download count for a dataset using atomic SQL update"""
        from sqlalchemy import text

        stmt = text("UPDATE datasets SET download_count = download_count + 1 WHERE id = :id")
        result = await db.execute(stmt, {"id": dataset_id})
        await db.commit()

        return result.rowcount > 0


# Create an instance
crud_dataset = CRUDDataset()
