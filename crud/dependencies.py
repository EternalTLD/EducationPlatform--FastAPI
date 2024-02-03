from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db_session
from models.base import BaseModel
from .base import BaseCRUD


def get_crud(
    model: type[BaseModel], crud: BaseCRUD
) -> Callable[[AsyncSession], BaseCRUD]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return crud(model, session)

    return func
