import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from models.videos import VideoModel
from .base import BaseCRUD
from .dependencies import get_crud


class VideoBaseCRUD(BaseCRUD[VideoModel]):
    """Data access class for Video model"""


VideoCRUD = Annotated[VideoBaseCRUD, Depends(get_crud(VideoModel, VideoBaseCRUD))]
