from fastapi import APIRouter, File, UploadFile, Depends, BackgroundTasks

from schemas.videos import VideoUploadSchema, VideoResponseSchema
from api.auth.endpoints import get_current_user
from models.users import UserModel
from .tasks import save_video

videos_router = APIRouter()


@videos_router.post("/upload", response_model=VideoResponseSchema)
async def upload_video(
    background_tasks: BackgroundTasks,
    data: VideoUploadSchema = Depends(),
    video: UploadFile = File(),
    request_user: UserModel = Depends(get_current_user),
) -> VideoResponseSchema:
    background_tasks.add_task(save_video, video.filename, video.file)
    return VideoResponseSchema(
        user=request_user,
        filename=video.filename,
        title=data.title,
        description=data.description,
    )
