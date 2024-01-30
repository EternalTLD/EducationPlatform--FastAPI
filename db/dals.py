"""Data Access Layer"""
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
