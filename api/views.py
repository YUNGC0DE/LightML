import requests
import json

from django.shortcuts import _get_queryset
from rest_framework.generics import *
from rest_framework import permissions
from .serializers import *
from django.views.generic import View
from containers.kuber_api import get_request_url
from django.http import HttpResponse


class RequestView(View):
    def post(self, request, app_uuid, **kwargs):
        # handle the post request
        print(app_uuid)
        return {"status": app_uuid}

    def get(self, request, app_uuid, **kwargs):
        url = get_request_url(app_uuid)
        if url is None:
            return HttpResponse(json.dumps({"status": "Does not exist"}))
        # handle the get request
        extra_path = list(kwargs.values())
        for p in extra_path:
            url += f'/{p}'
        r = requests.get(url)
        return HttpResponse(r)


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


# ---------- custom permissions --------- #

class IsContainerOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        container = get_object_or_none(Container, pk=view.kwargs['pk'])
        if container is None:
            return False
        user = container.project.account.user
        return user == request.user


class IsProjectOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        account = Account.objects.get(user=request.user)
        if request.data.get("project") is not None:
            return account == Project.objects.get(pk=request.data['project']).account

        project = get_object_or_none(Project, pk=view.kwargs['pk'])
        if project is None:
            return False
        return account == Project.objects.get(pk=view.kwargs['pk']).account


class IsAccountOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        account = Account.objects.get(user=request.user)
        pk = view.kwargs.get("pk")
        if pk is not None:
            return account.id == int(pk)
        return account.id == int(request.data["account"])


class IsNewAccount(permissions.BasePermission):

    def has_permission(self, request, view):
        user_id = request.user.id
        return get_object_or_none(Account, user=user_id) is None


#  -------------- account --------------- #

class AccountAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsNewAccount]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class AccountUpdateAPIView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]

    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_field = 'pk'


#  -------------- project --------------- #


class ProjectsAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        acc = Account.objects.get(user=self.request.user)
        return Project.objects.filter(account=acc)


class ProjectCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class ProjectAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'pk'


class ProjectUpdateAPIView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'pk'


class ProjectDeleteAPIView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'pk'


#  -------------- container --------------- #

class ContainerAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContainerSerializer

    def get_queryset(self):
        acc = Account.objects.get(user=self.request.user)
        projects = Project.objects.get(account=acc)
        return Container.objects.filter(project=projects)


class ContainerCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]
    serializer_class = ContainerSerializer
    queryset = Container.objects.all()


class ContainerUpdateAPIView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsContainerOwner]
    serializer_class = ContainerSerializer
    queryset = Container.objects.all()
    lookup_field = 'pk'


class ContainerDeleteAPIView(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsContainerOwner]

    serializer_class = ContainerSerializer
    queryset = Container.objects.all()
    lookup_field = 'pk'
