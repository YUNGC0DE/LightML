import time
import requests

from .kuber_api import create_app, delete_app


def start_container(uuid: str, github_link: str, target_file: str = "main.py", replicas: int = 1):
    container_address = create_app(uuid, github_link, target_file, replicas=replicas)
    if container_address is None:
        raise
    for i in range(200):
        time.sleep(1)
        try:
            if requests.get(f"{container_address}").status_code:
                return True
            else:
                return False
        except requests.exceptions.ConnectionError:
            continue

    return False


def stop_container(uuid: str):
    delete_app(uuid)
