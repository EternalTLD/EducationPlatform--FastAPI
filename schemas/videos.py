import uuid
import datetime

from .base import BaseSchema
from .users import UserResponseSchema


class VideoUploadSchema(BaseSchema):
    title: str
    description: str


class VideoResponseSchema(BaseSchema):
    # id: uuid.UUID
    filename: str
    title: str
    description: str
    user: UserResponseSchema
    # created_at: datetime.datetime
