"""
News model based on ERD specifications
"""

from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base
from .enums import AccessLevel, ContentStatus

if TYPE_CHECKING:
    from .categories import NewsCategoryLink
    from .user import User


class News(Base):
    """News model matching ERD specifications"""

    __tablename__ = "news"
    __allow_unmapped__ = True  # Disable dataclass transform

    # Primary key as UUID to match ERD
    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)

    # Core news fields matching ERD
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    content: Mapped[str | None] = mapped_column(Text, default=None)  # Markdown content

    # News specific fields
    thumbnail_url: Mapped[str | None] = mapped_column(Text, default=None)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)  # TEXT[] in ERD

    # Access control and status
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel), default=AccessLevel.public)
    status: Mapped[ContentStatus] = mapped_column(Enum(ContentStatus), default=ContentStatus.draft)

    # User relationship
    created_by: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), index=True, init=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    # Relationships
    creator: Mapped[User] = relationship("User", back_populates="news", init=False)
    category_links: Mapped[list[NewsCategoryLink]] = relationship("NewsCategoryLink", back_populates="news", init=False)

    # Helper property to get categories
    @property
    def categories(self):
        """Get all categories for this news"""
        return [link.category for link in self.category_links]
