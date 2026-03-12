"""
Common enums for content models based on ERD specifications
"""

import enum

from sqlalchemy import Enum as SQLAlchemyEnum


class AccessLevel(enum.Enum):
    """Access level enum for all content types matching ERD"""

    public = "public"
    registered = "registered"
    premium = "premium"


class ContentStatus(enum.Enum):
    """Status enum for all content types matching ERD"""

    draft = "draft"
    published = "published"


class ProjectComplexity(enum.Enum):
    """Complexity level enum for projects"""

    easy = "easy"
    medium = "medium"
    hard = "hard"


# Create reusable SQLAlchemy ENUM types with create_type=False to prevent automatic creation
# The types should already exist in the database via migrations or manual creation
AccessLevelType = SQLAlchemyEnum(
    AccessLevel,
    name="accesslevel",
    create_constraint=True,
    native_enum=True,
    validate_strings=True,
    create_type=False,  # Don't auto-create, assume it exists
)

ContentStatusType = SQLAlchemyEnum(
    ContentStatus,
    name="contentstatus",
    create_constraint=True,
    native_enum=True,
    validate_strings=True,
    create_type=False,  # Don't auto-create, assume it exists
)

ProjectComplexityType = SQLAlchemyEnum(
    ProjectComplexity,
    name="projectcomplexity",
    create_constraint=True,
    native_enum=True,
    validate_strings=True,
    create_type=False,  # Don't auto-create, assume it exists
)
