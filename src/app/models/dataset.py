"""
Dataset model based on ERD specifications
"""

from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base
from .enums import AccessLevel, ContentStatus

if TYPE_CHECKING:
    from .categories import DatasetCategoryLink
    from .contributor import DatasetContributorLink
    from .user import User


class Dataset(Base):
    """Dataset model matching ERD specifications with enhanced fields"""

    __tablename__ = "datasets"
    __allow_unmapped__ = True  # Disable dataclass transform

    # Primary key as UUID to match ERD
    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)

    # Core dataset fields matching ERD
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None)

    # Enhanced Core Info fields
    tagline: Mapped[str | None] = mapped_column(String(500), default=None)
    samples: Mapped[int | None] = mapped_column(Integer, default=0)  # Number of samples in dataset
    view_count: Mapped[int] = mapped_column(Integer, default=0)  # Visitor counter
    download_count: Mapped[int] = mapped_column(Integer, default=0)  # Download counter
    gradient: Mapped[str | None] = mapped_column(String(100), default=None)  # UI gradient colors
    version: Mapped[str | None] = mapped_column(String(50), default="1.0")
    format: Mapped[str | None] = mapped_column(String(100), default=None)  # CSV, JSON, etc.
    license: Mapped[str | None] = mapped_column(String(255), default=None)
    citation: Mapped[str | None] = mapped_column(Text, default=None)

    # Key Features & Use Cases (arrays)
    key_features: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)
    use_cases: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)

    # Technical Specifications (JSON object)
    technical_specs: Mapped[dict | None] = mapped_column(JSONB, default=None)

    # Statistics (JSON object)
    statistics: Mapped[dict | None] = mapped_column(JSONB, default=None)

    # Sample Images (array of URLs)
    sample_images: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)

    # Original Dataset specific fields
    sample_image_url: Mapped[str | None] = mapped_column(Text, default=None)
    file_url: Mapped[str | None] = mapped_column(Text, default=None)
    source: Mapped[str | None] = mapped_column(String(255), default=None)
    size: Mapped[int | None] = mapped_column(BigInteger, default=None)  # File size in bytes

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
    creator: Mapped[User] = relationship("User", back_populates="datasets", init=False)
    category_links: Mapped[list[DatasetCategoryLink]] = relationship(
        "DatasetCategoryLink", back_populates="dataset", init=False
    )
    contributor_links: Mapped[list[DatasetContributorLink]] = relationship(
        "DatasetContributorLink", back_populates="dataset", init=False
    )

    # Helper property to get categories
    @property
    def categories(self):
        """Get all categories for this dataset"""
        return [link.category for link in self.category_links]

    # Helper property to get contributors
    @property
    def contributors(self):
        """Get all contributors for this dataset"""
        return [link.contributor for link in self.contributor_links]
