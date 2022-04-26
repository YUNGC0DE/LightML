from django.db.models import signals
from django.db import models
from django.contrib.auth.models import User
from api.choices import InputDataFormat, PythonVersion
from containers.tasks import run, stop


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    git_token = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    repository_link = models.TextField(max_length=200)
    input_data_type = models.TextField(choices=InputDataFormat.choices)
    # dead param
    is_online = models.BooleanField(blank=False, default=False)
    python_version = models.TextField(choices=PythonVersion.choices, default=PythonVersion.Python36)

    def __str__(self):
        return self.name


class Container(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False)
    status = models.TextField(blank=True, default="starting", max_length=110)
    container_name = models.TextField(max_length=20)


def run_container(sender, instance, signal, *args, **kwargs):
    run.delay(instance.id)


def stop_container(sender, instance, signal, *args, **kwargs):
    stop(instance.id)


signals.post_save.connect(run_container, sender=Container)

signals.pre_delete.connect(stop_container, sender=Container)


class ModelInference(models.Model):
    date = models.DateTimeField(auto_created=True)
    inference_time = models.FloatField(blank=True)
    is_successful = models.BooleanField(default=False, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
