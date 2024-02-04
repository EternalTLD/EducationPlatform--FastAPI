import uuid
import datetime

from .base import BaseScheme
from .users import UserResponse


class VideoUpload(BaseScheme):
    title: str
    description: str


class VideoResponse(BaseScheme):
    # id: uuid.UUID
    filename: str
    title: str
    description: str
    user: UserResponse
    # created_at: datetime.datetime
