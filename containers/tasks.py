from LightML.celery import app
from django.apps import apps


@app.task
def run(container_id):
    ## MAGIC ##
    container = apps.get_model('api.Container')
    container.objects.filter(id=container_id).update(status='started')
