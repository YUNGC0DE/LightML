from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
    path('account/', AccountAPIView.as_view()),
    path('account/create/', AccountCreateAPIView.as_view()),
    path('account/<int:pk>/update/', AccountUpdateAPIView.as_view()),
    path('projects/', ProjectsAPIView.as_view()),
    path('projects/create/', ProjectCreateAPIView.as_view()),
    path('projects/<int:pk>/', ProjectAPIView.as_view()),
    path('projects/<int:pk>/update/', ProjectUpdateAPIView.as_view()),
    path('projects/<int:pk>/delete/', ProjectDeleteAPIView.as_view()),
    path('containers/', ContainerAPIView.as_view()),
    path('containers/create/', ContainerCreateAPIView.as_view()),
    path('containers/<int:pk>/update/', ContainerUpdateAPIView.as_view()),
    path('containers/<int:pk>/delete/', ContainerDeleteAPIView.as_view()),
]