"""
CRUD operations for Contributor model using FastCRUD
"""

from datetime import UTC, datetime
from uuid import UUID

from fastcrud import FastCRUD
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from ..models.contributor import Contributor


class CRUDContributor(FastCRUD):
    def __init__(self):
        super().__init__(Contributor)

    async def get_with_stats(self, db: AsyncSession, id: UUID) -> dict | None:
        """Get contributor with project/publication/dataset counts"""

        contributor = await self.get(db=db, id=id)
        if not contributor:
            return None

        # Count assignments
        project_count_query = text("SELECT COUNT(*) FROM project_contributor_links WHERE contributor_id = :id")
        publication_count_query = text("SELECT COUNT(*) FROM publication_contributor_links WHERE contributor_id = :id")
        dataset_count_query = text("SELECT COUNT(*) FROM dataset_contributor_links WHERE contributor_id = :id")

        project_count = (await db.execute(project_count_query, {"id": id})).scalar()
        publication_count = (await db.execute(publication_count_query, {"id": id})).scalar()
        dataset_count = (await db.execute(dataset_count_query, {"id": id})).scalar()

        return {
            **contributor,
            "project_count": project_count or 0,
            "publication_count": publication_count or 0,
            "dataset_count": dataset_count or 0,
            "total_contributions": (project_count or 0) + (publication_count or 0) + (dataset_count or 0),
        }

    async def assign_to_project(
        self, db: AsyncSession, *, project_id: UUID, contributor_id: UUID, role_in_project: str | None = None
    ) -> None:
        """Assign contributor to a project"""

        stmt = text("""
        INSERT INTO project_contributor_links (id, project_id, contributor_id, role_in_project, created_at)
        VALUES (:id, :project_id, :contributor_id, :role, :created_at)
        ON CONFLICT DO NOTHING
        """)

        await db.execute(
            stmt,
            {
                "id": uuid7(),
                "project_id": project_id,
                "contributor_id": contributor_id,
                "role": role_in_project,
                "created_at": datetime.now(UTC),
            },
        )
        await db.commit()

    async def assign_to_publication(
        self, db: AsyncSession, *, publication_id: UUID, contributor_id: UUID, role_in_publication: str | None = None
    ) -> None:
        """Assign contributor to a publication"""

        stmt = text("""
        INSERT INTO publication_contributor_links (id, publication_id, contributor_id, role_in_publication, created_at)
        VALUES (:id, :publication_id, :contributor_id, :role, :created_at)
        ON CONFLICT DO NOTHING
        """)

        await db.execute(
            stmt,
            {
                "id": uuid7(),
                "publication_id": publication_id,
                "contributor_id": contributor_id,
                "role": role_in_publication,
                "created_at": datetime.now(UTC),
            },
        )
        await db.commit()

    async def assign_to_dataset(
        self, db: AsyncSession, *, dataset_id: UUID, contributor_id: UUID, role_in_dataset: str | None = None
    ) -> None:
        """Assign contributor to a dataset"""

        stmt = text("""
        INSERT INTO dataset_contributor_links (id, dataset_id, contributor_id, role_in_dataset, created_at)
        VALUES (:id, :dataset_id, :contributor_id, :role, :created_at)
        ON CONFLICT DO NOTHING
        """)

        await db.execute(
            stmt,
            {
                "id": uuid7(),
                "dataset_id": dataset_id,
                "contributor_id": contributor_id,
                "role": role_in_dataset,
                "created_at": datetime.now(UTC),
            },
        )
        await db.commit()

    async def remove_from_project(self, db: AsyncSession, *, project_id: UUID, contributor_id: UUID) -> None:
        """Remove contributor from a project"""

        stmt = text(
            "DELETE FROM project_contributor_links WHERE project_id = :project_id AND contributor_id = :contributor_id"
        )
        await db.execute(stmt, {"project_id": project_id, "contributor_id": contributor_id})
        await db.commit()

    async def get_project_contributors(self, db: AsyncSession, project_id: UUID) -> list[dict]:
        """Get all contributors for a project"""

        query = text("""
        SELECT c.*, pcl.role_in_project
        FROM contributors c
        JOIN project_contributor_links pcl ON c.id = pcl.contributor_id
        WHERE pcl.project_id = :project_id
        ORDER BY pcl.created_at
        """)

        result = await db.execute(query, {"project_id": project_id})
        return [dict(row._mapping) for row in result]


# Create instance
crud_contributor = CRUDContributor()
