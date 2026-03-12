"""
AI Model model based on ERD specifications
"""

from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base
from .enums import AccessLevel, AccessLevelType, ContentStatus, ContentStatusType

if TYPE_CHECKING:
    from .categories import ModelCategoryLink
    from .gallery import Gallery
    from .user import User


class AIModel(Base):
    """AI Model matching ERD specifications"""

    __tablename__ = "models"
    __allow_unmapped__ = True  # Disable dataclass transform

    # Primary key as UUID to match ERD
    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)

    # Core model fields matching ERD
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    # AI Model specific fields
    architecture: Mapped[str | None] = mapped_column(String(255), default=None)
    dataset_used: Mapped[str | None] = mapped_column(String(255), default=None)
    metrics: Mapped[dict | None] = mapped_column(JSONB, default=None)  # Store accuracy, f1, fid, etc.
    model_file_url: Mapped[str | None] = mapped_column(Text, default=None)

    # Access control and status
    access_level: Mapped[AccessLevel] = mapped_column(AccessLevelType, default=AccessLevel.public)
    status: Mapped[ContentStatus] = mapped_column(ContentStatusType, default=ContentStatus.draft)

    # User relationship
    created_by: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), index=True, init=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    # Relationships
    creator: Mapped[User] = relationship("User", back_populates="ai_models", init=False)
    category_links: Mapped[list[ModelCategoryLink]] = relationship(
        "ModelCategoryLink", back_populates="model", init=False
    )
    gallery_items: Mapped[list[Gallery]] = relationship(
        "Gallery", back_populates="model", init=False
    )  # One model can generate many gallery items

    # Helper property to get categories
    @property
    def categories(self):
        """Get all categories for this model"""
        return [link.category for link in self.category_links]
