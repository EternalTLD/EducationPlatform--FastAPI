import shutil

from fastapi import APIRouter, File, UploadFile, Depends

from schemas.videos import VideoUpload, VideoResponse
from api.auth.endpoints import get_current_user
from models.users import User

videos_router = APIRouter()


@videos_router.post("/upload", response_model=VideoResponse)
async def upload_video(
    data: VideoUpload = Depends(),
    video: UploadFile = File(...),
    request_user: User = Depends(get_current_user),
) -> VideoResponse:
    with open(f"{video.filename}", "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    return VideoResponse(
        user=request_user,
        filename=video.filename,
        title=data.title,
        description=data.description,
    )
