from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from base.models import BaseModel
from base.repository import BaseCRUD
from dependencies.session import get_db_session


def get_crud(
    model: type[BaseModel], crud: BaseCRUD
) -> Callable[[AsyncSession], BaseCRUD]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return crud(model, session)

    return func
