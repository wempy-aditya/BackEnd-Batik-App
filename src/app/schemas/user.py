import uuid as uuid_pkg
from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema
from ..models.user import UserRole


class UserBase(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=255, examples=["User Userson"])]
    email: Annotated[EmailStr, Field(examples=["user.userson@example.com"])]


class User(TimestampSchema, UserBase, UUIDSchema, PersistentDeletion):
    username: Annotated[str | None, Field(min_length=2, max_length=50, examples=["userson"], default=None)]
    profile_image_url: str | None = None
    password_hash: str  # Renamed from hashed_password to match model
    role: UserRole = UserRole.registered
    is_active: bool = True
    is_superuser: bool = False
    tier_id: int | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str  # UUID as string
    name: Annotated[str, Field(min_length=2, max_length=255, examples=["User Userson"])]
    username: str | None
    email: Annotated[EmailStr, Field(examples=["user.userson@example.com"])]
    profile_image_url: str | None
    role: UserRole
    is_active: bool
    is_superuser: bool
    tier_id: int | None
    created_at: str
    updated_at: str | None

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, v: Any) -> str:
        """Convert UUID to string"""
        if isinstance(v, uuid_pkg.UUID):
            return str(v)
        return v

    @field_validator("created_at", mode="before")
    @classmethod
    def validate_created_at(cls, v: Any) -> str:
        """Convert datetime to ISO string"""
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    @field_validator("updated_at", mode="before")
    @classmethod
    def validate_updated_at(cls, v: Any) -> str | None:
        """Convert datetime to ISO string"""
        if isinstance(v, datetime):
            return v.isoformat()
        return v


class UserCreate(UserBase):
    model_config = ConfigDict(extra="forbid")

    username: Annotated[
        str | None, Field(min_length=2, max_length=50, pattern=r"^[a-z0-9]+$", examples=["userson"], default=None)
    ]
    password: Annotated[str, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])]


class UserRegister(BaseModel):
    """Public registration schema - only for UMM email domains"""

    model_config = ConfigDict(extra="forbid")

    name: Annotated[str, Field(min_length=2, max_length=255, examples=["Budi Santoso"])]
    email: Annotated[EmailStr, Field(examples=["budi@webmail.umm.ac.id"])]
    username: Annotated[str, Field(min_length=2, max_length=50, pattern=r"^[a-z0-9]+$", examples=["budisantoso"])]
    password: Annotated[
        str,
        Field(
            min_length=8,
            pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$",
            examples=["Str1ngst!"],
        ),
    ]

    @model_validator(mode="after")
    def validate_umm_email(self) -> "UserRegister":
        allowed_domains = ("@webmail.umm.ac.id", "@umm.ac.id")
        if not any(self.email.endswith(domain) for domain in allowed_domains):
            raise ValueError("Email harus menggunakan domain @webmail.umm.ac.id atau @umm.ac.id")
        return self


class UserCreateInternal(UserBase):
    password_hash: str  # Renamed from hashed_password
    username: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=2, max_length=30, examples=["User Userberg"], default=None)]
    username: Annotated[
        str | None, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userberg"], default=None)
    ]
    email: Annotated[EmailStr | None, Field(examples=["user.userberg@example.com"], default=None)]
    profile_image_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", examples=["https://www.profileimageurl.com"], default=None
        ),
    ]


class UserAdminUpdate(BaseModel):
    """Admin-only user update schema with role and status management"""

    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=2, max_length=255, examples=["User Userberg"], default=None)]
    username: Annotated[
        str | None, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userberg"], default=None)
    ]
    email: Annotated[EmailStr | None, Field(examples=["user.userberg@example.com"], default=None)]
    profile_image_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", examples=["https://www.profileimageurl.com"], default=None
        ),
    ]
    role: Annotated[UserRole | None, Field(description="User role: admin, registered, or premium", default=None)]
    is_active: Annotated[bool | None, Field(description="User active status", default=None)]
    is_superuser: Annotated[bool | None, Field(description="Superuser privileges", default=None)]
    tier_id: Annotated[int | None, Field(description="User tier ID", default=None)]


class UserUpdateInternal(UserUpdate):
    updated_at: datetime


class UserAdminUpdateInternal(UserAdminUpdate):
    """Internal schema for admin updates with timestamp"""

    updated_at: datetime


class UserTierUpdate(BaseModel):
    tier_id: int


class UserDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class UserRestoreDeleted(BaseModel):
    is_deleted: bool
