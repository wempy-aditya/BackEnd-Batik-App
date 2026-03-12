"""
Project model based on ERD specifications
"""

from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base
from .enums import AccessLevel, AccessLevelType, ContentStatus, ContentStatusType, ProjectComplexity, ProjectComplexityType

if TYPE_CHECKING:
    from .categories import ProjectCategoryLink
    from .contributor import ProjectContributorLink
    from .user import User


class Project(Base):
    """Project model matching ERD specifications"""

    __tablename__ = "projects"
    __allow_unmapped__ = True  # Disable dataclass transform

    # Primary key as UUID to match ERD
    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)

    # Core project fields matching ERD
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    full_description: Mapped[str | None] = mapped_column(Text, default=None)

    # Technologies and project details
    technologies: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)
    challenges: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)
    achievements: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)
    future_work: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)

    # Media and metadata
    thumbnail_url: Mapped[str | None] = mapped_column(Text, default=None)
    demo_url: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)  # Multiple demo/prototype links
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)

    # Project metadata
    complexity: Mapped[ProjectComplexity | None] = mapped_column(ProjectComplexityType, default=None)
    start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)  # TEXT[] in ERD

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
    creator: Mapped[User] = relationship("User", back_populates="projects", init=False)
    category_links: Mapped[list[ProjectCategoryLink]] = relationship(
        "ProjectCategoryLink", back_populates="project", init=False
    )
    contributor_links: Mapped[list[ProjectContributorLink]] = relationship(
        "ProjectContributorLink", back_populates="project", init=False
    )

    # Helper property to get categories
    @property
    def categories(self):
        """Get all categories for this project"""
        return [link.category for link in self.category_links]

    # Helper property to get contributors
    @property
    def contributors(self):
        """Get all contributors for this project"""
        return [link.contributor for link in self.contributor_links]
