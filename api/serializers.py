from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class AccountSerializer(ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Account
        fields = "__all__"


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"


class ModelInferenceSerializer(ModelSerializer):

    class Meta:
        model = ModelInference
        fields = "__all__"
