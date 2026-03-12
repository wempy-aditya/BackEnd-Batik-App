"""enhance_datasets_table_with_comprehensive_fields

Revision ID: 4c1e0f46831c
Revises: pub_fields_202512
Create Date: 2025-12-03 14:37:50.801323

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4c1e0f46831c"
down_revision: Union[str, None] = "pub_fields_202512"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add comprehensive new fields to datasets table

    # Core Info fields
    op.add_column("datasets", sa.Column("tagline", sa.String(500), nullable=True))
    op.add_column("datasets", sa.Column("samples", sa.Integer(), nullable=True, default=0))
    op.add_column("datasets", sa.Column("download_count", sa.Integer(), nullable=True, default=0))
    op.add_column("datasets", sa.Column("gradient", sa.String(100), nullable=True))
    op.add_column("datasets", sa.Column("version", sa.String(50), nullable=True, default="1.0"))
    op.add_column("datasets", sa.Column("format", sa.String(100), nullable=True))
    op.add_column("datasets", sa.Column("license", sa.String(255), nullable=True))
    op.add_column("datasets", sa.Column("citation", sa.Text(), nullable=True))

    # Features & Use Cases (arrays)
    op.add_column("datasets", sa.Column("key_features", postgresql.ARRAY(sa.String()), nullable=True))
    op.add_column("datasets", sa.Column("use_cases", postgresql.ARRAY(sa.String()), nullable=True))

    # Technical Specifications (JSON)
    op.add_column("datasets", sa.Column("technical_specs", postgresql.JSONB(), nullable=True))

    # Statistics (JSON)
    op.add_column("datasets", sa.Column("statistics", postgresql.JSONB(), nullable=True))

    # Sample Images (array of URLs)
    op.add_column("datasets", sa.Column("sample_images", postgresql.ARRAY(sa.String()), nullable=True))


def downgrade() -> None:
    # Remove the added columns
    op.drop_column("datasets", "sample_images")
    op.drop_column("datasets", "statistics")
    op.drop_column("datasets", "technical_specs")
    op.drop_column("datasets", "use_cases")
    op.drop_column("datasets", "key_features")
    op.drop_column("datasets", "citation")
    op.drop_column("datasets", "license")
    op.drop_column("datasets", "format")
    op.drop_column("datasets", "version")
    op.drop_column("datasets", "gradient")
    op.drop_column("datasets", "download_count")
    op.drop_column("datasets", "samples")
    op.drop_column("datasets", "tagline")
