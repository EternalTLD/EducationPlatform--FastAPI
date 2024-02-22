import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends, BackgroundTasks, status

from schemas.videos import VideoUploadSchema, VideoResponseSchema, VideoUpdateSchema
from api.auth.endpoints import get_current_user
from models.users import UserModel
from crud.videos import VideoCRUD
from .tasks import save_video, get_video_upload_path

videos_router = APIRouter()


@videos_router.post("/upload", response_model=VideoResponseSchema)
async def upload_video(
    background_tasks: BackgroundTasks,
    video_crud: VideoCRUD,
    data: VideoUploadSchema = Depends(),
    video_file: UploadFile = File(),
    request_user: UserModel = Depends(get_current_user),
) -> VideoResponseSchema:
    filepath = get_video_upload_path(video_file.filename)
    background_tasks.add_task(save_video, video_file, filepath)
    video = await video_crud.create(
        title=data.title,
        description=data.description,
        filepath=filepath,
        user_id=request_user.id,
    )
    return VideoResponseSchema(
        id=video.id,
        title=video.title,
        description=video.description,
        created_at=video.created_at,
        user_id=video.user_id,
    )


@videos_router.patch("/{id}", response_model=VideoResponseSchema)
async def update_video(
    id: uuid.UUID,
    data: VideoUpdateSchema = Depends(),
    video: UploadFile = File(),
    request_user: UserModel = Depends(get_current_user),
) -> VideoResponseSchema:
    ...
    return VideoResponseSchema(
        user=request_user,
        filename=video.filename,
        title=data.title,
        description=data.description,
    )


@videos_router.delete("/{id}", response_model=VideoResponseSchema)
async def delete_video(
    id: uuid.UUID,
    video_crud: VideoCRUD,
    request_user: UserModel = Depends(get_current_user),
) -> VideoResponseSchema:
    video = await video_crud.get_by_id(id)
    if video.user_id != request_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be an author of video"
        )

    deleted_video = await video_crud.delete(id)
    if deleted_video is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video doesn't exists.",
        )
    return VideoResponseSchema(
        id=deleted_video.id,
        title=deleted_video.title,
        description=deleted_video.description,
        created_at=deleted_video.created_at,
        user_id=deleted_video.user_id,
    )

