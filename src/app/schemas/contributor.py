"""
Contributor schemas for request/response models
"""

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContributorBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255, examples=["John Doe"])]
    email: Annotated[EmailStr | None, Field(examples=["john@example.com"], default=None)]
    role: Annotated[str | None, Field(max_length=100, examples=["Lead Developer"], default=None)]
    bio: Annotated[str | None, Field(max_length=1000, examples=["Experienced software engineer..."], default=None)]

    profile_image: Annotated[str | None, Field(examples=["https://example.com/avatar.jpg"], default=None)]
    github_url: Annotated[str | None, Field(examples=["https://github.com/johndoe"], default=None)]
    linkedin_url: Annotated[str | None, Field(examples=["https://linkedin.com/in/johndoe"], default=None)]
    website_url: Annotated[str | None, Field(examples=["https://johndoe.com"], default=None)]


class ContributorCreate(ContributorBase):
    model_config = ConfigDict(extra="forbid")


class ContributorUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=1, max_length=255, default=None)]
    email: Annotated[EmailStr | None, Field(default=None)]
    role: Annotated[str | None, Field(max_length=100, default=None)]
    bio: Annotated[str | None, Field(max_length=1000, default=None)]

    profile_image: Annotated[str | None, Field(default=None)]
    github_url: Annotated[str | None, Field(default=None)]
    linkedin_url: Annotated[str | None, Field(default=None)]
    website_url: Annotated[str | None, Field(default=None)]


class ContributorRead(ContributorBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime | None


# Assignment schemas
class ContributorAssignment(BaseModel):
    """Schema for assigning contributors to content"""

    model_config = ConfigDict(extra="forbid")

    contributor_ids: list[UUID] = Field(description="List of contributor UUIDs to assign")
    roles: list[str | None] | None = Field(
        default=None, description="Optional: specific roles for each contributor in this content"
    )
