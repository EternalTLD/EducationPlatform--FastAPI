import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from base.repository import BaseCRUD
from dependencies.repository import get_crud
from utils.hasher import Hasher

from .models import UserModel


class UserBaseCRUD(BaseCRUD[UserModel]):
    """Data access class for User model"""

    async def get_by_email(self, email: str) -> UserModel | None:
        query = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return query.scalar_one_or_none()

    async def authenticate(self, email: str, password: str) -> UserModel | None:
        user = await self.get_by_email(email)
        if user is None or not Hasher.verify_password(password, user.hashed_password):
            return None
        return user

    async def delete(self, id: uuid.UUID) -> UserModel | None:
        user = await self.get_by_id(id)
        if user is None:
            return None
        user.is_active = False
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


UserCRUD = Annotated[UserBaseCRUD, Depends(get_crud(UserModel, UserBaseCRUD))]
