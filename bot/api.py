import requests
from config import BACKEND_API_URL


def auth(user_id: int, username: str) -> bool:
    response = requests.post(
        f"{BACKEND_API_URL}/api/auth", json={"user_id": user_id, "username": username}
    )
    return response.status_code == 200


def get_task(user_id: int) -> dict:
    response = requests.get(f"{BACKEND_API_URL}/api/task/{user_id}")
    return response.json()


def get_profile(user_id: int) -> dict:
    response = requests.get(f"{BACKEND_API_URL}/api/profile/{user_id}")
    return response.json()


def get_scoreboard() -> dict:
    response = requests.get(f"{BACKEND_API_URL}/api/scoreboard")
    return response.json()


def get_users() -> dict:
    response = requests.get(f"{BACKEND_API_URL}/api/users")
    return response.json()


def pass_task(user_id: int, task_id: int, file_id: str) -> bool:
    response = requests.post(
        f"{BACKEND_API_URL}/api/pass_task",
        json={"user_id": user_id, "task_id": task_id, "file_id": file_id},
    )
    return response.status_code == 200


def send_vote(user_id: int, task_id: int, vote_value: int) -> bool:
    response = requests.post(
        f"{BACKEND_API_URL}/api/send_vote",
        json={"user_id": user_id, "task_id": task_id, "vote_value": vote_value},
    )
    return response.status_code == 200


def start_game() -> bool:
    response = requests.post(f"{BACKEND_API_URL}/api/admin/start_game")
    return response.status_code == 200
