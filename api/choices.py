from django.db import models


class InputDataFormat(models.TextChoices):
    STR_TO_PANDAS = 'to_pandas'
    STR_TO_NP_ARRAY = 'to_numpy'
    STR_TO_TENSOR = 'to_tensor'
    BASE64_STR_TO_TENSOR = 'base64_to_tensor'


class PythonVersion(models.TextChoices):
    Python36 = 'python_3.6'
    Python37 = 'python_3.7'
    Python38 = 'python_3.8'
    Python39 = 'python_3.9'
