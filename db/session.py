"""Database Interaction Layer"""
from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from settings import db_settings


engine = create_async_engine(db_settings.DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=True)


async def get_session() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
