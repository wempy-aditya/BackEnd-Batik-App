from typing import Annotated, Any, cast

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_rate_limit import crud_rate_limits
from ...crud.crud_tier import crud_tiers
from ...crud.crud_users import crud_users
from ...schemas.tier import TierRead
from ...schemas.user import UserAdminUpdate, UserCreate, UserCreateInternal, UserRead, UserTierUpdate, UserUpdate

router = APIRouter(tags=["users"])


@router.post("/user", response_model=UserRead, status_code=201)
async def write_user(
    request: Request, user: UserCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> UserRead:
    email_row = await crud_users.exists(db=db, email=user.email)
    if email_row:
        raise DuplicateValueException("Email is already registered")

    # Only check username if it's provided
    if user.username is not None:
        username_row = await crud_users.exists(db=db, username=user.username)
        if username_row:
            raise DuplicateValueException("Username not available")

    user_internal_dict = user.model_dump()
    user_internal_dict["password_hash"] = get_password_hash(password=user_internal_dict["password"])
    del user_internal_dict["password"]

    user_internal = UserCreateInternal(**user_internal_dict)
    created_user = await crud_users.create(db=db, object=user_internal)

    user_read = await crud_users.get(db=db, id=created_user.id, schema_to_select=UserRead)
    if user_read is None:
        raise NotFoundException("Created user not found")

    return cast(UserRead, user_read)


@router.get("/users", response_model=PaginatedListResponse[UserRead])
async def read_users(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    users_data = await crud_users.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=users_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/user/me/", response_model=UserRead)
async def read_users_me(request: Request, current_user: Annotated[dict, Depends(get_current_user)]) -> dict:
    return current_user


@router.get("/user/{username}", response_model=UserRead)
async def read_user(request: Request, username: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> UserRead:
    db_user = await crud_users.get(db=db, username=username, is_deleted=False, schema_to_select=UserRead)
    if db_user is None:
        raise NotFoundException("User not found")

    return cast(UserRead, db_user)


@router.patch("/user/{username}")
async def patch_user(
    request: Request,
    values: UserUpdate,
    username: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_user = await crud_users.get(db=db, username=username)
    if db_user is None:
        raise NotFoundException("User not found")

    if isinstance(db_user, dict):
        db_username = db_user["username"]
        db_email = db_user["email"]
    else:
        db_username = db_user.username
        db_email = db_user.email

    if db_username != current_user["username"]:
        raise ForbiddenException()

    if values.email is not None and values.email != db_email:
        if await crud_users.exists(db=db, email=values.email):
            raise DuplicateValueException("Email is already registered")

    if values.username is not None and values.username != db_username:
        if await crud_users.exists(db=db, username=values.username):
            raise DuplicateValueException("Username not available")

    await crud_users.update(db=db, object=values, username=username)
    return {"message": "User updated"}


@router.delete("/user/{username}")
async def erase_user(
    request: Request,
    username: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
    token: str = Depends(oauth2_scheme),
) -> dict[str, str]:
    db_user = await crud_users.get(db=db, username=username, schema_to_select=UserRead)
    if not db_user:
        raise NotFoundException("User not found")

    # Allow user to delete their own account OR superuser to delete any account
    is_superuser = current_user.get("is_superuser", False)
    if username != current_user["username"] and not is_superuser:
        raise ForbiddenException()

    await crud_users.delete(db=db, username=username)
    await blacklist_token(token=token, db=db)
    return {"message": "User deleted"}


@router.delete("/db_user/{username}", dependencies=[Depends(get_current_superuser)])
async def erase_db_user(
    request: Request,
    username: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    token: str = Depends(oauth2_scheme),
) -> dict[str, str]:
    db_user = await crud_users.exists(db=db, username=username)
    if not db_user:
        raise NotFoundException("User not found")

    await crud_users.db_delete(db=db, username=username)
    await blacklist_token(token=token, db=db)
    return {"message": "User deleted from the database"}


@router.get("/user/{username}/rate_limits", dependencies=[Depends(get_current_superuser)])
async def read_user_rate_limits(
    request: Request, username: str, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, Any]:
    db_user = await crud_users.get(db=db, username=username, schema_to_select=UserRead)
    if db_user is None:
        raise NotFoundException("User not found")

    db_user = cast(UserRead, db_user)
    user_dict = db_user.model_dump()
    if db_user.tier_id is None:
        user_dict["tier_rate_limits"] = []
        return user_dict

    db_tier = await crud_tiers.get(db=db, id=db_user.tier_id, schema_to_select=TierRead)
    if db_tier is None:
        raise NotFoundException("Tier not found")

    db_tier = cast(TierRead, db_tier)
    db_rate_limits = await crud_rate_limits.get_multi(db=db, tier_id=db_tier.id)

    user_dict["tier_rate_limits"] = db_rate_limits["data"]

    return user_dict


@router.get("/user/{username}/tier")
async def read_user_tier(
    request: Request, username: str, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict | None:
    db_user = await crud_users.get(db=db, username=username, schema_to_select=UserRead)
    if db_user is None:
        raise NotFoundException("User not found")

    db_user = cast(UserRead, db_user)
    if db_user.tier_id is None:
        return None

    db_tier = await crud_tiers.get(db=db, id=db_user.tier_id, schema_to_select=TierRead)
    if not db_tier:
        raise NotFoundException("Tier not found")

    db_tier = cast(TierRead, db_tier)

    user_dict = db_user.model_dump()
    tier_dict = db_tier.model_dump()

    for key, value in tier_dict.items():
        user_dict[f"tier_{key}"] = value

    return user_dict


@router.patch("/user/{username}/tier", dependencies=[Depends(get_current_superuser)])
async def patch_user_tier(
    request: Request, username: str, values: UserTierUpdate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    db_user = await crud_users.get(db=db, username=username, schema_to_select=UserRead)
    if db_user is None:
        raise NotFoundException("User not found")

    db_user = cast(UserRead, db_user)
    db_tier = await crud_tiers.get(db=db, id=values.tier_id, schema_to_select=TierRead)
    if db_tier is None:
        raise NotFoundException("Tier not found")

    await crud_users.update(db=db, object=values.model_dump(), username=username)
    return {"message": f"User {db_user.name} Tier updated"}


@router.patch("/user/{username}/admin", dependencies=[Depends(get_current_superuser)])
async def admin_update_user(
    request: Request,
    username: str,
    values: UserAdminUpdate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    """
    Admin endpoint to update user role, status, and other fields
    Requires superuser privileges
    """
    db_user = await crud_users.get(db=db, username=username)
    if db_user is None:
        raise NotFoundException("User not found")

    # Check for duplicate email if being changed
    if values.email is not None:
        current_email = db_user["email"] if isinstance(db_user, dict) else db_user.email
        if values.email != current_email:
            if await crud_users.exists(db=db, email=values.email):
                raise DuplicateValueException("Email is already registered")

    # Check for duplicate username if being changed
    if values.username is not None:
        current_username = db_user["username"] if isinstance(db_user, dict) else db_user.username
        if values.username != current_username:
            if await crud_users.exists(db=db, username=values.username):
                raise DuplicateValueException("Username not available")

    # Verify tier exists if being changed
    if values.tier_id is not None:
        db_tier = await crud_tiers.get(db=db, id=values.tier_id)
        if db_tier is None:
            raise NotFoundException("Tier not found")

    await crud_users.update(db=db, object=values.model_dump(exclude_unset=True), username=username)

    action_messages = []
    if values.role is not None:
        action_messages.append(f"role set to {values.role.value}")
    if values.is_active is not None:
        action_messages.append(f"status set to {'active' if values.is_active else 'inactive'}")
    if values.is_superuser is not None:
        action_messages.append(f"superuser set to {values.is_superuser}")

    action_str = ", ".join(action_messages) if action_messages else "updated"
    return {"message": f"User {username} {action_str}"}


@router.get("/users/role/{role}", dependencies=[Depends(get_current_superuser)])
async def get_users_by_role(
    request: Request,
    role: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    """
    Get users by role (admin, registered, premium)
    Requires superuser privileges
    """
    from ...models.user import UserRole

    try:
        user_role = UserRole(role)
    except ValueError:
        raise NotFoundException(f"Invalid role: {role}. Must be one of: admin, registered, premium")

    users_data = await crud_users.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        role=user_role,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=users_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/users/status/{status}", dependencies=[Depends(get_current_superuser)])
async def get_users_by_status(
    request: Request,
    status: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    """
    Get users by active status (active/inactive)
    Requires superuser privileges
    """
    if status.lower() not in ["active", "inactive"]:
        raise NotFoundException(f"Invalid status: {status}. Must be 'active' or 'inactive'")

    is_active = status.lower() == "active"

    users_data = await crud_users.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        is_active=is_active,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=users_data, page=page, items_per_page=items_per_page)
    return response
