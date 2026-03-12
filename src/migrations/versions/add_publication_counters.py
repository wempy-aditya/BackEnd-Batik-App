"""Add view_count and download_count to publications

Revision ID: add_publication_counters
Revises: add_files_table
Create Date: 2025-12-18

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "add_publication_counters"
down_revision = "add_files_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add view_count and download_count columns to publications table
    op.add_column("publications", sa.Column("view_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("publications", sa.Column("download_count", sa.Integer(), nullable=False, server_default="0"))

    # Create indexes for better query performance
    op.create_index("ix_publications_view_count", "publications", ["view_count"])
    op.create_index("ix_publications_download_count", "publications", ["download_count"])


def downgrade() -> None:
    # Drop indexes
    op.drop_index("ix_publications_download_count", "publications")
    op.drop_index("ix_publications_view_count", "publications")

    # Drop columns
    op.drop_column("publications", "download_count")
    op.drop_column("publications", "view_count")
