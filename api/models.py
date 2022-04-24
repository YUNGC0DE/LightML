from django.db import models
from django.contrib.auth.models import User
from api.choices import InputDataFormat, PythonVersion


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
    is_online = models.BooleanField(blank=False, default=False)
    python_version = models.TextField(choices=PythonVersion.choices, default=PythonVersion.Python36)

    def __str__(self):
        return self.name


class ModelInference(models.Model):
    date = models.DateTimeField(auto_created=True)
    inference_time = models.FloatField(blank=True)
    is_successful = models.BooleanField(default=False, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
