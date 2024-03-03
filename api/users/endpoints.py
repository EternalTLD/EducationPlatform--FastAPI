import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from ..auth.endpoints import get_current_user
from .models import UserModel
from .repository import UserCRUD
from .schemas import UserResponseSchema, UserUpdateSchema

user_router = APIRouter()


@user_router.get("/{id}", response_model=UserResponseSchema)
async def get_user(
    id: uuid.UUID,
    user_crud: UserCRUD,
    request_user: UserModel = Depends(get_current_user),
) -> UserResponseSchema:
    user = await user_crud.get_by_id(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    return user


@user_router.delete("/{id}", response_model=UserResponseSchema)
async def delete_user(
    id: uuid.UUID,
    user_crud: UserCRUD,
    request_user: UserModel = Depends(get_current_user),
) -> UserResponseSchema:
    if request_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete other user"
        )

    user = await user_crud.delete(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    return user


@user_router.put("/{id}", response_model=UserResponseSchema)
async def update_user(
    id: uuid.UUID,
    data: UserUpdateSchema,
    user_crud: UserCRUD,
    request_user: UserModel = Depends(get_current_user),
) -> UserResponseSchema:
    if request_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't update other user"
        )

    user = await user_crud.update(
        id, first_name=data.first_name, last_name=data.last_name, email=data.email
    )
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user
