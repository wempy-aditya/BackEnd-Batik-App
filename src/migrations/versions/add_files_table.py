"""Add files table

Revision ID: add_files_table
Revises: add_contributors
Create Date: 2025-12-17

"""

import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "add_files_table"
down_revision = "add_contributors"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create files table
    op.create_table(
        "files",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("original_filename", sa.String(255), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False, unique=True),
        sa.Column("file_path", sa.Text, nullable=False),
        sa.Column("file_url", sa.Text, nullable=False),
        sa.Column("file_type", sa.String(50), nullable=False),
        sa.Column("mime_type", sa.String(100), nullable=False),
        sa.Column("file_size", sa.Integer, nullable=False),
        sa.Column("uploaded_by", UUID(as_uuid=True), nullable=True),
        sa.Column("metadata", sa.Text, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True, onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(["uploaded_by"], ["users.id"], ondelete="SET NULL"),
    )

    # Create indexes
    op.create_index("ix_files_filename", "files", ["filename"])
    op.create_index("ix_files_file_type", "files", ["file_type"])
    op.create_index("ix_files_uploaded_by", "files", ["uploaded_by"])
    op.create_index("ix_files_created_at", "files", ["created_at"])


def downgrade() -> None:
    # Drop indexes
    op.drop_index("ix_files_created_at", "files")
    op.drop_index("ix_files_uploaded_by", "files")
    op.drop_index("ix_files_file_type", "files")
    op.drop_index("ix_files_filename", "files")

    # Drop table
    op.drop_table("files")
