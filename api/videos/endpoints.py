import uuid

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from ..auth.endpoints import get_current_user
from ..users.models import UserModel
from .repository import VideoCRUD
from .schemas import VideoResponseSchema, VideoUpdateSchema, VideoUploadSchema
from .services import get_video_upload_path
from .tasks import save_video

videos_router = APIRouter()


@videos_router.post("/upload", response_model=VideoResponseSchema)
async def upload_video(
    background_tasks: BackgroundTasks,
    video_crud: VideoCRUD,
    data: VideoUploadSchema = Depends(),
    video_file: UploadFile = File(),
    request_user: UserModel = Depends(get_current_user),
) -> VideoResponseSchema:
    filepath = get_video_upload_path(video_file.filename, request_user.id)
    background_tasks.add_task(save_video, video_file, filepath)
    video = await video_crud.create(
        title=data.title,
        description=data.description,
        filepath=filepath,
        user_id=request_user.id,
    )
    return video


@videos_router.get("/{id}", response_model=VideoResponseSchema)
async def get_video(id: uuid.UUID, video_crud: VideoCRUD) -> VideoResponseSchema:
    video = await video_crud.get_by_id(id)
    if video is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found."
        )
    return video


@videos_router.patch("/{id}", response_model=VideoResponseSchema)
async def update_video(
    id: uuid.UUID,
    video_crud: VideoCRUD,
    data: VideoUpdateSchema = Depends(),
    video: UploadFile = File(),
    request_user: UserModel = Depends(get_current_user),
) -> VideoResponseSchema:
    video = await video_crud.get_by_id(id)
    if video.user_id != request_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be an author of video.",
        )
    updated_video = await video_crud.update(id, data.model_dump())
    return updated_video


@videos_router.delete("/{id}", response_model=VideoResponseSchema)
async def delete_video(
    id: uuid.UUID,
    video_crud: VideoCRUD,
    request_user: UserModel = Depends(get_current_user),
) -> VideoResponseSchema:
    video = await video_crud.get_by_id(id)
    if video.user_id != request_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be an author of video.",
        )

    deleted_video = await video_crud.delete(id)
    if deleted_video is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video doesn't exists.",
        )
    return deleted_video


@videos_router.get("/all/", response_model=list[VideoResponseSchema])
async def get_all_videos(video_crud: VideoCRUD) -> list[VideoResponseSchema]:
    videos = await video_crud.get_all()
    return videos


@videos_router.get("/user/{user_id}", response_model=list[VideoResponseSchema])
async def get_user_videos(
    user_id: uuid.UUID, video_crud: VideoCRUD
) -> list[VideoResponseSchema]:
    videos = await video_crud.filter(user_id=user_id)
    return videos
