"""Add missing project fields

Revision ID: add_project_fields_20251203
Revises: d1ffbce560e2
Create Date: 2025-12-03 15:30:00

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "add_project_fields_20251203"
down_revision: Union[str, None] = "d1ffbce560e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add missing columns to projects table

    # Add ProjectComplexity enum
    projectcomplexity = postgresql.ENUM("easy", "medium", "hard", name="projectcomplexity")
    projectcomplexity.create(op.get_bind())

    # Add new columns
    op.add_column("projects", sa.Column("full_description", sa.Text(), nullable=True))
    op.add_column("projects", sa.Column("technologies", sa.ARRAY(sa.String()), nullable=True))
    op.add_column("projects", sa.Column("challenges", sa.ARRAY(sa.String()), nullable=True))
    op.add_column("projects", sa.Column("achievements", sa.ARRAY(sa.String()), nullable=True))
    op.add_column("projects", sa.Column("future_work", sa.ARRAY(sa.String()), nullable=True))
    op.add_column("projects", sa.Column("complexity", projectcomplexity, nullable=True))
    op.add_column("projects", sa.Column("start_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    # Remove added columns
    op.drop_column("projects", "start_at")
    op.drop_column("projects", "complexity")
    op.drop_column("projects", "future_work")
    op.drop_column("projects", "achievements")
    op.drop_column("projects", "challenges")
    op.drop_column("projects", "technologies")
    op.drop_column("projects", "full_description")

    # Drop ProjectComplexity enum
    op.execute("DROP TYPE IF EXISTS projectcomplexity;")
