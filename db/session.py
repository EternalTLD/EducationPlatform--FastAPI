"""Database Interaction Layer"""
from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config.settings import DBSettings


engine = create_async_engine(DBSettings().DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=True)


async def get_db_session() -> Generator[AsyncSession, None, None]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
