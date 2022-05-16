from LightML.celery import app
from django.apps import apps
from .controller import start_container, stop_container


@app.task
def run(container_id):
    container = apps.get_model('api.Container')
    container = container.objects.get(id=container_id)
    github_link = container.project.repository_link
    container_name = container.container_name
    is_started = start_container(container_name, github_link=github_link)
    container_update = apps.get_model('api.Container').objects.filter(id=container_id)
    if is_started:
        container_update.update(status='started')
    else:
        container_update.update(status='Error')


@app.task
def stop(container_id):
    container = apps.get_model('api.Container')
    container = container.objects.get(id=container_id)
    container_name = container.container_name
    stop_container(container_name)
