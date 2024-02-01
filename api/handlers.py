"""Project handlers"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db_session
from db.dals import UserDAL
from api.models import ShowUser, CreateUser, DeleteUser, UpdateUser
from api.utils import Hasher

user_router = APIRouter()


@user_router.post("/user_create", response_model=ShowUser)
async def create_user(
    body: CreateUser, db_session: AsyncSession = Depends(get_db_session)
) -> ShowUser:
    async with db_session.begin():
        user_dal = UserDAL(db_session)
        user = await user_dal.create_user(
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            password=Hasher.get_hash_password(body.password),
        )
        return ShowUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


@user_router.get("/{user_id}", response_model=ShowUser)
async def get_user(
    user_id: uuid.UUID, db_session: AsyncSession = Depends(get_db_session)
) -> ShowUser:
    async with db_session.begin():
        user_dal = UserDAL(db_session)
        user = await user_dal.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with id {user_id} not found"
            )
        return ShowUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


@user_router.delete("/{user_id}", response_model=DeleteUser)
async def delete_user(
    user_id: uuid.UUID, db_session: AsyncSession = Depends(get_db_session)
) -> DeleteUser:
    async with db_session.begin():
        user_dal = UserDAL(db_session)
        user = await user_dal.delete_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with id {user_id} not found"
            )
        return DeleteUser(id=user.id, is_active=user.is_active)


@user_router.patch("/{user_id}", response_model=ShowUser)
async def update_user(
    user_id: uuid.UUID,
    body: UpdateUser,
    db_session: AsyncSession = Depends(get_db_session),
) -> ShowUser:
    if body.model_dump(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail="At least one parameter required")

    async with db_session.begin():
        user_dal = UserDAL(db_session)
        user = await user_dal.update_user(user_id, **body.model_dump(exclude_none=True))
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with id {user_id} not found"
            )
        return ShowUser(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
