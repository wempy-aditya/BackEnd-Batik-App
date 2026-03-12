"""
Publication model based on ERD specifications
"""

from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base
from .enums import AccessLevel, AccessLevelType, ContentStatus, ContentStatusType

if TYPE_CHECKING:
    from .categories import PublicationCategoryLink
    from .contributor import PublicationContributorLink
    from .user import User


class Publication(Base):
    """Publication model matching ERD specifications"""

    __tablename__ = "publications"
    __allow_unmapped__ = True  # Disable dataclass transform

    # Primary key as UUID to match ERD
    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)

    # Core publication fields matching ERD
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    abstract: Mapped[str | None] = mapped_column(Text, default=None)

    # New Core Info fields
    authors: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)
    venue: Mapped[str | None] = mapped_column(String(255), default=None)
    citations: Mapped[int | None] = mapped_column(Integer, default=0)
    doi: Mapped[str | None] = mapped_column(String(255), default=None)
    keywords: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)
    impact: Mapped[str | None] = mapped_column(String(50), default=None)  # Can be factor like "2.5" or rating
    pages: Mapped[str | None] = mapped_column(String(50), default=None)  # e.g., "123-145"

    # Journal Specific fields
    volume: Mapped[str | None] = mapped_column(String(50), default=None)
    issue: Mapped[str | None] = mapped_column(String(50), default=None)
    publisher: Mapped[str | None] = mapped_column(String(255), default=None)

    # Content Sections
    methodology: Mapped[str | None] = mapped_column(Text, default=None)
    results: Mapped[str | None] = mapped_column(Text, default=None)
    conclusions: Mapped[str | None] = mapped_column(Text, default=None)

    # Publication specific fields
    pdf_url: Mapped[str | None] = mapped_column(Text, default=None)
    journal_name: Mapped[str | None] = mapped_column(String(255), default=None)
    year: Mapped[int | None] = mapped_column(Integer, default=None)
    graphical_abstract_url: Mapped[str | None] = mapped_column(Text, default=None)

    # Statistics/Counters
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    download_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

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
    creator: Mapped[User] = relationship("User", back_populates="publications", init=False)
    category_links: Mapped[list[PublicationCategoryLink]] = relationship(
        "PublicationCategoryLink", back_populates="publication", init=False
    )
    contributor_links: Mapped[list[PublicationContributorLink]] = relationship(
        "PublicationContributorLink", back_populates="publication", init=False
    )

    # Helper property to get categories
    @property
    def categories(self):
        """Get all categories for this publication"""
        return [link.category for link in self.category_links]

    # Helper property to get contributors
    @property
    def contributors(self):
        """Get all contributors for this publication"""
        return [link.contributor for link in self.contributor_links]
