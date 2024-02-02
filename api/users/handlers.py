"""Project handlers"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db_session
from db.dals import UserDAL
from db.models import User
from api.schemas.users import UserResponse, UserUpdate
from api.auth.handlers import get_current_user

user_router = APIRouter()


@user_router.get("/{id}", response_model=UserResponse)
async def get_user(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    credentials: User = Depends(get_current_user),
) -> UserResponse:
    user_dal = UserDAL(session)
    user = await user_dal.get_user_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
    )


@user_router.delete("/{id}", response_model=UserResponse)
async def delete_user(
    id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
    credentials: User = Depends(get_current_user),
) -> UserResponse:
    user_dal = UserDAL(session)
    user = await user_dal.delete_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
    )


@user_router.patch("/{id}", response_model=UserResponse)
async def update_user(
    id: uuid.UUID,
    data: UserUpdate,
    session: AsyncSession = Depends(get_db_session),
    credentials: User = Depends(get_current_user),
) -> UserResponse:
    if data.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail="At least one parameter required")

    user_dal = UserDAL(session)
    user = await user_dal.update_user(id, **data.model_dump(exclude_none=True))
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
    )
