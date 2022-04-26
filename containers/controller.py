import os
import time
import requests


def start_container(name, port):
    os.system(f"docker run -i -t -d --rm --name {name} -p {port}:8080 python:3.8.13-bullseye bash")
    os.system(f"docker exec -d {name} bash -c 'git clone https://github.com/YUNGC0DE/testSHit.git; cd testSHit; pip install -r requirements.txt; python main.py'")
    for i in range(200):
        time.sleep(1)
        try:
            if requests.get(f"http://localhost:{port}/hello/kek").status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.ConnectionError:
            continue

    return False


def stop_container(name):
    os.system(f"docker stop {name}")


def get_free_port():
    pass
