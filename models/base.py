import uuid

from sqlalchemy import types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, primary_key=True, default=uuid.uuid4
    )
