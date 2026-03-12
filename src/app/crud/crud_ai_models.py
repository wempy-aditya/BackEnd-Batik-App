"""
CRUD operations for AI Model using FastCRUD
"""

from typing import Any
from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.ai_models import AIModel
from ..schemas.ai_models import AIModelCreate, AIModelUpdate


class CRUDAIModel(FastCRUD):
    def __init__(self):
        super().__init__(AIModel)

    async def create_with_categories(
        self, db: AsyncSession, *, obj_in: AIModelCreate, created_by: UUID, category_ids: list[UUID] | None = None
    ) -> AIModel:
        """Create an AI model with optional categories"""

        # Create the AI model with created_by using direct SQLAlchemy
        from datetime import UTC, datetime

        from sqlalchemy import insert
        from uuid6 import uuid7

        # Get data as dict and add required fields
        model_data = obj_in.model_dump()
        model_data["id"] = uuid7()  # Generate UUID manually
        model_data["created_by"] = created_by
        model_data["created_at"] = datetime.now(UTC)  # Set timestamp

        # Insert directly using SQLAlchemy
        stmt = insert(AIModel).values(**model_data).returning(AIModel)
        result = await db.execute(stmt)
        ai_model = result.scalar_one()
        await db.commit()
        await db.refresh(ai_model)

        # Add categories if provided
        if category_ids:
            from ..models.categories import ModelCategory

            for category_id in category_ids:
                # Check if category exists
                category_exists = await db.get(ModelCategory, category_id)
                if category_exists:
                    # Create the link
                    link_stmt = text("""
                    INSERT INTO model_category_links (id, model_id, category_id, created_at)
                    VALUES (:id, :model_id, :category_id, :created_at)
                    ON CONFLICT (model_id, category_id) DO NOTHING
                    """)
                    await db.execute(
                        link_stmt,
                        {
                            "id": uuid7(),
                            "model_id": ai_model.id,
                            "category_id": category_id,
                            "created_at": datetime.now(UTC),
                        },
                    )

            await db.commit()
            await db.refresh(ai_model)

        return ai_model

    async def get_with_relations(self, db: AsyncSession, id: UUID) -> dict | None:
        """Get AI model with all related data (creator, categories)"""

        from sqlalchemy import select

        # Use direct SQLAlchemy query to properly load relationships
        from ..models.categories import ModelCategoryLink

        stmt = (
            select(AIModel)
            .where(AIModel.id == id)
            .options(
                selectinload(AIModel.creator),
                selectinload(AIModel.category_links).selectinload(ModelCategoryLink.category),
                selectinload(AIModel.gallery_items),
            )
        )

        result = await db.execute(stmt)
        ai_model = result.scalar_one_or_none()

        if not ai_model:
            return None

        # Convert to dict and add categories manually
        ai_model_dict = {
            "id": ai_model.id,
            "name": ai_model.name,
            "slug": ai_model.slug,
            "description": ai_model.description,
            "architecture": ai_model.architecture,
            "dataset_used": ai_model.dataset_used,
            "metrics": ai_model.metrics,
            "model_file_url": ai_model.model_file_url,
            "access_level": ai_model.access_level.value
            if hasattr(ai_model.access_level, "value")
            else ai_model.access_level,
            "status": ai_model.status.value if hasattr(ai_model.status, "value") else ai_model.status,
            "created_by": ai_model.created_by,
            "created_at": ai_model.created_at,
            "updated_at": ai_model.updated_at,
            "creator_name": ai_model.creator.name if ai_model.creator else None,
            "categories": [link.category.name for link in ai_model.category_links],
            "gallery_count": len(ai_model.gallery_items) if ai_model.gallery_items else 0,
        }

        return ai_model_dict

    async def get_by_creator(
        self, db: AsyncSession, creator_id: UUID, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get AI models by creator with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, created_by=creator_id, schema_to_select=AIModel)

    async def get_by_access_level(
        self, db: AsyncSession, access_level: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get AI models by access level with pagination"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, access_level=access_level, schema_to_select=AIModel
        )

    async def get_by_status(self, db: AsyncSession, status: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get AI models by status with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, status=status, schema_to_select=AIModel)

    async def get_by_model_type(
        self, db: AsyncSession, model_type: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get AI models by type with pagination"""

        return await self.get_multi(db=db, offset=skip, limit=limit, model_type=model_type, schema_to_select=AIModel)

    async def get_by_framework(
        self, db: AsyncSession, framework: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get AI models by framework with pagination"""

        return await self.get_multi(
            db=db, offset=skip, limit=limit, framework__icontains=framework, schema_to_select=AIModel
        )

    async def search_ai_models(self, db: AsyncSession, query: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Search AI models by title or description"""

        return await self.get_multi(db=db, offset=skip, limit=limit, title__icontains=query, schema_to_select=AIModel)

    async def update_with_categories(
        self,
        db: AsyncSession,
        *,
        ai_model: dict,  # Changed from db_obj: AIModel
        obj_in: AIModelUpdate,
        category_ids: list[UUID] | None = None,
    ) -> dict:
        """Update AI model and optionally update categories"""

        # Update the AI model fields using direct UPDATE and fetch
        from datetime import UTC, datetime

        from sqlalchemy import select, update

        # Get update data excluding unset fields
        model_data = obj_in.model_dump(exclude={"category_ids"}, exclude_unset=True)

        if model_data:
            model_data["updated_at"] = datetime.now(UTC)

            # Update using SQLAlchemy update
            stmt = update(AIModel).where(AIModel.id == ai_model["id"]).values(**model_data)
            await db.execute(stmt)
            await db.commit()

        # Fetch updated AI model
        select_stmt = select(AIModel).where(AIModel.id == ai_model["id"])
        result = await db.execute(select_stmt)
        updated_ai_model = result.scalar_one()

        # Update categories if provided
        if category_ids is not None:
            # Remove all existing category links
            delete_stmt = text("DELETE FROM model_category_links WHERE model_id = :model_id")
            await db.execute(delete_stmt, {"model_id": ai_model["id"]})

            # Add new category links
            for category_id in category_ids:
                # Check if category exists
                from ..models.categories import ModelCategory

                category_exists = await db.get(ModelCategory, category_id)
                if category_exists:
                    from datetime import UTC, datetime

                    from uuid6 import uuid7

                    link_stmt = text("""
                    INSERT INTO model_category_links (id, model_id, category_id, created_at)
                    VALUES (:id, :model_id, :category_id, :created_at)
                    """)
                    await db.execute(
                        link_stmt,
                        {
                            "id": uuid7(),
                            "model_id": ai_model["id"],
                            "category_id": category_id,
                            "created_at": datetime.now(UTC),
                        },
                    )

            await db.commit()
            await db.refresh(updated_ai_model)

        return updated_ai_model

    async def assign_categories(self, db: AsyncSession, *, ai_model_id: UUID, category_ids: list[UUID]) -> dict:
        """Assign categories to existing AI model"""

        from datetime import UTC, datetime

        from sqlalchemy import select, text
        from uuid6 import uuid7

        # Get the AI model first
        select_stmt = select(AIModel).where(AIModel.id == ai_model_id)
        result = await db.execute(select_stmt)
        ai_model = result.scalar_one_or_none()

        if not ai_model:
            return None

        # Remove all existing category links for this model
        delete_stmt = text("DELETE FROM model_category_links WHERE model_id = :model_id")
        await db.execute(delete_stmt, {"model_id": ai_model_id})

        # Add new category links
        for category_id in category_ids:
            # Check if category exists
            from ..models.categories import ModelCategory

            category_exists = await db.get(ModelCategory, category_id)
            if category_exists:
                link_stmt = text("""
                INSERT INTO model_category_links (id, model_id, category_id, created_at)
                VALUES (:id, :model_id, :category_id, :created_at)
                """)
                await db.execute(
                    link_stmt,
                    {
                        "id": uuid7(),
                        "model_id": ai_model_id,
                        "category_id": category_id,
                        "created_at": datetime.now(UTC),
                    },
                )

        await db.commit()
        await db.refresh(ai_model)

        # Convert to dict for return
        return {
            "id": ai_model.id,
            "name": ai_model.name,
            "slug": ai_model.slug,
            "description": ai_model.description,
            "architecture": ai_model.architecture,
            "dataset_used": ai_model.dataset_used,
            "metrics": ai_model.metrics,
            "model_file_url": ai_model.model_file_url,
            "access_level": ai_model.access_level.value
            if hasattr(ai_model.access_level, "value")
            else ai_model.access_level,
            "status": ai_model.status.value if hasattr(ai_model.status, "value") else ai_model.status,
            "created_by": ai_model.created_by,
            "created_at": ai_model.created_at,
            "updated_at": ai_model.updated_at,
        }

    async def delete_with_cascade(self, db: AsyncSession, *, id: UUID) -> bool:
        """Delete AI model with proper cascade handling"""

        from sqlalchemy import delete, text

        # First, remove all category links for this model
        delete_links_stmt = text("DELETE FROM model_category_links WHERE model_id = :model_id")
        await db.execute(delete_links_stmt, {"model_id": id})

        # Also remove any gallery items that reference this model
        delete_gallery_stmt = text("DELETE FROM gallery WHERE model_id = :model_id")
        await db.execute(delete_gallery_stmt, {"model_id": id})

        # Now delete the model itself
        delete_model_stmt = delete(AIModel).where(AIModel.id == id)
        result = await db.execute(delete_model_stmt)

        await db.commit()

        # Return True if any rows were deleted
        return result.rowcount > 0


# Create an instance
crud_ai_model = CRUDAIModel()
