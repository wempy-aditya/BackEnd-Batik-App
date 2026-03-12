"""
CRUD operations for Project model using FastCRUD
"""

from typing import Any
from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(FastCRUD):
    def __init__(self):
        super().__init__(Project)

    async def create_with_categories(
        self, db: AsyncSession, *, obj_in: ProjectCreate, created_by: UUID, category_ids: list[UUID] | None = None
    ) -> Project:
        """Create a project with optional categories"""

        # Create the project with created_by
        from datetime import UTC, datetime

        from sqlalchemy import insert
        from uuid6 import uuid7

        # Get data as dict and add required fields
        project_data = obj_in.model_dump()
        project_data["id"] = uuid7()  # Generate UUID manually
        project_data["created_by"] = created_by
        project_data["created_at"] = datetime.now(UTC)  # Set timestamp

        # Insert directly using SQLAlchemy
        from ..models.project import Project

        stmt = insert(Project).values(**project_data).returning(Project)
        result = await db.execute(stmt)
        project = result.scalar_one()
        await db.commit()
        await db.refresh(project)

        # Add categories if provided
        if category_ids:
            from uuid6 import uuid7

            from ..models.categories import ProjectCategory, ProjectCategoryLink

            for category_id in category_ids:
                # First check if category exists
                category_exists = await db.get(ProjectCategory, category_id)
                if category_exists:
                    # Create the link using SQLAlchemy model
                    link = ProjectCategoryLink(project_id=project.id, category_id=category_id)
                    db.add(link)

            await db.commit()
            await db.refresh(project)

        return project

    async def get_with_relations(self, db: AsyncSession, id: UUID) -> Project | None:
        """Get project with all related data (creator, categories)"""
        from sqlalchemy import select

        from ..models.categories import ProjectCategoryLink

        query = (
            select(Project)
            .options(
                selectinload(Project.creator),
                selectinload(Project.category_links).selectinload(ProjectCategoryLink.category),
            )
            .where(Project.id == id)
        )

        result = await db.execute(query)
        project = result.scalar_one_or_none()

        return project

    async def get_by_creator(
        self, db: AsyncSession, creator_id: UUID, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get projects by creator with pagination"""

        return await self.get_multi(
            db=db,
            offset=skip,
            limit=limit,
            created_by=creator_id,
        )

    async def get_by_access_level(
        self, db: AsyncSession, access_level: str, skip: int = 0, limit: int = 100
    ) -> dict[str, Any]:
        """Get projects by access level with pagination"""

        return await self.get_multi(
            db=db,
            offset=skip,
            limit=limit,
            access_level=access_level,
        )

    async def get_by_status(self, db: AsyncSession, status: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Get projects by status with pagination"""

        return await self.get_multi(
            db=db,
            offset=skip,
            limit=limit,
            status=status,
        )

    async def search_projects(self, db: AsyncSession, query: str, skip: int = 0, limit: int = 100) -> dict[str, Any]:
        """Search projects by title or description"""

        return await self.get_multi(
            db=db,
            offset=skip,
            limit=limit,
            title__icontains=query,
            # Note: FastCRUD might not support OR queries directly
            # You might need to implement custom search logic here
        )

    async def update_with_categories(
        self, db: AsyncSession, *, db_obj: Project, obj_in: ProjectUpdate, category_ids: list[UUID] | None = None
    ) -> Project:
        """Update project and optionally update categories"""

        # Update the project fields
        project_data = obj_in.model_dump(exclude={"category_ids"}, exclude_unset=True)
        await self.update(db=db, object=project_data, id=db_obj["id"])

        # Get updated project
        updated_project = await self.get(db=db, id=db_obj["id"])

        # Update categories if provided
        if category_ids is not None:
            # First, remove all existing category links
            from sqlalchemy import text

            delete_stmt = text("DELETE FROM project_category_links WHERE project_id = :project_id")
            await db.execute(delete_stmt, {"project_id": db_obj["id"]})

            # Add new category links
            for category_id in category_ids:
                # Check if category exists
                from ..models.categories import ProjectCategory, ProjectCategoryLink

                category_exists = await db.get(ProjectCategory, category_id)
                if category_exists:
                    # Create the link using SQLAlchemy model instead of raw SQL
                    link = ProjectCategoryLink(project_id=db_obj["id"], category_id=category_id)
                    db.add(link)

            await db.commit()
            # Refresh updated project after categories update
            updated_project = await self.get(db=db, id=db_obj["id"])

        return updated_project

    async def delete_with_cascade(self, db: AsyncSession, *, id: UUID) -> bool:
        """Delete project with proper cascade handling"""

        from sqlalchemy import delete

        # First, remove all category links for this project
        delete_links_stmt = text("DELETE FROM project_category_links WHERE project_id = :project_id")
        await db.execute(delete_links_stmt, {"project_id": id})

        # Now delete the project itself
        delete_project_stmt = delete(Project).where(Project.id == id)
        result = await db.execute(delete_project_stmt)

        await db.commit()

        # Return True if any rows were deleted
        return result.rowcount > 0


# Create an instance
crud_project = CRUDProject()
