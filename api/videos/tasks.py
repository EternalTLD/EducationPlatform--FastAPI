from typing import BinaryIO
import shutil


def save_video(filepath: str, file: BinaryIO):
    with open(f"{filepath}", "wb") as buffer:
        shutil.copyfileobj(file, buffer)
