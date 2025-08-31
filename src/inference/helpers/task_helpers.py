from json import dumps
from os.path import join

import httpx
from cryptography.fernet import Fernet

from src.inference.settings import BASE_API_SERVER_URL, FERNET_KEY


def fernet_encode(data):
    fernet = Fernet(FERNET_KEY)
    token = fernet.encrypt(data.encode())
    return token


def update_video_data(video_data, task_id, user_id):
    try:
        token = fernet_encode(task_id)
        data = {
            "token": token,
            "user": user_id,
            "data": video_data
        }

        update_url = join(BASE_API_SERVER_URL, f"{task_id}/")
        with httpx.Client() as client:
            response = client.post(
                update_url,
                json=dumps(data),
            )
            response.raise_for_status()
    except Exception as e:
        print(f"failed to update the backend for task: {task_id}")
        print(e)

