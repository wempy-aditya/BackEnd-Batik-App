"""
Contributor model - Master table for team members/contributors
Can be assigned to projects, publications, datasets, etc.
"""

from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base

if TYPE_CHECKING:
    from .dataset import Dataset
    from .project import Project
    from .publication import Publication


class Contributor(Base):
    """Contributor/Team member master data"""

    __tablename__ = "contributors"
    __allow_unmapped__ = True

    # Primary key
    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7, init=False)

    # Contributor info
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255), default=None)
    role: Mapped[str | None] = mapped_column(String(100), default=None)  # e.g., "Developer", "Researcher", "Designer"
    bio: Mapped[str | None] = mapped_column(Text, default=None)

    # Social/Professional links
    profile_image: Mapped[str | None] = mapped_column(Text, default=None)
    github_url: Mapped[str | None] = mapped_column(Text, default=None)
    linkedin_url: Mapped[str | None] = mapped_column(Text, default=None)
    website_url: Mapped[str | None] = mapped_column(Text, default=None)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), init=False)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, onupdate=lambda: datetime.now(UTC), init=False
    )

    # Relationships to link tables
    project_links: Mapped[list[ProjectContributorLink]] = relationship(
        "ProjectContributorLink", back_populates="contributor", init=False
    )
    publication_links: Mapped[list[PublicationContributorLink]] = relationship(
        "PublicationContributorLink", back_populates="contributor", init=False
    )
    dataset_links: Mapped[list[DatasetContributorLink]] = relationship(
        "DatasetContributorLink", back_populates="contributor", init=False
    )


class ProjectContributorLink(Base):
    """Link table: Projects <-> Contributors"""

    __tablename__ = "project_contributor_links"
    __allow_unmapped__ = True

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7, init=False)

    project_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), init=False
    )
    contributor_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contributors.id", ondelete="CASCADE"), init=False
    )

    # Optional: role in this specific project
    role_in_project: Mapped[str | None] = mapped_column(String(100), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), init=False)

    # Relationships
    project: Mapped[Project] = relationship("Project", back_populates="contributor_links", init=False)
    contributor: Mapped[Contributor] = relationship("Contributor", back_populates="project_links", init=False)


class PublicationContributorLink(Base):
    """Link table: Publications <-> Contributors"""

    __tablename__ = "publication_contributor_links"
    __allow_unmapped__ = True

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7, init=False)

    publication_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("publications.id", ondelete="CASCADE"), init=False
    )
    contributor_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contributors.id", ondelete="CASCADE"), init=False
    )

    # Optional: role in this publication
    role_in_publication: Mapped[str | None] = mapped_column(String(100), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), init=False)

    # Relationships
    publication: Mapped[Publication] = relationship("Publication", back_populates="contributor_links", init=False)
    contributor: Mapped[Contributor] = relationship("Contributor", back_populates="publication_links", init=False)


class DatasetContributorLink(Base):
    """Link table: Datasets <-> Contributors"""

    __tablename__ = "dataset_contributor_links"
    __allow_unmapped__ = True

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid7, init=False)

    dataset_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("datasets.id", ondelete="CASCADE"), init=False
    )
    contributor_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contributors.id", ondelete="CASCADE"), init=False
    )

    # Optional: role in this dataset
    role_in_dataset: Mapped[str | None] = mapped_column(String(100), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), init=False)

    # Relationships
    dataset: Mapped[Dataset] = relationship("Dataset", back_populates="contributor_links", init=False)
    contributor: Mapped[Contributor] = relationship("Contributor", back_populates="dataset_links", init=False)
