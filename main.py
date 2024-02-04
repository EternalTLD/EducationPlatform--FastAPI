import uvicorn
from fastapi import FastAPI, APIRouter

from api.users.endpoints import user_router
from api.auth.endpoints import auth_router
from api.videos.endpoints import videos_router


app = FastAPI(title="education-platform")

main_router = APIRouter()

main_router.include_router(user_router, prefix="/user", tags=["user"])
main_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_router.include_router(videos_router, prefix="/video", tags=["video"])

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
