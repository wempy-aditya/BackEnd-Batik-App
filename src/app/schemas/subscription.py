"""
Subscription schemas updated for UUID-based User model
"""

from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..models.subscription import SubscriptionStatus


class SubscriptionBase(BaseModel):
    plan_name: Annotated[str, Field(min_length=1, max_length=100, examples=["Premium Monthly"])]
    price: Annotated[Decimal, Field(ge=0, decimal_places=2, examples=[9.99])]
    start_date: datetime
    end_date: datetime
    payment_ref: Annotated[str | None, Field(max_length=255, examples=["PAYMENT_123456"], default=None)]


class SubscriptionCreate(SubscriptionBase):
    model_config = ConfigDict(extra="forbid")

    user_id: UUID  # Required when creating


class SubscriptionUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    plan_name: Annotated[str | None, Field(min_length=1, max_length=100, default=None)]
    price: Annotated[Decimal | None, Field(ge=0, decimal_places=2, default=None)]
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: SubscriptionStatus | None = None
    payment_ref: Annotated[str | None, Field(max_length=255, default=None)]


class SubscriptionUpdateInternal(SubscriptionUpdate):
    updated_at: datetime


class SubscriptionRead(SubscriptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    status: SubscriptionStatus
    created_at: datetime
    updated_at: datetime | None


class SubscriptionReadWithUser(SubscriptionRead):
    user_name: str | None = None
    user_email: str | None = None


class SubscriptionBulkUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subscription_ids: list[UUID]
    updates: SubscriptionUpdate
