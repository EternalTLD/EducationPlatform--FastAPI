import os
import shutil
from fastapi import UploadFile


def get_video_upload_path(filename):
    directory = "videos"
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    return path


def save_video(file: UploadFile, path: str):
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
