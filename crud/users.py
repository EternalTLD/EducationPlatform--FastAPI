import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from models.users import User
from utils.hasher import Hasher
from .base import BaseCRUD
from .dependencies import get_crud


class UserBaseCRUD(BaseCRUD[User]):
    """Data access class for User model"""

    async def get_by_email(self, email: str) -> User | None:
        query = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return query.scalar_one_or_none()

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.get_by_email(email)
        if user is None or not Hasher.verify_password(password, user.hashed_password):
            return None
        return user

    async def delete(self, id: uuid.UUID) -> User | None:
        user = await self.get_by_id(id)
        if user is None:
            return None
        user.is_active = False
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


UserCRUD = Annotated[UserBaseCRUD, Depends(get_crud(User, UserBaseCRUD))]
