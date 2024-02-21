import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from models.users import UserModel
from .base import BaseCRUD
from .dependencies import get_crud


class VideoBaseCRUD(BaseCRUD[UserModel]):
    """Data access class for Video model"""

    def get_video(self, id: uuid.UUID):
        pass


VideoCRUD = Annotated[VideoBaseCRUD, Depends(get_crud(UserModel, VideoBaseCRUD))]
