import os


def get_video_upload_path(filename, user_id):
    directory = f"videos/{user_id}/"
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    return path