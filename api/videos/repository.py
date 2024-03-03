from typing import Annotated

from fastapi import Depends

from base.repository import BaseCRUD
from dependencies.repository import get_crud

from .models import VideoModel


class VideoBaseCRUD(BaseCRUD[VideoModel]):
    """Data access class for Video model"""


VideoCRUD = Annotated[VideoBaseCRUD, Depends(get_crud(VideoModel, VideoBaseCRUD))]
