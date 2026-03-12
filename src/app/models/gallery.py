"""
Gallery model based on existing database structure
"""

from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base

if TYPE_CHECKING:
    from .ai_models import AIModel
    from .categories import GalleryCategoryLink
    from .user import User


class Gallery(Base):
    """Gallery model matching existing database structure"""

    __tablename__ = "gallery"
    __allow_unmapped__ = True  # Disable dataclass transform

    # Primary key
    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7, init=False)

    # Gallery fields (matching existing database)
    prompt: Mapped[str | None] = mapped_column(default=None)
    image_url: Mapped[str | None] = mapped_column(default=None)
    extra_metadata: Mapped[dict | None] = mapped_column(JSONB, default=None)

    # Foreign keys (matching existing database)
    model_id: Mapped[uuid_pkg.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("models.id"), default=None, init=False
    )
    created_by: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), init=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), init=False)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, onupdate=lambda: datetime.now(UTC), init=False
    )

    # Relationships
    created_by_user: Mapped[User] = relationship("User", back_populates="gallery_items", init=False)
    model: Mapped[AIModel] = relationship("AIModel", back_populates="gallery_items", init=False)
    category_links: Mapped[list[GalleryCategoryLink]] = relationship(
        "GalleryCategoryLink", back_populates="gallery", init=False
    )

    # Helper property to get categories
    @property
    def categories(self):
        """Get all categories for this gallery item"""
        return [link.category for link in self.category_links]
