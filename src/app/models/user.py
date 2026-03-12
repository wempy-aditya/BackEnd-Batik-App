from __future__ import annotations

import enum
import uuid as uuid_pkg
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SQLAlchemyEnum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from ..core.db.database import Base

if TYPE_CHECKING:
    from .ai_models import AIModel
    from .dataset import Dataset
    from .file import File
    from .gallery import Gallery
    from .news import News
    from .project import Project
    from .publication import Publication
    from .subscription import Subscription


class UserRole(enum.Enum):
    """User role enum matching ERD specifications"""

    admin = "admin"
    registered = "registered"
    premium = "premium"


# Create reusable SQLAlchemy ENUM type
UserRoleType = SQLAlchemyEnum(
    UserRole,
    name="userrole",
    create_constraint=True,
    native_enum=True,
    validate_strings=True,
    create_type=False,  # Don't auto-create, assume it exists
)


class User(Base):
    __tablename__ = "users"  # Changed to plural to match ERD
    __allow_unmapped__ = True  # Disable dataclass transform

    # Primary key as UUID to match ERD
    id: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid7, init=False)

    # Core user fields matching ERD
    name: Mapped[str] = mapped_column(String(255))  # Increased length
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)  # Renamed to match ERD

    # Role enum matching ERD
    role: Mapped[UserRole] = mapped_column(UserRoleType, default=UserRole.registered)

    # Status fields
    is_active: Mapped[bool] = mapped_column(default=True)  # Added from ERD
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    # Optional fields (keep some boilerplate features)
    username: Mapped[str | None] = mapped_column(String(50), unique=True, index=True, default=None)
    profile_image_url: Mapped[str | None] = mapped_column(String, default=None)

    # Legacy fields for compatibility (can be removed later)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    # Keep tier relationship for backward compatibility
    tier_id: Mapped[int | None] = mapped_column(ForeignKey("tier.id"), index=True, default=None, init=False)

    # Relationships
    subscriptions: Mapped[list[Subscription]] = relationship("Subscription", back_populates="user", init=False)

    # Content relationships (one user can create many content items)
    projects: Mapped[list[Project]] = relationship("Project", back_populates="creator", init=False)
    datasets: Mapped[list[Dataset]] = relationship("Dataset", back_populates="creator", init=False)
    publications: Mapped[list[Publication]] = relationship("Publication", back_populates="creator", init=False)
    news: Mapped[list[News]] = relationship("News", back_populates="creator", init=False)
    ai_models: Mapped[list[AIModel]] = relationship("AIModel", back_populates="creator", init=False)
    gallery_items: Mapped[list[Gallery]] = relationship("Gallery", back_populates="created_by_user", init=False)
    uploaded_files: Mapped[list[File]] = relationship("File", back_populates="uploader", init=False)
