"""Data Access Layer"""
import uuid

from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_user(self, first_name: str, last_name: str, email: str) -> User:
        user = User(first_name=first_name, last_name=last_name, email=email)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar()
        if user is not None:
            return user

    async def delete_user(self, user_id: uuid.UUID) -> User | None:
        stmt = (
            update(User)
            .where(User.id == user_id, User.is_active == True)
            .values(is_active=False)
            .returning(User)
        )
        result = await self.session.execute(stmt)
        deleted_user = result.scalar()
        if deleted_user is not None:
            return deleted_user

    async def update_user(self, user_id: uuid.UUID, **kwargs: dict) -> User | None:
        stmt = update(User).where(User.id == user_id).values(kwargs).returning(User)
        result = await self.session.execute(stmt)
        user = result.scalar()
        if user is not None:
            return user
