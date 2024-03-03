import shutil

from fastapi import UploadFile


def save_video(file: UploadFile, path: str):
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


def delete_video(path: str):
    ...
