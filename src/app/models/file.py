"""
File model for file management system
"""

from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base

if TYPE_CHECKING:
    from .user import User


class File(Base):
    __tablename__ = "files"
    __allow_unmapped__ = True

    # Primary key as UUID
    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)

    # Original filename from user
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)

    # Stored filename (unique, generated)
    filename: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    # File path on server (relative path from upload root)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)

    # Public URL to access file
    file_url: Mapped[str] = mapped_column(Text, nullable=False)

    # File type category (image, document, archive, etc)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # MIME type (image/png, application/pdf, etc)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # File size in bytes
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    # User who uploaded (optional, can be null for public uploads)
    uploaded_by: Mapped[Optional[uuid_pkg.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Additional metadata (JSON stored as text)
    file_metadata: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Description/alt text for the file
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    # Relationship to user
    uploader: Mapped[Optional[User]] = relationship("User", back_populates="uploaded_files", init=False)
