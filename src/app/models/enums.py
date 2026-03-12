"""
Common enums for content models based on ERD specifications
"""

import enum


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
