import uuid
from typing import Generic, TypeVar

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from base.models import BaseModel

Model = TypeVar("Model", bound=BaseModel)


class BaseCRUD(Generic[Model]):
    """Base data access class for CRUD operations"""

    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, id: uuid.UUID) -> Model | None:
        return await self.session.get(self.model, id)

    async def create(self, **kwargs) -> Model:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, id: uuid.UUID, **kwargs) -> Model:
        await self.session.execute(
            update(self.model).filter_by(self.model.id == id).values(**kwargs)
        )
        await self.session.commit()

        updated_instance = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )

        return updated_instance.scalar_one()

    async def delete(self, id: uuid.UUID) -> Model | None:
        instance = await self.get_by_id(id)
        if instance:
            self.session.delete(instance)
            await self.session.commit()
        return instance

    async def filter(self, **kwargs) -> list[Model]:
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all(self) -> list[Model]:
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
