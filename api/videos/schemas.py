import datetime
import uuid

from base.schemas import BaseSchema


class VideoUploadSchema(BaseSchema):
    title: str
    description: str


class VideoUpdateSchema(VideoUploadSchema):
    pass


class VideoResponseSchema(BaseSchema):
    id: uuid.UUID
    title: str
    description: str
    created_at: datetime.datetime
    user_id: uuid.UUID
