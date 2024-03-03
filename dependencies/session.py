"""Database Interaction Layer"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.settings import DBSettings

engine = create_async_engine(DBSettings().DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=True)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
