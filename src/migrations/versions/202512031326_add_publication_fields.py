"""add_publication_fields

Revision ID: pub_fields_202512
Revises: add_project_fields_20251203
Create Date: 2025-12-03 13:26:00.000000

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "pub_fields_202512"
down_revision: Union[str, None] = "add_project_fields_20251203"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new fields to publications table only
    op.add_column("publications", sa.Column("authors", postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column("publications", sa.Column("venue", sa.String(length=255), nullable=True))
    op.add_column("publications", sa.Column("citations", sa.Integer(), nullable=True))
    op.add_column("publications", sa.Column("doi", sa.String(length=255), nullable=True))
    op.add_column("publications", sa.Column("keywords", postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column("publications", sa.Column("impact", sa.String(length=50), nullable=True))
    op.add_column("publications", sa.Column("pages", sa.String(length=50), nullable=True))
    op.add_column("publications", sa.Column("volume", sa.String(length=50), nullable=True))
    op.add_column("publications", sa.Column("issue", sa.String(length=50), nullable=True))
    op.add_column("publications", sa.Column("publisher", sa.String(length=255), nullable=True))
    op.add_column("publications", sa.Column("methodology", sa.Text(), nullable=True))
    op.add_column("publications", sa.Column("results", sa.Text(), nullable=True))
    op.add_column("publications", sa.Column("conclusions", sa.Text(), nullable=True))


def downgrade() -> None:
    # Remove publication fields
    op.drop_column("publications", "conclusions")
    op.drop_column("publications", "results")
    op.drop_column("publications", "methodology")
    op.drop_column("publications", "publisher")
    op.drop_column("publications", "issue")
    op.drop_column("publications", "volume")
    op.drop_column("publications", "pages")
    op.drop_column("publications", "impact")
    op.drop_column("publications", "keywords")
    op.drop_column("publications", "doi")
    op.drop_column("publications", "citations")
    op.drop_column("publications", "venue")
    op.drop_column("publications", "authors")
