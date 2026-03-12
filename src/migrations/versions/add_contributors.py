"""Add contributors and contributor link tables

Revision ID: add_contributors
Revises: 4c1e0f46831c
Create Date: 2025-12-16 10:00:00.000000

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "add_contributors"
down_revision = "4c1e0f46831c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create contributors table
    op.create_table(
        "contributors",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=100), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("profile_image", sa.Text(), nullable=True),
        sa.Column("github_url", sa.Text(), nullable=True),
        sa.Column("linkedin_url", sa.Text(), nullable=True),
        sa.Column("website_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_contributors_name", "contributors", ["name"])

    # Create project_contributor_links table
    op.create_table(
        "project_contributor_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("contributor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_in_project", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["contributor_id"], ["contributors.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", "contributor_id", name="uq_project_contributor"),
    )
    op.create_index("ix_project_contributor_project", "project_contributor_links", ["project_id"])
    op.create_index("ix_project_contributor_contributor", "project_contributor_links", ["contributor_id"])

    # Create publication_contributor_links table
    op.create_table(
        "publication_contributor_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("publication_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("contributor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_in_publication", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["publication_id"], ["publications.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["contributor_id"], ["contributors.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("publication_id", "contributor_id", name="uq_publication_contributor"),
    )
    op.create_index("ix_publication_contributor_publication", "publication_contributor_links", ["publication_id"])
    op.create_index("ix_publication_contributor_contributor", "publication_contributor_links", ["contributor_id"])

    # Create dataset_contributor_links table
    op.create_table(
        "dataset_contributor_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("contributor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_in_dataset", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["dataset_id"], ["datasets.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["contributor_id"], ["contributors.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("dataset_id", "contributor_id", name="uq_dataset_contributor"),
    )
    op.create_index("ix_dataset_contributor_dataset", "dataset_contributor_links", ["dataset_id"])
    op.create_index("ix_dataset_contributor_contributor", "dataset_contributor_links", ["contributor_id"])


def downgrade() -> None:
    # Drop link tables first (due to foreign keys)
    op.drop_index("ix_dataset_contributor_contributor", table_name="dataset_contributor_links")
    op.drop_index("ix_dataset_contributor_dataset", table_name="dataset_contributor_links")
    op.drop_table("dataset_contributor_links")

    op.drop_index("ix_publication_contributor_contributor", table_name="publication_contributor_links")
    op.drop_index("ix_publication_contributor_publication", table_name="publication_contributor_links")
    op.drop_table("publication_contributor_links")

    op.drop_index("ix_project_contributor_contributor", table_name="project_contributor_links")
    op.drop_index("ix_project_contributor_project", table_name="project_contributor_links")
    op.drop_table("project_contributor_links")

    # Drop contributors table
    op.drop_index("ix_contributors_name", table_name="contributors")
    op.drop_table("contributors")
