import uvicorn
from fastapi import APIRouter, FastAPI

from api.auth.endpoints import auth_router
from api.users.endpoints import user_router
from api.videos.endpoints import videos_router

app = FastAPI(title="VideoHosting")

main_router = APIRouter()

main_router.include_router(user_router, prefix="/users", tags=["Users"])
main_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
main_router.include_router(videos_router, prefix="/videos", tags=["Videos"])

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
