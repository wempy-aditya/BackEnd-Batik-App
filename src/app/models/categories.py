"""
Category models for all content types based on ERD specifications.
Each content domain has its own category table for better organization.
"""

from __future__ import annotations

import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base

if TYPE_CHECKING:
    from .ai_models import AIModel
    from .dataset import Dataset
    from .gallery import Gallery
    from .news import News
    from .project import Project
    from .publication import Publication


# ==================== CATEGORY TABLES ====================
# Each content domain has its own category table as per ERD


class ProjectCategory(Base):
    """Categories for Projects content"""

    __tablename__ = "project_categories"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Relationships
    project_links: Mapped[list[ProjectCategoryLink]] = relationship(
        "ProjectCategoryLink", back_populates="category", init=False
    )


class DatasetCategory(Base):
    """Categories for Datasets content"""

    __tablename__ = "dataset_categories"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Relationships
    dataset_links: Mapped[list[DatasetCategoryLink]] = relationship(
        "DatasetCategoryLink", back_populates="category", init=False
    )


class PublicationCategory(Base):
    """Categories for Publications content"""

    __tablename__ = "publication_categories"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Relationships
    publication_links: Mapped[list[PublicationCategoryLink]] = relationship(
        "PublicationCategoryLink", back_populates="category", init=False
    )


class NewsCategory(Base):
    """Categories for News content"""

    __tablename__ = "news_categories"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Relationships
    news_links: Mapped[list[NewsCategoryLink]] = relationship("NewsCategoryLink", back_populates="category", init=False)


class ModelCategory(Base):
    """Categories for Models content"""

    __tablename__ = "model_categories"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Relationships
    model_links: Mapped[list[ModelCategoryLink]] = relationship(
        "ModelCategoryLink", back_populates="category", init=False
    )


class GalleryCategory(Base):
    """Categories for Gallery content"""

    __tablename__ = "gallery_categories"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Relationships
    gallery_links: Mapped[list[GalleryCategoryLink]] = relationship(
        "GalleryCategoryLink", back_populates="category", init=False
    )


# ==================== MANY-TO-MANY LINK TABLES ====================
# These tables handle the many-to-many relationships between content and categories


class ProjectCategoryLink(Base):
    """Many-to-many link between Projects and ProjectCategories"""

    __tablename__ = "project_category_links"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    project_id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id"), index=True)
    category_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("project_categories.id"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Ensure unique project-category combinations
    __table_args__ = (UniqueConstraint("project_id", "category_id", name="unique_project_category"),)

    # Relationships
    project: Mapped[Project] = relationship("Project", back_populates="category_links", init=False)
    category: Mapped[ProjectCategory] = relationship("ProjectCategory", back_populates="project_links", init=False)


class DatasetCategoryLink(Base):
    """Many-to-many link between Datasets and DatasetCategories"""

    __tablename__ = "dataset_category_links"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    dataset_id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("datasets.id"), index=True)
    category_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("dataset_categories.id"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Ensure unique dataset-category combinations
    __table_args__ = (UniqueConstraint("dataset_id", "category_id", name="unique_dataset_category"),)

    # Relationships
    dataset: Mapped[Dataset] = relationship("Dataset", back_populates="category_links", init=False)
    category: Mapped[DatasetCategory] = relationship("DatasetCategory", back_populates="dataset_links", init=False)


class PublicationCategoryLink(Base):
    """Many-to-many link between Publications and PublicationCategories"""

    __tablename__ = "publication_category_links"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    publication_id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("publications.id"), index=True)
    category_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("publication_categories.id"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Ensure unique publication-category combinations
    __table_args__ = (UniqueConstraint("publication_id", "category_id", name="unique_publication_category"),)

    # Relationships
    publication: Mapped[Publication] = relationship("Publication", back_populates="category_links", init=False)
    category: Mapped[PublicationCategory] = relationship(
        "PublicationCategory", back_populates="publication_links", init=False
    )


class NewsCategoryLink(Base):
    """Many-to-many link between News and NewsCategories"""

    __tablename__ = "news_category_links"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    news_id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("news.id"), index=True)
    category_id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("news_categories.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Ensure unique news-category combinations
    __table_args__ = (UniqueConstraint("news_id", "category_id", name="unique_news_category"),)

    # Relationships
    news: Mapped[News] = relationship("News", back_populates="category_links", init=False)
    category: Mapped[NewsCategory] = relationship("NewsCategory", back_populates="news_links", init=False)


class ModelCategoryLink(Base):
    """Many-to-many link between Models and ModelCategories"""

    __tablename__ = "model_category_links"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    model_id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("models.id"), index=True)
    category_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("model_categories.id"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Ensure unique model-category combinations
    __table_args__ = (UniqueConstraint("model_id", "category_id", name="unique_model_category"),)

    # Relationships
    model: Mapped[AIModel] = relationship("AIModel", back_populates="category_links", init=False)
    category: Mapped[ModelCategory] = relationship("ModelCategory", back_populates="model_links", init=False)


class GalleryCategoryLink(Base):
    """Many-to-many link between Gallery and GalleryCategories"""

    __tablename__ = "gallery_category_links"
    __allow_unmapped__ = True  # Disable dataclass transform

    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)
    gallery_id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gallery.id"), index=True)
    category_id: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("gallery_categories.id"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    # Ensure unique gallery-category combinations
    __table_args__ = (UniqueConstraint("gallery_id", "category_id", name="unique_gallery_category"),)

    # Relationships
    gallery: Mapped[Gallery] = relationship("Gallery", back_populates="category_links", init=False)
    category: Mapped[GalleryCategory] = relationship("GalleryCategory", back_populates="gallery_links", init=False)
