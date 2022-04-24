from django.shortcuts import _get_queryset
from rest_framework.generics import *
from rest_framework import permissions
from .serializers import *


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if
    more than one object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None

# ---------- custom permissions --------- #


class IsProjectOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        account = Account.objects.get(user=request.user)
        return account == Project.objects.get(pk=view.kwargs['pk']).account


class IsAccountOwner(permissions.BasePermission):
    # ## # # #
    def has_permission(self, request, view):
        account = Account.objects.get(user=request.user)
        return account.id == int(request.data["account"])


class IsNewAccount(permissions.BasePermission):

    def has_permission(self, request, view):
        user_id = request.user.id
        return get_object_or_none(Account, user=user_id) is None


"""



class IsOrderOwnerCatToOrder(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user == Order.objects.get(pk=request.data.get('order')).user

"""


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
    permission_classes = [IsProjectOwner]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'pk'


class ProjectUpdateAPIView(UpdateAPIView):
    permission_classes = [IsProjectOwner]

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'pk'


class ProjectDeleteAPIView(DestroyAPIView):
    permission_classes = [IsProjectOwner]

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'pk'
